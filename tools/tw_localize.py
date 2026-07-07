#!/usr/bin/env python3
"""
PPT Master TW Localizer

Convert the maintained Traditional Chinese fork after syncing from upstream.
The converter uses OpenCC s2twp, protects en/ja i18n content plus the
dual-Chinese UI source dictionaries, derives Traditional Chinese artifacts,
and applies a repo-local override table for terms OpenCC does not own.

Usage:
    python3 tools/tw_localize.py [--check]

Examples:
    python3 tools/tw_localize.py
    python3 tools/tw_localize.py --check

Dependencies:
    /opt/homebrew/bin/opencc with s2twp.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional


ROOT = Path(__file__).resolve().parents[1]
OPENCC_BIN = Path(os.environ.get("OPENCC_BIN", "/opt/homebrew/bin/opencc"))
OPENCC_CONFIG = os.environ.get("OPENCC_CONFIG", "s2twp.json")
OVERRIDES_PATH = Path(__file__).with_name("tw_localize_overrides.json")
README_CN_PATH = ROOT / "README_CN.md"
README_TW_PATH = ROOT / "README_TW.md"

TEXT_EXTENSIONS = {".md", ".py", ".js", ".html", ".css", ".json"}
EXCLUDED_PARTS = {"projects", "examples", ".git"}
ROOT_MARKDOWN_LOCALIZATION_EXCLUDES = {"README_CN.md", "README_TW.md"}
README_EN_NAV = "English | [正體中文](./README_TW.md) | [简体中文](./README_CN.md)"
README_TW_NAV = "[English](./README.md) | 正體中文 | [简体中文](./README_CN.md)"
UI_APP_JS_PATHS = {
    "skills/ppt-master/scripts/confirm_ui/static/app.js",
    "skills/ppt-master/scripts/svg_editor/static/app.js",
}
UI_INDEX_HTML_PATHS = {
    "skills/ppt-master/scripts/confirm_ui/static/index.html",
    "skills/ppt-master/scripts/svg_editor/static/index.html",
}
PREFILTER_RE = re.compile(
    r"[\u4e00-\u9fff]|Microsoft YaHei|微软雅黑|微軟雅黑|SimHei|SimSun|"
    r"PingFang SC|Hiragino Sans GB|Source Han Sans SC|zh-CN"
)
HAN_RE = re.compile(r"[\u4e00-\u9fff]")
KANA_RE = re.compile(r"[\u3040-\u30ff\u31f0-\u31ff]")
URL_RE = re.compile(r"(?:https?|file)://[^\s<>'\")\]]+")
SOURCE_PATH_LITERAL_RE = re.compile(
    r"(?P<quote>[\"'])(?:\\.|(?!\1).)*\."
    r"(?:md|markdown|json|jsonl|yaml|yml|svg|png|jpg|jpeg|gif|webp|"
    r"pptx|docx|xlsx|csv|tsv|html|css|js|py)(?P=quote)",
    flags=re.IGNORECASE,
)

FONT_FACE_MARKER_START = "/* ---- Traditional Chinese web fonts ---- */"
FONT_FACE_MARKER_END = "/* ---- End Traditional Chinese web fonts ---- */"
UI_FONT_STACK = (
    '"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", '
    '"GenSekiGothic2TW", "GenSenRounded2TW", "GenRyuMin2TW", '
    '"LXGWWenKaiTC", "Iansui", "JasonHandwriting1", '
    '"JasonHandwriting2", -apple-system, BlinkMacSystemFont, "Segoe UI", '
    "sans-serif"
)

FONT_FACE_BLOCK = f"""{FONT_FACE_MARKER_START}
@font-face {{
    font-family: "GenSekiGothic2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-genseki-tw@latest/GenSekiGothic2TW-R.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "GenSenRounded2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-gensen-tw@latest/GenSenRounded2TW-R.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "GenRyuMin2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-genryu-tw@latest/GenRyuMin2TW-R.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "LXGWWenKaiTC";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-lxgw-wenkai-tc@latest/LXGWWenKaiTC-Regular.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "Iansui";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-iansui@latest/Iansui-Regular.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "JasonHandwriting1";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-jason1@latest/JasonHandwriting1-Regular.woff2") format("woff2");
    font-display: swap;
}}

@font-face {{
    font-family: "JasonHandwriting2";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-jason2@latest/JasonHandwriting2-Regular.woff2") format("woff2");
    font-display: swap;
}}

:root {{
    --tw-ui-font-stack: {UI_FONT_STACK};
}}
{FONT_FACE_MARKER_END}
"""

PRESENTATION_CJK_STACK = [
    "Microsoft JhengHei",
    "PingFang TC",
    "Noto Sans TC",
    "GenSekiGothic2TW",
]
SIMPLIFIED_FONT_NAMES = {
    "Microsoft YaHei",
    "微软雅黑",
    "微軟雅黑",
    "SimHei",
    "SimSun",
    "PingFang SC",
    "Hiragino Sans GB",
    "Source Han Sans SC",
}
CJK_FONT_NAMES = {
    "Microsoft JhengHei",
    "PingFang TC",
    "Noto Sans TC",
    "PMingLiU",
    "GenSekiGothic2TW",
    "GenSenRounded2TW",
    "GenRyuMin2TW",
    "LXGWWenKaiTC",
    "Iansui",
    "JasonHandwriting1",
    "JasonHandwriting2",
}


@dataclass(frozen=True)
class Overrides:
    replacements: list[tuple[str, str]]
    protected_keys: set[str]
    protected_suffixes: tuple[str, ...]


def configure_utf8_stdio() -> None:
    """Keep console output stable on non-UTF-8 terminals."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def load_overrides() -> Overrides:
    """Load the ordered custom replacement table."""
    raw = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    replacements = [
        (str(item["from"]), str(item["to"]))
        for item in raw.get("replacements", [])
    ]
    protected_keys = {str(item).lower() for item in raw.get("protected_keys", [])}
    protected_suffixes = tuple(
        str(item).lower() for item in raw.get("protected_key_suffixes", [])
    )
    return Overrides(replacements, protected_keys, protected_suffixes)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert this repo from Simplified Chinese to Traditional Chinese (Taiwan).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report files that would change; do not write files.",
    )
    return parser


def iter_target_files() -> Iterable[Path]:
    """Yield files owned by the localization pipeline."""
    roots = [ROOT / "skills/ppt-master", ROOT / "docs"]
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            if EXCLUDED_PARTS.intersection(rel.parts):
                continue
            suffix = path.suffix.lower()
            if suffix in TEXT_EXTENSIONS:
                yield path
                continue
            if suffix == ".svg" and rel.parts[:3] == ("skills", "ppt-master", "templates"):
                yield path
    for path in sorted(ROOT.glob("*.md")):
        if path.is_file():
            if path.name in ROOT_MARKDOWN_LOCALIZATION_EXCLUDES:
                continue
            yield path


def _merge_ranges(ranges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    clean = sorted((max(0, a), max(0, b)) for a, b in ranges if b > a)
    merged: list[tuple[int, int]] = []
    for start, end in clean:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged


def _transform_outside_ranges(
    text: str,
    ranges: Iterable[tuple[int, int]],
    transform: Callable[[str], str],
) -> str:
    protected = _merge_ranges(ranges)
    if not protected:
        return transform(text)
    parts: list[str] = []
    cursor = 0
    for start, end in protected:
        if cursor < start:
            parts.append(transform(text[cursor:start]))
        parts.append(text[start:end])
        cursor = end
    if cursor < len(text):
        parts.append(transform(text[cursor:]))
    return "".join(parts)


def _apply_replacements(
    text: str,
    replacements: list[tuple[str, str]],
    protected_ranges: Iterable[tuple[int, int]],
) -> str:
    def replace_segment(segment: str) -> str:
        for old, new in replacements:
            segment = segment.replace(old, new)
        return segment

    return _transform_outside_ranges(text, protected_ranges, replace_segment)


def _protect_for_opencc(text: str, ranges: Iterable[tuple[int, int]]) -> tuple[str, list[str]]:
    protected = _merge_ranges(ranges)
    if not protected:
        return text, []
    parts: list[str] = []
    originals: list[str] = []
    cursor = 0
    for idx, (start, end) in enumerate(protected):
        token = f"__TWLOC_PROTECTED_{idx:06d}__"
        parts.append(text[cursor:start])
        parts.append(token)
        originals.append(text[start:end])
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts), originals


def _restore_opencc_protected(text: str, originals: list[str]) -> str:
    for idx, original in enumerate(originals):
        token = f"__TWLOC_PROTECTED_{idx:06d}__"
        text = text.replace(token, original)
    return text


def _run_opencc(text: str) -> str:
    if not text or not HAN_RE.search(text):
        return text
    proc = subprocess.run(
        [str(OPENCC_BIN), "-c", OPENCC_CONFIG],
        input=text,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "opencc failed")
    return proc.stdout


def _opencc_selectively(text: str, protected_ranges: Iterable[tuple[int, int]]) -> str:
    tokenized, originals = _protect_for_opencc(text, protected_ranges)
    converted = _run_opencc(tokenized)
    return _restore_opencc_protected(converted, originals)


def _url_ranges(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in URL_RE.finditer(text)]


def _source_path_literal_ranges(text: str) -> list[tuple[int, int]]:
    return [match.span() for match in SOURCE_PATH_LITERAL_RE.finditer(text)]


def _japanese_line_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    cursor = 0
    for line in text.splitlines(keepends=True):
        end = cursor + len(line)
        if KANA_RE.search(line):
            ranges.append((cursor, end))
        cursor = end
    return ranges


def _is_protected_key(key: Optional[str], overrides: Overrides) -> bool:
    if not key:
        return False
    lower = key.lower()
    if lower in overrides.protected_keys:
        return True
    return any(lower.endswith(suffix) for suffix in overrides.protected_suffixes)


def _looks_like_non_prose_literal(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    if URL_RE.search(stripped):
        return True
    if stripped.startswith(("data:", "#", "--")):
        return True
    if "\n" not in stripped and re.search(r"[\\/]", stripped):
        if not re.search(r"\s[\\/]\s", stripped):
            return True
    if "\n" not in stripped and re.search(r"\.[A-Za-z0-9]{1,8}$", stripped):
        if not re.search(r"\s", stripped):
            return True
    if re.fullmatch(r"[A-Za-z0-9_./\\:;,@%#${}<>\[\]\-|+=*?&~]+", stripped):
        return True
    if re.fullmatch(r"[A-Za-z0-9_.:-]+", stripped):
        return True
    return False


def _read_json_string(text: str, start: int) -> tuple[int, str]:
    i = start + 1
    escaped = False
    while i < len(text):
        ch = text[i]
        if escaped:
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == '"':
            raw = text[start : i + 1]
            try:
                return i + 1, json.loads(raw)
            except json.JSONDecodeError:
                return i + 1, ""
        i += 1
    return len(text), ""


def _json_string_ranges(
    text: str,
    overrides: Overrides,
    *,
    hard_only: bool,
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    stack: list[dict[str, Optional[str]]] = []
    i = 0

    def current_value_key() -> Optional[str]:
        if not stack:
            return None
        ctx = stack[-1]
        if ctx["type"] == "object":
            return ctx.get("current_key")
        return ctx.get("parent_key")

    def mark_value_complete() -> None:
        if not stack:
            return
        ctx = stack[-1]
        if ctx["type"] == "object":
            ctx["expect"] = "comma_or_end"
            ctx["current_key"] = None
        elif ctx["type"] == "array":
            ctx["expect"] = "comma_or_end"

    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "{":
            stack.append({"type": "object", "expect": "key", "current_key": None, "parent_key": current_value_key()})
            i += 1
            continue
        if ch == "[":
            stack.append({"type": "array", "expect": "value", "parent_key": current_value_key()})
            i += 1
            continue
        if ch in "}]":
            if stack:
                stack.pop()
            mark_value_complete()
            i += 1
            continue
        if ch == ",":
            if stack:
                ctx = stack[-1]
                ctx["expect"] = "key" if ctx["type"] == "object" else "value"
            i += 1
            continue
        if ch == ":":
            if stack and stack[-1]["type"] == "object":
                stack[-1]["expect"] = "value"
            i += 1
            continue
        if ch == '"':
            end, decoded = _read_json_string(text, i)
            ctx = stack[-1] if stack else None
            is_key = bool(ctx and ctx["type"] == "object" and ctx.get("expect") == "key")
            if is_key:
                if not hard_only:
                    ranges.append((i, end))
                ctx["current_key"] = decoded
                ctx["expect"] = "colon"
            else:
                key = current_value_key()
                if _is_protected_key(key, overrides):
                    ranges.append((i, end))
                elif not hard_only and _looks_like_non_prose_literal(decoded):
                    ranges.append((i, end))
                mark_value_complete()
            i = end
            continue
        if ch in "-0123456789tfn":
            while i < len(text) and text[i] not in ",]}":
                i += 1
            mark_value_complete()
            continue
        i += 1
    return ranges


def _quoted_string_ranges(text: str, *, backticks: bool = False) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    quotes = {'"', "'"}
    if backticks:
        quotes.add("`")
    i = 0
    while i < len(text):
        ch = text[i]
        if ch not in quotes:
            i += 1
            continue
        if ch in {'"', "'"} and text[i : i + 3] == ch * 3:
            quote = ch * 3
            end = text.find(quote, i + 3)
            if end == -1:
                ranges.append((i, len(text)))
                break
            ranges.append((i, end + 3))
            i = end + 3
            continue
        quote = ch
        j = i + 1
        escaped = False
        while j < len(text):
            cur = text[j]
            if escaped:
                escaped = False
            elif cur == "\\":
                escaped = True
            elif cur == quote:
                ranges.append((i, j + 1))
                i = j + 1
                break
            j += 1
        else:
            ranges.append((i, len(text)))
            break
    return ranges


def _unquote_source_literal(raw: str) -> str:
    if len(raw) >= 6 and raw[:3] == raw[-3:] and raw[:1] in {'"', "'"}:
        return raw[3:-3]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'", "`"}:
        return raw[1:-1]
    return raw


def _previous_property_key(text: str, start: int) -> Optional[str]:
    prefix = text[max(0, start - 160) : start]
    match = re.search(r"([A-Za-z_$][\w$]*|[\"'][^\"']+[\"'])\s*:\s*$", prefix)
    if not match:
        return None
    key = match.group(1)
    if key[:1] in {'"', "'"}:
        key = key[1:-1]
    return key


def _js_protected_property_string_ranges(text: str, overrides: Overrides) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    key_pattern = (
        r"[A-Za-z_$][\w$]*"
        r"|[\"'][A-Za-z_$][\w$]*[\"']"
    )
    pattern = re.compile(
        rf"(?P<key>{key_pattern})\s*:\s*(?P<quote>[\"'])(?:\\.|(?!\2).)*\2",
        flags=re.DOTALL,
    )
    for match in pattern.finditer(text):
        key = match.group("key")
        if key[:1] in {'"', "'"}:
            key = key[1:-1]
        if not _is_protected_key(key, overrides):
            continue
        value_start = match.start("quote")
        value_end = match.end()
        ranges.append((value_start, value_end))
    return ranges


def _js_py_protected_string_ranges(
    text: str,
    overrides: Overrides,
    *,
    hard_only: bool,
    js: bool,
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for start, end in _quoted_string_ranges(text, backticks=js):
        raw = text[start:end]
        value = _unquote_source_literal(raw)
        key = _previous_property_key(text, start)
        if _is_protected_key(key, overrides):
            ranges.append((start, end))
        elif not hard_only and _looks_like_non_prose_literal(value):
            ranges.append((start, end))
    return ranges


def _repo_rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _is_ui_app_js(path: Path) -> bool:
    return _repo_rel(path) in UI_APP_JS_PATHS


def _is_ui_index_html(path: Path) -> bool:
    return _repo_rel(path) in UI_INDEX_HTML_PATHS


def _find_matching_brace(text: str, open_pos: int) -> int:
    depth = 0
    i = open_pos
    in_string: Optional[str] = None
    escaped = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue
        if ch in {'"', "'", "`"}:
            in_string = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def _top_level_js_object_bounds(text: str, object_name: str) -> Optional[tuple[int, int]]:
    marker = f"var {object_name}"
    pos = text.find(marker)
    if pos == -1:
        return None
    open_pos = text.find("{", pos)
    if open_pos == -1:
        return None
    return open_pos, _find_matching_brace(text, open_pos)


def _top_level_js_object_value_ranges(
    text: str,
    object_name: str,
    keys: set[str],
) -> list[tuple[int, int]]:
    bounds = _top_level_js_object_bounds(text, object_name)
    if bounds is None:
        return []
    open_pos, close_pos = bounds
    ranges: list[tuple[int, int]] = []
    i = open_pos + 1
    depth = 1
    in_string: Optional[str] = None
    escaped = False
    while i < close_pos:
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue
        if ch in {'"', "'", "`"}:
            in_string = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
            i += 1
            continue
        if ch == "}":
            depth -= 1
            i += 1
            continue
        if depth == 1 and (ch.isalpha() or ch in "_$"):
            start = i
            i += 1
            while i < close_pos and (text[i].isalnum() or text[i] in "_$"):
                i += 1
            key = text[start:i]
            j = i
            while j < close_pos and text[j].isspace():
                j += 1
            if key in keys and j < close_pos and text[j] == ":":
                j += 1
                while j < close_pos and text[j].isspace():
                    j += 1
                if j < close_pos and text[j] == "{":
                    value_end = _find_matching_brace(text, j)
                    ranges.append((j, value_end))
                    i = value_end
                    continue
            continue
        i += 1
    return ranges


def _top_level_js_object_range(text: str, object_name: str) -> list[tuple[int, int]]:
    bounds = _top_level_js_object_bounds(text, object_name)
    if bounds is None:
        return []
    return [bounds]


def _top_level_js_object_value_range(
    text: str,
    object_name: str,
    key: str,
) -> Optional[tuple[int, int]]:
    ranges = _top_level_js_object_value_ranges(text, object_name, {key})
    if not ranges:
        return None
    return ranges[0]


def _ui_lang_attribute_call_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    needle = 'document.documentElement.setAttribute("lang"'
    cursor = 0
    while True:
        start = text.find(needle, cursor)
        if start == -1:
            return ranges
        end = text.find(");", start)
        if end == -1:
            return ranges
        ranges.append((start, end + 2))
        cursor = end + 2


def _ui_lang_menu_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    pattern = re.compile(r'<ul id="lang-menu"[\s\S]*?</ul>')
    for match in pattern.finditer(text):
        ranges.append(match.span())
    return ranges


def _derive_zhtw_messages_block(zh_block: str, overrides: Overrides) -> str:
    text = _apply_replacements(zh_block, overrides.replacements, [])
    text = _opencc_selectively(text, [])
    return _apply_replacements(text, overrides.replacements, [])


def _replace_or_insert_zhtw_messages(
    text: str,
    zh_range: tuple[int, int],
    zhtw_block: str,
) -> str:
    zhtw_range = _top_level_js_object_value_range(text, "MESSAGES", "zhtw")
    if zhtw_range is not None:
        start, end = zhtw_range
        return text[:start] + zhtw_block + text[end:]

    _zh_start, zh_end = zh_range
    cursor = zh_end
    while cursor < len(text) and text[cursor] in " \t":
        cursor += 1
    if cursor < len(text) and text[cursor] == ",":
        insert = "\n        zhtw: " + zhtw_block + ","
        return text[: cursor + 1] + insert + text[cursor + 1 :]
    insert = ",\n        zhtw: " + zhtw_block
    return text[:zh_end] + insert + text[zh_end:]


def _derive_ui_zhtw_messages(path: Path, text: str, overrides: Overrides) -> str:
    if not _is_ui_app_js(path):
        return text
    zh_range = _top_level_js_object_value_range(text, "MESSAGES", "zh")
    if zh_range is None:
        return text
    zh_block = text[zh_range[0] : zh_range[1]]
    zhtw_block = _derive_zhtw_messages_block(zh_block, overrides)
    return _replace_or_insert_zhtw_messages(text, zh_range, zhtw_block)


def _line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def _with_readme_nav(text: str, nav: str) -> str:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines[:30]):
        stripped = line.strip()
        if "中文" not in stripped:
            continue
        if (
            "README.md" not in stripped
            and "README_CN.md" not in stripped
            and "README_TW.md" not in stripped
        ):
            continue
        lines[index] = nav + _line_ending(line)
        return "".join(lines)
    return text


def _normalize_readme_nav(path: Path, text: str) -> str:
    if _repo_rel(path) == "README.md":
        return _with_readme_nav(text, README_EN_NAV)
    return text


def _markdown_code_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for match in re.finditer(r"(^```.*?^```|^~~~.*?^~~~)", text, flags=re.MULTILINE | re.DOTALL):
        ranges.append(match.span())
    for match in re.finditer(r"`[^`\n]+`", text):
        if any(start <= match.start() < end for start, end in ranges):
            continue
        ranges.append(match.span())
    return ranges


def _hard_protected_ranges(path: Path, text: str, overrides: Overrides) -> list[tuple[int, int]]:
    ranges = _url_ranges(text) + _japanese_line_ranges(text)
    suffix = path.suffix.lower()
    if suffix in {".py", ".js"}:
        ranges += _source_path_literal_ranges(text)
    if suffix == ".json":
        ranges += _json_string_ranges(text, overrides, hard_only=True)
    elif suffix == ".js":
        message_keys = {"en", "ja"}
        if _is_ui_app_js(path):
            message_keys.add("zh")
            ranges += _top_level_js_object_range(text, "LANG_NAMES")
            ranges += _ui_lang_attribute_call_ranges(text)
        ranges += _top_level_js_object_value_ranges(text, "MESSAGES", message_keys)
        ranges += _js_protected_property_string_ranges(text, overrides)
    elif suffix == ".py":
        ranges += _js_py_protected_string_ranges(text, overrides, hard_only=True, js=False)
    elif suffix == ".html" and _is_ui_index_html(path):
        ranges += _ui_lang_menu_ranges(text)
    return _merge_ranges(ranges)


def _opencc_protected_ranges(path: Path, text: str, overrides: Overrides) -> list[tuple[int, int]]:
    ranges = _hard_protected_ranges(path, text, overrides)
    suffix = path.suffix.lower()
    if suffix == ".md":
        ranges += _markdown_code_ranges(text)
    elif suffix == ".json":
        ranges += _json_string_ranges(text, overrides, hard_only=False)
    elif suffix == ".js":
        ranges += _js_protected_property_string_ranges(text, overrides)
    elif suffix == ".py":
        ranges += _js_py_protected_string_ranges(text, overrides, hard_only=False, js=False)
    return _merge_ranges(ranges)


def _strip_quotes(name: str) -> str:
    stripped = name.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
        return stripped[1:-1]
    return stripped


def _normalize_font_stack(stack: str) -> str:
    parts = [_strip_quotes(part) for part in stack.split(",")]
    parts = [part.strip() for part in parts if part.strip()]
    replaced: list[str] = []
    for part in parts:
        if part in {"Microsoft YaHei", "微软雅黑", "微軟雅黑", "SimHei"}:
            part = "Microsoft JhengHei"
        elif part == "SimSun":
            part = "PMingLiU"
        elif part in {"PingFang SC", "Hiragino Sans GB"}:
            part = "PingFang TC"
        elif part == "Source Han Sans SC":
            part = "Noto Sans TC"
        replaced.append(part)

    has_cjk = any(part in CJK_FONT_NAMES for part in replaced)
    if has_cjk:
        ordered = [item for item in PRESENTATION_CJK_STACK]
        ordered += [part for part in replaced if part not in ordered and part not in SIMPLIFIED_FONT_NAMES]
    else:
        ordered = [part for part in replaced if part not in SIMPLIFIED_FONT_NAMES]

    deduped: list[str] = []
    for part in ordered:
        if part and part not in deduped:
            deduped.append(part)
    return ", ".join(deduped)


def _normalize_svg_font_families(text: str) -> str:
    def replace_attr(match: re.Match[str]) -> str:
        prefix, quote, value = match.group(1), match.group(2), match.group(3)
        return f"{prefix}{quote}{_normalize_font_stack(value)}{quote}"

    return re.sub(r'(font-family\s*=\s*)(["\'])(.*?)(\2)', replace_attr, text)


def _normalize_reference_font_guidance(path: Path, text: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in {
        "skills/ppt-master/templates/design_spec_reference.md",
        "skills/ppt-master/templates/spec_lock_reference.md",
    }:
        return text

    text = text.replace(
        'Every stack\'s exported Latin / EA typefaces MUST resolve to cross-platform pre-installed fonts: `"Microsoft JhengHei"` / `PMingLiU` / `Arial` / `"Times New Roman"` / `Consolas`.',
        'Every stack\'s exported Latin / EA typefaces MUST resolve to Traditional-Chinese-safe fonts: `"Microsoft JhengHei"` / `"PingFang TC"` / `"Noto Sans TC"` / `PMingLiU` / `Arial` / `"Times New Roman"` / `Consolas`. Free TW fonts such as `GenSekiGothic2TW`, `GenSenRounded2TW`, and `GenRyuMin2TW` are allowed when the spec notes the install or embedding requirement.',
    )
    text = text.replace(
        'Every stack\'s exported Latin / EA typefaces MUST resolve to cross-platform pre-installed fonts: `"Microsoft JhengHei"` / `PMingLiU` / `Arial` / `"Times New Roman"` / `Consolas`.',
        'Every stack\'s exported Latin / EA typefaces MUST resolve to Traditional-Chinese-safe fonts: `"Microsoft JhengHei"` / `"PingFang TC"` / `"Noto Sans TC"` / `PMingLiU` / `Arial` / `"Times New Roman"` / `Consolas`. Free TW fonts such as `GenSekiGothic2TW`, `GenSenRounded2TW`, and `GenRyuMin2TW` are allowed when the spec notes the install or embedding requirement.',
    )
    text = text.replace(
        '`"Microsoft JhengHei", "PingFang TC"` for macOS preview nicety',
        '`"Microsoft JhengHei", "PingFang TC", "Noto Sans TC", "GenSekiGothic2TW"` for TC preview nicety',
    )
    text = text.replace(
        '`"Microsoft JhengHei", "PingFang TC"`',
        '`"Microsoft JhengHei", "PingFang TC", "Noto Sans TC", "GenSekiGothic2TW"`',
    )
    text = text.replace(
        '`Georgia, "Microsoft JhengHei", serif`',
        '`Georgia, "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", serif`',
    )
    text = text.replace(
        '`"Microsoft JhengHei", Georgia, serif`',
        '`"Microsoft JhengHei", "PingFang TC", "Noto Sans TC", Georgia, serif`',
    )
    text = text.replace(
        'Lead with Windows-preinstalled fonts (`Microsoft JhengHei` / `PMingLiU` / `Arial` / `Georgia` / `Consolas`); keep at most **one** macOS-exclusive family (typically `"PingFang TC"`) as a browser-preview nicety.',
        'Lead with Traditional-Chinese-safe PPT fonts (`Microsoft JhengHei` / `PMingLiU` / `Arial` / `Georgia` / `Consolas`); add `"PingFang TC"` for macOS preview and `"Noto Sans TC"` / `GenSekiGothic2TW` / `GenSenRounded2TW` only when the deck notes an install or embedding requirement.',
    )
    return text


def _replace_css_font_block(text: str) -> str:
    pattern = re.compile(
        re.escape(FONT_FACE_MARKER_START) + r".*?" + re.escape(FONT_FACE_MARKER_END) + r"\n*",
        flags=re.DOTALL,
    )
    text = pattern.sub("", text)
    return FONT_FACE_BLOCK + "\n" + text.lstrip()


def _normalize_ui_css(path: Path, text: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel not in {
        "skills/ppt-master/scripts/confirm_ui/static/style.css",
        "skills/ppt-master/scripts/svg_editor/static/style.css",
    }:
        return text
    text = _replace_css_font_block(text)
    if rel.endswith("confirm_ui/static/style.css"):
        text = re.sub(
            r'font-family:\s*-apple-system,\s*BlinkMacSystemFont,\s*"Segoe UI",\s*"Microsoft JhengHei",\s*"PingFang TC",\s*"PingFang TC",\s*sans-serif;',
            "font-family: var(--tw-ui-font-stack);",
            text,
        )
        text = re.sub(
            r'font-family:\s*-apple-system,\s*BlinkMacSystemFont,\s*"Segoe UI",\s*"Microsoft JhengHei",\s*"PingFang TC",\s*sans-serif;',
            "font-family: var(--tw-ui-font-stack);",
            text,
        )
        text = re.sub(
            r'font-family:\s*-apple-system,\s*BlinkMacSystemFont,\s*"Segoe UI",\s*"Microsoft YaHei",\s*"PingFang SC",\s*"Hiragino Sans GB",\s*sans-serif;',
            "font-family: var(--tw-ui-font-stack);",
            text,
        )
    else:
        text = re.sub(
            r'font-family:\s*-apple-system,\s*BlinkMacSystemFont,\s*"Segoe UI",\s*Roboto,\s*"Helvetica Neue",\s*Arial,\s*sans-serif;',
            "font-family: var(--tw-ui-font-stack);",
            text,
        )
    return text


def _localize_once(path: Path, text: str, overrides: Overrides) -> str:
    if not PREFILTER_RE.search(text):
        text = _derive_ui_zhtw_messages(path, text, overrides)
        text = _normalize_ui_css(path, text)
        return _normalize_readme_nav(path, text)

    hard_ranges = _hard_protected_ranges(path, text, overrides)
    text = _apply_replacements(text, overrides.replacements, hard_ranges)

    opencc_ranges = _opencc_protected_ranges(path, text, overrides)
    text = _opencc_selectively(text, opencc_ranges)

    hard_ranges = _hard_protected_ranges(path, text, overrides)
    text = _apply_replacements(text, overrides.replacements, hard_ranges)

    if path.suffix.lower() == ".svg":
        text = _normalize_svg_font_families(text)
    text = _normalize_reference_font_guidance(path, text)
    text = _derive_ui_zhtw_messages(path, text, overrides)
    text = _normalize_ui_css(path, text)
    return _normalize_readme_nav(path, text)


def localize_text(path: Path, text: str, overrides: Overrides) -> str:
    current = text
    for _ in range(4):
        updated = _localize_once(path, current, overrides)
        if updated == current:
            return updated
        current = updated
    return current


def process_file(path: Path, overrides: Overrides, *, check: bool) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    converted = localize_text(path, original, overrides)
    if converted == original:
        return False
    if not check:
        path.write_text(converted, encoding="utf-8")
    return True


def process_derived_readme_tw(overrides: Overrides, *, check: bool) -> bool:
    try:
        source = README_CN_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"cannot read {_repo_rel(README_CN_PATH)}: {exc}") from exc

    expected = localize_text(README_TW_PATH, source, overrides)
    expected = _with_readme_nav(expected, README_TW_NAV)

    try:
        current = README_TW_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        current = ""
    except UnicodeDecodeError:
        current = ""

    if current == expected:
        return False
    if not check:
        README_TW_PATH.write_text(expected, encoding="utf-8")
    return True


def ensure_opencc() -> Optional[str]:
    if not OPENCC_BIN.exists():
        return f"opencc not found at {OPENCC_BIN}"
    try:
        proc = subprocess.run(
            [str(OPENCC_BIN), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            check=False,
        )
    except OSError as exc:
        return str(exc)
    if proc.returncode != 0:
        return proc.stderr.strip() or "opencc --version failed"
    return None


def main(argv: Optional[list[str]] = None) -> int:
    configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)

    opencc_error = ensure_opencc()
    if opencc_error:
        print(f"ERROR: {opencc_error}", file=sys.stderr)
        return 2

    overrides = load_overrides()
    changed: list[Path] = []
    total = 0
    try:
        if process_derived_readme_tw(overrides, check=args.check):
            changed.append(README_TW_PATH)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for path in iter_target_files():
        total += 1
        if process_file(path, overrides, check=args.check):
            changed.append(path)

    if args.check:
        if changed:
            print(f"FAIL: 殘留 {len(changed)} 檔")
            for path in changed:
                print(path.relative_to(ROOT).as_posix())
            return 1
        print("PASS: 殘留 0 檔")
        return 0

    print(f"Converted {len(changed)} file(s); scanned {total} file(s).")
    for path in changed:
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
