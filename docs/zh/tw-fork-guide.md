# .TW Fork 擴充與維護指南

本檔案集中記錄 `ppt-master.TW` 相對上游 [`yelban/ppt-master`](https://github.com/yelban/ppt-master) 的**所有新增功能與差異**，同時當作上游同步時的檢查清單。管線內部細節（覆蓋表、雙中文字典、README 衍生）見 [`tools/README.md`](../../tools/README.md)，本檔案不重複，只補使用者面的用法。

## 這個 fork 加了什麼

| 類別 | 新增內容 | 檔案 |
|------|----------|------|
| 繁化管線 | OpenCC `s2twp` ＋ 覆蓋表，全 repo 可重複執行繁化 | `tools/tw_localize.py`、`tools/tw_localize_overrides.json` |
| 預覽 UI | 語系選單新增「正體中文」；繁中 webfont（jsDelivr CDN） | `scripts/confirm_ui/`、`scripts/svg_editor/` |
| 匯出擴充 | `--html-deck` / `--embed-fonts`：輸出可離線瀏覽的 HTML 投影片 | `scripts/svg_to_pptx/pptx_package/html_deck.py` |
| 檔案 | 繁中 README（`README_TW.md`，由管線衍生）、本指南 | `README_TW.md`、`docs/zh/tw-fork-guide.md` |

## 匯出 HTML 投影片（`--html-deck`）

`svg_to_pptx.py` 在既有的 PPTX 匯出之外，可額外輸出一份把每頁 SVG inline 進去的自足 HTML，開啟即可用鍵盤瀏覽，不需伺服器、不經過 PPTX。

```bash
# 只要 PPTX（預設行為，不變）
python3 skills/ppt-master/scripts/svg_to_pptx.py <專案路徑>

# 額外產出可瀏覽的 HTML
python3 skills/ppt-master/scripts/svg_to_pptx.py <專案路徑> --html-deck

# 再把繁中 webfont 一起打包（給沒裝字型的檢視者）
python3 skills/ppt-master/scripts/svg_to_pptx.py <專案路徑> --html-deck --embed-fonts
```

- **輸出位置**：與 PPTX 同資料夾，`<專案>/exports/<專案名>_<時間戳>.html`。用 `-o path/deck.pptx` 指定時，HTML 放同目錄同名換 `.html`。
- **來源**：優先讀自足的 `svg_final/`；不存在則退回 `svg_output/`（此時圖片/icon 可能未內嵌，stdout 會提醒）。
- **操作**：`←` `→` / 空白鍵翻頁、`Home` `End` 首末頁、點畫面右半下一頁、左半上一頁、右下角頁碼。

### 兩個旗標怎麼選

| 情境 | 指令 | 原因 |
|------|------|------|
| 自己在本機看 | `--html-deck` | 本機已裝字型即可顯示，檔案較小 |
| 傳給別人／上傳分享 | `--html-deck --embed-fonts` | 注入指向 jsDelivr CDN 的 `@font-face`，對方免裝字型也能顯示繁中 |

> `--embed-fonts` 是注入 CDN `@font-face`（開啟時線上抓字型），**不是**把字型 base64 內嵌，離線環境仍需本機有字型。

## 繁中字型

分兩個層面，用途不同：

1. **預覽 UI 的 webfont**：`tools/tw_localize.py` 的 `FONT_FACE_BLOCK` 已把 7 支繁中免費字型（源石黑體、源泉圓體、源流明體、霞鶩文楷 TC、芫荽、清松手寫體 1／2）以 jsDelivr `@font-face` 注入兩個預覽頁面。重跑管線會自動維持，無需手動。
2. **本機渲染字型**：`rsvg-convert`、LibreOffice、或不吃 webfont 的離線瀏覽，需要字型**實際安裝在本機**。

### 本機安裝步驟（macOS）

CDN 上是 woff2，但系統／rsvg／LibreOffice 只吃 sfnt（ttf/otf），需先解壓：

```bash
# 1) 下載 7 支 woff2（與 UI 同源）
cd "$(mktemp -d)"
base="https://cdn.jsdelivr.net/gh/yelban"
for f in \
  "font-genseki-tw@latest/GenSekiGothic2TW-R.woff2" \
  "font-gensen-tw@latest/GenSenRounded2TW-R.woff2" \
  "font-genryu-tw@latest/GenRyuMin2TW-R.woff2" \
  "font-lxgw-wenkai-tc@latest/LXGWWenKaiTC-Regular.woff2" \
  "font-iansui@latest/Iansui-Regular.woff2" \
  "font-jason1@latest/JasonHandwriting1-Regular.woff2" \
  "font-jason2@latest/JasonHandwriting2-Regular.woff2"; do
  curl -sL "$base/$f" -o "${f##*/}"
done

# 2) woff2 → sfnt（需 fonttools + brotli）
uv run --with fonttools --with brotli python3 - <<'PY'
from fontTools.ttLib import TTFont
import glob, os
for w in glob.glob("*.woff2"):
    f = TTFont(w); f.flavor = None
    out = os.path.splitext(w)[0] + (".otf" if "CFF " in f else ".ttf")
    f.save(out)
PY

# 3) 安裝並更新快取
cp *.otf *.ttf ~/Library/Fonts/
fc-cache -f ~/Library/Fonts

# 4) 驗證（每支應指向剛裝的檔案，非 fallback）
for n in GenSekiGothic2TW GenSenRounded2TW GenRyuMin2TW LXGWWenKaiTC Iansui JasonHandwriting1 JasonHandwriting2; do
  fc-match "$n"
done
```

> 另建議一併安裝 **Noto Sans TC**（繁中字型堆疊的首選）：
> `curl -sL "https://github.com/google/fonts/raw/main/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf" -o ~/Library/Fonts/NotoSansTC.ttf && fc-cache -f`

字型內部 family 名帶空格（如 `GenSekiGothic2 TW`），但 fontconfig 的模糊比對能對應簡報用的無空格名（`GenSekiGothic2TW`），已驗證 `fc-match` 解析正確。

## 匯出 PDF 的三條路徑

三種產物各有獨立的 PDF 路徑，彼此無先後依賴：

| 產物 | 出 PDF 方式 | 特性 |
|------|-------------|------|
| PPTX | `soffice --headless --convert-to pdf <檔>.pptx`（需裝 LibreOffice）或 PowerPoint | 原生 DrawingML 形狀、可編輯級；需本機裝字型 |
| `svg_final/` SVG | `rsvg-convert -f pdf -o out.pdf svg_final/*.svg` | 與螢幕預覽畫素級一致 |
| HTML deck | Chrome headless 列印 | 本質同上一列 |

無論哪條路，**轉檔那臺機器都必須裝有簡報用到的繁中字型**，否則替換字型、版面跑掉。

## 上游同步檢查清單

```bash
git fetch upstream && git merge upstream/main   # 首次先 git remote add upstream https://github.com/yelban/ppt-master.git
# 解決衝突後：
python3 tools/tw_localize.py                     # 全 repo 繁化 + 衍生 zhtw 字典 + README_TW.md
python3 tools/tw_localize.py --check             # 必須 PASS: 殘留 0 檔
git diff                                          # 檢視
```

同步後另需人工確認（管線不會自動處理的部分）：

- **UI 若新增字串**：上游在 `MESSAGES.zh` 加了新 key → 繁化自動衍生 `zhtw`，但若出現需要臺灣在地化的用語，加進 `tw_localize_overrides.json`。
- **匯出 CLI 若被上游改動**：確認 `--html-deck` / `--embed-fonts` 的接線（`scripts/svg_to_pptx/pptx_package/cli.py`）與 `html_deck.py` 仍相容。
- **字型清單若調整**：`FONT_FACE_BLOCK` 的 woff2 檔名須對得上 jsDelivr 實際檔案（`-R.woff2` vs `-Regular.woff2` 曾出錯）。
