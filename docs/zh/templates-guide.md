# 模板指南：選用、派生與邊界

[English](../templates-guide.md) | [Chinese](./templates-guide.md)

---

PPT Master 模板是一種可複用工作區，明確分為三類：**Brand** 只擁有身份系統，**Layout** 只擁有品牌中立的可複用頁面結構，**Deck** 擁有一類可重複演示的描述性應用語境及一體化身份與結構。Layout 與 Deck 工作區包含宣告 Master / Layout / slot 合同的完整 SVG 原型；Brand 工作區則有意不包含 SVG roster。每個工作區的 `design_spec.md` 與配套素材共同宣告該 kind 實際提供什麼。

本文回答三個問題：

1. [怎麼用已有模板？](#一選用已有模板)
2. [怎麼把別人的 PPT / 自己的品牌做成模板？（重點）](#二派生新模板重點)
3. [模板的邊界是什麼？](#三模板的邊界)

## 60 秒選對模板路線

先看你手裡有什麼，以及最終想得到什麼：

| 起點與目標 | 路線 | 可直接複製的請求 |
|---|---|---|
| 手裡是原始 `.pptx`，想保留現有頁面殼並替換內容 | **Fill Native PPTX** | `用 projects/source/template.pptx 套入 projects/source/content.md 的内容。` |
| 已有可複用 Brand/Layout/Deck 工作區，想生成一份全新 deck | **Generate PPTX + 顯式工作區路徑** | `用 sources/report.pdf 做 deck，模板用 skills/ppt-master/templates/layouts/presentation_core/。` |
| 手裡是 PPTX、SVG、品牌手冊、網站、圖片或混合參考，想先建立可複用系統 | **Create Template → Generate PPTX** | `用 /create-template 从 projects/brand/our_deck.pptx 创建一个可复用 Deck 工作区。` |

不要把原始 `.pptx` 當作 Generate PPTX 的模板路徑。想沿用它的現有頁面就直接回填；想建立可複用系統，就先執行 Create Template。

再按需要複用的內容選擇工作區 kind：

| Kind | 複用什麼 | 原生 PowerPoint 結果 |
|---|---|---|
| **Brand** | 顏色、字型、Logo、語調、圖示風格 | 只提供身份約束。生成頁面保持 Slide 本地，檔案只有乾淨的專案 Master 與 Blank Layout 腳手架。 |
| **Layout** | 品牌中立的頁面語法、Master/Layout 身份、語義文字角色、槽位與版式 roster | 結構化 deck，包含可複用原生 Master、具名 Layout 與 placeholder；身份、閱讀模式字號和溝通應用另行解析。 |
| **Deck** | 一類可重複演示：描述性應用語境、身份、頁面結構與真實原型 | AI 根據模板實物與當前內容自動生成頁面/原型應用計劃。 |

Theme、Slide Master、Slide Layout 與 Placeholder 是 PowerPoint 原生物件，不是新的工作區 kind。Brand 與 Layout 的規則會被編譯進這些物件。使用 `layout` 時，語義文字角色來自 Layout，最終字型和字號體系由身份與閱讀模式共同解析；使用 `mirror` 時則保留來源的字面格式。最終 Master 可以同時包含結構幾何和品牌視覺，但來源合同仍保持分離。

最容易避免誤用的兩條規則：

1. 提供**工作區根目錄**，不要只給它的 `templates/` 子目錄，也不要只寫模板名。
2. 在 [Generate PPTX Step 3](../../skills/ppt-master/workflows/generate-pptx.md#step-3-template-option) 之前明確給出工作區路徑。同一對話剛完成 Create Template 時，也可直接把已驗證工作區交給 Generate PPTX。

---

## 一、選用已有模板

### 觸發方式

工作流**預設走自由設計**——不會主動問你要不要用模板，也不會基於內容主動推薦模板。模板是 opt-in 的，**只接受顯式目錄路徑**：在 Generate PPTX 進入 Step 3 前把模板目錄路徑寫出來。

### 怎麼觸發模板流程

在 Generate PPTX 進入 Step 3 前，於對話裡寫出 Brand/Layout/Deck 工作區根目錄（位置不重要，只要明確即可）：

> "用這個模板做：`skills/ppt-master/templates/layouts/presentation_core/`" ✅
> "用上次那個模板：`projects/last_deck/`" ✅
> "做一份產品介紹，模板用 `/Users/me/Desktop/our_brand_v3/`" ✅

對於當前所有模板型別，這裡給的都是**模板工作區根目錄**。Step 3 會解析其中的 `templates/design_spec.md`，然後把 `templates/` 及實際存在的 `images/`、`icons/` 安裝進目標專案；如果工作區本來就是該專案根目錄，則原地消費，並且始終不復制 `exports/`。Deck/Layout 還會校驗 structured SVG 合同。路徑可以指向 `skills/ppt-master/templates/<kind>/<id>/` 下的內建庫工作區、`projects/<name>/` 下的專案工作區，或其他保持同樣路由的工作區。當前對話剛完成 create-template 時，可把精確的已驗證工作區根目錄直接交給 Step 3；使用者顯式提供路徑與當前對話的 Create Template 交接是兩種合法觸發方式。

> **相容性預檢：** Step 3 也接受 `design_spec.md` 與 SVG 直接位於所給根目錄的平鋪工作區，但這些 SVG 必須已經滿足當前合同。目錄平鋪本身沒有問題；舊的原子 placeholder、未對映 Master/Layout 等語義舊包會被拒絕。先執行 `create-template` 建立新工作區，再從該工作區生成新的 structured 頁面；不會原地升級舊包。

### 什麼**不會**觸發模板流程

- **只寫模板名、不給路徑**："用 presentation_core 模板" / "做一份中國電信模板的產品介紹" → 走自由設計。AI 不會替你把名字解析成路徑。要用模板，請直接給路徑。
- **風格描述**："麥肯錫風格" / "Google style" / "麥肯錫那種" / "極簡風" / "Keynote 風" → 走自由設計。這些描述會順著對話流到 Strategist 那邊作為風格說明使用，但**不會複製任何模板檔案**。
- **模糊意圖**："想用個模板" / "選一個吧"——沒給路徑 → 走自由設計。

這是有意的——AI 永遠**不做模糊 / 解釋性判斷**，不替你把名字解析成路徑。要用模板，直接給路徑。

想知道內建庫裡有哪些模板，問一句"有哪些模板可以用？"——AI 會從發現索引裡列出名字和對應路徑。單純列出並不進入模板流程，需要你**把其中一條路徑**再發回來才會觸發 Step 3。

### 可直接複製的用法

使用一個工作區：

```text
用 projects/q3-report/sources/report.pdf 做一份 deck。
模板工作区：skills/ppt-master/templates/layouts/presentation_core/
```

組合身份與結構：

```text
用 projects/launch/sources/brief.md 做产品发布 deck。
Brand 工作区：skills/ppt-master/templates/brands/anthropic/
Layout 工作区：skills/ppt-master/templates/layouts/presentation_core/
```

使用之前建立的專案級模板：

```text
用 projects/annual-report/sources/report.md 做一份 deck。
模板工作区：projects/acme_template/
```

“模板工作區”這些標籤可以不寫，但路徑本身必須明確。如果給出兩個相同 kind 的路徑，工作流會進入既有衝突解決門，不會靜默替你選一個。

你不需要選擇模板使用模式。預設由 Strategist 讀取真實的 Master/Layout/原型集合和當前內容，決定選哪些頁、哪些重複/跳過/重排，以及是否重組。如果你在意某個邊界，直接在同一句請求裡用普通語言說明即可，例如“封面和結束頁原樣保留，中間頁由你選擇”或“只參考視覺語言”；明確文字優先於 AI 判斷。

### 現有模板一覽

模板按三種 kind 分目錄，並分別由發現索引維護：

- [`brands_index.json`](../../skills/ppt-master/templates/brands/brands_index.json) — 僅身份工作區：color / typography / logo / voice / icon style，不含 SVG 頁面 roster
- [`layouts_index.json`](../../skills/ppt-master/templates/layouts/layouts_index.json) — 僅結構工作區：canvas / 頁面語法 / page types / SVG roster，身份系統下游再選
- [`decks_index.json`](../../skills/ppt-master/templates/decks/decks_index.json) — 可重複演示應用，包含一體化身份、結構與原型事實描述

直接問“有哪些模板可以用？”即可得到帶工作區路徑的可讀清單。索引是當前安裝內容的真值，三類 README 負責定義合同。完整資料模型與三類的合成 / 衝突解決規則見 [`templates-architecture.md`](./templates-architecture.md)。

### 自由設計 vs 模板

自由設計不是“沒有結構”或“沒有風格”——Strategist 仍會為這份 deck 規劃敘事、層級與視覺系統，但生成頁面使用 `pptx_structure.mode: flat`，所有可見物件都保留在 Slide 本地。僅使用 Brand 工作區時同樣保持 `flat`，只是由 Brand 提供身份約束。Layout 與 Deck 工作區提供可複用 Master / Layout / slot 合同；Strategist 會讀取真實原型和當前內容，自動判斷是複用結構，還是隻參考視覺語言。

> 經驗：需要鎖定身份系統時用 Brand；需要複用品牌中立結構、但讓用途保持開放時用 Layout；需要把品牌化結構或可重複溝通場景作為一份契約複用時用 Deck；希望版式從當前內容出發重新生長時走自由設計。

### 風格不是模板

**風格說明**是解釋性語言（“極簡風” / “Keynote 風” / “雜誌風”），由 Strategist 轉化為具體設計選擇。**模板**則是真實存在的 Brand / Layout / Deck 工作區，只有在你給出**顯式目錄路徑**時才會被工作流消費。

| | 模板 | 風格 |
|---|---|---|
| 怎麼觸發 | 訊息裡給出明確的目錄路徑 | 訊息裡寫自由描述 |
| 提供什麼 | 由 kind 宣告的身份段、結構段或兩者 | 由 Strategist 解釋為 mode、visual style、色彩、字型、圖示與圖片方向 |
| 如何確認 | 模板擁有的值構成起始合同；使用者最終確認的選擇仍然權威 | 沒有預寫數值；Strategist 給出具體候選，由使用者確認 |
| 適用場景 | 複用已有身份系統和 / 或頁面系統 | 只表達想要的感覺，不採用已存工作區 |

風格描述和模板名仍走**兩套機制**：“極簡風”是解釋性語言，`presentation_core/` 則是真實模板目錄，必須提供顯式路徑。

### 風格說明如何被解釋

Strategist 會把方向拆成兩個彼此獨立的選擇：

- **Mode** 決定 deck 怎麼表達：`pyramid`、`narrative`、`instructional`、`showcase`、`briefing`，或經過確認的 `custom`。
- **Visual style** 決定頁面怎麼呈現：內建方向包括 `swiss-minimal`、`editorial`、`dark-tech`、`data-journalism`、`ink-wash` 等，也支援 `custom`。

任意 mode 都可以搭配任意 visual style。“Keynote 風產品釋出”這類描述可能同時影響兩條軸，例如形成 `showcase` 敘事與高留白視覺系統，但它永遠不是模板查詢詞。生成前，使用者會確認最終組合。規範目錄位於 [`references/modes/`](../../skills/ppt-master/references/modes/) 與 [`references/visual-styles/`](../../skills/ppt-master/references/visual-styles/)。

---

## 二、派生新模板（重點）

把一個或多個 PPTX/SVG、圖片/PDF、檔案/網站、品牌資產或直接文字要求，做成 PPT Master 可呼叫的模板。參考材料可以混合使用，也可以不提供外部來源，僅根據確認後的簡報從零設計。這是本文的核心。

### 入口：`/create-template` 工作流

完整規範見 [`workflows/create-template.md`](../../skills/ppt-master/workflows/create-template.md)。本節是面向使用者的簡要版本——你只需要在 IDE 對話裡說：

```
请用 /create-template 工作流，基于下面的参考材料生成一个新模板。
```

接下來工作流會**強制**先和你確認一份模板簡報（不允許跳過）。

入口名稱始終保持 **Create Template**。它只分派一個子工作流：僅複用身份走 Create Brand；複用品牌中立結構、且溝通應用保持開放時走 Create Layout；複用品牌化結構或可重複演示應用時走 Create Deck。來源是一份完整 PPTX 並不會自動決定 kind，工作流只按真正穩定、值得重複使用的規則分類。子工作流一旦選定，不會在簡報裡再次選 kind。

### 第一步：準備參考材料包或簡報

你可以直接在對話中輸入文字或貼上要求，也可以提供 Markdown/TXT、DOCX/PDF/HTML/URL、網站、圖片/截圖、logo/icon/字型資產、PPTX/SVG，或這些材料的任意組合。工作流會分析每個適用通道，保留來源，並在強制簡報中暴露衝突，而不是靜默選擇某一個來源。凡是你本人明確寫出的值，無論來自對話、貼上文字還是你編寫的簡報檔案，都屬於決策；檔案載體本身不會把它變成事實。事實必須來自可獨立追溯的外部權威，或可由機器直接觀察的原始檔/包後設資料。視覺估算與模糊文字的解釋在確認前都只是建議。

**當現有簡報的原生結構很重要時，請直接提供原始 `.pptx` 檔案。** 匯入器會讀取 OOXML，把包內實際存在且受支援的 Master、Layout、placeholder、主題、原生形狀與可複用素材事實提取成分層分析參考。你只需用普通語言說明想要的結果，例如“原樣保留”“提取成可複用母版和版式”或“保留視覺語言但重做結構”；AI 會據此選擇相容的內部實現。原 PPTX 始終是不可變的分析證據，不進入新模板包。

也可以基於品牌指南從零設計：提供 logo、主色 HEX、字型、調性描述、幾張氛圍參考圖，AI 會現場設計頁面骨架。適合品牌方還沒有成型 PPT、只有 VI 手冊的場景。

> **證據邊界：** 圖片、截圖、文字、檔案、網站和零散資產可以驅動重新創作；更廣的來源對齊需要 PPTX/SVG 頁面證據；字面保留原生結構需要原始 PPTX 或完整的當前結構化 SVG 合同。補充來源可以解釋保留意圖，但不能補造或改變原生拓撲。

### 第二步：模板簡報（強制確認環節）

工作流會在動手前寫出一份簡潔的自然語言方案，等待你修正或確認；不會要求你選擇模板模式、保真列舉或頁面/內容政策。

| 欄位 | 說明 |
|------|------|
| **輸出範圍** | `library`（預設）或 `project`；兩者使用相同的可移植工作區路由，只有 library 會進入全域性索引 |
| **目標專案** | 僅 `project` 必填；必須給出已初始化專案的精確路徑 |
| **已選子工作流** | Create Brand / Create Layout / Create Deck，由入口分派後固定 |
| **模板 ID** | 模板的可移植身份；在 `library` 下同時也是目錄名 / 索引鍵。優先 ASCII slug，如 `acme_consulting`；中文品牌名也行，但要檔案系統安全 |
| **顯示名稱** | 檔案中的人類可讀名 |
| **模板語境** | AI 提議一個類別、適用場景、顯示名稱、調性概要和索引關鍵詞；你可直接修改文字 |
| **畫布與視覺方向** | 僅 Create Layout/Create Deck：建議畫布、明暗關係、身份和從來源觀察到的視覺規則 |
| **建立方案** | AI 將保留、重建、簡化或提取什麼；原型範圍多大；如何處理原生結構——全部用普通語言說明 |
| **來源事實與素材** | 可觀察的 Master/Layout 事實、受支援原生能力、採用/排除的素材及重要限制 |

確認後，工作流會回顯一份完整簡報並寫入標記 `[TEMPLATE_BRIEF_CONFIRMED]`，從這一刻起後續步驟才會啟動。**這是一個硬門——簡報沒確認，不會開始生成**。

無論選擇哪種範圍，第一次寫最終檔案前都會做一次完整預檢：解析必需的 `templates/` 和實際需要的可選素材目錄，要求 `templates/` 為空，並檢查 `images/` 與 `icons/imported/` 中計劃寫入的點陣圖和匯入向量檔名沒有衝突；只有明確要求審閱 PPTX 時才檢查 `exports/`。專案範圍還要求目標專案已經初始化。專案初始化時已存在的空腳手架目錄可以保留且不會被算作模板產物；Create Template 不會為了保留空路徑而新建可選目錄。任一檢查失敗都會在寫入前停止，不合並、不覆蓋，也不會留下半套輸出。

> 為什麼這麼嚴？無論模板進入全域性庫，還是隻服務當前專案，它都是結構契約。先確認歸屬和幾何，可避免半成品或資產落錯目錄。

### 第三步：AI 推導內部實現

你不需要選擇建立模式。AI 會把已確認的自然語言方案轉換成一個內部策略，供確定性工具執行：

- 需要精煉時，建立緊湊的可複用系統；
- 來源本身包含有價值的多種版式時，建立更廣的來源對齊原型；
- 明確要求原樣保留、且來源結構完整受支援時，進行字面物化。

frontmatter 仍會記錄 `replication_mode: standard|fidelity|mirror` 以相容工具並保留審計資訊；它是實現記錄，不是使用者選項。品牌中立的 Layout 不能同時字面保留品牌/應用事實，AI 會按目標重新創作 Layout，或把這些事實留在 Deck 中。

**關於精靈圖**：PPTX 匯出的素材常常是**一張大圖 + 多頁通過 viewBox 裁剪不同區域**。`fidelity` 和 `mirror` 模式下必須保留這層巢狀 `<svg viewBox=...>` 包裝，不能扁平化為單張 `<image>`——否則裁剪資訊丟失，畫面會錯位。工作流會自動校驗這一點。

**關於 PowerPoint 原生形狀**：完整匯入 SVG 作為原生載荷後備留在臨時分析工作區且保持不可變；模板建立使用輕量、可編輯的 `authoring-svg/` IR 及其 source-ref/hash manifest。創作模式使用專案規範化 SVG，只有精確匹配已登記 preset 時才使用 compact authored-preset 組。Mirror 從 IR 物化最終模板 SVG，只為未改且 hash 匹配的 Slide-local/slot ref 重新接入轉換器已支援的載荷；固定 Master/Layout 層保持直接原子，不支援或已修改的物件保留當前 SVG fallback，最終模板不包含 IR 專用 ref。

對於 PPTX 來源的 Type A mirror，最終物化統一使用一個確定性命令：

```bash
python3 skills/ppt-master/scripts/mirror_template_materialize.py \
  "<import_workspace>" "<empty_template_workspace>"
```

它會先校驗 IR manifest、不可變來源 hash、完整原生圖譜、可見性事實和
匯入向量閉包，再原子釋出按源順序排列的 SVG roster 及
`icons/imported/`、`images/` 素材。它不要求、也不會把按需生成的
`svg-flat/` 校驗檢視當成模板來源，並且不會生成 `design_spec.md`；設計角色必須針對物化後的 roster 編寫該簡報。

**Mirror 圖譜邊界**：mirror 保留完整且受支援的來源 Master/Layout 圖譜。它為每張來源 Slide 輸出一個完整原型，併為未被任何來源 Slide 使用的 Layout 額外輸出一個定義專用的 `layout_<layout_key>.svg`。後者通過獨立 Layout roster 註冊進 PowerPoint，不會變成釋出頁面；其父 Master 也隨之保留。預檢只在必要來源事實或受支援幾何缺失時停止，不會僅因 Layout 未使用而停止。

**按 mirror 建立的工作區怎麼消費**：從來源到工作區的 `replication_mode: mirror` 是一種能力，不是專案選擇。Strategist 會讀取真實原型、當前內容和使用者明確要求，自動決定選哪些頁、哪些重複/跳過/重排，以及採用字面、結構還是僅視覺參考。字面複用時，Executor 複製完整 SVG，只修改允許變更的可見文字，同時保留裝飾、精靈圖裁剪、幾何座標和規範化結構宣告；仍不要求沿用來源頁數或頁序。

### 第四步：驗證、預覽匯出、註冊與發現

模板生成完，兩種範圍都會先跑 [`svg_quality_checker.py`](../../skills/ppt-master/scripts/svg_quality_checker.py) 作為硬門：Brand 校驗 identity-only 規範與素材引用，Layout/Deck 校驗 SVG roster 和 structured 合同。如果需要 PowerPoint 審閱檔案，再執行可選預覽匯出；它會按需建立 `exports/<id>_template_preview.pptx`。創作型模板會只在臨時預覽副本中使用簡短佔位示例，避免較長的 canonical marker 換行，不會修改源 SVG。唯一按範圍分流的動作是全域性註冊：

| 範圍 | 工作區根目錄 | 預覽 | 發現行為 |
|---|---|---|---|
| `library`（預設） | `skills/ppt-master/templates/<kind>/<id>/` | Create Brand：不適用；Create Layout/Create Deck：單 Master 可選、多 Master 必須 | 校驗後註冊到對應 `brands_index.json`、`layouts_index.json` 或 `decks_index.json` |
| `project` | `projects/<name>/` | 沿用同一套 kind-specific 審閱規則 | 跳過全域性索引註冊 |

全域性註冊讓模板**可被發現**——下次有人問“有哪些模板可用？”時，AI 會從索引裡把它列出來。兩種範圍的用法相同：按 [Generate PPTX Step 3](../../skills/ppt-master/workflows/generate-pptx.md#step-3-template-option) 的規則，在 Step 3 執行前給出工作區根目錄，例如 `用这个模板：skills/ppt-master/templates/layouts/<your_template_id>/` 或 `用这个模板：projects/<name>/`。專案工作區也可以遷移或被其他工作區複用，因為核心結構完全一致；只有放進全域性庫並需要被發現時才執行註冊。

選擇 Deck/Layout 模板後，Strategist 會自動生成頁面/原型應用計劃：可以使用全套或子集，重複或重排原型，並按內容需要重組。`strict` / `adaptive` 只作為內部匯出值，不再出現在確認選項中。

### 如何確認母版與版式真的生效

使用 Layout 或 Deck 工作區生成後，在 Microsoft PowerPoint 中檢查釋出檔案：

| 檢查位置 | 預期結果 |
|---|---|
| **檢視 → 幻燈片母版** | 能看到模板宣告的 Master 與具名 Layout。 |
| **開始 → 新建幻燈片** | 版式選擇器中能在預期 Master 下看到可複用 Layout 名稱。 |
| 選中生成頁並檢視 **版式** | 頁面繫結到宣告的 Layout，而不是匯出器猜出的通用版式。 |
| 點選可複用內容區域 | 模板槽位表現為帶宣告型別與邊界的原生 placeholder。 |
| 從某個已匯出 Layout 新建一頁 | 不復製成品內容頁，也能得到該 Master/Layout 的固定視覺與 placeholder 幾何。 |

Brand-only 的目標不同：它只施加身份約束，創作內容仍保持 Slide 本地，因此不應期待除乾淨包腳手架之外的可複用 Layout roster。

`exports/<id>_template_preview.pptx` 是 Create Template 按需或按規則生成的審閱證據，不是模板輸入；真正生成時始終傳工作區根目錄。

Master/Layout 行為以 Microsoft PowerPoint 為驗收目標。Keynote、WPS 與 LibreOffice 可以開啟 PPTX，但可能歸一化模板結構，或在載入包含大量未使用 Layout 的 mirror roster 時明顯更慢。

### 派生後的模板工作區長什麼樣

全域性庫與專案範圍使用相同的核心結構。把下面的 `<template_workspace>` 替換為 `skills/ppt-master/templates/<kind>/<id>/` 或 `projects/<name>/` 即可：

```
<template_workspace>/
├── templates/
│   ├── design_spec.md
│   ├── 01_cover.svg
│   ├── 02_toc.svg              # 可选；不含时为 02_chapter、03_content、04_ending
│   ├── 03_chapter.svg
│   ├── 04_content.svg          # 同类有多个变体时改用 04a/04b 兄弟命名
│   └── 05_ending.svg
├── images/                         # 可选
│   └── *.png / *.jpg           # SVG 统一引用 ../images/<name>
├── icons/                          # 可选
│   └── imported/
│       └── *.svg               # 导入向量素材的唯一规范副本
└── exports/                        # 可选；按需生成审阅文件
    └── <id>_template_preview.pptx
```

`standard` 和 `fidelity` 模式下的頁面 SVG 使用統一的佔位符約定（`{{TITLE}}`、`{{CHAPTER_TITLE}}`、`{{PAGE_TITLE}}`、`{{CONTENT_AREA}}` 等）。每個原生槽位都是帶語義型別與正數 bounds 的頂層 `<g>`，普通槽位恰好包含一個 carrier；固定 Master/Layout 視覺是根級直接原子元素，絕不使用層級 `<g>`。Layout 可以有意保持零槽位。

`mirror` 工作區使用同一棵目錄樹，只是把按源頁排序的 `001_cover.svg`、`002_toc.svg` 等檔案放進 `templates/`。它可以保留原示例文字而不寫 `{{...}}`，但匯入識別出的原生內容槽仍帶語義 metadata。

匯入向量佔位符統一寫成 `data-icon="imported/<name>"`。校驗、預覽匯出與最終匯出都解析工作區根目錄下同一份 `icons/imported/<name>.svg`；不需要、也不允許再建立 `templates/icons/` 副本。

### 全域性註冊與專案放置

- **全域性庫範圍（`library`，預設）**把工作區寫入 `skills/ppt-master/templates/<kind>/<id>/`，並完成全域性註冊。
- **專案範圍（`project`）**把同一份可移植工作區寫入 `projects/<name>/`，並跳過註冊。

專案範圍不是私有或縮減格式。Step 3 可以直接接收任一工作區根目錄；`templates/` 及實際存在的 `images/`、`icons/` 可以在兩類根目錄之間複製或遷移，無需改形。如果遷入全域性庫，再執行註冊，讓發現索引反映新位置。

---

## 三、模板的邊界

避免常見誤解：

- **可複用模板是一份顯式工作區，不是打包後的源 PPTX。** Brand 可以只有身份系統；Layout 與 Deck 才增加 structured SVG 合同。創作模式建立這份合同，mirror 則把經過驗證的來源歸屬事實對映進去；匯出只編譯已宣告的結構
- **模板不是一張不可拆分的“風格皮膚”。** Brand、Layout 與 Deck 有意把身份和結構拆開，使每一段都能按明確所有權單獨複用或參與合成
- **模板不會替你做內容決策**。策略師仍然會按內容判斷每頁用哪個版式、要不要擴充套件為變體，模板提供候選，不預設結果
- **`fidelity` 模式不等於畫素級搬運**。即便是 `literal` 保真，AI 仍會把雜質和不必要的重複結構清理掉——載體保留幾何，但不照抄冗餘
- **`mirror` 的目標是受支援範圍內的視覺與來源拓撲忠實，不是位元組級 OOXML**。它繼承源 PPT 的匯入限制，只允許固定結構層 group 展開等機械歸一化。不支援的原生物件保留可用 SVG fallback 或明確報告；mirror 不歸納替代 ownership。

---

## 相關檔案

- [`workflows/create-template.md`](../../skills/ppt-master/workflows/create-template.md) — 完整工作流規範（面向 AI 執行）
- [`templates/layouts/README.md`](../../skills/ppt-master/templates/layouts/README.md) — 現有模板一覽
- [`references/template-designer.md`](../../skills/ppt-master/references/template-designer.md) — 模板設計師角色定義和 SVG 技術約束
- [常見問題：如何製作自定義模板](./faq.md#q-如何製作自定義模板) — FAQ 簡版
