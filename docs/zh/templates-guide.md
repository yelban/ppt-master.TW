# 模板指南：選用、派生與邊界

PPT Master 的"模板"是一份**結構 + 風格**的預設包：包含若干頁面佈局 SVG（封面/章節/目錄/內容/結尾及其變體）、`design_spec.md` 設計規範，以及配套素材（logo、背景、裝飾圖）。它不是 PPTX 母版，也不是單純的配色方案——而是一組可被工作流直接複用的頁面骨架。

本文回答三個問題：

1. [怎麼用已有模板？](#一選用已有模板)
2. [怎麼把別人的 PPT / 自己的品牌做成模板？（重點）](#二派生新模板重點)
3. [模板的邊界是什麼？](#三模板的邊界)

---

## 一、選用已有模板

### 觸發方式

工作流**預設走自由設計**——不會主動問你要不要用模板，也不會基於內容主動推薦模板。模板是 opt-in 的，**只接受顯式目錄路徑**：你在第一條訊息裡把模板目錄的路徑寫出來。

### 怎麼觸發模板流程

在對話裡把模板目錄的路徑寫進去（位置不重要，只要明確即可）：

> "用這個模板做：`skills/ppt-master/templates/layouts/academic_defense/`" ✅
> "用上次那個模板：`projects/last_deck/template/`" ✅
> "做一份產品介紹，模板用 `/Users/me/Desktop/our_brand_v3/`" ✅

AI 會把這個目錄裡的 SVG、`design_spec.md` 和素材複製到專案目錄，然後進入 Strategist 階段。路徑可以是任意位置——內建庫的 `skills/ppt-master/templates/layouts/` 下、上一個專案的 `template/` 資料夾、或者磁碟上其他任何地方都行。

### 什麼**不會**觸發模板流程

- **只寫模板名、不給路徑**："用 academic_defense 模板" / "做一份 招商銀行 模板的產品介紹" → 走自由設計。AI 不會替你把名字解析成路徑。要用模板，請直接給路徑。
- **風格描述**："麥肯錫風格" / "Google style" / "麥肯錫那種" / "極簡風" / "Keynote 風" → 走自由設計。這些描述會順著對話流到 Strategist 那邊作為風格說明使用，但**不會複製任何模板檔案**。
- **模糊意圖**："想用個模板" / "選一個吧"——沒給路徑 → 走自由設計。

這是有意的——AI 永遠**不做模糊 / 解釋性判斷**，不替你把名字解析成路徑。要用模板，直接給路徑。

想知道內建庫裡有哪些模板，問一句"有哪些模板可以用？"——AI 會從發現索引裡列出名字和對應路徑。單純列出並不進入模板流程，需要你**把其中一條路徑**再發回來才會觸發 Step 3。

### 現有模板一覽

模板按三種身份分目錄：

- [`templates/brands/README.md`](../../skills/ppt-master/templates/brands/README.md) — 僅身份預設（color / typography / logo / voice / icon style），無 SVG 頁面；Anthropic、Google
- [`templates/layouts/README.md`](../../skills/ppt-master/templates/layouts/README.md) — 僅結構樣板（canvas / page structure / page types / SVG roster），無身份；academic_defense、government_blue/red、ai_ops、medical_university、pixel_retro、psychology_attachment
- [`templates/decks/README.md`](../../skills/ppt-master/templates/decks/README.md) — 完整 PPT 復刻（身份 + 結構 + 中間段）；招商銀行、中國電建_*、中汽研_*、重慶大學、中國電信

完整資料模型與三類的合成 / 衝突解決規則見 [`templates-architecture.md`](./templates-architecture.md)。

### 自由設計 vs 模板

自由設計不是"沒有風格"，而是 AI 根據你的內容**為這一份 deck 現場設計**視覺系統；模板則是**沿用一套已經定型的結構和風格**。兩條路都不會少做"設計"，區別只在於風格是即興還是預設。

> 經驗：內容方向明確、品牌或場景有強約束（諮詢報告、政府彙報、答辯）→ 用模板。內容偏散文式、視覺氛圍更重要（雜誌風、紀錄式敘事）→ 自由設計往往效果更好。

### 風格不是模板

**風格**是一種描述（"極簡風" / "Keynote 風" / "雜誌風"）——你在對話裡打幾個字。**模板**是一份要複製貼上的資產包（SVG + design_spec + 素材），只在你給出**顯式目錄路徑**時由工作流安裝到專案裡。

| | 模板 | 風格 |
|---|---|---|
| 怎麼觸發 | 訊息裡給出明確的目錄路徑 | 訊息裡寫自由描述 |
| 發生什麼 | 檔案複製到專案；layouts 繼承自模板 SVG | 描述流到 Strategist；色彩 / 字型 / 調性在策略師確認階段裡推薦 |
| 數值鎖定 | 是 — 來源於模板的 `design_spec.md` | 否 — Strategist 現場推適合 deck 的具體值 |
| 適用場景 | 品牌鎖定的 deck；強視覺約定的場景 | 心裡有感覺但沒有具體品牌承諾 |

風格描述可能看起來像模板名（比如 "學術風" 聽上去像 `academic_defense/` 模板目錄），但走的是**兩套機制**——模板需要你給一個真實可複製的路徑，風格描述是解釋性語言。字面接近，落地完全是兩條路。

### 常見風格描述

三條軸自由組合（"暗色科技 + 極簡" 或 "雜誌風 + 新中式" 都行）：

**美學路線**

| 風格 | 一句話特徵 |
|---|---|
| **極簡風 / Minimalist** | 高留白、2-3 色、單焦點、幾乎零裝飾 |
| **資訊密集 / Information-dense** | 麥肯錫派結構化表格、密度高、conclusion-first |
| **Keynote 風** | 單頁 Hero 文字、premium 留白、Apple 感 |
| **雜誌風 / Editorial** | 大圖當主體、不對稱版式、字型反差強 |
| **文藝手繪** | 暖色、手繪質感、像 zine |

**行業 / 場景**

| 風格 | 一句話特徵 |
|---|---|
| **商務諮詢風** | 資料驅動、專業剋制、藍/灰主調 |
| **學術答辯風** | 嚴謹層級、citation-heavy、清晰樸素 |
| **政府彙報風** | 紅/藍、莊重對稱、標題加粗 |
| **產品釋出風** | 視覺衝擊、營銷大膽、Hero 單圖 |
| **教學課件風** | 清晰層級、友好親和、配色明亮 |
| **路演/BP 風** | 敘事驅動、金句配圖、conclusion-bold |

**視覺調性**

| 風格 | 一句話特徵 |
|---|---|
| **暗色科技風** | 深藍/黑底、霓虹強調、未來感 |
| **畫素復古** | 8-bit、掃描線、遊戲機美學 |
| **新中式** | 留白、傳統紋樣剋制使用、墨色/硃砂 |
| **北歐極簡** | 淺色、原木自然、字號剋制 |
| **孟菲斯/波普風** | 高飽和大色塊、幾何圖形、80 年代 |
| **賽博朋克/蒸汽波** | 霓虹紫粉、網格、迷幻 |

你描述風格時，AI **不會基於這些詞去挑模板**——它把這些詞解釋為對應的色彩 / 字型 / 版式建議，放到 策略師確認階段裡 `d` 項的第二層（視覺風格），然後驅動 e/f/g/h（色彩 / 圖示 / 字型 / 圖片）。你可以確認或調整。如果你想要的風格剛好對上庫裡某個模板（如 `academic_defense` / `pixel_retro` / `psychology_attachment`），有兩條路可選：把模板的目錄路徑發出來鎖定值，或描述風格讓 AI 現場推適配你內容的值。

---

## 二、派生新模板（重點）

把你自己喜歡的 PPT、品牌指南、或一份現成的 PPTX，做成 PPT Master 可呼叫的模板。這是本文的核心。

### 入口：`/create-template` 工作流

完整規範見 [`workflows/create-template.md`](../../skills/ppt-master/workflows/create-template.md)。本節是面向使用者的簡要版本——你只需要在 IDE 對話裡說：

```
请用 /create-template 工作流，基于下面的参考材料生成一个新模板。
```

接下來工作流會**強制**先和你確認一份模板簡報（不允許跳過）。

### 第一步：準備參考材料

**強烈推薦：直接給原始 `.pptx` 檔案。** 當前的 PPTX 匯入管線已經做到接近高保真還原——工作流會用 [`pptx_template_import.py`](../../skills/ppt-master/scripts/pptx_template_import.py) 直接讀取 OOXML，提取主題色、字型、每個 master 的主題摘要、母版/版式結構、placeholder 後設資料和可複用圖片資源。它會輸出作為機器事實源的 layered `svg/`，以及用於視覺預覽的自包含 `svg-flat/`，再交給 Template_Designer 重建出乾淨可維護的 SVG。封面、章節、裝飾繁複的頁面都能穩定還原，這是目前最靠譜的派生路徑。

也可以基於品牌指南從零設計：提供 logo、主色 HEX、字型、調性描述、幾張氛圍參考圖，AI 會現場設計頁面骨架。適合品牌方還沒有成型 PPT、只有 VI 手冊的場景。

> **沒有源 PPTX 時的兜底**：截圖集（`cover.png` / `chapter.png` / `content.png` / `closing.png` 等）也能跑，但保真度會明顯下降——裝飾、字型、版式細節都靠 AI 視覺推斷。能拿到 `.pptx` 就儘量用 `.pptx`。截圖更適合作為標註輔助（"這頁是我想要的樣子"）混進 PPTX 一起給。

### 第二步：模板簡報（強制確認環節）

工作流不會偷偷推斷——它會在動手前向你列出以下條目，等你確認或補全：

| 欄位 | 說明 |
|------|------|
| **模板 ID** | 目錄名 / 索引鍵。優先 ASCII slug，如 `acme_consulting`；中文品牌名也行，但要檔案系統安全 |
| **顯示名稱** | 檔案中的人類可讀名 |
| **類別** | `brand` / `general` / `scenario` / `government` / `special` 五選一 |
| **適用場景** | 年報 / 諮詢 / 答辯 / 政府彙報…… |
| **調性概要** | 一句話，如"現代剋制、資料驅動" |
| **主題模式** | 淺色 / 深色 / 漸變…… |
| **畫布格式** | 預設 `ppt169`（16:9），其他格式需提前指定 |
| **復刻模式** | `standard`（預設 5 頁基本套）/ `fidelity`（按 PPTX 源裡"視覺上真正不同"的版式簇各開一個變體——數量由源決定）/ `mirror`（每張源頁 1:1 原樣複製，零抽象、不插佔位符）—— `fidelity` 和 `mirror` 都必須有 `.pptx` 源 |
| **保真級別** | （`standard` / `fidelity` 有源時必填）`literal`（按原樣復刻幾何/裝飾/精靈圖裁剪）/ `adapted`（借結構和調性、允許設計演化）。封面 / 章節 / 結尾通常用 `literal`。**`mirror` 模式不詢問**——隱含 literal |
| **關鍵詞** | 3–5 個標籤，用於索引檢索 |
| 主題色 / 設計風格 / 素材清單 | 可選，可讓 AI 從源裡自動提取 |

確認後，工作流會回顯一份完整簡報並寫入標記 `[TEMPLATE_BRIEF_CONFIRMED]`，從這一刻起後續步驟才會啟動。**這是一個硬門——簡報沒確認，不會開始生成**。

> 為什麼這麼嚴？因為模板是入庫資產，未來會被複用。一次說清楚，比生成完再返工便宜得多。

### 第三步：選 standard、fidelity 還是 mirror？

這是派生模板裡最容易混淆的決策。

| | **standard** | **fidelity** | **mirror** |
|---|---|---|---|
| 輸出頁數 | 5 頁（封面/章節/目錄/內容/結尾） | 視覺上真正不同的版式簇各一個變體——數量由源決定 | 每張源頁 1:1 一頁 |
| 抽象程度 | 高 —— 乾淨可複用骨架 | 中 —— 聚類後清理 | **零** —— 原樣複製 |
| 是否插佔位符 | 是（`{{TITLE}}`、`{{CONTENT_AREA}}` 等） | 是 | **否** —— Executor 直接在 SVG 裡就地編輯文字 |
| 適合場景 | 你只需要"調性 + 基本骨架"，未來用模板生成全新 deck | 源 PPTX 本身就是高度定製的版式庫 | 別人的精裝 deck 直接好用、想把每頁都當參考頁 |
| 典型例子 | 給品牌做基礎模板 | 復刻一套政府彙報的 20 種章節版式 | 把一份 50 頁的麥肯錫風格 deck 整套用作模板 |
| 必須有 PPTX 源嗎 | 否 | **是** | **是** |
| 裝飾複雜度 | 通常較簡潔 | 需要保留精靈圖（sprite sheet）裁剪等結構 | 源頁啥樣就啥樣，逐位元組繼承 |

**關於精靈圖**：PPTX 匯出的素材常常是**一張大圖 + 多頁通過 viewBox 裁剪不同區域**。`fidelity` 和 `mirror` 模式下必須保留這層巢狀 `<svg viewBox=...>` 包裝，不能扁平化為單張 `<image>`——否則裁剪資訊丟失，畫面會錯位。工作流會自動校驗這一點。

**`mirror` 模板怎麼消費**：mirror 模板裡沒有 `{{}}` 佔位符——Strategist 根據 `design_spec.md §V Page Roster` 的逐頁描述為每個專案頁選一張參考頁，Executor 把那張參考 SVG 拷過去，**僅在原位修改文字內容**，所有裝飾、精靈圖裁剪、幾何座標全部保留。庫資產保持 100% 原樣；針對專案的修改只存在於 `projects/<project>/svg_output/`。

### 第四步：註冊與發現

模板生成完，工作流會：

1. 跑 [`svg_quality_checker.py`](../../skills/ppt-master/scripts/svg_quality_checker.py) 驗證（硬門，不通過不入庫）
2. 把模板 ID 註冊到 [`layouts_index.json`](../../skills/ppt-master/templates/layouts/layouts_index.json)
3. 同步 [`templates/layouts/README.md`](../../skills/ppt-master/templates/layouts/README.md) 表格

註冊讓模板**可被發現**——下次有人問"有哪些模板可用？"時，AI 會從索引裡把它列出來。要在新專案裡用它，仍然按 SKILL.md Step 3 的規則：在第一條訊息裡把目錄路徑寫出來，例如 `用这个模板：skills/ppt-master/templates/layouts/<your_template_id>/`。

### 派生後的目錄長什麼樣

```
skills/ppt-master/templates/layouts/<your_template_id>/
├── design_spec.md          # 设计规范，§VI 列出全部页面
├── 01_cover.svg
├── 02_chapter.svg
├── 02_toc.svg              # 可选
├── 03_content.svg
├── 03a_content_two_col.svg # fidelity 模式下的变体
├── 04_ending.svg
├── logo.png                # 品牌素材
└── bg_pattern.jpg
```

`standard` 和 `fidelity` 模式下的頁面 SVG 裡使用統一的佔位符約定（`{{TITLE}}`、`{{CHAPTER_TITLE}}`、`{{PAGE_TITLE}}`、`{{CONTENT_AREA}}` 等），策略師階段會按內容填充。

`mirror` 模板按源頁序號每頁一張 SVG，**SVG 內部沒有佔位符**：

```
skills/ppt-master/templates/layouts/<your_template_id>/
├── design_spec.md          # frontmatter 设 replication_mode: mirror；§V Page Roster 逐页描述
├── 001_cover.svg
├── 002_toc.svg
├── 003_content.svg
├── 004_content.svg
├── ...
├── 049_content.svg
├── 050_ending.svg
└── *.png / *.jpg
```

### 專案級一次性定製 vs 全域性模板

二者別搞混：

- **派生新模板** = 入全域性庫，在 `skills/ppt-master/templates/layouts/` 下，未來所有專案都能呼叫
- **專案級定製** = 只在 `projects/<project>/templates/` 裡改這一份 deck 的頁面，不入庫、不影響其他專案

`/create-template` 工作流只做前者。後者直接在專案目錄裡改 SVG 即可，不需要走這個流程。

---

## 三、模板的邊界

避免常見誤解：

- **模板 ≠ 母版（Slide Master）**。PPT Master 的輸出是原生 DrawingML 形狀，不依賴 PowerPoint 母版機制。模板是 SVG 骨架，最終在匯出階段被翻譯為 PPTX 形狀
- **模板不是"風格皮膚"**。它包含結構（頁面有幾塊、資訊層級如何分佈）+ 風格（配色、字型、裝飾），兩者不可分割。試圖只換"皮膚"不換結構，往往會讓資訊架構和視覺打架
- **模板不會替你做內容決策**。策略師仍然會按內容判斷每頁用哪個版式、要不要擴充套件為變體，模板提供候選，不預設結果
- **`fidelity` 模式不等於畫素級搬運**。即便是 `literal` 保真，AI 仍會把雜質和不必要的重複結構清理掉——載體保留幾何，但不照抄冗餘
- **`mirror` 模式確實是畫素級搬運——但它繼承源 PPT 的匯入限制**。圖表、SmartArt、OLE 物件、EMF / WMF 媒體如果在 `pptx_template_import.py` 裡 round-trip 失敗，mirror 也會同樣失敗。flat SVG 是事實源——`<workspace>/svg-flat/` 裡看著斷了，mirror 模板也會斷

---

## 相關檔案

- [`workflows/create-template.md`](../../skills/ppt-master/workflows/create-template.md) — 完整工作流規範（面向 AI 執行）
- [`templates/layouts/README.md`](../../skills/ppt-master/templates/layouts/README.md) — 現有模板一覽
- [`references/template-designer.md`](../../skills/ppt-master/references/template-designer.md) — 模板設計師角色定義和 SVG 技術約束
- [常見問題：如何製作自定義模板](./faq.md#q-如何製作自定義模板) — FAQ 簡版
