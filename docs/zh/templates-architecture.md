# 模板架構：Brand / Layout / Deck 三分類

[English](../templates-architecture.md) | [Chinese](./templates-architecture.md)

---

> 本文是**架構對齊檔案**，定義"模板"在資料模型層面的三種身份、各自的 `design_spec.md` 欄位集、以及多路徑合成與衝突解決規則。面向貢獻者與 AI 工作流，回答"一個模板目錄裡應該寫什麼、不寫什麼；多個模板同時給時怎麼合成"。
>
> 使用者視角的用法（怎麼觸發、怎麼選）見 [`templates-guide.md`](./templates-guide.md)；本文不重複。

---

## 一、三分類

| 分類 | 全域性庫工作區根目錄 | 寫什麼 | 不寫什麼 | 出處工作流 |
|---|---|---|---|---|
| **Brand** | `templates/brands/<id>/` | 僅身份段：color / typography / logo / voice / icon style | 不寫 canvas、page structure、SVG roster | `workflows/create-template/create-brand.md` |
| **Layout** | `templates/layouts/<id>/` | 僅品牌中立的結構段：canvas / page structure / 語義文字角色 / page types / SVG roster | 不寫品牌身份，也不擁有可重複溝通場景 | `workflows/create-template/create-layout.md` |
| **Deck** | `templates/decks/<id>/` | 一類可重複演示：描述性應用語境 + 一體化身份與結構 | —— | `workflows/create-template/create-deck.md` |

每張新建的 Layout/Deck SVG 都是完整預覽，並在根節點宣告 Master/Layout key 與選擇器名稱；固定 Master/Layout 視覺是直接原子元素；語義槽位是頂層 group。普通槽位必須有正數設計區域 bounds 和恰好一個相容 carrier；複合 `object` 區域走顯式 proxy 繫結，零槽 Layout 也合法。這些專用標記具有最高優先順序；最小 `data-pptx-role` 只補充它們無法表達的頁面框架行為。Create Template 根據自然語言意圖與來源證據在內部推導 `standard` / `fidelity` / `mirror`；Strategist 再根據真實原型與當前內容推導 strict/adaptive 匯出行為。這些實現值都不是使用者必選項。根目錄平鋪 `design_spec.md` 的目錄只有在 SVG 已滿足當前合同時才相容；帶舊結構語義的包必須替換為新建模板工作區，不能原地升級。

三者是**三種並列的可複用規則包**，不是 PowerPoint 包物件型別。在全域性庫範圍內，物理目錄與 frontmatter `kind` 欄位雙向對齊：

多路徑合成後的專案級 `design_spec.md` 沿用現有路由 `kind`：同時具備身份段和結構段時為 `deck`，只有結構段時為 `layout`，只有身份段時為 `brand`。對於專案內臨時組合的 Brand + Layout，這個標籤只表示“已安裝兩種能力”，不會把組合自動提升為可註冊的 Deck，也不會憑空生成應用語境；當前專案的 Stage 1 溝通契約負責提供場景。Strategist 在內部生成模板應用計劃，確認頁不顯示模板模式控制元件。

```yaml
# templates/brands/anthropic/templates/design_spec.md
---
kind: brand
...
---

# templates/layouts/presentation_core/templates/design_spec.md
---
kind: layout
native_structure_mode: structured
...
---

# templates/decks/中国电信/templates/design_spec.md
---
kind: deck
native_structure_mode: structured
...
---
```

### PowerPoint 原生物件是編譯目標

專案模板 kind 與 PresentationML 物件不是一一對應關係：

| 專案合同 | 原生投影 |
|---|---|
| **Brand** | Theme 的顏色、字型與效果，以及 Logo 等固定身份資產規則 |
| **Layout** | Master/Layout/Placeholder 拓撲、可複用幾何、語義文字角色與槽位空間行為 |
| **Deck** | Brand 與 Layout 的投影，再加描述性重複應用語境和真實原型 |

一個 Slide Master 可以同時包含結構幾何和品牌視覺。來源規則仍分開歸屬：Layout 決定拓撲、位置、語義文字角色與空間行為，Brand 決定身份值與資產。下游選擇 `layout` 時，匯出結合已確認的閱讀模式和字號體系解析最終 placeholder 格式；選擇 `mirror` 時則保留來源的字面格式與文字拓撲。最後再把適用規則編譯進同一套 Master/Layout 圖譜。因此 Theme 是已解析身份的實現投影——身份可以來自 Brand、Deck 或當前專案——而不是第四種模板 kind。

### 輸出範圍與 kind 相互獨立

`create-template` 會確認 Layout/Deck 工作區放在哪裡。這個執行選擇不會增加第四種 kind，也不會增加新的 PPTX 結構模式：

| 範圍 | 工作區根目錄 | 核心結構 | 發現行為 |
|---|---|---|---|
| `library`（預設） | `skills/ppt-master/templates/<kind>/<id>/` | 必需 `templates/`；可選 `images/`、`icons/` 與按需 `exports/` | 寫入對應全域性索引 |
| `project` | `projects/<name>/` | 完全相同的路由合同 | 不更新全域性索引 |

兩種根目錄都保持相同的核心形態：

```text
<template_workspace>/
├── templates/
│   ├── design_spec.md
│   └── *.svg
├── images/                     # 可选；SVG 统一引用 ../images/<name>
├── icons/
│   └── imported/               # 可选；导入向量素材的唯一规范副本
└── exports/                    # 可选；用户要求审阅或多 Master 包需要证据时创建
    └── <id>_template_preview.pptx
```

空的可選目錄直接省略，不新增佔位檔案。預覽 PPTX 是派生審閱證據，不是模板源資產；單 Master 按需生成，多 Master 必須通過該 package gate。Step 3 讀取工作區根目錄，只消費 `templates/` 及實際存在的 `images/`、`icons/`，不會複製或使用 `exports/`；全域性庫下的 `exports/` 統一由 Git 忽略。

匯入向量統一使用 `data-icon="imported/<name>"`，唯一規範檔案位於 `icons/imported/<name>.svg`。具備工作區感知的校驗與匯出會直接解析這個根目錄路徑；`templates/icons/` 不屬於模板包結構。

原生形狀 metadata 採用兩級模型。完整匯入 SVG 儲存 native metadata、隱藏 carrier 和預覽證據，並作為不可變原生載荷後備；`svg_authoring_view.py` 生成可編輯 authoring IR，其中輕量 SVG 使用檔案內 source ref 標識物件，manifest 只儲存路徑和初始 hash。創作模式使用專案規範化 SVG，只有精確匹配已登記 preset 時才使用 compact authored-preset 組。Mirror 從 IR 物化模板，僅為未改且 hash 匹配的 Slide-local/slot ref 重新接入轉換器已支援的載荷；固定結構層保持直接原子，不支援或已修改的物件保留 SVG fallback，最終模板不包含 IR 專用 ref。匯出只編譯宣告的結構，不推斷歸屬。

兩種範圍都在可移植 frontmatter 中保留 `kind: layout` 或 `kind: deck`。`output_scope` 與 `target_project` 只屬於工作流簡報，不寫入 `design_spec.md`。

任何範圍第一次寫最終檔案前，都必須解析工作區根目錄、確認 `templates/` 為空，並檢查全部計劃寫入的圖片與圖示檔名無衝突；使用者要求預覽或已確認 roster 含多個 Master 時檢查預覽 PPTX 目標。專案範圍還必須確認目標專案已初始化。任一失敗都在寫入前停止，不合並、不覆蓋。

### 三段的欄位切分

為了讓多路徑合成能幹淨覆蓋，所有欄位按段歸屬，**段級整段替換是預設粒度**：

| 段 | 包含的章節 | 歸屬（覆蓋優先順序）|
|---|---|---|
| **身份段** | Color Scheme / Typography / Logo / Voice & Tone / Icon Style | brand 覆蓋 |
| **結構段** | 可移植 canvas/page-type 後設資料、結構歸屬的 Signature 規則、SVG Page Roster，以及 SVG Master/Layout/slot 合同 | layout 覆蓋 |
| **應用段** | Template Overview：重複場景、受眾與結果、交付假設及代表性敘事/頁面角色 | deck 獨有；brand / layout 不寫 |

### 為什麼需要 Deck 這一類

Deck 編碼的是**一類可重複演示**，而不只是預先組合好的 Brand 和 Layout。它描述模板服務哪些溝通場景、支援哪些受眾結果，以及常見的敘事或頁面角色。身份與結構圍繞這份語境形成一個整體；具體選哪些原型、如何處理內容，由當前 Strategist 決定。

`standard` / `fidelity` 根據已確認的證據創作新完整系統；mirror 把已驗證的來源身份與父子關係一對一對映進新工作區。Mirror 能保留來源事實，但不能單獨證明來源就是可複用 Deck：建立時仍要識別穩定的應用規則。只得到身份時建立 Brand；得到品牌中立的可複用結構時建立 Layout；結構帶品牌身份，或者包含場景敘事與內容語法時建立 Deck。

這也約束建立模式：只有來源合同本身已經品牌中立且應用中立時，Layout mirror 才成立。刪除品牌色、字型、Logo、固定身份物件或可複用應用規則都屬於重新創作；越過這條邊界的來源要麼使用 `standard` / `fidelity` 創作新的 Layout，要麼保留這些事實並建立 Deck mirror。

---

## 二、各分類的 `design_spec.md` Schema

欄位集只規定**必須寫**的部分。「非必要不表明」——當前 schema 沒列出的欄位，不寫。

### Brand schema

**Frontmatter**

```yaml
---
brand_id: <slug>
kind: brand
summary: <一句话描述用途，含主色>
primary_color: "<HEX>"
---
```

**正文章節**（身份段全集）

| 節 | 標題 | 必寫欄位 |
|---|---|---|
| I | Brand Overview | Brand Name / Use Cases / Tone |
| II | Color Scheme | role / HEX / provenance（`fact` 官方真值 \| `approx` 推導）/ notes |
| III | Typography | role / family / weight |
| IV | Logo | file / form / usage + clearspace 與組合規則 |
| V | Voice & Tone | formality / person / emoji / abbreviation 策略 |
| VI | Icon Style | preference（stroke / filled / duotone …）+ 推薦字型檔 |

**不允許出現**：canvas viewBox、page types、SVG roster——這些是 layout 的職責。

### Layout schema

**Frontmatter**

```yaml
---
layout_id: <slug>
kind: layout
category: general | scenario | government | special
native_structure_mode: structured
summary: <一句话描述用途>
keywords: [tag1, tag2, tag3]
canvas_format: <ppt169 | ppt43 | a4 | ...>
canvas_width: <像素>
canvas_height: <像素>
canvas_viewbox: "0 0 <width> <height>"
source_canvas_width: <像素>       # 已知 PPTX/SVG 来源画布时填写
source_canvas_height: <像素>
source_viewbox: "0 0 <width> <height>"
replication_mode: standard | fidelity | mirror
page_count: <N>
page_types: [<cover, toc, chapter, content, ending, ...>]
---
```

**正文章節**（該包特有的結構段）

| 節 | 標題 | 必寫欄位 |
|---|---|---|
| IV | Signature Design Elements | 該 Layout 特有的網格、區域、圖片行為、密度節奏、中性框架、語義文字角色、對齊/換行/容量行為和 slot 約定 |
| V | Page Roster | 每個 SVG 檔案、Layout key、picker name、適用內容與 slot 行為 |

只有 Layout 改寫規範佔位詞彙時才增加 `Placeholder Overrides`。frontmatter
`summary` 承擔簡短的選型語境；Layout 不寫 deck 獨有的 Template Overview。

`category: scenario` 只表示發現時的適配標籤。Layout 可以針對某種內容形態或交付環境最佳化幾何，但不能規定溝通目的、受眾結果、必需敘事順序、固定措辭或示例內容；如果這些規則也要重複使用，應建立 Deck。

**不允許出現**：Color Scheme、品牌字型家族/字重身份、最終字號體系、品牌 logo、品牌 voice & tone、Icon Style 或官方真值色（`provenance: fact`）。Layout 可以保留語義文字角色、對齊、換行與容量規則，因為它們屬於結構；SVG 中性 paint、字型和字號只用於審閱。最終色彩與字型由策略師確認階段或其他模板 kind 解析。

### Deck schema

**Frontmatter**

```yaml
---
deck_id: <slug>
kind: deck
category: brand | general | scenario | government | special
native_structure_mode: structured
summary: <一句话描述可重复演示类型与预期结果>
keywords: [tag1, tag2, tag3]
canvas_format: <ppt169 | ...>
canvas_width: <像素>
canvas_height: <像素>
canvas_viewbox: "0 0 <width> <height>"
source_canvas_width: <像素>       # 已知 PPTX/SVG 来源画布时填写
source_canvas_height: <像素>
source_viewbox: "0 0 <width> <height>"
replication_mode: standard | fidelity | mirror
page_count: <N>
primary_color: "<HEX>"
---
```

**正文章節**（應用契約 + 一體化身份/結構）

| 節 | 標題 | 歸屬段 |
|---|---|---|
| I | Template Overview | 應用段 |
| II | Color Scheme | 身份段 |
| III | Typography | 身份段；只有使用共享預設字型棧時才省略 |
| IV | Signature Design Elements | 模板特有的身份圖形與可複用結構語法 |
| V | Page Roster | 結構段 |
| VI | Assets | 身份/支撐資產；無資產時省略 |
| VII | Placeholder Overrides | 結構詞彙；無覆蓋時省略 |

Template Overview 寫明可重複演示型別、目標受眾與結果、交付/閱讀假設及代表性敘事或頁面角色。Page Roster 只需如實描述每個原型的 Master/Layout/slot 合同、視覺特徵、用途和容量，不得新增必需/可選/可重複或固定/可替換/僅示例政策；當前 Strategist 會按實際內容推導這些決定。

可移植 canvas 欄位、`page_count` 和顯式 SVG roster 承載其餘結構合同。通用間距、字號比例、SVG 和 placeholder 規則保持集中管理，不復制進每個 deck spec。省略條件章節只表示“採用共享預設值或沒有資產”，不表示該段改由其他 kind 所有。

---

## 三、三套 index 檔案

每個 index 跟物理目錄一一對應，欄位按需精簡，沿用 [`charts_index.json`](../../skills/ppt-master/templates/charts/charts_index.json) 的緊湊“meta + summary”模式，同時保留對 Strategist 選型有用的結構化後設資料。

三套索引只覆蓋全域性庫範圍。專案根工作區有意不進入任何索引，仍可通過顯式 `projects/<name>/` 路徑使用。因為兩種範圍採用相同工作區形態，完整核心工作區可在兩者之間移動或複製，不需要重寫素材路徑；只有全域性庫註冊不同。

### `templates/brands/brands_index.json`

```json
{
  "<brand_id>": {
    "summary": "Anthropic brand identity — AI/LLM tech talks, developer conferences",
    "primary_color": "#D97757"
  }
}
```

- 保留 `primary_color` —— Strategist 選 brand 時第一眼就要知道主色
- 去掉 keywords —— summary 自帶英文等價詞，AI 用自然語言匹配（沿用 charts 經驗）

### `templates/layouts/layouts_index.json`

```json
{
  "<layout_id>": {
    "summary": "Standard academic defense layout — cover/toc/chapter/content/ending",
    "canvas_format": "ppt169",
    "page_count": 5,
    "page_types": ["cover", "toc", "chapter", "content", "ending"]
  }
}
```

- 加 `canvas_format` / `page_count` / `page_types` —— Strategist 選 layout 時要快速判斷"頁面骨架能不能裝下我的 deck"
- 無 `primary_color` —— layout 無身份

### `templates/decks/decks_index.json`

```json
{
  "<deck_id>": {
    "summary": "中国电信政企方案说明与下一步对齐汇报",
    "canvas_format": "ppt169",
    "page_count": 5,
    "primary_color": "#XXXXXX"
  }
}
```

- 含 `primary_color`（deck 自帶身份）+ 結構後設資料
- `summary` 優先描述可重複演示型別與預期結果，而不只是視覺氣質
- 詳細應用契約留在 Template Overview；緊湊索引不重複整份契約

---

## 四、多路徑合成與衝突解決

### 合成優先順序（隱式觸發）

使用者給出一組顯式工作區根目錄路徑後，Step 3 按以下表合成 `<project>/templates/design_spec.md`：

| 使用者路徑 | 合成行為 |
|---|---|
| 無 | 跳過 Step 3，走自由設計 |
| 只 brand | 複製 brand 全部，結構走自由設計 |
| 只 layout | 複製 layout 全部，身份走自由設計（策略師確認階段 e/f/g 決策） |
| 只 deck | 複製 deck 全部 |
| brand + layout | brand 提供身份段 + layout 提供結構段；這是專案內組合輸入，不是可複用 Deck 應用契約 |
| brand + deck | brand 段級覆蓋 deck 的身份段，結構段與應用段從 deck 拿 |
| layout + deck | 只有 layout 能表達 Deck 的必需敘事/內容角色時才覆蓋結構段；身份段與應用段從 deck 拿 |
| brand + layout + deck | brand 覆蓋身份 + 相容的 layout 覆蓋結構 + deck 提供應用段；身份/結構段的 deck 原值整段丟棄 |

Layout 覆蓋 Deck 前，必須把 Deck 應用契約與 Layout 的頁面角色、槽位型別和容量對照。如果必需角色無法表達，就把它作為合成衝突交給使用者：保留 Deck 結構、改選 Layout，或明確修改應用契約。不能保留一份當前結構無法兌現的場景承諾。

### 段級整段替換（預設粒度）

合成預設是**段級整段替換**——例如 deck + brand 時，整個 Color Scheme / Typography / Logo / Voice / Icon Style 五段從 brand 拿，**不做欄位級混搭**（即不會發生"primary 從 brand 拿、secondary 從 deck 拿"這類隱式混合）。

欄位級微調走 策略師確認階段這條已有路徑——使用者在 chat 裡說"用 anthropic brand，但 primary 改成 #FF0000"，由 Strategist 在 e/g 現場調整，不在 Step 3 的 fusion 層加欄位級語法。

### 同類多份 = git 衝突解決

使用者給 `brands/anthropic` + `brands/google`（同類多份的任意排列組合）：

```
AI: 你给了两个 brand，检测到段级冲突：
    - Color Scheme（Anthropic 橙红 vs Google 多色）
    - Typography（Styrene/AnthropicSans vs GoogleSans/Roboto）
    - Logo（Anthropic 标 vs Google 标）
    - Voice & Tone（restrained vs friendly）
    - Icon Style（stroke vs filled）

    要 (a) 全部按 Anthropic / (b) 全部按 Google / (c) 逐段挑？
```

- 預設無隱式順序，所有衝突都問
- 僅在使用者選 (c) 才進入逐段問答；不做欄位級衝突解決
- `layout × 2`、`deck × 2`、`brand × 2` 同處理
- 三類各最多兩份（再多讓使用者先在 chat 裡收斂）

### Provenance 記錄

合成後的 `<project>/templates/design_spec.md` 頂部必須加：

```markdown
> **Fused from:**
> - deck: `templates/decks/中国电信/` （base）
> - brand: `templates/brands/anthropic/` （identity 段覆盖）
> - layout: `templates/layouts/presentation_core/` （structure 段覆盖）
> - conflicts resolved: Color Scheme from anthropic（用户选 a）
```

讓 AI 和人類都能回溯每段來自哪。

---

## 五、與 Generate PPTX Step 3 的關係

**觸發規則仍以路徑為準**——仍需顯式工作區根目錄路徑（見 [Generate PPTX Step 3](../../skills/ppt-master/workflows/generate-pptx.md#step-3-template-option)），裸名稱絕不觸發。Step 3 先解析 `<workspace>/templates/design_spec.md`；為相容目錄形態，也接受根目錄直接包含 `<workspace>/design_spec.md` 的平鋪工作區，但其中 SVG 必須已經滿足當前合同。若包仍使用 `native_structure_mode: template`、缺 Master 身份、原子 placeholder 或蒸餾時代標記等舊語義，Step 3 必須拒絕；先由 `create-template` 產出新工作區，再繼續生成。唯一的窄例外是當前對話剛完成 `create-template`：驗證通過後可把精確的工作區根目錄直接交給 Step 3。`kind` 欄位決定**觸發後 AI 怎麼處理**：

| 使用者路徑指向 | Step 3 行為（按 kind 分支）|
|---|---|
| `kind: brand` | 把工作區 `templates/` 及實際存在的 `images/`、`icons/` 對映到專案同名目錄；忽略 `exports/` |
| `kind: layout` | 把工作區 `templates/` 及實際存在的 `images/`、`icons/` 對映到專案同名目錄；忽略 `exports/` |
| `kind: deck` | 把工作區 `templates/` 及實際存在的 `images/`、`icons/` 對映到專案同名目錄；忽略 `exports/` |
| 多路徑 | 按上表合成單份 `design_spec.md`，解決衝突後再合併實際存在的可移植目錄 |
| 同類多份 | 按上節"git 衝突解決"問答，得到合成結果 |

點陣圖統一進入工作區 `images/`，模板 SVG 通過 `../images/` 引用。如果顯式輸入根目錄本來就是目標專案根目錄，Step 3 原地消費：不得複製到自身，也不得再次移動素材。除此之外，完整核心工作區是可移植的：可以從專案根複製到全域性庫根、從全域性庫複製到專案，或從另一個工作區直接複用，而不改變內部結構。註冊是唯一與範圍相關的步驟。

### 策略師確認階段在不同 kind 下的行為

安裝模板不會讓溝通問題消失。Stage 1 始終獨立確認同一份開放式溝通契約。Brand 提供身份約束、結構仍然自由；Layout 提供結構能力；Deck 還提供描述性應用語境。Stage 1 之後，Strategist 會讀取真實原型和當前內容，生成一份頁面/原型計劃，只把 `mirror`、`layout` 或 `style` 記錄為內部匯出值。按 mirror 建立的工作區因此只提供原樣複用能力，不會強制使用；Confirm UI 不顯示模板模式欄位。規劃語義由 `references/strategist.md` 與 `references/strategist-template.md` 負責，機器結構由 `templates/schemas/spec_lock.schema.json` 負責。

---

## 六、與路線和子工作流的關係

| 路線或子工作流 | 產出 |
|---|---|
| `workflows/create-template.md` | 固定 Create Template 入口，以及範圍、確認、預檢、結構創作、註冊、完成和交接的共享合同；只分派一個子工作流 |
| `workflows/create-template/create-brand.md` | 僅身份的 Brand 工作區；無 SVG roster，空的可選目錄省略 |
| `workflows/create-template/create-layout.md` | 品牌中立、帶結構化 SVG roster 的 Layout 工作區 |
| `workflows/create-template/create-deck.md` | 應用契約與身份/結構一體化、帶結構化 SVG roster 的 Deck 工作區；可複用成果帶品牌身份或場景語義時選擇，不能只因來源是一份完整 PPTX 就預設選擇 |

在全域性庫範圍，frontmatter `kind` 欄位決定工作區父目錄位於 `templates/brands/` / `templates/layouts/` / `templates/decks/`。專案範圍在專案工作區根目錄保留同一 kind 語義。完整工作區可在兩種範圍之間移動而不改形，只需增加或移除全域性索引註冊。

---

## 七、不做（與本文 framing 配套的拒絕列表）

- **不在 fusion 層支援欄位級覆蓋語法** —— 欄位級微調走 策略師確認階段這條已有路徑
- **不為同類三份及以上設計批次衝突解決** —— 使用者先在 chat 裡收斂到兩份
- **不引入雙名對映表** —— 模板命名按其品牌/場景母語（中文模板用中文名，英文模板用 snake_case），不強制統一
- **不為輸出範圍新增結構分支或 CLI flag** —— 輸出範圍是 `create-template` 簡報裡的執行選擇；兩種範圍的 Layout/Deck 都宣告 `native_structure_mode: structured`
- **不增加第四種 Theme kind** —— Theme 投影 Brand、Deck 或當前專案解析後的身份，不是新的使用者側複用合同
- **不把 Brand + Layout 自動提升成可註冊的 Deck** —— 專案內組合可以按同時具備身份/結構能力來路由，但可複用 Deck 仍必須包含應用契約
