# 技術路線

[English](../technical-design.md) | [中文](./technical-design.md)

---

## 設計哲學 —— AI 是你的設計師，不是完工師

生成的 PPTX 是一份**設計稿**，而非成品。把它理解成建築師的效果圖：AI 負責視覺設計、排版佈局和內容結構，交付給你一個高質量的起點。要想獲得真正精良的成品，**需要你自己在 PowerPoint 裡做精裝修**：換掉形狀、細化圖表、調整配色、把佔位圖形替換成原生物件。這個工具的目標是消除 90% 的從零開始的工作量，而不是替代人在最後一公里的判斷。不要指望 AI 一遍搞定所有——好的簡報從來不是這樣做出來的。

**工具的上限是你的上限。** PPT Master 放大的是你已有的能力——你有設計感和內容判斷力，它幫你快速落地；你不知道一個好的簡報應該長什麼樣，它也沒法替你知道。輸出的質量，歸根結底是你自身品味與判斷力的對映。

---

## 系統架構

```
用户输入 (PDF/DOCX/XLSX/PPTX/URL/Markdown/主题文本)
    ↓
[源内容转换] → source_to_md/pdf_to_md.py / doc_to_md.py / excel_to_md.py / ppt_to_md.py / web_to_md.py
    ├── sources/ 内容型文件是内容契约
    └── PPTX intake 写入 analysis/<stem>.identity.json、<stem>.slide_library.json、source_profile.json
    ↓
[创建项目] → project_manager.py init <项目名> --format <格式>
    ↓
[模板 / 品牌 / 布局（可选）] — 默认跳过，直接自由设计
    仅在用户提供明确模板目录路径且其中 design_spec.md 声明 kind: brand/layout/deck 时触发
    原生 PPTX 模板请求进入 template-fill；可复用 SVG 模板需先通过 create-template 创建
    ↓
[Strategist] 策略师 - 三阶段策略师确认与设计规范 → design_spec.md + spec_lock.md
    ↓
[Image Acquisition] 图片获取（当资源列表中有需要 AI 生成、网络搜索或切片的图片时）
    ↓
[Executor] 执行师
    ├── 生成开始前启动 live preview，并在生成期间保持可用
    ├── 视觉构建：按页顺序连续生成 SVG 页面 → svg_output/
    ├── [Quality Check] svg_quality_checker.py（强制通过，0 错误）
    └── 讲稿生成：完整讲稿 → notes/total.md
    ↓
[图表校准（可选）] → verify-charts 工作流（含数据图表的幻灯片在此步骤校准坐标）
    ↓
[视觉自检（可选，opt-in）] → visual-review 工作流（仅在用户明确请求时触发）
    ↓
[后处理] → total_md_split.py（拆分讲稿）→ finalize_svg.py → svg_to_pptx.py
    ↓
输出：
    exports/
    ├── presentation_<timestamp>.pptx                ← 原生形状版（DrawingML）— 唯一标准产物，编辑/交付从这里走
    ├── presentation_<timestamp>_native_charts.pptx  ← 原生图表/表格对象版（而非压平形状，加 --native-objects 时生成）
    └── presentation_<timestamp>_svg.pptx            ← SVG 快照版 pptx — 像素级视觉参考（加 --svg-snapshot 时生成）

    # 默认流程（未指定 -o）始终写入
    backup/<timestamp>/
    └── svg_output/                            ← Executor 原始 SVG 备份（重跑 finalize_svg → svg_to_pptx 即可重建 pptx）
```

以下直接 PPTX 工作流會有意繞過這條 SVG 路線：

| 工作流 | 輸入角色 | 輸出機制 | 為什麼獨立 |
|---|---|---|---|
| `template-fill-pptx` | 原生 PPTX 模板 deck + 新材料 | 克隆選中的幻燈片，並在 OOXML 層改寫文本 / 表格 / 圖表 | 保留使用者的 PowerPoint 原生頁面殼，而不是轉成 SVG |
| `native-enhance-pptx` | 內容與版式都應保持穩定的已完成 PPTX | 在 OOXML 層直接補講稿、旁白、計時和轉場 | 只追加原生增強，不重新設計 |
| `beautify-pptx` | 頁數、頁序、每頁措辭都必須 1:1 保留的已有 PPTX | 抽取源事實後走 SVG 流水線重新生成 native deck | 只改佈局和層級，不做原地編輯 |

---

## 路線判定速查表

可執行路線判定以 [`workflows/routing.md`](../../skills/ppt-master/workflows/routing.md) 為準；本節只是面向技術設計的速查和解釋，不是第二份路線矩陣。

先用這張表判定路線，再討論實現細節。大多數失敗執行不是命令錯了，而是一開始就走錯了路線。

| 請求形態 | 路線 | 邊界 |
|---|---|---|
| 只有主題，沒有原始檔或足夠源文本 | 先走 `topic-research`，再進入主流水線 | 網路 / 來源收集是前置步驟 |
| 有原始檔或對話文本，deck 結構可以重想 | 主 SVG 流水線 | Strategist 可以拆分、合併、刪除、重排和重設計 |
| PPTX 作為源材料，使用者允許重構故事和頁結構 | `ppt_to_md` + `pptx_intake`，再走主 SVG 流水線 | PPTX 身份和幾何是事實與候選，不是復刻約束 |
| 原生 PPTX 模板 + 新材料 / 新主題 | `template-fill-pptx` | 克隆並填充原生頁面；不生成 SVG |
| 現有 PPTX，頁數 / 頁序 / 措辭 1:1 保留，只改善排版 | `beautify-pptx` | 通過 SVG 重新生成；內容和分頁鎖定 |
| 已完成 PPTX，保持內容 / 佈局穩定，只加講稿、音訊、計時、轉場 | `native-enhance-pptx` | 直接 OOXML patch；不重新設計 |
| 使用者想從 PPTX 或設計參考構建可複用模板包 | `create-template` 或 `create-brand` | 輸出後續能觸發 Step 3 的目錄 |
| 使用者提供明確的 `templates/.../<id>/` 目錄且宣告 `kind: brand/layout/deck` | 主 SVG 流水線 Step 3 | 應用模板片段所有權和融合規則 |
| 使用者要求調整物件級動畫順序 / 效果 / 計時 | `customize-animations` | 通過 `animations.json` 控制可選匯出策略 |
| 使用者要求預覽、選擇、註解或重匯出瀏覽器編輯 | `live-preview` | 瀏覽器工作流；註解只在規定交接點應用 |

“最佳化這份 PPT”這類含糊請求歸約為一個判定點：是否保留原始頁數、頁序和逐頁措辭。保留就是 `beautify-pptx`；允許重構就是主流水線。

---

## 技術流程

**核心流程：AI 生成 SVG → 後處理轉換為 DrawingML（PPTX）。**

整個流程分為三個階段：

**第一階段：內容理解與設計規劃**
原始檔（PDF/DOCX/XLSX/PPTX/URL/Markdown/主題文本）會被轉換成 Strategist 所需的內容事實與分析事實。Strategist 角色分析材料、讀取相關 `analysis/` artifact、規劃頁面結構，並確認視覺風格，最終輸出完整設計規格。

**第二階段：AI 視覺生成**
Executor 角色逐頁生成簡報的視覺內容，輸出為 SVG 檔案。這個階段的產物是**設計稿**，而非成品。

**第三階段：工程化轉換**
後處理指令碼將 SVG 轉換為 DrawingML，每一個形狀都變成真正的 PowerPoint 原生物件——可點選、可編輯、可改色，而不是嵌入的圖片。

---

## 產物流

Artifact 的來源 / 派生所有權以 [`artifact-ownership.md`](../../skills/ppt-master/references/artifact-ownership.md) 為準；本節只把同一資料流視覺化成架構說明。

維護這套系統時，把資料夾理解成資料流會比“這些目錄剛好存在”更清楚：

```text
sources/<content files> ────────┐
analysis/source_profile.json ───┼─> Strategist -> design_spec.md + spec_lock.md
analysis/image_analysis.csv ────┘

spec_lock.md + images/ + icons/ + templates/
    └─> Executor -> svg_output/
              ├─> svg_quality_checker.py
              ├─> finalize_svg.py -> svg_final/
              └─> svg_to_pptx.py -> exports/<name>_<ts>.pptx
                                      backup/<ts>/svg_output/

直接 OOXML 路由：
analysis/<stem>.slide_library.json + 源 PPTX + fill_plan.json
    └─> template_fill_pptx.py -> exports/*.pptx
源 PPTX 项目归档副本 + 增强计划 + 讲稿/音频/计时资产
    └─> native_enhance_pptx.py -> exports/*.pptx
```

關鍵切分是：`svg_output/` 是作者狀態，`svg_final/`、`exports/` 和 `backup/` 是派生的交付或歸檔狀態。模糊這條線，會讓校驗、重匯出和人工修復都更難推理。

---

## 為什麼是 SVG？

SVG 是這套流程的核心樞紐。這個選擇是通過逐一排除其他方案得出的。

**直接生成 DrawingML** 看起來最直接——跳過中間格式，AI 直接輸出 PowerPoint 的底層 XML。但 DrawingML 極其繁瑣，一個簡單的圓角矩形就需要數十行巢狀 XML，AI 的訓練資料中遠少於 SVG，生成質量不穩定，除錯幾乎無法肉眼完成。

**HTML/CSS** 是 AI 最熟悉的格式之一，但 HTML 和 PowerPoint 有根本不同的世界觀。HTML 描述的是**檔案**——標題、段落、列表，元素的位置由內容流動決定。PowerPoint 描述的是**畫布**——每個元素都是獨立的、絕對定位的物件，沒有流，沒有上下文關係。這不只是排版計算的問題，而是兩種完全不同的內容組織方式之間的鴻溝。就算解決了瀏覽器排版引擎的問題（Chromium 用數百萬行程式碼做這件事），HTML 裡的一個 `<table>` 也沒法自然地變成 PPT 裡的幾個獨立形狀。

**WMF/EMF**（Windows 圖元檔案）是微軟自家的原生向量圖形格式，與 DrawingML 有直接的血緣關係——理論上轉換損耗最小。但 AI 對它幾乎沒有訓練資料，這條路死在起點。值得注意的是：連微軟自家的格式在這裡都輸給了 SVG。

**SVG 作為嵌入圖片** 是最簡單的路線——把整張幻燈片渲染成圖片塞進 PPT。但這樣完全喪失可編輯性，形狀變成畫素，文字無法選中，顏色無法修改，和截圖沒有本質區別。

SVG 勝出，因為它與 DrawingML 擁有相同的世界觀：兩者都是絕對座標的二維向量圖形格式，共享同一套概念體系：

| SVG | DrawingML |
|---|---|
| `<path d="...">` | `<a:custGeom>` |
| `<rect rx="...">` | `<a:prstGeom prst="roundRect">` |
| `<circle>` / `<ellipse>` | `<a:prstGeom prst="ellipse">` |
| `transform="translate/scale/rotate"` | `<a:xfrm>` |
| `linearGradient` / `radialGradient` | `<a:gradFill>` |
| `fill-opacity` / `stroke-opacity` | `<a:alpha>` |

轉換不是格式錯配，而是兩種方言之間的精確翻譯。

SVG 也是唯一同時滿足流程中所有角色需要的格式：**AI 能可靠地生成它，人能在任意瀏覽器裡直接預覽和除錯，指令碼能精確地轉換它**——在生成任何 DrawingML 之前，設計稿就已經完全透明可見。

---

## 源內容轉換

原始檔（PDF / DOCX / EPUB / XLSX / PPTX / 網頁）會在 Strategist 開始前完成歸一化，但當前架構已經不是“全部轉成 Markdown 後其他資訊都不重要”的單通道模型。現在有兩條事實通道，各自擁有明確職責：

| 通道 | 產物 | 所有者 | 用途 |
|---|---|---|---|
| 內容契約 | `sources/` 內容型檔案（以 `<stem>.md` 為主） | `source_to_md/*` 轉換器 + `import-sources` | 文本、表格、圖表數值、引用和源材料敘事 |
| 結構化分析 | `analysis/*.json` / `analysis/*.csv` | intake 與分析工具 | PPTX 身份資訊、頁面幾何、原生表格/圖表、圖片尺寸/色彩/主體 |

對 PPTX 原始檔，`project_manager.py import-sources` 會同時執行 `ppt_to_md.py` 和 `pptx_intake.py`。Markdown 仍然是主生成流水線的內容源；intake bundle 會寫出 `<stem>.identity.json`、`<stem>.slide_library.json`，並把緊湊的多 deck 索引合併到 `analysis/source_profile.json`。Strategist 預設讀取這個緊湊索引來獲取源事實；只有特定工作流需要原始細節時，才打開單個 deck 的原始 artifact。這個邊界很重要：主流水線可以重構頁數和敘事，而 `template-fill` 與 `beautify` 會把同一批 intake 事實中的一部分提升為更強約束。

轉換器生成的圖片資產也會被歸一化。伴隨的 `<stem>_files/` 目錄會匯入專案級 `images/` 池，`image_manifest.json` 按檔名合併；當匯入後目錄名發生變化時，Markdown 中的資源引用會被重寫。Office 向量圖（`.emf` / `.wmf`）是一等執行時資產：intake 階段不柵格化它們，`finalize_svg.py` 為 native 路徑保留外部引用，`svg_to_pptx.py` 以 Office 向量媒體嵌入，避免 CJK 字型替換和向量細節損失。

兩個轉換器設計選擇仍然成立：

**Native-Python 優先，外部二進位制兜底。** 常見格式由純 Python wheel 處理，pandoc 僅在長尾小眾格式時才被呼叫。讓每個使用者都去裝一份可能沒有許可權裝的系統級二進位制是一種可用性稅，而大多數輸入是 docx / pdf / html / pptx，這種稅不值得。

**TLS 指紋模擬應對高安全站點。** 網頁抓取預設走 Python 版 `web_to_md.py`，並在可用時依賴 `curl_cffi` 做類 Chrome TLS 指紋模擬。微信公眾號和不少 CDN 會直接遮蔽 Python 預設握手；把這件事留在 Python 轉換路徑裡，避免讓 Node 抓取器成為主架構。

---

## 專案結構與生命週期

`project_manager.py init` 建立的是一個自包含工作區，而不只是輸出目錄：

| 目錄 | 職責 |
|---|---|
| `sources/` | 原件歸檔、歸一化 Markdown、轉換器伴隨檔案 |
| `analysis/` | 機器抽取事實：PPTX intake bundle 與按需重算的圖片分析 |
| `images/` | 單一執行時圖片池：使用者圖、抽取圖、公式圖、網路圖、AI 圖、切片圖、EMF/WMF |
| `icons/` | 由 `icon_sync.py` 複製的專案級圖示集；匯出時可回退到全域性庫 |
| `templates/` | 複製進專案的模板 spec / SVG reference / 非圖片模板資產 |
| `svg_output/` | 唯一手寫 SVG 源目錄 |
| `svg_final/` | 派生出的自包含 SVG，服務 IDE / 瀏覽器 / 預覽快照 |
| `live_preview/` | 預覽服務狀態、直接編輯歷史和註解日誌 |
| `notes/` | `total.md` 與拆分後的逐頁講稿 |
| `exports/` | 帶時間戳的 native PPTX 交付物 |
| `backup/<timestamp>/` | 預設匯出時寫入的凍結 `svg_output/` 快照 |

CLI 仍支援三種匯入模式：`--move`、`--copy`，以及“倉庫內檔案 move、倉庫外檔案 copy”的自動預設。`SKILL.md` 中的生產工作流會刻意收緊這一點：agent 必須呼叫 `import-sources ... --move`，讓所有原始檔和中間產物進入 `sources/`，保持工作根目錄乾淨。指令碼級預設服務臨時 CLI 使用的安全性；工作流級契約更嚴格，是為了讓 AI 執行具備可復現和可審計性。

---

## 架構不變數

可執行的 artifact ownership 不變數以 [`artifact-ownership.md`](../../skills/ppt-master/references/artifact-ownership.md) 為準；本節解釋這些邊界為什麼在架構上重要。

這些不變數強於普通實現偏好。如果某個改動破壞了其中一條，它很可能是在改變架構，而不是做重構。

| 不變數 | 實際後果 |
|---|---|
| `sources/` 內容型檔案是主流水線內容契約 | 主 SVG 路線中的文本、表格和圖表數值來自 `sources/` 內容型檔案（Markdown 為主，`.txt` / `.csv` / `.json` / `.yaml` 等同樣計入）；已知 sidecar（`*.conversion_profile.json`、`*_files/image_manifest.json`）排除在外 |
| `analysis/` 存機器事實，不存設計契約 | `source_profile.json` 和 intake artifact 輔助 Strategist；除非工作流明確規定，否則不鎖定頁數 / 頁序 |
| `design_spec.md` 解釋設計；`spec_lock.md` 執行設計 | Executor 從 `spec_lock.md` 取鎖定值，而不是從敘述記憶裡取 |
| 每頁生成前重讀 `spec_lock.md` | 長 deck 中的顏色、字型、圖示、圖片、節奏、佈局和圖表選擇保持穩定 |
| `svg_output/` 是唯一手寫 SVG 目錄 | 質量檢查、手工編輯、重匯出和 `update_spec.py` 都面向作者源 |
| `svg_final/` 是派生產物 | 它可以從 `svg_output/` 重建，不應成為 native 匯出的事實源 |
| native PPTX 預設讀取 `svg_output/` | 轉換器要在 finalize 重寫前保留圖示、`preserveAspectRatio`、圓角矩形和原生圖片裁剪語義 |
| 直接 OOXML 路由不進入 SVG 流水線 | 保留型工作流直接 patch 原生 PPTX parts |
| 圖片事實來自重算後設資料 | `analysis/image_analysis.csv` 從即時 `images/` 目錄重算；agent 不直接看圖片畫素 |
| 原生 PPTX 模板不是 Step 3 模板 | Step 3 只消費可複用模板目錄 |

---

## Canvas 格式系統

PPT Master 不只服務 PPT——同一套 SVG → DrawingML 流水線還能產出方形海報、9:16 故事、A4 印刷品。各格式特定的約定（比例、安全區、品牌區等）住在 [`references/canvas-formats.md`](../../skills/ppt-master/references/canvas-formats.md)。

值得標註的架構選擇：**viewBox 是畫素，不是絕對單位。** 畫素空間讓 AI Executor 思考佈局沒有歧義（`x="100"` 就是左緣 +100px），人類在瀏覽器裡檢查也直接。到 EMU 的換算只在匯出時發生一次——選畫素意味著流水線的其餘環節（Strategist、Executor、質量檢查、後處理）永遠不需要在 EMU 思維下工作，那對 AI 生成和人類除錯都是敵對的。

---

## 模板系統與可選路徑

模板是**可選項，不是預設**。Strategist 預設走自由設計——AI 完全憑源內容創造視覺系統。模板路徑只在使用者明確提供目錄路徑時啟用。

**為什麼預設自由設計。** 模板是地板，但很容易變成天花板：它會把整個 deck 鎖進模板自有的視覺慣用語，無視內容本身想要怎樣被呈現。自由設計的佈局從源內容的結構推導而來，而不是從一套固定語法套上去——視覺節奏跟著內容走，而不是跟內容打架。約束模式在窄場景裡確實更好（品牌鎖定的 deck、強型別場景如學術答辯或政府報告），所以它一直在；但 AI 不主動去抓，是使用者去抓。

**機械觸發，不做語義匹配。** 像 `academic_defense` 這樣的裸名字、品牌提及，或“麥肯錫風格”這類風格短語，即使庫裡存在相似目錄，也不會觸發 Step 3。Step 3 只消費一個能解析為目錄的路徑，並且該目錄的 `design_spec.md` 必須宣告 `kind: brand`、`kind: layout` 或 `kind: deck`。發現性交給模板索引和顯式問答（“有哪些模板可以用？”），不交給執行時 fuzzy matching。

三類別範本擁有不同的設計契約片段：

| Kind | 擁有的片段 | 典型內容 | 對 Strategist 的影響 |
|---|---|---|---|
| `brand` | 身份片段 | 配色、字型、logo、語氣、圖示風格 | 鎖定身份；結構保持自由 |
| `layout` | 結構片段 | 畫布、頁面結構、頁面型別、SVG roster | 鎖定結構；身份仍在策略師確認階段裡確定 |
| `deck` | 身份 + 結構 + 模板總覽 | 完整復刻型包 | 鎖定完整模板語法，只剩內容相關選擇 |

當使用者提供多個路徑時，融合是**片段級**而不是欄位級：brand 覆蓋身份片段，layout 覆蓋結構片段，deck 提供中間的 template overview 片段。同類衝突會被顯式列為衝突，而不是按輸入順序默默決定。這樣融合後的 spec 能明確說明每個片段來自哪裡，便於審計和復現。

**原生 PPTX 模板不屬於 Step 3。** `.pptx` 可以作為源材料進入流水線，PPTX intake 也能抽取其身份和幾何資訊。但“給一個原生 PPTX 模板並生成新 PPTX”的請求會進入 `template-fill`，因為使用者期望的是克隆 PowerPoint 頁面殼並替換文本 / 表格 / 圖表。SVG 路線只能消費可複用模板包；如果要把某個 PPTX 的設計語言用於 SVG 路線，必須先通過 `create-template` 生成模板目錄，再把該目錄路徑提供給 Step 3。

**佈局是 opt-in，圖表和圖示不是。** 這種不對稱不是矛盾——*佈局*正是鎖定視覺慣用語的那一層（地板/天花板問題），而圖表和圖示是不會施加 deck 級風格約束的複用原語。同一個 `templates/` 目錄，但在視覺契約裡扮演的角色不同。

---

## 角色系統：單一流水線中的專業模式

PPT Master 用的是**單主代理內的角色切換**，不是並行子代理。Strategist、Image_Generator、Executor 以及各獨立工作流模式，本質上都是按需載入的指令作用域；它們不是帶著各自過期 deck 狀態的獨立 agent。這個選擇有三條互相支撐的理由：

**為什麼是單代理而非並行子代理。** 頁面設計依賴完整的上游上下文——Strategist 的色彩選擇、圖片資源是否成功獲取（還是失敗被替代）、之前幾頁的視覺節奏。子代理拿到的只能是這個上下文的過期區域性快照，產出的 deck 視覺會逐頁漂。同一邏輯也禁止分批生成（比如一次 5 頁）：分批加速上下文壓縮，deck 的視覺一致性下降速度比節省的速度更快——不划算。

**為什麼是角色專屬 reference 而不是一個超大 prompt。** Strategist 跑的是「跟使用者協商」模式（開放式、對話式、可以回退），Executor 跑的是「產出嚴格 XML」模式（不準即興、不準漏屬性）。把兩者塞進同一個 prompt，強迫模型在同一個 turn 裡持守相互矛盾的紀律——所有混合模式的 prompt 工程病灶都會出現。按角色拆開，每個角色只加載它需要的、扔掉其他。

**策略師確認階段是唯一的阻塞 gate。** Strategist 階段以一個三階段確認 gate 作為核心阻塞決策點：第一階段確認方向錨點（畫布、受眾、改寫幅度、交付目的、mode、visual style）；第二階段基於已確認錨點重新推導並確認設計系統（頁數、調色盤、字型、圖示、公式策略）；第三階段基於已確認設計系統重新推導並確認圖片與執行方式（圖片來源、生成圖風格、AI 圖片路徑、生成模式、refine-spec）。最終的 `confirm_ui/result.json` 是權威輸入——使用者改過的欄位必須進入 `design_spec.md` 和 `spec_lock.md`，不能回退到 AI 的原始推薦。

**圖片分析走重算後設資料，不讀畫素。** 當專案裡存在圖片時，Strategist 和 Executor 使用 `analyze_images.py` 的輸出（`analysis/image_analysis.csv`），而不是直接開啟圖片檔案。這個 CSV 是基於當前 `images/` 目錄重算出來的檢視，不是持久快取。每次做圖片敏感決策前重跑分析，就是它的防陳舊策略：使用者圖、抽取圖、網路圖、AI 圖、公式圖和切片圖最終都會匯入同一張可度量事實表。

**逐頁 spec_lock 重讀** 是長 deck 的抗漂移機制——完整理由見下面的 § 設計規範的傳播。

---

## 執行紀律

流水線由 [`SKILL.md` § 全域性執行紀律](../../skills/ppt-master/SKILL.md) 中的 10 條規則強制——那份檔案是權威，規則住在那裡。它們看起來很官僚，但存在的理由是：LLM 預設行為是“讓我在這一 turn 裡把整個問題搞定”，而這恰好是序列流水線最不該有的形狀——序列流水線要求每一步的輸出都是有界、過 checkpoint、被下一步消費的。這套規則共同關閉了實際反覆出現的失敗模式：亂序執行、AI 代為做使用者設計決策、跨階段打包、前置條件未滿足、投機預先準備、子代理上下文丟失、分批漂移、長 deck 色彩字型漂移、指令碼批次生成 SVG 漂移，以及路由歧義。

常見失敗的停 / 繼續規則以 [`failure-recovery.md`](../../skills/ppt-master/workflows/failure-recovery.md) 為準；本節不復制恢復矩陣。

其中兩條新邊界尤其關鍵。第一，Executor 頁面 SVG 必須由當前主代理逐頁手寫；禁止寫 Python / Node / shell 生成器批次吐 SVG，因為這種輸出會丟失跨頁判斷和視覺連續性。第二，路由是確定性的：原生 PPTX 模板、beautify、native enhancement、自定義動畫、live preview 等觸發條件已經在倉庫裡定義清楚時，不再額外拋給使用者一個開放式路線選擇題。

角色切換協議（切換模式前必須 `read_file references/<role>.md`）有兩個互相支撐的作用：把新鮮的角色指令載入上下文，覆蓋前一模式的漂移；對話 transcript 中的可見標記構成審計軌跡，讓使用者能看到 agent 何時切換了模式——回看一個具體決策為什麼這樣做時，這條線索很關鍵。

---

## 設計規範的傳播：spec_lock.md 作為執行契約

Strategist 階段產出兩份看起來冗餘但服務不同物件的產物：

- `design_spec.md` —— 人類可讀敘述；設計的「為什麼」（目標受眾、風格目標、配色理由、頁面大綱）
- `spec_lock.md` —— 機器可讀執行契約；Executor 必須**字面照搬**的「是什麼」（HEX 顏色、確切的 font family 字串、圖示庫選擇、帶狀態的圖片資源列表）

為什麼兩份都要？沒有 `spec_lock.md` 的話，Executor 在長 deck 裡會逐頁重讀 `design_spec.md`，LLM 上下文壓縮漂移會逐漸扭曲色值和字型。`spec_lock.md` 是**抗漂移機制**——SKILL.md 強制要求生成每一頁前 `read_file <project>/spec_lock.md`，讓數值在 20+ 頁裡保持字面一致。

這份 lock 同時也是逐頁路由表。除了全域性配色和字型，它還承載 `page_rhythm`（`anchor` / `dense` / `breathing`）、`page_layouts`（某頁是否繼承某個 layout 模板 SVG）、`page_charts`（某頁應適配哪個圖表模板）、帶放置/裁剪契約的圖片行，以及決定載入哪些執行規則檔案的 `mode` / `visual_style`。空值本身也是訊號：沒有模板、沒有圖表、沒有圖片，很多時候是設計選擇，而不是漏填。

`update_spec.py` 把生成後的修改用兩個協調步驟傳播：把新值寫入 `spec_lock.md`，然後字面替換到每一份 `svg_output/*.svg`。工具的範圍**故意收得很窄**——只支援 `colors.*`（HEX 值，大小寫不敏感替換）和 `typography.font_family`（屬性級）。其他欄位（字號、圖示、圖片、畫布）**有意不支援**——它們的替換需要屬性級或語義級理解，風險/收益不值得做批次傳播。這些情況手動改 `spec_lock.md` 然後重做受影響的頁面。

工具拒絕做備份：依賴 git 回滾。加備份機制只是重複 git 的工作，還會留下過時快照。

---

## 圖片獲取與嵌入

這一階段有多項架構層面的決策：

**provider 專屬 config key，不用通用 `IMAGE_API_KEY`。** 每個 backend 用自己的 `OPENAI_API_KEY` / `MINIMAX_API_KEY` 等等，當前 backend 由顯式的 `IMAGE_BACKEND=<name>` 選定。統一的 `IMAGE_API_KEY` 欄位第一眼看著乾淨，但當使用者同時配了多個 provider 又不確定哪個在生效時會造成靜默混亂——這種 fault 通常只表現為「影像生成結果怪怪的」，找不到清晰失敗點。強制 per-provider key 讓「我現在用的是哪個 backend」從推理變成可讀配置。

**預設寬鬆 license 過濾，配以嚴格模式應對沒法放致謝的版面。** 網路圖片搜尋預設允許 CC BY / CC BY-SA 加內聯致謝——大部分幻燈片都有視覺空間放一個致謝元素。`--strict-no-attribution` 是給全屏 hero image 和緊湊構圖的逃生口，那些場景沒法放致謝又不打破設計。NC（CC BY-NC*）和 ND（CC BY-ND*）自動拒絕，因為 PPT Master 的典型產物會用於商用或修改場景；寬鬆預設 + 這個底線正好對應使用者實際想要的 fail-mode。

**Manifest-first 獲取。** 流水線內的 AI 圖片生成永遠先寫 `images/image_prompts.json`，並渲染旁路 `image_prompts.md`，哪怕只有一張圖。`image_gen.py "prompt"` 這種位置引數形式只保留給一次性除錯，因為它沒有 manifest / sidecar 審計軌跡。網路圖片獲取也類似：多行 web 資源寫入 `images/image_queries.json` 批次執行，並用 `image_sources.json` 追蹤來源和致謝資訊。

**相關小插畫用一張統一 sheet。** 當 deck 需要三個或更多同風格小插畫時，資源計劃使用一個 AI illustration sheet 行，再用若干 `slice` 行派生元素，而不是分別生成多張小圖。`slice_images.py` 把 sheet 切成具名透明元素，這些派生檔案進入 `images/`，隨後重跑 `analyze_images.py`，讓 Executor 看到真實尺寸。這既是成本規則，也是風格一致性規則：一張 sheet 會強迫這些小元素來自同一種視覺手法。

**Executor 前必須進入終態。** 需要獲取的資源行必須落到 `Generated`、`Sourced` 或 `Needs-Manual`；`Pending` 和 `Failed` 不能漏進 Executor。`Needs-Manual` 可以作為已知佔位 / 依賴繼續進入 SVG 生成，但 Step 7 會在最終匯出前重新檢查必需檔案是否已經存在。

**開發期外部引用，交付期分叉成兩套嵌入策略。** 在 `svg_output/` 裡編輯時，圖片是外部檔案引用——快速迭代、單點替換。兩份交付產物隨後分叉：`svg_final/` 走 Base64 內聯（產出一組自包含 SVG，IDE 預覽、瀏覽器、preview pptx 都能開而不丟點陣圖依賴）；native pptx 反過來把點陣圖複製進 PPTX 的 media 資料夾，用 `<a:srcRect>` 表達裁剪。分叉的理由：在 DrawingML 裡塞 Base64 能跑但檔案膨脹 3-4 倍；檔案引用的點陣圖是 PowerPoint 原生表達方式，配 `<a:srcRect>` 的裁剪也是 DrawingML 的規範寫法——任一方向用錯工具都要付出可編輯性或檔案大小的代價。

**AI 圖片三維繫統：Strategist 階段就鎖定。** 當 deck 包含 AI 生成圖片時，Strategist 在前置階段一次性確定三個正交維度——`rendering`（視覺風格家族：vector-illustration / editorial / 3d-isometric / sketch-notes / ……）、`palette`（deck 的 HEX 在圖裡**怎麼用**：比例 + 角色 + 氣質）、`type`（每張圖的內部構圖：background / hero / framework / comparison / ……）。前兩個是 deck 級、寫進 `spec_lock.md`；Image_Generator 此後每張圖的 prompt 都從同一份鎖定的 rendering + palette 加上該圖的 type 組裝出來，而不是逐圖重決風格。沒有這層鎖定，每張圖都會自己風格漂移，整套 deck 讀起來就是一摞互不相關的插畫。這是 `spec_lock` 字型/色彩抗漂移機制在畫素上游的對偶——同一思路，往前推一層。Strategist 在策略師確認階段會向用戶呈現 **≥3 個 `rendering × palette` 候選**，絕不靜默地自動鎖定單一組合，因為這是一個會牽動全 deck 視覺的選擇，唯一權威只有使用者的品味。

---

## 圖文版式：Primary 主結構 + Modifier 修飾層

「圖片**怎麼放上幻燈片**」的詞表（完整詞彙在 [`references/image-layout-patterns.md`](../../skills/ppt-master/references/image-layout-patterns.md)）把 72 條編號技法拆成兩層、自由組合：

- **Primary 主結構**（容器佈局 / 圖作畫布 + 原生覆蓋 / 多圖組合）—— 頁面的骨架。一頁可一個也可多個；跨 Primary 的組合，如「側邊對比 + 圖作畫布的註解卡」，是合規的。
- **Modifier 修飾層**（非矩形裁剪 / 遮罩與疊加 / 紋理 / 特殊技法）—— 裝飾層。一頁可疊任意多個，附著在 Primary 之上。

**為什麼顯式鼓勵複合，而不是「一頁一個 primary」。** 這份詞表對抗的 AI 失敗模式不是「疊太多」，而是「用得太少」——把每頁圖片預設堆成裸的 `#2 左三分` 或 `#48 侧边对比`，Modifier 層完全不動，產出視覺扁平的「AI 預設感」版式。早先的規則「一頁一個 primary，modifier 可疊」聽起來有原則，實際上加劇了 Modifier 層的棄用——AI 把它讀作「可以不疊」的許可。現在的措辭反過來：組合是常態，單 Primary + 無 Modifier 才需要解釋。

**為什麼物理拆分兩層，而不是隻打標籤。** 詞表被重排成「Primary 全部在前，Modifier 全部在後」——Strategist 或 Executor 讀一次目錄，就能從結構上內化「兩層」心智模型。編號是穩定 id（`#38` 永遠是「圖作畫布 + 註解卡」，不論它在檔案裡的物理位置），所以 `spec_lock.md`、`design_spec.md §VIII`、歷史 executor 輸出、過往示例裡所有 `#<id>` 引用照樣解析。

**為什麼組合走 Strategist 資源列表，不只交給 Executor 臨場發揮。** `§VIII 图片资源列表` 的 `Layout pattern` 列接受 `#<id> + #<id> ...` 表示式——Primary id 加可選 Modifier id——所以組合在 SVG 生成**之前**就被宣告、被 `svg_quality_checker` 審計、並能在 session 重入後存活。把組合責任只壓在 Executor 身上，長 deck 上下文壓縮時就會丟；把它編碼進 spec_lock 旁的資源列表，組合就成為設計契約的一部分。

**為什麼真正的硬約束留在上游。** 跨切的技術硬約束（`<clipPath>` 只能用在 `<image>` 上、用 `fill-opacity` 而非 `rgba()`、禁 `<mask>`、alpha 效果的路由表）獨家住在 [`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md)。版式詞表只用一行指標指向它們，不復述——這樣某條約束放開時（比如某個 DrawingML 特性變得可靠），只有一個檔案要改，詞表裡也不會留下一份過期副本繼續暗中強制舊規則。

---

## SVG 約束：停用特性與條件允許

PowerPoint 的 DrawingML 是 SVG 表達力的嚴格子集。Executor 在一份經驗生長起來的黑名單（mask、style/class、`@font-face`、foreignObject、symbol+use、textPath、animate*、script/iframe ……）裡執行，外加對 `marker-start`/`marker-end` 和僅 `<image>` 上的 `clip-path` 的窄條件允許。權威清單和每條特性的具體約束——包括 `<mask>` 的替代效果路由表（漸變疊加、clipPath、filter shadow、源圖烘焙）——住在 [`references/shared-standards.md`](../../skills/ppt-master/references/shared-standards.md)。

值得在架構層標記的理由：

- **為什麼是黑名單，不是白名單。** SVG 是個寬規範；窮舉允許特性會隨著 Executor 不斷發現新的有用構造而要持續維護。黑名單隻圈住語義上沒有 DrawingML 表達的窄集合，其餘隱式可用。
- **為什麼是經驗性，不是從規範推導。** 這份清單從真實的 PPT 匯出失敗長出來，不是讀 OOXML 規範讀出來的。有幾個特性（如 `<mask>`）理論上能在 DrawingML 表達，但跨 PowerPoint 版本不可靠；黑名單反映的是實際能交付的子集。
- **XML 良構性陷阱。** 兩個獨立於 DrawingML 的跨切陷阱：排版字元必須用裸 Unicode（`—`、`→`、`©`、NBSP），HTML 命名實體（`&mdash;`）在 SVG 裡是非法 XML；XML 保留字元（`& < >`）必須實體轉義，否則 `R&D` 直接終止匯出。這兩個坑出現頻率高到值得在架構層 flag 一下。
- **黑名單在後處理之前執行。** `svg_quality_checker.py` 在 `svg_output/` 上執行；後處理會重寫 SVG，會掩蓋源級別違規。修復永遠是 Executor 重新寫——有意沒有 auto-fix 模式（見 § 質量門）。

---

## 質量門

**為什麼需要這道檢查器。** LLM 生成的 SVG 不是確定性的——停用特性會在長 deck 中悄悄混入，只在 `svg_to_pptx` 中途崩或 PowerPoint 靜默丟元素時才暴露。檢查器把「PowerPoint 在第 14 頁匯出失敗」轉化為「Executor 在第 14 頁用了 `<style>`，重新生成它」，診斷速度提升一個數量級——這正是讓長 deck 在經濟上可迭代的關鍵。

**為什麼放在後處理之前，而不是之後。** 後處理會重寫 SVG（圖示嵌入、圖片內聯），會掩蓋源級別違規。直接讀 `svg_output/` 抓的是 Executor 的實際輸出，先於任何可能掩蓋 bug 的清理動作。

**嚴重性模型：error 阻塞、warning 不阻塞，且有意沒有 auto-fix。** error 要求 Executor 在上下文裡重新寫出錯的頁面——一個被禁的 `<style>` 元素不是機械 patch，因為 Executor 用它是有原因的，替代方案（比如改成內聯屬性）需要帶著同樣的設計意圖重新落地。Auto-fix 會靜默丟失這份意圖，交付一個更難看的頁面。

**為什麼圖表座標驗證掛在同一道 gate。** 圖表頁面有幾何正確性需求（柱高、餅圖扇角、座標軸刻度位置），這些不是結構問題，SVG 合法性規則也抓不到。最自然的捕捉位置就是已經要求 AI 回看自己輸出的那道 gate——把「看一眼你剛生成的東西然後修」的認知上下文打包到一個階段，比把結構和幾何審查分到兩輪 review 更高效。

---

## 後處理流水線

> 工程化轉換階段中每一份產物和每一個模組為何存在，刪除它會破壞哪些工作流。在考慮簡化 `svg_final/` / `finalize_svg.py` / `svg_to_pptx.py` 之前，先讀這一節。

### 五份產物，五種工作流

後處理階段涉及五份產物。每一份都服務於一種流水線中無法替代的工作流。

| 產物 | 服務的工作流 | 為何無可替代 |
| --- | --- | --- |
| `svg_output/` | 唯一源、手工編輯入口、`update_spec.py`、`svg_quality_checker.py` | 流水線中唯一**手寫**而非派生的目錄 |
| `svg_final/` | IDE 內即時預覽（VSCode/Cursor 直接開啟 `.svg`）、瀏覽器單頁預覽 | `.pptx` 在 IDE 裡打不開；`svg_output/` 因圖示 / 圖片是外部引用，IDE 中渲染不完整 |
| `exports/<name>_<ts>.pptx`（native） | 主交付物——PowerPoint 中以 DrawingML 形狀形態可編輯 | 唯一一份使用者可在 PowerPoint 中原生改尺寸 / 改色 / 改樣式的產物 |
| `exports/<name>_<ts>_native_charts.pptx`（需 `--native-objects` 顯式開啟） | 讓帶 `data-pptx-native` 標記的圖表/表格以真·PowerPoint 原生物件交付,而非壓平形狀 | 帶資料、可在 PowerPoint 中直接編輯的圖表/表格物件;命名與普通壓平形狀匯出區分開 |
| `exports/<name>_<ts>_svg.pptx`（preview，需 `--svg-snapshot` 顯式開啟） | 跨平臺單檔案分發、整體多頁瀏覽、郵件附件 | 自包含、多頁、PowerPoint / Keynote / WPS / LibreOffice 都能直接開啟；`svg_final/` 是資料夾，分發不便。預設關閉——live preview 已經覆蓋 dev / 診斷場景的 SVG 視覺參考需求 |
| `backup/<ts>/svg_output/`（預設流程下始終生成） | 不重跑 LLM 的前提下從凍結 SVG 源重建 pptx、長期存檔 | 專案下游被改動後，Executor 原始 SVG 唯一的留存副本 |

### `svg_finalize/` 包有**兩種**消費者

這是讀程式碼時容易忽略的關鍵事實。同一組 `skills/ppt-master/scripts/svg_finalize/` 下的模組，在兩個地方被使用，服務兩份不同的產物。

**寫盤消費者** —— `finalize_svg.py` 每次執行都把 `svg_output/` → `svg_final/` 寫到磁碟一次。`svg_final/` 隨後供 IDE 預覽和 preview pptx 使用。

**記憶體消費者** —— native pptx 直接讀 `svg_output/`（不經磁碟中轉），但 DrawingML 無法內聯處理兩種 SVG 特性，所以轉換器在記憶體中呼叫 `svg_finalize` 模組：

| 記憶體呼叫點 | 複用的模組 | native pptx 為何需要 |
| --- | --- | --- |
| `svg_to_pptx/use_expander.py` | `svg_finalize.embed_icons` | DrawingML 不識別 `<use data-icon="...">`；不展開圖示會靜默丟失 |
| `svg_to_pptx/tspan_flattener.py` | `svg_finalize.flatten_tspan` | DrawingML 文本塊無法在段落中跳位置；`dy` 堆疊的多行 `<tspan>` 會塌成一行，`x` 錨定的 tspan 會跑到錯誤的列 |

### 各模組消費者一覽

| 模組 | 寫盤消費者 | 記憶體消費者 | 刪除影響 |
| --- | --- | --- | --- |
| `embed_icons.py` | `finalize_svg` 的 `embed-icons` 步驟 | `svg_to_pptx/use_expander.py` | native pptx 丟失全部圖示 + `svg_final/` 不再自包含 |
| `flatten_tspan.py` | `finalize_svg` 的 `flatten-text` 步驟 | `svg_to_pptx/tspan_flattener.py` | **native pptx 中 `dy` 堆疊的多行文本塌成一行** |
| `align_embed_images.py` | `finalize_svg` 的 `align-images` 步驟 | — | `svg_final/` 失去圖片嵌入 → IDE 預覽 / preview pptx 都沒圖 |
| `crop_images.py` / `embed_images.py` / `fix_image_aspect.py` | 被 `align_embed_images.py` import | — | `align_embed_images` `ImportError`，整條鏈路 broken |
| `svg_rect_to_path.py` | `finalize_svg` 的 `fix-rounded` 步驟 | — | 隻影響 PowerPoint 內手動「Convert to Shape」時圓角丟失；瀏覽器 / IDE / PowerPoint 自帶的 SVG 渲染器都正常 |

---

## 直接 OOXML 路由

不是所有 PPTX 相關請求都應該重新生成頁面。PPT Master 現在為“原生 deck 本身就是編輯物件”的場景提供直接 OOXML 路由。

`template_fill_pptx.py` 是 `scripts/template_fill_pptx/` 包的薄 CLI 入口。analyzer 抽取帶文本槽位、表格、圖表和幾何資訊的 slide library；fill plan 選擇源頁面並確認替換內容；applier 克隆幻燈片並直接 patch XML parts。這條路線故意繞開 SVG：使用者提供 PowerPoint 模板時，通常期望原生母版、佔位符、表格和圖表繼續保持 PowerPoint-native。

`native_enhance_pptx.py` 是已完成 deck 原生增強的穩定入口。它委託 native narration / timing 實現，在專案歸檔副本上直接 patch PPTX package：講稿、頁面轉場、錄製旁白媒體、頁面計時和相關後設資料。它的契約是保留：已有內容、佈局和格式不重新生成。

這些直接路線會和主流水線共享部分分析原語，尤其是 PPTX intake，但不共享 SVG 作者階段和後處理階段。這個分離是有意的：SVG 生成是設計合成路徑；直接 OOXML 編輯是保留路徑。

---

## Native PPTX 轉換器內部

**為什麼是逐元素派發而不是整體翻譯。** SVG 的層級模型乾淨地對映到 DrawingML 的 group / shape / picture 型別——不需要一個全域性最佳化器去重新規劃幻燈片。每種形狀都有自己窄的翻譯器，簡單到能單獨除錯和單元測試。一張幻燈片的最終質量等於這些獨立區域性轉換之和；這個性質在整體翻譯下脆弱，在元素派發下穩健。

**為什麼 Office 相容模式預設開啟。** 2019 之前的 PowerPoint 不能原生渲染 SVG。轉換器為每頁生成 PNG 兜底，與原生形狀並存——新版 Office 仍顯示可編輯形狀，舊版回退到 PNG。預設開啟的取捨是：用適度的檔案大小代價換取「不會靜默地把打不開的 deck 交給跑老版本的使用者」；逃生口給那些明確知道自己在新棧上、想要更小檔案的使用者。

---

## 動畫與轉場模型

值得講的設計選擇是動畫**錨點**，不是效果列表。

**為什麼把入場動畫錨在頂層 `<g>` group。** PowerPoint 的動畫時序基於形狀 ID——每個被動畫的物件需要穩定的 shape ID。給單個原語做動畫會產出每頁 30+ 個分別飛入的原子（動感氾濫），只給整頁做動畫又損失視覺敘事。頂層 group 是自然粒度：Executor 本來就被強制要求用 `<g id="...">` 標記邏輯內容塊，而這些塊正是觀眾讀作「一個東西到達」的單位——動畫對齊了已有的邏輯結構，而不是另立門戶。

**為什麼頁面裝飾自動跳過。** 名為 `background` / `header` / `footer` / `decoration` / `watermark` / `page_number` 的 group 代表靜態頁面框架，不是內容；讓它們飛入會讓人出戲（頁面本身在每次切換時具象化），幾乎不會是使用者想要的。按 id token 過濾原則上脆弱，實際上可靠——因為 token 詞表很小，命名權又掌握在 Executor 手裡。

**為什麼物件級動畫用 sidecar，而不是 SVG 屬性。** SVG 繼續作為靜態視覺源。自定義 PPTX 動畫屬於匯出策略，所以物件級覆蓋放在可選的 `animations.json`，按 slide stem 和頂層 group id 關聯。這樣不會把 PowerPoint 專用後設資料塞進 SVG，同時仍能在預設全域性動畫不夠用時調整順序、效果、延遲和時長。

**為什麼錄製旁白讓自動推進時長跟著片段時長走。** 嵌入旁白意味著 deck 目標是影片匯出——影片裡沒有演講者去點選。把每頁自動推進時長設為該頁音訊片段的實際時長，PowerPoint 能幹淨地匯出為 MP4，無需人工配時。任何其他時長來源（估算朗讀速度、固定每頁時長）都會破壞音畫同步。

**為什麼錄製旁白拒絕 on-click 物件動畫。** PowerPoint 可以在真實排練時記錄點選計時，但 PPT Master 不合成物件級點選事件。錄製旁白路徑只寫頁面級音訊和頁面自動推進計時，所以單擊觸發的物件入場會讓匯出依賴額外的 PowerPoint 人工排練。帶旁白的 deck 必須使用無點選入場（`after-previous` 或 `with-previous`）。

---

## 維護邊界：不要合併什麼

下面這些“簡化”都有明確代價。除非要有意識地重新設計周邊架構，否則應把它們視作反向契約。

| 不要合併或新增 | 原因 |
|---|---|
| 不要把模板名或風格短語模糊匹配到庫路徑 | Step 3 必須確定性觸發；選錯模板比自由設計更難恢復 |
| 不要把原生 PPTX 模板當作 Step 3 模板 | 原生 PPTX 模板請求期待的是克隆 / 填充原生頁面，不是 SVG 合成 |
| 不要把 `template-fill-pptx`、`beautify-pptx`、`native-enhance-pptx` 合成一個“PPTX 最佳化”路線 | 三者的保留契約不同：原生填充、1:1 重排、直接增強是三種操作 |
| 不要用指令碼批次生成 Executor SVG 頁面 | 跨頁設計判斷依賴主代理逐頁連續創作 |
| 不要把 `image_analysis.csv` 當持久快取 | `images/` 是即時工作目錄；事實必須按需重算 |
| 不要讓 `svg_final/` 成為 native PPTX 預設輸入 | `svg_final/` 為自包含預覽而重寫，native 轉換需要 `svg_output/` 的高保真語義 |
| 不要預設開啟物件級入場動畫 | 頁面轉場是預設；物件 build 是顯式匯出策略 |
| 不要把 visual review、旁白、圖表校準或動畫定製預設塞進每次執行 | 這些工作流觸發範圍窄，且有額外依賴 |
| 不要用檔案複製替代 `finalize_svg.py` | finalize 會嵌入圖示 / 圖片、展開特殊文本並準備預覽產物 |
| 不要在主流水線裡把 `analysis/<stem>.slide_library.json` 當作第二份圖表數值來源 | Markdown 擁有內容數值；除非直接 PPTX 工作流接管，否則 intake 圖表 / 表格條目只是結構摘要 |

---

## Standalone Workflows（獨立工作流）

獨立工作流注冊表以 [`workflows/index.md`](../../skills/ppt-master/workflows/index.md) 為準；本節解釋為什麼這些能力保持獨立。

獨立工作流是路線定義，不是可有可無的裝飾。只有當某個能力與主流水線契約不同，或觸發頻率太低、不值得預設載入時，才會獨立成 `workflows/<name>.md`。

| 工作流 | 觸發條件 | 契約 |
|---|---|---|
| `topic-research` | 使用者只有主題、沒有源材料 | 在 Step 1 前收集網路材料 |
| `template-fill-pptx` | 原生 PPTX 模板 + 新材料 / 新主題 | 直接克隆並填充原生頁面；不進入 SVG 流水線 |
| `beautify-pptx` | 現有 PPTX，頁數/頁序/措辭必須 1:1 保留，只改善排版 | 鎖定源身份與內容後，通過 SVG 流水線重新生成 |
| `create-template` | 構建可複用 layout/deck 模板包 | 輸出後續 Step 3 可消費的目錄 |
| `create-brand` | 提取或定義可複用品牌身份 | 輸出 `templates/brands/<id>/` |
| `resume-execute` | 規劃會話後新開聊天，使用者要求繼續某專案 | 不重跑 Strategist，直接進入執行會話 |
| `refine-spec` | 使用者明確要求生成前先審閱 / 修改 spec | 寫出完整 spec/lock 後停下，使用者修改後再恢復 |
| `verify-charts` | 生成 deck 含資料圖表 | 匯出前校準圖表幾何 |
| `customize-animations` | 使用者要求調物件級動畫順序 / 效果 / 計時 | 建立 / 校驗 `animations.json` 並控制再匯出策略 |
| `live-preview` | 使用者要求預覽、點選選擇、應用註解或重匯出瀏覽器編輯 | 啟動 / 重入瀏覽器預覽，並只在規定時機應用提交內容 |
| `visual-review` | 使用者明確要求逐頁視覺自檢 | 在 Executor 與後處理之間做 rubric pass |
| `generate-audio` | 使用者要求旁白 / 影片匯出 | 生成旁白音訊並走錄製計時匯出路徑 |
| `native-enhance-pptx` | 已完成 PPTX 要保留內容/佈局，同時追加原生增強 | 直接 OOXML patch 路線 |

保持這些檔案獨立，是依賴控制決策。主路徑只加載當前需要的角色和 reference；旁白 backend、動畫 sidecar、圖表校準 rubric、模板匯入契約等，只有觸發命中時才進入上下文。這樣預設 deck 生成路徑保持緊湊，同時讓低頻能力也有確定實現，而不是臨場發揮。
