# 工具與上游同步 SOP

本目錄放置 `ppt-master.TW` fork 的可重複執行維護工具。繁體中文化以 `tw_localize.py` 為唯一入口；任何需要長期保留的詞彙修正，請加入 `tw_localize_overrides.json` 或腳本邏輯，不要只做一次性手工修改。

> 使用者面的擴充用法（`--html-deck` 匯出、繁中字型安裝、PDF 路徑、同步檢查清單）見 [`docs/zh/tw-fork-guide.md`](../docs/zh/tw-fork-guide.md)。本檔只記管線內部細節。

## 上游同步流程

> 交給 AI agent 執行的完整逐步手冊（衝突分流、回歸驗證、暫停時機）見 [`docs/zh/upstream-sync-runbook.md`](../docs/zh/upstream-sync-runbook.md)。

```bash
git remote add upstream https://github.com/hugohe3/ppt-master.git
git fetch upstream
git merge upstream/main
python3 tools/tw_localize.py
python3 tools/tw_localize.py --check
git diff
```

如果 `upstream` 已存在，第一行可略過。合併後先解決衝突，再重跑繁中化工具；`--check` 必須輸出 `PASS: 殘留 0 檔` 才算完成。

## 覆蓋表

`tw_localize_overrides.json` 是 OpenCC 之外的專案詞彙表，適合放：

- OpenCC 不處理的 UI 語系標記，例如 `zh-CN` → `zh-TW`
- 簡中專用字體到繁中常用字體的替換
- 經人工確認後需要固定的台灣用語

覆蓋表會避開 en/ja i18n 內容、URL、路徑與程式碼指令區塊。

## 雙中文 UI 字典（2026-07 起改為 overlay 模式）

fork 政策已改為「不再對上游內容跑全量繁化，zh-TW 只存在於 web UI 層」，UI 的正體中文改為手工維護、貼近上游：

- `confirm_ui/static/app.js` 與 `svg_editor/static/app.js` 保留上游 `MESSAGES.zh` 原文不動，`MESSAGES.zhtw` 是 fork 直接維護的字典區塊；`t()` 依 `LANG_FALLBACK` 鏈查詢，zhtw 缺鍵時自動退回 zh。
- `confirm_ui/static/catalogs.json` 與上游逐位元組相同，**不要**為了繁化去改它。正體標籤放在 sidecar `catalogs.zhtw.json`，由 `app.js` 的 `applyZhtwCatalogOverlay()` 在載入時注入 `*_zhtw` 欄位（`visual_styles` 依上游 group 標籤巢狀，`_image_comparison` 區塊修補 app.js 內的 `IMAGE_COMPARISON_LABELS`）。
- 每次上游同步後執行 `python3 tools/ui_zhtw_overlay.py`：回報 overlay 缺譯（上游新增或改動的 zh 字串）、失效項目（上游已移除）與兩個 app.js 的 `MESSAGES` 鍵位落差；`--derive` 會用 OpenCC 印出草稿翻譯供人工審閱後併入。此檢查不通過（exit 1）就代表 zhtw 介面會出現簡體 fallback 或原始鍵名。

`tw_localize.py` 的 `derive_ui_zhtw_messages` 流程已停用，保留僅供歷史參考。

## README 衍生

根目錄 `README_CN.md` 保留上游簡體原文並排除於一般繁化掃描之外；`tw_localize.py` 每次執行時會用 OpenCC `s2twp` 加覆蓋表從它重新衍生 `README_TW.md`。這個模式與 UI 的 `MESSAGES.zh` → `MESSAGES.zhtw` 相同：簡體來源受保護，繁體產物由管線覆寫，繁中用語修正請放進 `tw_localize_overrides.json`。
