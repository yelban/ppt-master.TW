# 路線圖

[English](../roadmap.md) | [Chinese](./roadmap.md)

---

> PPT Master 是一個由個人維護的開源專案，按**優先順序而非固定時間表**推進。這份路線圖用來對齊預期：專案往哪個方向走、當下在做什麼、哪些事等真實需求出現再做、哪些明確不做。優先順序會隨使用者反饋和真實使用訊號調整——不承諾交付時間視窗。

---

## 方向

專案的主軸是**原生深度**：逐版本創作或保留更多 PowerPoint 自身的物件模型、行為與可複用結構——持續向 PowerPoint 本身靠攏。完整論述見[專案定位章程](./project-positioning.md)；[PowerPoint ↔ SVG 對映指南](./powerpoint-svg-mapping.md)逐特性誠實記錄當前邊界。

這條主軸今天體現為四條顯式產物路線：**Generate PPTX** 通過受約束的 SVG → DrawingML 創作全新設計的頁面；**Create Template** 產出可複用的 Brand / Layout / Deck 模板工作區；**Fill Native PPTX** 與 **Enhance Native PPTX** 通過限定範圍的 OOXML 操作保留既有檔案包。

---

## 進行中 / 下一步

明確在做或下一步要做，不承諾時間視窗。

- **在真實 deck 上校準新落地的體系** — 多 deck 合併 intake、材料發散度、插畫體系、結構化模板創作均已上線；它們現在需要的是真實使用訊號，而不是更多機制。不預先加機械閾值或配額。
- **Prompt 精簡** — 在不降質量的前提下壓縮各角色 prompt 的 token 佔用、提升快取命中率，帶來間接的成本 / 速度改善。與「純速度最佳化」的邊界見下方「明確不做」。

---

## 未來方向（訊號驅動）

已評估為「真實需求出現時值得做」的候選項，列出來是為了公開意圖，均不構成承諾。

- **持續收窄[對映指南](./powerpoint-svg-mapping.md)記錄的原生覆蓋缺口** — 逐版本把更多「僅 SVG」的格子推向 PowerPoint 原生結構與行為。
- **創作型預設形狀的效果支援**（如原生陰影）— 等形成精確的 preset-effect 契約並補齊 checker 覆蓋再做；在此之前，需要陰影的庫存形狀保守留普通 SVG。
- **生成側超連結創作** — 源 deck 裡已有的超連結如今能在轉換中保留；讓 Strategist 主動創作新連結，等需求出現再做。
- **圖片頁面背景提升為原生背景填充** — 純色 / 漸變頁面背景已匯出為 PowerPoint 原生底色；圖片背景按需求驅動。

---

## 已交付里程碑

一個月一行，細節見 [Release 釋出說明](https://github.com/hugohe3/ppt-master/releases)與 commit log。

| 時間 | 主題 |
|---|---|
| 2026-03 | **原生 PPTX 路線成形** — SVG → DrawingML 鏈路可用；圖表 / 版式模板索引上線 |
| 2026-04 | **管線規模化** — 僅憑主題生成、70 個圖表模板 + 三套圖示庫、`spec_lock` 跨頁一致性契約、逐元素動畫與旁白 / 影片匯出 |
| 2026-05 | **視覺化編輯 + AI 圖片體系化** — Live Preview 確定性原位編輯（基於 [@WodenJay](https://github.com/WodenJay) 的 [PR #85](https://github.com/hugohe3/ppt-master/pull/85)）、從 PPTX 建立模板工作區、rendering × palette × type 圖片體系、LaTeX 公式渲染 |
| 2026-06 | **mode 與 visual-style 雙 catalog + intake 擴充套件** — 5 種敘事 mode × 18 種視覺風格（+ `custom`）、內容忠實的美化 profile、多 deck 合併 intake、插畫切片管線、網路圖片質量閘門、源轉換保真提升（圖注識別基於 [@suay1113](https://github.com/suay1113) 的 [PR #191](https://github.com/hugohe3/ppt-master/pull/191)，超連結保留提煉自 [@ZhaoZuohong](https://github.com/ZhaoZuohong) 的 [PR #155](https://github.com/hugohe3/ppt-master/pull/155)） |
| 2026-07 | **定位章程 + 原生母版 / 版式 + token 效率**（[v4.0.0](https://github.com/hugohe3/ppt-master/releases/tag/v4.0.0)）— 三段式分步確認 UI、真 `p:sldMaster` / `p:sldLayout` 匯出、`--native-charts-and-tables` opt-in、動效匯出加固、圖表模板庫壓縮 |

---

## 明確不做（Non-goals）

下面這些方向被多次提過，已經評估並決定**不做**。列出來不是否定需求價值，而是說明它們與本專案產品方向不匹配；如果你剛好需要這些能力，建議看其他工具或 fork 本專案走自己的路。

### 對任意 PPTX placeholder 系統做無契約盲填

**對應 Issue**：[#53](https://github.com/hugohe3/ppt-master/issues/53)、[#118](https://github.com/hugohe3/ppt-master/issues/118)

Generate PPTX 路線圍繞完全可控的新形狀、文字與版式創作。結構完整的 PPTX 可以通過兩種顯式方式為經過確認的可複用模板包提供依據：`standard` / `fidelity` 以視覺證據為參考，創作新的 SVG 與 Master/Layout 系統；`mirror` 把來源包內實際存在的全部受支援事實物化到新工作區，包括未使用的 Layout 定義。兩者都不修改來源 PPTX，也不補造缺失的設計意圖。但「開啟任意 PPTX 後不經規範化就盲填所有佔位框」仍是另一種產品形態。

**基礎訴求其實很簡單**：如果只是「固定位置替換 Excel 資料到 PPT 模板」，直接讓 AI 寫一段 `python-pptx` 指令碼即可，幾行程式碼搞定，不需要本專案這套管線。

> **已支援邊界**：Fill Native PPTX（`template-fill-pptx`）直接回填選中的源頁面；Create Template（`create-template`）根據自然語言請求和來源證據，在內部推導重新創作或 mirror 物化實現；Strategist 再根據真實模板和當前內容推導 strict/adaptive 匯出行為。仍不做未經審查、沒有契約的任意第三方 placeholder 全自動替換。

### 把原生 PowerPoint 圖表設為預設路線

**對應 Issue**：[#99](https://github.com/hugohe3/ppt-master/issues/99)、[#100](https://github.com/hugohe3/ppt-master/issues/100) 類

跨四渲染器（PowerPoint / Keynote / LibreOffice / WPS）的位置保真是專案主軸。把預設路線改成 PowerPoint 原生圖表會讓「畫素級一致性」破功——同一個 PPTX 在不同渲染器裡圖表會顯示不同佈局。圖表預設用 SVG 是 **by design**，不是能力缺失。

窄例外是 `data-pptx-replace-with` marker：Design Spec §IX 頁面塊中獨立規劃、且寫明 `Native-ready: yes` 的受支援資料圖表與純文本網格表格可以攜帶 PowerPoint 原生 Chart/Table 替換 payload；`no` 與零星微型圖形保持普通 shape。§VII 只記錄真正選中的可複用參考。匯出加 `--native-charts-and-tables` 才啟用已準備的 marker——供主動用跨渲染器保真換取帶資料來源物件及圖表/表格專屬編輯模型的使用者使用；啟用後的物件會保留 deck 的 chart-area / plot / 軸線 / 網格線 / 標籤顏色與原生表格格式，不再塌回 PowerPoint 預設主題（見 [v4.0.0 釋出說明](https://github.com/hugohe3/ppt-master/releases/tag/v4.0.0)）。預設匯出路徑與可編輯的 SVG 派生形狀系統不變。

### uv 作為預設 / 必需依賴

**對應 Issue**：[#111](https://github.com/hugohe3/ppt-master/issues/111)

`pip + requirements.txt` 是唯一官方安裝路徑，因為它在所有 Python 環境下都可用、不需要額外學習成本。uv 是好工具，但「讓 uv 成為預設」會抬高新使用者的入門門檻。如果你個人偏好 uv，完全可以在 fork 裡用，不影響主線。

### 純速度最佳化

**對應 Issue**：[#97](https://github.com/hugohe3/ppt-master/issues/97)

成本 / 速度 / 質量三角下，本專案選擇**質量優先**。20 分鐘生成一個高質量 PPTX 是當前的合理點。

會做：通過 prompt 精簡 / 快取命中率提升帶來的間接改善；
不會做：以犧牲質量為代價的「隨便幾頁應付交差」式提速。

如果對速度敏感且能接受質量下降，零配置的瀏覽器 SaaS 工具更合適。

### 獨立 CLI / 託管 SaaS / 桌面 App 形態

產品形態明確為**執行在支援 Agent 的 AI 工具中的對話式工作流 / skill**（Claude Code、Codex、Cursor、VS Code agents 等）。

不會做：獨立 CLI（`ppm` 之類）、SaaS Web 服務、Electron 桌面殼。所有「讓它脫離 chat 獨立執行」的提案都會被拒。chat 是互動核心，不是包裝層。

---

## 反饋渠道

- **Issues**：[github.com/hugohe3/ppt-master/issues](https://github.com/hugohe3/ppt-master/issues) — 報告 Bug / 提建議
- **Discussions**：[github.com/hugohe3/ppt-master/discussions](https://github.com/hugohe3/ppt-master/discussions) — 用法討論 / 經驗分享
- **郵箱**：heyug3@gmail.com

提需求前先掃一眼上面的 **Non-goals**；如果你的需求落在那一節，多半不會被採納，但歡迎討論是否還有別的路徑解決你的真實問題。
