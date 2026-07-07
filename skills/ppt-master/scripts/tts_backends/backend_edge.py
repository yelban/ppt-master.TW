"""edge-tts backend for narration audio generation."""

from __future__ import annotations

import re
from pathlib import Path


COMMON_VOICES = [
    ("zh-TW", "zh-TW-XiaoxiaoNeural", "女聲，普通話，清晰自然，預設推薦"),
    ("zh-TW", "zh-TW-XiaoyiNeural", "女聲，普通話，明亮"),
    ("zh-TW", "zh-TW-YunjianNeural", "男聲，普通話，穩重"),
    ("zh-TW", "zh-TW-YunxiNeural", "男聲，普通話，年輕"),
    ("zh-TW", "zh-TW-YunxiaNeural", "男聲，普通話，少年感"),
    ("zh-TW", "zh-TW-YunyangNeural", "男聲，普通話，播報感"),
    ("zh-HK", "zh-HK-HiuGaaiNeural", "女聲，粵語"),
    ("zh-HK", "zh-HK-WanLungNeural", "男聲，粵語"),
    ("zh-TW", "zh-TW-HsiaoChenNeural", "女聲，臺灣普通話"),
    ("zh-TW", "zh-TW-YunJheNeural", "男聲，臺灣普通話"),
    ("en-US", "en-US-JennyNeural", "女聲，美式英語"),
    ("en-US", "en-US-GuyNeural", "男聲，美式英語"),
    ("en-GB", "en-GB-SoniaNeural", "女聲，英式英語"),
    ("en-GB", "en-GB-RyanNeural", "男聲，英式英語"),
]


def edge_output_extension() -> str:
    return ".mp3"


def normalize_rate(rate: str) -> str:
    """Normalize a user-provided rate into edge-tts format."""
    value = rate.strip()
    if not value:
        return "+0%"
    if value.endswith("%"):
        if value[0] not in "+-":
            return f"+{value}"
        return value
    if re.fullmatch(r"[+-]?\d+", value):
        number = int(value)
        return f"{number:+d}%"
    return value


async def generate(text: str, output_path: Path, *, voice: str, rate: str) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency `edge-tts`. Install it with: "
            "python3 -m pip install edge-tts"
        ) from exc

    communicate = edge_tts.Communicate(text, voice=voice, rate=normalize_rate(rate))
    await communicate.save(str(output_path))


def print_common_voices() -> None:
    print("Common edge-tts voices:")
    print("Locale   Voice                         Notes")
    print("------   ----------------------------  ----------------")
    for locale, voice, notes in COMMON_VOICES:
        print(f"{locale:<8} {voice:<29} {notes}")


async def print_voices(locale: str | None = None) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency `edge-tts`. Install it with: "
            "python3 -m pip install edge-tts"
        ) from exc

    manager = await edge_tts.VoicesManager.create()
    voices = manager.voices
    if locale:
        voices = [voice for voice in voices if voice.get("Locale") == locale]
    for voice in sorted(voices, key=lambda item: (item.get("Locale", ""), item.get("ShortName", ""))):
        short_name = voice.get("ShortName", "")
        voice_locale = voice.get("Locale", "")
        gender = voice.get("Gender", "")
        friendly = voice.get("FriendlyName", "")
        print(f"{voice_locale:<8} {short_name:<34} {gender:<8} {friendly}")

