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

## 雙中文 UI 字典

`confirm_ui/static/app.js` 與 `svg_editor/static/app.js` 會保留上游 `MESSAGES.zh` 作為簡體中文來源，`tw_localize.py` 會保護這個區塊不做繁化，並在每次執行時用 OpenCC `s2twp` 加覆蓋表重新衍生 `MESSAGES.zhtw`。因此繁中文案修正一律加入 `tw_localize_overrides.json`，不要手工維護 `zhtw` 副本。

## README 衍生

根目錄 `README_CN.md` 保留上游簡體原文並排除於一般繁化掃描之外；`tw_localize.py` 每次執行時會用 OpenCC `s2twp` 加覆蓋表從它重新衍生 `README_TW.md`。這個模式與 UI 的 `MESSAGES.zh` → `MESSAGES.zhtw` 相同：簡體來源受保護，繁體產物由管線覆寫，繁中用語修正請放進 `tw_localize_overrides.json`。
