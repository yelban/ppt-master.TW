#!/usr/bin/env python3
"""Check the confirm-UI zh-TW overlay against upstream catalogs after a sync.

The fork keeps ``catalogs.json`` byte-identical to upstream; zh-TW strings live
in the sidecar ``catalogs.zhtw.json`` that ``app.js`` merges at load time.
After each upstream sync, run this to find:

  * catalog fields whose zh text changed or appeared upstream but have no
    ``*_zhtw`` overlay entry (the UI falls back to Simplified until translated);
  * stale overlay entries pointing at sections/ids/fields that no longer exist;
  * ``MESSAGES`` dictionary keys present in ``zh`` but missing from ``zhtw``
    (those would render as raw key names without the t() fallback) in both
    confirm_ui and svg_editor app.js.

Usage:
    python3 tools/ui_zhtw_overlay.py            # report only, exit 1 if issues
    python3 tools/ui_zhtw_overlay.py --derive   # also print draft overlay JSON
                                                # for missing entries (OpenCC
                                                # s2twp when available)

``--derive`` output is a review draft, never applied automatically.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIRM_STATIC = REPO / 'skills/ppt-master/scripts/confirm_ui/static'
CATALOGS = CONFIRM_STATIC / 'catalogs.json'
OVERLAY = CONFIRM_STATIC / 'catalogs.zhtw.json'
APP_JS = {
    'confirm_ui': CONFIRM_STATIC / 'app.js',
    'svg_editor': REPO / 'skills/ppt-master/scripts/svg_editor/static/app.js',
}

CJK = re.compile(r'[㐀-鿿]')


def to_tw(text: str) -> str | None:
    """Best-effort s2twp conversion; None when OpenCC is unavailable."""
    try:
        import opencc  # type: ignore
        return opencc.OpenCC('s2twp').convert(text)
    except Exception:
        pass
    try:
        import subprocess
        r = subprocess.run(['opencc', '-c', 's2twp.json'], input=text,
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return r.stdout.rstrip('\n')
    except Exception:
        pass
    return None


def zh_fields(item: dict) -> dict[str, str]:
    """Translatable fields of one catalog item: *_zh plus bare CJK strings."""
    out = {}
    for field, value in item.items():
        if not isinstance(value, str):
            continue
        if field.endswith('_zh'):
            out[field[:-3]] = value
        elif not re.search(r'_(en|ja|zhtw)$', field) and CJK.search(value):
            out[field] = value
    return out


def walk_catalog(cat: dict):
    """Yield (section, group_key_or_None, item_id, base_field, zh_value)."""
    for section, value in cat.items():
        if not isinstance(value, list):
            continue
        for entry in value:
            if not isinstance(entry, dict):
                continue
            if section == 'visual_styles':
                gkey = entry.get('group')
                for base, zh in zh_fields(entry).items():
                    yield section, gkey, '_group', base, zh
                for item in entry.get('items', []):
                    for base, zh in zh_fields(item).items():
                        yield section, gkey, item['id'], base, zh
            elif 'id' in entry:
                for base, zh in zh_fields(entry).items():
                    yield section, None, entry['id'], base, zh


def overlay_lookup(ov: dict, section: str, gkey, item_id: str) -> dict:
    node = ov.get(section, {})
    if gkey is not None:
        node = node.get(gkey, {})
    return node.get(item_id, {}) if isinstance(node, dict) else {}


def messages_keys(js_path: Path, lang: str) -> set[str]:
    """Heuristically extract key names of MESSAGES.<lang> from an app.js."""
    src = js_path.read_text(encoding='utf-8')
    m = re.search(rf'^\s{{8}}{lang}:\s*{{', src, re.M)
    if not m:
        return set()
    depth, i = 0, src.index('{', m.start())
    start = i
    while i < len(src):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1
    block = src[start:i]
    return set(re.findall(r'^\s{12}([A-Za-z0-9_]+):', block, re.M))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--derive', action='store_true',
                        help='print draft overlay JSON for missing entries')
    args = parser.parse_args()

    cat = json.loads(CATALOGS.read_text(encoding='utf-8'))
    ov = json.loads(OVERLAY.read_text(encoding='utf-8'))

    missing, draft = [], {}
    live_keys = set()
    for section, gkey, item_id, base, zh in walk_catalog(cat):
        live_keys.add((section, gkey, item_id, base + '_zhtw'))
        if base + '_zhtw' in overlay_lookup(ov, section, gkey, item_id):
            continue
        tw = to_tw(zh)
        if tw is not None and tw == zh:
            continue  # identical in Traditional; fallback to zh is lossless
        where = f'{section}.{gkey + "." if gkey else ""}{item_id}.{base}'
        missing.append(f'{where}: {zh!r}' + ('' if tw else ' (opencc unavailable — review manually)'))
        if tw:
            node = draft.setdefault(section, {})
            if gkey is not None:
                node = node.setdefault(gkey, {})
            node.setdefault(item_id, {})[base + '_zhtw'] = tw

    stale = []
    for section, node in ov.items():
        if section.startswith('_'):
            continue
        for k1, v1 in node.items():
            for k2, v2 in v1.items():
                if isinstance(v2, dict):  # visual_styles: group -> item -> fields
                    for field in v2:
                        if (section, k1, k2, field) not in live_keys:
                            stale.append(f'{section}.{k1}.{k2}.{field}')
                elif (section, None, k1, k2) not in live_keys:
                    stale.append(f'{section}.{k1}.{k2}')

    parity = []
    for name, path in APP_JS.items():
        zh = messages_keys(path, 'zh')
        zhtw = messages_keys(path, 'zhtw')
        if not zh or not zhtw:
            parity.append(f'{name}: could not locate MESSAGES zh/zhtw blocks')
            continue
        for key in sorted(zh - zhtw):
            parity.append(f'{name}: MESSAGES.zhtw missing {key!r}')
        for key in sorted(zhtw - zh):
            parity.append(f'{name}: MESSAGES.zhtw stale key {key!r}')

    ok = not (missing or stale or parity)
    for title, rows in (('Missing overlay entries', missing),
                        ('Stale overlay entries', stale),
                        ('MESSAGES parity', parity)):
        print(f'{title}: {len(rows)}')
        for row in rows:
            print(f'  {row}')
    if args.derive and draft:
        print('\n--- draft additions (review before merging into catalogs.zhtw.json) ---')
        print(json.dumps(draft, ensure_ascii=False, indent=2))
    print('\nOK' if ok else '\nIssues found — translate or prune, see above.')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
