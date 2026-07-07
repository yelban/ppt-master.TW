#!/usr/bin/env python3
"""
Codex CLI image generation backend.

Spawns the local `codex exec --json` command and instructs Codex to use its
built-in image_gen tool. The Codex CLI uses the user's logged-in Codex /
ChatGPT subscription; no OpenAI API key is read.

Configuration keys:
  CODEX_IMAGE_TIMEOUT_MS       (optional) Per-attempt timeout, default 300000
  CODEX_IMAGE_TIMEOUT_SECONDS  (optional) Alternative timeout in seconds
  CODEX_IMAGE_RETRIES          (optional) Retry count, capped at 2
  CODEX_IMAGE_RETRY_DELAY      (optional) Initial retry delay in seconds
  CODEX_IMAGE_LOG_DIR          (optional) Directory for raw codex exec logs

Dependencies:
  Pillow (for PNG validation)
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

configure_utf8_stdio()

if __name__ == "__main__":
    print(__doc__)
    print("Use via: python3 skills/ppt-master/scripts/image_gen.py \"prompt\" --backend codex")
    raise SystemExit(0 if any(arg in {"-h", "--help", "help"} for arg in sys.argv[1:]) else 1)

import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

from image_backends.backend_common import (
    detect_image_extension,
    normalize_image_size,
    report_resolution,
    resolve_output_path,
)

try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


DEFAULT_MODEL_LABEL = "codex-image-gen"
DEFAULT_TIMEOUT_MS = 300_000
DEFAULT_RETRIES = 2
MAX_RETRIES = 2
DEFAULT_RETRY_DELAY_SECONDS = 2.0

SUPPORTED_ASPECT_RATIOS = ("1:1", "16:9", "9:16", "4:3", "2.35:1")
ASPECT_RATIO_ALIASES = {
    "21:9": "2.35:1",
}

SHELL_METACHARS = set(";|&`$<>\n\r()'\"")
LOGIN_MARKERS = (
    "not logged in",
    "not authenticated",
    "authentication required",
    "please log in",
    "codex login",
    "login required",
)
REFUSAL_MARKERS = (
    "i can't comply",
    "i cannot comply",
    "i can't help",
    "i cannot help",
    "unable to comply",
    "policy",
    "refused",
    "refusal",
)

_CODEX_EXEC_LOCK = threading.Lock()


class CodexImageError(RuntimeError):
    """Runtime error with a stable diagnostic kind."""

    def __init__(self, kind: str, message: str, *, retryable: bool = True):
        super().__init__(message)
        self.kind = kind
        self.retryable = retryable


def _env_int(name: str) -> int | None:
    """Read a positive integer environment variable."""
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got '{raw}'.") from exc
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}.")
    return value


def _env_float(name: str) -> float | None:
    """Read a positive float environment variable."""
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got '{raw}'.") from exc
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}.")
    return value


def _resolve_timeout_ms() -> int:
    """Resolve the per-attempt Codex timeout."""
    explicit_ms = _env_int("CODEX_IMAGE_TIMEOUT_MS")
    if explicit_ms is not None:
        return explicit_ms
    explicit_seconds = _env_float("CODEX_IMAGE_TIMEOUT_SECONDS")
    if explicit_seconds is not None:
        return int(explicit_seconds * 1000)
    return DEFAULT_TIMEOUT_MS


def _resolve_retries(max_retries: int | None) -> int:
    """Resolve retry count and cap total attempts at three."""
    env_retries = _env_int("CODEX_IMAGE_RETRIES")
    retries = max_retries if max_retries is not None else DEFAULT_RETRIES
    if env_retries is not None:
        retries = env_retries
    retries = max(0, retries)
    if retries > MAX_RETRIES:
        print(
            f"  [WARN] CODEX backend caps retries at {MAX_RETRIES} "
            "(3 total attempts) to avoid burning subscription quota."
        )
        retries = MAX_RETRIES
    return retries


def _resolve_retry_delay() -> float:
    """Resolve the initial retry delay in seconds."""
    return _env_float("CODEX_IMAGE_RETRY_DELAY") or DEFAULT_RETRY_DELAY_SECONDS


def _resolve_aspect_ratio(aspect_ratio: str) -> tuple[str, str | None]:
    """Validate or explicitly map a Codex-supported aspect ratio."""
    ratio = aspect_ratio.strip()
    if ratio in SUPPORTED_ASPECT_RATIOS:
        return ratio, None
    mapped = ASPECT_RATIO_ALIASES.get(ratio)
    if mapped:
        return mapped, f"{ratio} -> {mapped}"
    supported = ", ".join(SUPPORTED_ASPECT_RATIOS)
    aliases = ", ".join(f"{src} -> {dst}" for src, dst in ASPECT_RATIO_ALIASES.items())
    raise ValueError(
        f"Unsupported aspect ratio '{aspect_ratio}' for Codex backend. "
        f"Supported: {supported}. Explicit mappings: {aliases}."
    )


def _assert_safe_instruction_path(path: Path) -> None:
    """Reject paths that are unsafe to place in an agent shell instruction."""
    text = str(path)
    if any(char in SHELL_METACHARS for char in text):
        raise ValueError(
            f"Codex output path contains shell metacharacters and is unsafe: {path}"
        )


def _short_prompt(prompt: str) -> str:
    """Return a compact prompt preview."""
    return f"{prompt[:120]}{'...' if len(prompt) > 120 else ''}"


def _raw_log_path() -> Path:
    """Create a raw log path for one codex exec invocation."""
    base = os.environ.get("CODEX_IMAGE_LOG_DIR", "").strip()
    if base:
        log_dir = Path(base).expanduser()
        log_dir.mkdir(parents=True, exist_ok=True)
    else:
        log_dir = Path(tempfile.mkdtemp(prefix="ppt-codex-image-"))
    return log_dir / "codex_exec.jsonl"


def _write_raw_log(log_path: Path, stdout: str, stderr: str) -> None:
    """Persist the raw Codex event stream and stderr for diagnostics."""
    text = stdout
    if stderr:
        text += "\n--- stderr ---\n" + stderr
    log_path.write_text(text, encoding="utf-8")


def _build_instruction(prompt: str, aspect_ratio: str, output_path: Path) -> str:
    """Build the stdin instruction for `codex exec`."""
    output_json = json.dumps(str(output_path))
    return f"""Use your built-in image_gen tool to generate exactly one PNG image.

Prompt:
{prompt}

Aspect ratio: {aspect_ratio}
Final output path: {output_path}

Required sequence:
1. Call image_gen before any filesystem search or copy operation.
2. Use the prompt and aspect ratio above for the generated image.
3. After image_gen finishes, copy or move only the image created in this turn to the final output path.
4. Verify the file exists and has non-zero byte size.
5. Reply with one JSON object on a single line and no Markdown:
   {{"status":"ok","path":{output_json},"bytes":<file_size_in_bytes>}}

Constraints:
- Do not use external image APIs, curl, wget, or browser downloads.
- Do not create synthetic image bytes with a script.
- Do not reuse a pre-existing file from generated_images or any other directory.
- Do not inspect generated_images until after image_gen has completed.
- The only valid source of pixels is the image_gen tool call from this turn.
"""


def _derive_tool_name(item: dict) -> str:
    """Derive a stable tool name from a Codex JSON event item."""
    candidates = [
        item.get("type"),
        item.get("tool"),
        item.get("name"),
        item.get("tool_name"),
    ]
    for value in candidates:
        if not isinstance(value, str):
            continue
        normalized = value.strip().lower()
        if normalized in {"image_gen", "image_generation"}:
            return "image_gen"
        if normalized == "command_execution":
            return "shell"
        if normalized:
            return normalized
    return "unknown"


def _string_from_content(value) -> str:
    """Best-effort extraction of text from agent message content."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        chunks: list[str] = []
        for item in value:
            if isinstance(item, str):
                chunks.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunks)
    return ""


def _parse_event_stream(raw: str) -> dict:
    """Parse the `codex exec --json` event stream."""
    thread_id = None
    tool_calls: list[str] = []
    agent_message = ""

    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_type = event.get("type")
        if event_type == "thread.started":
            thread_id = event.get("thread_id") or event.get("threadId")
            continue

        item = event.get("item")
        if not isinstance(item, dict):
            continue
        tool_name = _derive_tool_name(item)
        if tool_name != "unknown":
            tool_calls.append(tool_name)
        if item.get("type") == "agent_message" and event_type == "item.completed":
            agent_message = (
                _string_from_content(item.get("text"))
                or _string_from_content(item.get("content"))
            )

    return {
        "thread_id": thread_id,
        "tool_calls": tool_calls,
        "agent_message": agent_message,
    }


def _codex_home() -> Path:
    """Return the Codex home directory."""
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def _image_gen_evidence(parsed: dict) -> tuple[bool, str]:
    """Return whether this run shows evidence of an image_gen invocation."""
    if "image_gen" in parsed.get("tool_calls", []):
        return True, "image_gen event in codex stream"

    thread_id = parsed.get("thread_id")
    if not thread_id:
        return False, "no thread id and no image_gen event in codex stream"

    generated_dir = _codex_home() / "generated_images" / str(thread_id)
    try:
        pngs = [
            entry for entry in generated_dir.iterdir()
            if entry.is_file() and entry.suffix.lower() == ".png"
        ]
    except OSError as exc:
        return False, f"cannot inspect {generated_dir}: {exc}"
    if pngs:
        return True, f"PNG found in {generated_dir}"
    return False, f"no PNG found in {generated_dir}"


def _looks_like_login_error(text: str) -> bool:
    """Return true when process output suggests `codex login` is required."""
    lowered = text.lower()
    return any(marker in lowered for marker in LOGIN_MARKERS)


def _looks_like_refusal(text: str) -> bool:
    """Return true when process output suggests an agent refusal."""
    lowered = text.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


def _classify_process_failure(stdout: str, stderr: str, log_path: Path) -> CodexImageError:
    """Classify a non-zero Codex process exit."""
    combined = "\n".join(part for part in (stdout, stderr) if part)
    lowered = combined.lower()
    if (
        "failed to initialize in-process app-server client" in lowered
        and "operation not permitted" in lowered
    ):
        return CodexImageError(
            "codex_runtime_blocked",
            "codex exec could not initialize its in-process app-server client "
            "in this sandbox (Operation not permitted). Run the same command "
            "from a host shell with Codex CLI access, or use a direct API "
            f"backend in this environment. Raw log: {log_path}",
            retryable=False,
        )
    if _looks_like_login_error(combined):
        return CodexImageError(
            "not_logged_in",
            "Codex CLI is not logged in or the session expired. "
            f"Run `codex login` and retry. Raw log: {log_path}",
            retryable=False,
        )
    if _looks_like_refusal(combined):
        return CodexImageError(
            "agent_refused",
            f"Codex refused the image request. Raw log: {log_path}",
        )
    return CodexImageError(
        "spawn_failed",
        f"codex exec failed. Raw log: {log_path}",
    )


def _run_codex_exec(instruction: str, timeout_ms: int) -> tuple[str, str, Path]:
    """Run `codex exec --json` and return stdout, stderr, and raw log path."""
    codex_bin = shutil.which("codex")
    if not codex_bin:
        raise CodexImageError(
            "codex_not_installed",
            "codex CLI not found on PATH. Install with "
            "`npm install -g @openai/codex`, then run `codex login`.",
            retryable=False,
        )

    args = [
        codex_bin,
        "exec",
        "--json",
        "--sandbox",
        "danger-full-access",
        "--skip-git-repo-check",
        "-",
    ]
    log_path = _raw_log_path()

    with _CODEX_EXEC_LOCK:
        try:
            child = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except OSError as exc:
            raise CodexImageError(
                "spawn_failed",
                f"Failed to spawn codex CLI: {exc}",
            ) from exc

        try:
            stdout, stderr = child.communicate(
                instruction,
                timeout=timeout_ms / 1000,
            )
        except subprocess.TimeoutExpired as exc:
            child.kill()
            stdout, stderr = child.communicate()
            _write_raw_log(log_path, stdout or "", stderr or "")
            raise CodexImageError(
                "timeout",
                f"codex exec timed out after {timeout_ms}ms. "
                "Set CODEX_IMAGE_TIMEOUT_MS to a larger value if needed. "
                f"Raw log: {log_path}",
            ) from exc

    _write_raw_log(log_path, stdout or "", stderr or "")
    if child.returncode != 0:
        raise _classify_process_failure(stdout or "", stderr or "", log_path)
    return stdout or "", stderr or "", log_path


def _validate_png(path: Path) -> int:
    """Validate that a path exists and contains a real non-empty PNG."""
    try:
        image_bytes = path.read_bytes()
    except FileNotFoundError as exc:
        raise CodexImageError(
            "output_missing",
            f"Codex reported success but output file is missing: {path}",
        ) from exc
    except OSError as exc:
        raise CodexImageError("output_missing", f"Cannot read output file {path}: {exc}") from exc

    if not image_bytes:
        raise CodexImageError("invalid_png", f"Output file is empty: {path}")
    if detect_image_extension(image_bytes) != ".png":
        raise CodexImageError("invalid_png", f"Output is not a valid PNG: {path}")

    if HAS_PIL:
        try:
            with PILImage.open(path) as img:
                img.verify()
            with PILImage.open(path) as img:
                if img.format != "PNG":
                    raise CodexImageError(
                        "invalid_png",
                        f"Output format is {img.format}, expected PNG: {path}",
                    )
                width, height = img.size
            if width <= 0 or height <= 0:
                raise CodexImageError(
                    "invalid_png",
                    f"Output PNG has invalid dimensions {width}x{height}: {path}",
                )
        except CodexImageError:
            raise
        except Exception as exc:
            raise CodexImageError("invalid_png", f"Pillow cannot open PNG {path}: {exc}") from exc

    return len(image_bytes)


def _remove_stale_output(path: Path) -> None:
    """Remove a previous output so a failed attempt cannot pass on stale bytes."""
    try:
        if path.exists():
            path.unlink()
    except OSError as exc:
        raise CodexImageError(
            "output_prepare_failed",
            f"Cannot remove stale output before Codex generation: {path}: {exc}",
            retryable=False,
        ) from exc


def _generate_once(prompt: str, aspect_ratio: str, output_path: Path,
                   timeout_ms: int) -> str:
    """Run one Codex generation attempt."""
    _remove_stale_output(output_path)
    instruction = _build_instruction(prompt, aspect_ratio, output_path)
    start = time.time()
    stdout, stderr, log_path = _run_codex_exec(instruction, timeout_ms)
    elapsed = time.time() - start

    parsed = _parse_event_stream(stdout)
    agent_text = parsed.get("agent_message", "") or stdout or stderr
    try:
        bytes_written = _validate_png(output_path)
    except CodexImageError as exc:
        if exc.kind == "output_missing" and _looks_like_refusal(agent_text):
            raise CodexImageError(
                "agent_refused",
                f"Codex refused the image request. Raw log: {log_path}",
            ) from exc
        raise

    has_evidence, reason = _image_gen_evidence(parsed)
    if not has_evidence:
        raise CodexImageError(
            "no_image_gen_tool_use",
            "Codex produced an output file but the run did not show evidence "
            f"that image_gen was invoked ({reason}). Raw log: {log_path}",
        )

    print(f"\n  [DONE] Codex image_gen completed ({elapsed:.1f}s)")
    print(f"  Evidence:     {reason}")
    print(f"  Bytes:        {bytes_written}")
    print(f"  File saved to: {output_path}")
    report_resolution(str(output_path))
    return str(output_path)


def generate(prompt: str,
             aspect_ratio: str = "1:1", image_size: str = "1K",
             output_dir: str = None, filename: str = None,
             model: str = None, max_retries: int = DEFAULT_RETRIES) -> str:
    """Generate a single PNG through the local Codex CLI."""
    codex_aspect, mapping_note = _resolve_aspect_ratio(aspect_ratio)
    normalized_size = normalize_image_size(image_size or "1K")
    timeout_ms = _resolve_timeout_ms()
    retries = _resolve_retries(max_retries)
    retry_delay = _resolve_retry_delay()

    output_path = Path(
        resolve_output_path(prompt, output_dir=output_dir, filename=filename, ext=".png")
    ).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = output_path.resolve()
    _assert_safe_instruction_path(output_path)

    model_label = model or DEFAULT_MODEL_LABEL

    print("[Codex CLI]")
    print(f"  Model:        {model_label} (ignored; Codex CLI selects its image_gen model)")
    print(f"  Prompt:       {_short_prompt(prompt)}")
    if mapping_note:
        print(f"  Aspect Ratio: {mapping_note}")
    else:
        print(f"  Aspect Ratio: {codex_aspect}")
    print(f"  Image Size:   {normalized_size} (ignored; Codex chooses pixels from aspect ratio)")
    print(f"  Timeout:      {timeout_ms}ms per attempt")
    print(f"  Attempts:     {retries + 1} max")
    print()

    last_error: CodexImageError | None = None
    total_attempts = retries + 1
    attempts_made = 0
    for attempt in range(1, total_attempts + 1):
        attempts_made = attempt
        try:
            print(f"  [..] Running codex exec attempt {attempt}/{total_attempts}...", flush=True)
            return _generate_once(prompt, codex_aspect, output_path, timeout_ms)
        except CodexImageError as exc:
            last_error = exc
            if not exc.retryable or attempt >= total_attempts:
                break
            wait = retry_delay * (2 ** (attempt - 1))
            print(f"\n  [WARN] {exc.kind}: {exc}. Retrying in {wait:.1f}s...")
            time.sleep(wait)

    if last_error is None:
        raise RuntimeError("Codex image generation failed for an unknown reason.")
    raise RuntimeError(
        f"Codex image generation failed after {attempts_made} attempt(s). "
        f"{last_error.kind}: {last_error}"
    )
