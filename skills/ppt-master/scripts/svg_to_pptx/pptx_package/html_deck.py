#!/usr/bin/env python3
"""
PPT Master - HTML Deck Builder

Build a single HTML slide deck from inline SVG pages.

Usage:
    build_html_deck(project_path, svg_files, out_path, embed_fonts=False)

Examples:
    build_html_deck(project_path, svg_files, project_path / "exports" / "deck.html")

Dependencies:
    None (only uses standard library)
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from .dimensions import get_viewbox_dimensions


TW_FONT_FACE_BLOCK = """/* ---- Traditional Chinese web fonts ---- */
@font-face {
    font-family: "GenSekiGothic2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-genseki-tw@latest/GenSekiGothic2TW-R.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "GenSenRounded2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-gensen-tw@latest/GenSenRounded2TW-R.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "GenRyuMin2TW";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-genryu-tw@latest/GenRyuMin2TW-R.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "LXGWWenKaiTC";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-lxgw-wenkai-tc@latest/LXGWWenKaiTC-Regular.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "Iansui";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-iansui@latest/Iansui-Regular.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "JasonHandwriting1";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-jason1@latest/JasonHandwriting1-Regular.woff2") format("woff2");
    font-display: swap;
}

@font-face {
    font-family: "JasonHandwriting2";
    src: url("https://cdn.jsdelivr.net/gh/yelban/font-jason2@latest/JasonHandwriting2-Regular.woff2") format("woff2");
    font-display: swap;
}

:root {
    --tw-ui-font-stack: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", "GenSekiGothic2TW", "GenSenRounded2TW", "GenRyuMin2TW", "LXGWWenKaiTC", "Iansui", "JasonHandwriting1", "JasonHandwriting2", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
/* ---- End Traditional Chinese web fonts ---- */"""

_SVG_OPEN_RE = re.compile(r'<svg\b', re.IGNORECASE)
_SVG_CLOSE_RE = re.compile(r'</svg\s*>', re.IGNORECASE)


def _extract_svg_markup(svg_path: Path) -> str:
    text = svg_path.read_text(encoding='utf-8-sig')
    open_match = _SVG_OPEN_RE.search(text)
    close_matches = list(_SVG_CLOSE_RE.finditer(text))
    if not open_match or not close_matches:
        raise ValueError(f"SVG root element not found: {svg_path}")
    return text[open_match.start():close_matches[-1].end()].strip()


def _slide_dimensions(svg_path: Path) -> tuple[int, int]:
    dimensions = get_viewbox_dimensions(svg_path)
    if dimensions is None:
        return 1280, 720
    width, height = dimensions
    if width <= 0 or height <= 0:
        return 1280, 720
    return width, height


def _slide_html(svg_path: Path, index: int) -> str:
    width, height = _slide_dimensions(svg_path)
    ratio = width / height
    safe_name = html.escape(svg_path.name, quote=True)
    markup = _extract_svg_markup(svg_path)
    return (
        f'<section class="slide" data-slide="{index}" '
        f'aria-label="Slide {index + 1}: {safe_name}" '
        f'aria-hidden="true" '
        f'style="--w: {width}; --h: {height}; --ratio: {ratio:.8f};">\n'
        f'  <div class="stage">{markup}</div>\n'
        '</section>'
    )


def _style_block(embed_fonts: bool) -> str:
    font_css = TW_FONT_FACE_BLOCK + "\n\n" if embed_fonts else ""
    return f"""{font_css}* {{
    box-sizing: border-box;
}}

html,
body {{
    width: 100%;
    height: 100%;
    margin: 0;
    overflow: hidden;
    background: #101114;
}}

body {{
    color: #ffffff;
    font-family: var(--tw-ui-font-stack, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);
}}

.deck {{
    position: fixed;
    inset: 0;
    overflow: hidden;
    background: #101114;
}}

.slide {{
    position: absolute;
    inset: 0;
    display: none;
    place-items: center;
    overflow: hidden;
}}

.slide.active {{
    display: grid;
}}

.stage {{
    width: 100vw;
    max-width: calc(100vh * var(--ratio));
    max-height: 100vh;
    aspect-ratio: var(--w) / var(--h);
    background: #ffffff;
}}

.stage > svg {{
    display: block;
    width: 100%;
    height: 100%;
}}

.counter {{
    position: fixed;
    right: 16px;
    bottom: 14px;
    z-index: 20;
    min-width: 58px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(16, 17, 20, 0.72);
    color: #ffffff;
    font-size: 13px;
    line-height: 1;
    text-align: center;
    user-select: none;
    pointer-events: none;
    backdrop-filter: blur(8px);
}}"""


def _script_block(deck_title: str) -> str:
    title_json = json.dumps(deck_title)
    return f"""(() => {{
    const deckTitle = {title_json};
    const slides = Array.from(document.querySelectorAll('.slide'));
    const counter = document.getElementById('counter');
    let current = 0;

    function show(index) {{
        if (!slides.length) {{
            return;
        }}
        current = Math.max(0, Math.min(index, slides.length - 1));
        slides.forEach((slide, slideIndex) => {{
            const active = slideIndex === current;
            slide.classList.toggle('active', active);
            slide.setAttribute('aria-hidden', active ? 'false' : 'true');
        }});
        counter.textContent = `${{current + 1}} / ${{slides.length}}`;
        document.title = `${{deckTitle}} (${{current + 1}}/${{slides.length}})`;
    }}

    function next() {{
        show(current + 1);
    }}

    function previous() {{
        show(current - 1);
    }}

    document.addEventListener('keydown', (event) => {{
        if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) {{
            return;
        }}
        switch (event.key) {{
            case 'ArrowRight':
            case ' ':
            case 'PageDown':
                event.preventDefault();
                next();
                break;
            case 'ArrowLeft':
            case 'PageUp':
                event.preventDefault();
                previous();
                break;
            case 'Home':
                event.preventDefault();
                show(0);
                break;
            case 'End':
                event.preventDefault();
                show(slides.length - 1);
                break;
        }}
    }});

    document.addEventListener('click', (event) => {{
        if (event.button !== 0) {{
            return;
        }}
        if (event.clientX >= window.innerWidth / 2) {{
            next();
        }} else {{
            previous();
        }}
    }});

    show(0);
}})();"""


def build_html_deck(
    project_path: Path,
    svg_files: list[Path],
    out_path: Path,
    embed_fonts: bool,
) -> Path:
    """Write a single-file HTML deck with inline SVG slides."""
    if not svg_files:
        raise ValueError("No SVG files supplied for HTML deck")

    project_path = Path(project_path)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    deck_title = project_path.name
    slides = "\n".join(_slide_html(Path(svg_path), index) for index, svg_path in enumerate(svg_files))
    safe_title = html.escape(deck_title)
    document = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
<style>
{_style_block(embed_fonts)}
</style>
</head>
<body>
<main class="deck" id="deck" aria-label="Slide deck">
{slides}
</main>
<div class="counter" id="counter" aria-live="polite">1 / {len(svg_files)}</div>
<script>
{_script_block(deck_title)}
</script>
</body>
</html>
"""
    out_path.write_text(document, encoding='utf-8')
    return out_path
