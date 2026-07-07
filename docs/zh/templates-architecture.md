# 模板架構：Brand / Layout / Deck 三分類

> 本文是**架構對齊檔案**，定義"模板"在資料模型層面的三種身份、各自的 `design_spec.md` 欄位集、以及多路徑合成與衝突解決規則。面向貢獻者與 AI 工作流，回答"一個模板目錄裡應該寫什麼、不寫什麼；多個模板同時給時怎麼合成"。
>
> 使用者視角的用法（怎麼觸發、怎麼選）見 [`templates-guide.md`](./templates-guide.md)；本文不重複。

---

## 一、三分類

| 分類 | 物理目錄 | 寫什麼 | 不寫什麼 | 出處工作流 |
|---|---|---|---|---|
| **Brand** | `templates/brands/<id>/` | 僅身份段：color / typography / logo / voice / icon style | 不寫 canvas、page structure、SVG roster | `workflows/create-brand.md` |
| **Layout** | `templates/layouts/<id>/` | 僅結構段：canvas / page structure / page types / SVG roster | 不寫品牌身份（無 logo、無品牌色硬約束） | `workflows/create-template.md`（layout 分支）|
| **Deck** | `templates/decks/<id>/` | 全段：身份段 + 結構段 + 中間段（template overview） | —— | `workflows/create-template.md`（deck 分支，預設）|

三者是**三種並列的 reference bundle**，物理目錄與 frontmatter `kind` 欄位雙向對齊：

```yaml
# templates/brands/anthropic/design_spec.md
---
kind: brand
...
---

# templates/layouts/academic_defense/design_spec.md
---
kind: layout
...
---

# templates/decks/招商银行/design_spec.md
---
kind: deck
...
---
```

### 三段的欄位切分

為了讓多路徑合成能幹淨覆蓋，所有欄位按段歸屬，**段級整段替換是預設粒度**：

| 段 | 包含的章節 | 歸屬（覆蓋優先順序）|
|---|---|---|
| **身份段** | Color Scheme / Typography / Logo / Voice & Tone / Icon Style | brand 覆蓋 |
| **結構段** | Canvas Specification / Page Structure / Page Types / SVG Roster | layout 覆蓋 |
| **中間段** | Template Overview（use cases / design intent / page rhythm 等敘事欄位）| deck 獨有；brand / layout 不寫 |

### 為什麼需要 Deck 這一類

Deck 是一份現存 PPT 的"復刻全息"——SVG 幾何為該套配色和字型畫的，身份與結構在原 PPT 裡已經實戰搭配。它的價值是「已驗證的整體感」，是 layout + brand 自由拼合未必能達到的成品。

但 Deck **不是"不可篡改的復刻"**——它是"作為預設底圖的復刻，可被顯式 brand / layout 覆蓋"。這給了使用者最大自由度：預設拿到一份完整方案，需要時顯式換身份或換結構。

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
summary: <一句话描述用途>
canvas_format: <ppt169 | ppt43 | a4 | ...>
page_count: <N>
page_types: [<cover, toc, chapter, content, ending, ...>]
---
```

**正文章節**（結構段全集 + Template Overview）

| 節 | 標題 | 必寫欄位 |
|---|---|---|
| I | Template Overview | Use Cases / Design Intent / Page Rhythm 建議 |
| II | Canvas Specification | Format / Dimensions / viewBox / Margins / Content Area |
| III | Page Structure | General Layout Grid / Decorative DNA / Navigation 規則 |
| IV | Page Types | 每種頁面的角色（cover / toc / chapter / content / ending …）與變體說明 |
| V | SVG Page Roster | 檔案清單 + 用途，每個檔案對應 III/IV 哪一類 |

**不允許出現**：品牌 logo、品牌 voice & tone、官方真值色（`provenance: fact`）——這些是 brand 的職責。Layout 自身沒有兜底色/字型（這是定義：layout 不寫身份段；色彩與字型在 策略師確認階段現場決策）。

### Deck schema

**Frontmatter**

```yaml
---
deck_id: <slug>
kind: deck
summary: <一句话描述用途>
canvas_format: <ppt169 | ...>
page_count: <N>
primary_color: "<HEX>"
---
```

**正文章節**（身份段全部 + 結構段全部 + 中間段）

| 節 | 標題 | 歸屬段 |
|---|---|---|
| I | Template Overview | 中間段 |
| II | Canvas Specification | 結構段 |
| III | Color Scheme（含 provenance）| 身份段 |
| IV | Typography | 身份段 |
| V | Logo | 身份段 |
| VI | Voice & Tone | 身份段 |
| VII | Icon Style | 身份段 |
| VIII | Page Structure | 結構段 |
| IX | Page Types | 結構段 |
| X | SVG Page Roster | 結構段 |

> Deck 是身份段 + 結構段全欄位的並集，無可選段。這樣合成時段級替換粒度統一。

---

## 三、三套 index 檔案

每個 index 跟物理目錄一一對應，欄位按需精簡（參照 [[project-charts-index-full-read-intentional]] 的"meta + summary"模式，但保留對 Strategist 選型有用的結構化後設資料）。

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
    "summary": "China Merchants Bank transaction banking deck",
    "canvas_format": "ppt169",
    "page_count": 5,
    "primary_color": "#XXXXXX"
  }
}
```

- 含 `primary_color`（deck 自帶身份）+ 結構後設資料
- 不展開 `page_types` —— deck 的頁面型別與 layout 的相同集合，不冗餘記錄

---

## 四、多路徑合成與衝突解決

### 合成優先順序（隱式觸發）

使用者在第一條訊息裡給出一組路徑，Step 3 按以下表合成 `<project>/templates/design_spec.md`：

| 使用者路徑 | 合成行為 |
|---|---|
| 無 | 跳過 Step 3，走自由設計 |
| 只 brand | 複製 brand 全部，結構走自由設計 |
| 只 layout | 複製 layout 全部，身份走自由設計（策略師確認階段 e/f/g 決策） |
| 只 deck | 複製 deck 全部 |
| brand + layout | brand 提供身份段 + layout 提供結構段，沿用 SKILL.md 現有 fusion 表 |
| brand + deck | brand 段級覆蓋 deck 的身份段，結構段與中間段從 deck 拿 |
| layout + deck | layout 段級覆蓋 deck 的結構段，身份段與中間段從 deck 拿 |
| brand + layout + deck | brand 覆蓋身份 + layout 覆蓋結構 + deck 提供中間段；身份/結構段的 deck 原值整段丟棄 |

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
> - deck: `templates/decks/招商银行/` （base）
> - brand: `templates/brands/anthropic/` （identity 段覆盖）
> - layout: `templates/layouts/academic_defense/` （structure 段覆盖）
> - conflicts resolved: Color Scheme from anthropic（用户选 a）
```

讓 AI 和人類都能回溯每段來自哪。

---

## 五、與 SKILL.md Step 3 的關係

**觸發規則不變** —— 仍然是「顯式目錄路徑才觸發」（見 [[feedback-template-explicit-path-only]]）。`kind` 欄位決定**觸發後 AI 怎麼處理**：

| 使用者路徑指向 | Step 3 行為（按 kind 分支）|
|---|---|
| `kind: brand` | design_spec + 非圖片資產 → `<project>/templates/`；logo / 插畫 / 圖示**點陣圖** → `<project>/images/` |
| `kind: layout` | design_spec + SVG roster → `<project>/templates/`；**點陣圖**資產 → `<project>/images/` |
| `kind: deck` | design_spec + 模板 SVG → `<project>/templates/`；logo / 背景 / 其它**點陣圖** → `<project>/images/` |
| 多路徑 | 按上表合成單份 `design_spec.md`；SVG 進 `templates/`、點陣圖進 `images/` 合併複製 |

> 點陣圖統一進專案 `images/`（和 AI / 網路 / 使用者圖片同一個執行期圖片池，SVG 裡走 `../images/`）；`templates/` 只放 spec 和模板 SVG 等供 Strategist/Executor 閱讀、不被直接渲染的參考材料。
| 同類多份 | 按上節"git 衝突解決"問答，得到合成結果 |

### 策略師確認階段在不同 kind 下的收窄

Deck 路徑下使用者已經拿到完整方案，策略師確認階段收窄到"目標受眾 / 頁數 / 大綱 / 調性微調"等 deck 內容相關欄位；其他欄位直接從鎖定值複用。具體收窄規則落在 `references/strategist.md` 與 `spec_lock_reference.md`。

---

## 六、與 workflows 的關係

| 工作流 | 產出 |
|---|---|
| `workflows/create-brand.md` | brand 目錄（identity-only），從品牌資產逆向提取 |
| `workflows/create-template.md` | layout 或 deck 目錄，內部按 kind 分支：預設走 deck（使用者給了一份現存 PPT，提取完整身份 + 結構）；使用者明說"只要結構 / 丟掉品牌色"時走 layout |

產出後 frontmatter `kind` 欄位決定檔案落到 `templates/brands/` / `templates/layouts/` / `templates/decks/`。

---

## 七、不做（與本文 framing 配套的拒絕列表）

- **不在 fusion 層支援欄位級覆蓋語法** —— 欄位級微調走 策略師確認階段這條已有路徑
- **不為同類三份及以上設計批次衝突解決** —— 使用者先在 chat 裡收斂到兩份
- **不引入雙名對映表** —— 模板命名按其品牌/場景母語（中文模板用中文名，英文模板用 snake_case），不強制統一
