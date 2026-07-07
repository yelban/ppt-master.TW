# Chart SVG Style Guide

> 本檔案定義了 `templates/charts/` 下所有 SVG 圖表模板的視覺規範。  
> 新增或修改圖表時 **必須** 遵循以下標準，確保全庫視覺一致性。

## 0. 上游規範引用

本檔案是 **圖表模板專用** 的美學與實現規範。所有圖表同時必須遵守專案級通用技術約束：

> **[`references/shared-standards.md`](../../references/shared-standards.md)** — SVG 停用特性黑名單、PPT 相容性替代、Canvas 格式、tspan 內聯規則、分組規範、陰影/疊加技術、後處理管線

以下章節摘錄了 shared-standards 中與圖表模板最密切相關的條目。完整細節（如 marker 條件約束、clipPath 條件約束、弧線路徑計算公式等）請查閱上游檔案。

---

## 1. 色彩系統 (Tailwind CSS Palette)

### 1.1 文本顏色

| 用途 | 色值 | Tailwind Token | 示例 |
|------|------|----------------|------|
| **主標題** | `#0F172A` | Slate 900 | 圖表大標題 |
| **數值標籤** | `#0F172A` | Slate 900 | 柱頂數值、關鍵指標 |
| **副標題** | `#64748B` | Slate 500 | 日期、單位說明 |
| **座標軸標籤** | `#64748B` | Slate 500 | X/Y 軸刻度值 |
| **軸標題 / 圖例** | `#475569` | Slate 600 | "年薪（萬元）"、圖例文字 |
| **資料來源** | `#94A3B8` | Slate 400 | 頁面底部來源說明 |
| **腳註 / 淡化提示** | `#CBD5E1` | Slate 300 | "各階段可靈活調整" |

### 1.2 主題色（資料系列）

| 色名 | 主色 | 深色（漸變終點） | 用途 |
|------|------|------------------|------|
| **Blue** | `#3B82F6` | `#2563EB` | 第 1 系列（預設首選） |
| **Emerald** | `#10B981` | `#059669` | 第 2 系列 |
| **Amber** | `#F59E0B` | `#D97706` | 第 3 系列 |
| **Violet** | `#8B5CF6` | `#7C3AED` | 第 4 系列 |
| **Rose** | `#FB7185` | `#E11D48` | 第 5 系列 / 警告 |
| **Pink** | `#EC4899` | `#BE185D` | 對比組（如蝴蝶圖女性） |

> 徑向漸變（如氣泡圖）使用亮色變體：`#60A5FA`、`#34D399`、`#FBBF24`、`#A78BFA`、`#FB7185`

### 1.3 語義色

| 用途 | 色值 | 說明 |
|------|------|------|
| 達標 / 正面 | `#10B981` | Emerald 500 |
| 警告 / 中性 | `#F59E0B` | Amber 500 |
| 未達標 / 負面 | `#EF4444` | Red 500 |
| 異常值標註 | `#F43F5E` | Rose 500 |

### 1.4 UI 輔助色

| 用途 | 色值 | 說明 |
|------|------|------|
| **座標軸線** | `#94A3B8` | Slate 400, stroke-width="2" |
| **網格線** | `#E2E8F0` 或 `#E0E0E0` | stroke-dasharray="4,4" |
| **中心分隔線** | `#CBD5E1` | 如象限十字線 |
| **卡片背景** | `#F8FAFC` / `#F8F9FA` | Slate 50 |
| **卡片描邊** | `#E2E8F0` | Slate 200 |
| **行分隔線** | `#F1F5F9` | Slate 100（極淡） |
| **Tint 背景**（藍） | `#EFF6FF` | Blue 50 |
| **Tint 背景**（綠） | `#ECFDF5` | Emerald 50 |
| **Tint 背景**（紅） | `#FFF1F2` | Rose 50 |
| **Tint 背景**（黃） | `#FFFBEB` | Amber 50 |

---

## 2. 排版規範

### 2.1 字型棧

```
font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang TC', 'Microsoft JhengHei', sans-serif"
```

- 純英文場景可省略 `'PingFang TC', 'Microsoft JhengHei'`
- **禁止** 使用 `@font-face`、外部字型、`<style>` 標籤

### 2.2 字號層級

| 層級 | 字號 | font-weight | 用途 |
|------|------|-------------|------|
| H1 | `34px` | `bold` (700) | 圖表主標題 |
| H2 | `22px` | `600` | 區域標題（如"詳細資料"） |
| Body L | `18-20px` | `600` | 關鍵數值、百分比 |
| Body M | `15-16px` | `600` | 資料標籤、分類名 |
| Body S | `14px` | 正常 | 副標題、圖例、來源 |
| Caption | `12-13px` | 正常 | 座標軸刻度、註釋 |

> **最小字號下限：12px**。所有文本不得小於 12px。

### 2.3 tspan 規範

所有 `<text>` 元素的文本內容 **必須** 包裹在 `<tspan>` 中：

```xml
<!-- 正确 -->
<text x="60" y="80" font-size="34" fill="#0F172A">
    <tspan>图表标题</tspan>
</text>

<!-- 错误 -->
<text x="60" y="80" font-size="34" fill="#0F172A">图表标题</text>
```

### 2.4 內聯格式化規則（shared-standards SS4）

**單邏輯行 = 單 `<text>`**。同一行內需要多色/多粗細時，用內聯 `<tspan>` 實現，**不要**用多個並排 `<text>`：

```xml
<!-- 正确：一个 text frame，三个 run -->
<text x="100" y="200" font-size="24" fill="#333333">
  实现<tspan fill="#3B82F6" font-weight="bold">10倍</tspan>效率提升
</text>

<!-- 错误：三个独立 text frame，PPT 中无法作为一行编辑 -->
<text x="100" y="200">实现</text>
<text x="160" y="200" fill="#3B82F6">10倍</text>
<text x="240" y="200">效率提升</text>
```

> 內聯 tspan **不得** 攜帶 `x` / `y` / `dy`，否則後處理會將其拆分為獨立 text frame。`dx` 可用於微調字距。

### 2.5 資料高亮預設行為

圖表中的關鍵資料文本應預設高亮：
- **數值結果** — 百分比、倍數、金額 → `<tspan fill="主题色" font-weight="bold">`
- **對比項** — 增/減、達標/未達標 → 語義色（綠/紅）
- **不高亮** — 連線詞、普通動詞、結構性文字（軸標籤、圖例、頁碼）

---

## 3. 陰影濾鏡

`<filter>` 本身是允許的、且是 PPT 陰影/發光的官方推薦路徑（詳見本節末尾的"停用列表"說明）。本節統一陰影 primitive 寫法——使用 `feFlood` 方案，**禁止** `<filter>` 內部使用 `<feComponentTransfer>`：

```xml
<filter id="chartShadow" x="-15%" y="-15%" width="130%" height="130%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="2-4"/>
    <feOffset dx="0" dy="1-3" result="offsetBlur"/>
    <feFlood flood-color="#0F172A" flood-opacity="0.08-0.15" result="shadowColor"/>
    <feComposite in="shadowColor" in2="offsetBlur" operator="in" result="shadow"/>
    <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>
```

### 引數參考

| 場景 | stdDeviation | dy | flood-opacity |
|------|-------------|-----|---------------|
| 重型元素（箭頭、卡片） | 4-6 | 2-4 | 0.12-0.15 |
| 中型元素（柱子、箱體） | 2-3 | 1-2 | 0.10-0.15 |
| 輕型元素（底部卡片） | 4-6 | 2-4 | 0.06-0.08 |

### 停用列表

- `flood-color="#000000"` → 必須用 `#0F172A`
- `<feComponentTransfer>` + `<feFuncA slope=...>` → 用 `<feFlood flood-color flood-opacity>` 替代
- `flood-opacity > 0.20` → 陰影過重，最大 0.15-0.20

> **被禁的是 sub-element，不是 `<filter>` 本身。** `<filter>` 是 PPT Master 允許的、官方推薦的陰影/發光路徑（見 [`shared-standards.md`](../../references/shared-standards.md) §1 黑名單不含 filter、§6 把 filter shadow 列為 drop-shadow 的官方實現），轉換器 [`svg_to_pptx/drawingml/styles.py`](../../scripts/svg_to_pptx/drawingml/styles.py) 也主動把 `feGaussianBlur` + `feOffset` + `feFlood` + `feComposite` + `feMerge`（以及 `feDropShadow` 簡寫）對映成 DrawingML `<a:outerShdw>`。
>
> 單獨禁 `feComponentTransfer/feFuncA(slope)` 的原因：**它物理上只能調透明度、無法攜帶顏色**。轉換器讀到 `feFuncA slope` 時只把它當作 alpha，顏色欄位保持預設 `'000000'`——SVG 端看起來陰影顏色正常（因為 SourceAlpha 本身是黑），但匯出到 PPTX 後陰影顏色會被定死成純黑 `#000000`，與同頁其他用 `feFlood flood-color="#0F172A"` 的卡片產生肉眼可見的冷暖色差。
>
> 簡言之：**用 filter 沒問題，但 primitive 必須能把"顏色"顯式表達出來；只能表達"透明度"的 primitive 是被禁的。**

### 陰影使用原則（shared-standards SS6）

> **陰影是美學成分，不是預設處理。** 剋制而非豐富才能產生"經過設計"的感覺。 "陰影被感知而非被看見" 是高階美學標準。

**應加陰影**：浮在照片/彩色面板上方的卡片、唯一的主 CTA、疊加層（tooltip、callout）

**不應加陰影**：背景面板/分隔條、網格中平等的同級卡片、已有描邊/漸變的容器、正文段落容器、裝飾線/圖示、深色背景上（黑色陰影不可見）

**每頁預算**：最多 2-3 個帶陰影元素。第 4 個需要陰影時，先移除現有某個的陰影。

**統一光源**：同頁所有 `feOffset` 的 `dx`/`dy` 方向必須一致（預設 `dx=0, dy=正值`，光從上方來）。

**兩級高度上限**：

| 層級 | 場景 | dy | stdDeviation | flood-opacity |
|------|------|----|--------------|---------------|
| 地面（無陰影） | 背景、同級網格卡片、分隔線、正文容器 | — | — | — |
| 靜止 | 照片/面板上的卡片、次級 callout | 2-4 | 4-8 | 0.06-0.10 |
| 抬升 | 主 CTA、焦點/推薦卡片、覆蓋層 | 6-10 | 10-16 | 0.12-0.20 |

**不要堆疊**：陰影 + 描邊 + 圓角 + 漸變填充同時出現 = 模板感。容器的"看我"預算很小，選其一即可。

---

## 4. 漸變規範

### 4.1 線性漸變（柱狀/條形圖）

```xml
<linearGradient id="barGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
    <stop offset="100%" style="stop-color:#2563EB;stop-opacity:1" />
</linearGradient>
```

- 方向：從亮到深（頂到底 或 左到右）
- 每個漸變 ID 應語義化：`barGrad1`、`leftGrad`、`actualBarBlue`

### 4.2 徑向漸變（氣泡圖）

```xml
<radialGradient id="bubbleGrad1" cx="30%" cy="30%">
    <stop offset="0%" style="stop-color:#60A5FA;stop-opacity:0.9" />
    <stop offset="100%" style="stop-color:#2563EB;stop-opacity:0.7" />
</radialGradient>
```

- 高光偏左上方 (`cx="30%" cy="30%"`)
- 邊緣 opacity 降低至 0.7，製造通透感

---

## 5. 結構規範

### 5.1 層級分組（shared-standards SS4 Grouping）

使用 `<g id="...">` 進行語義分組，便於 PPT 中逐個操作/動畫：

```xml
<g id="chartArea">        <!-- 图表主体 -->
    <g id="bar-1">...</g>  <!-- 每个数据元素独立分组 -->
    <g id="bar-2">...</g>
</g>
<g id="legend">            <!-- 图例区域 -->
    <g id="legend-high">...</g>
</g>
<g id="detailList">        <!-- 详情面板 -->
    <g id="list-items">
        <g id="item-1">...</g>
    </g>
</g>
```

**分組單元參考**（來自 shared-standards）：

| 分組單元 | 包含內容 |
|---------|---------|
| 卡片/面板 | 背景 rect + 陰影（如適用）+ 圖示 + 標題 + 正文 |
| 流程步驟 | 編號圓 + 圖示 + 標籤 + 描述 |
| 列表項 | 圓點/編號 + 圖示 + 標題 + 描述 |
| 圖示-文字組合 | 圖示元素 + 相鄰標籤 |
| 頁頭 | 標題 + 副標題 + 裝飾 |
| 裝飾叢集 | 相關裝飾形狀（環、球、點） |

**命名約定**：使用描述性 `id`（如 `card-1`、`step-discover`、`header`、`footer`）。

> 只有 `<g opacity="...">` 被禁止（見 SS2）。純結構 `<g>` 是必需的。

### 5.2 viewBox

固定為 `0 0 1280 720`（PPT 16:9），不可修改。

### 5.3 背景

首行始終為白色全屏背景：
```xml
<rect width="1280" height="720" fill="#FFFFFF"/>
```

### 5.4 資料來源

位於頁面底部，固定格式：
```xml
<text x="60" y="695" font-family="..." font-size="14" fill="#94A3B8">
    <tspan>数据来源: XXX</tspan>
</text>
```

---

## 6. SVG 停用特性與相容性（shared-standards SS1-2）

### 6.1 絕對禁止

| 停用特性 | 替代方案 |
|---------|---------| 
| HTML 命名實體（`&nbsp;` `&mdash;` `&copy;` `&ndash;` `&reg;` `&hellip;` `&bull;` …） | 直接寫原生 Unicode 字元（`—` `–` `©` `®` `→` NBSP …） |
| 文本/屬性值中裸寫 `& < > " '` | 必須寫成 XML 實體 `&amp;` `&lt;` `&gt;` `&quot;` `&apos;` |
| `<style>` / `class` | 內聯屬性（`id` 在 `<defs>` 內合法） |
| `<foreignObject>` | `<text>` + `<tspan>` |
| `mask` | 疊加遮罩矩形 / gradient overlay |
| `<symbol>` + `<use>` | 直接寫出完整元素 |
| `textPath` | 手動排列 `<text>` |
| `@font-face` | 系統字型棧 |
| `<animate*>` / `<set>` | 無（PPT 側處理動畫） |
| `<script>` / event 屬性 | 無 |
| `<iframe>` | 無 |

### 6.2 PPT 相容性替代

| 禁止語法 | 正確替代 |
|---------|----------|
| `fill="rgba(255,255,255,0.1)"` | `fill="#FFFFFF" fill-opacity="0.1"` |
| `<g opacity="0.2">...</g>` | 在每個子元素上單獨設定 `fill-opacity` / `stroke-opacity` |
| `<image opacity="0.3"/>` | 在 image 後疊加 `<rect fill="背景色" opacity="0.7"/>` |

### 6.3 條件允許

| 特性 | 條件 | 轉換結果 |
|------|------|----------|
| `marker-start` / `marker-end` | `<marker>` 在 `<defs>` 中，`orient="auto"`，形狀為三角/菱形/圓 | DrawingML `<a:headEnd>` / `<a:tailEnd>` |
| `clipPath` on `<image>` | `<clipPath>` 在 `<defs>` 中，單子元素，**僅用於 image** | DrawingML `<a:prstGeom>` / `<a:custGeom>` |
| `stroke-dasharray` | 使用預設值 `4,4` / `2,2` / `8,4` / `8,4,2,4` | PPTX `<a:prstDash>` |
| `text-decoration` | `underline` / `line-through` | PPTX 原生文本格式 |
| `transform="rotate(...)"` | 所有元素型別均支援 | PPTX `<a:xfrm rot="...">` |

> 完整條件約束見 [`shared-standards.md`](../../references/shared-standards.md) SS1.1（marker 約束）和 SS1.2（clipPath 約束）。

### 6.4 虛線預設對照

| SVG 值 | PPTX 預設 | 適用場景 |
|--------|-----------|---------|
| `4,4` | Dash | 通用虛線、分隔線 |
| `2,2` | Dot (sysDot) | 佔位輪廓、細邊框 |
| `8,4` | Long dash | 時間線連線、流程箭頭 |
| `8,4,2,4` | Long dash-dot | 技術圖紙、尺寸線 |

---

## 7. 舊色對映速查表

在維護舊模板時，使用以下對映快速替換：

| 舊色 (Material/Flat) | → | 新色 (Tailwind) | 角色 |
|----------------------|---|-----------------|------|
| `#2C3E50` | → | `#0F172A` | 主文本 |
| `#7F8C8D` | → | `#64748B` | 副文本 |
| `#5D6D7E` | → | `#475569` | 圖例文本 |
| `#95A5A6` | → | `#94A3B8` | 資料來源 |
| `#BDC3C7` | → | `#CBD5E1` | 淡化元素 |
| `#2196F3` / `#1976D2` | → | `#3B82F6` / `#2563EB` | 藍色系列 |
| `#4CAF50` / `#388E3C` | → | `#10B981` / `#059669` | 綠色系列 |
| `#FF9800` / `#F57C00` | → | `#F59E0B` / `#D97706` | 橙色系列 |
| `#E91E63` | → | `#F43F5E` | 異常值 |
| `#000000` (shadow) | → | `#0F172A` | 陰影底色 |

---

## 8. 佔位內容規範 (Placeholder Content Strategy)

既然這些 SVG 檔案是供 AI 後續呼叫的“模板”，它們的核心價值在於展示 **圖形結構、排版約束與視覺空間**，而不是傳遞真實的業務資料。因此，寫入模板的文本內容應遵循以下“佔位原則”：

### 8.0 全英文原則 (English-Only Rule)
**強制要求**：所有圖表模板中的佔位文本（包括標題、副標題、座標軸、圖例、資料節點、詳情描述及底部來源說明）**必須全部使用英文編寫**。
- **目的**：確保後續自動化管線中的 LLM 能夠更精準地進行語義理解和結構化內容對映，同時英文單詞的天然長度特徵更易於在模板中展示排版時的換行邏輯與空間邊界。

### 8.1 結構邊界演示
- **展示最大寬度/換行邏輯**：刻意使用典型長度的字串（如兩到三個詞的短語、多行 `tspan`）來明確展示文本框的邊界。這樣能確保 AI 填入真實文本時有直觀的參考，防止溢位。
- **展示資料格式**：使用能體現完整格式特徵的佔位數值（如 `$1,234.5M`、`98.5%`）而不僅是簡單的 `10`，以驗證符號和字元寬度是否適配。

### 8.2 通用性與中立性
- 使用通用、專業的商業佔位符，避免過於垂直或具象的特定業務資料（除非該模板本身具有強烈的行業屬性）。
- **推薦做法**：使用 `Category A`、`Q1 Revenue`、`Strategic Objective`、`Phase 01`。
- **避免做法**：使用具體的長篇現實資料（如“某某品牌2023年特種裝置銷量分析”）。

### 8.3 視覺平衡
- 佔位文本應當在視覺上保持圖表的平衡性（例如蝴蝶圖左右文本長度應大致相等，列表文本應長短錯落有致），以便讓人一眼看清圖表的佈局設計意圖。

---

## 9. 註冊到 charts_index.json

新增 SVG 模板後，**必須** 在 [`charts_index.json`](./charts_index.json) 中登記，否則 Strategist 選型時不會發現它。

### 9.1 欄位規範

```json
"<key>": {
  "summary": "Pick for <内容形态 + 规模>. Skip if <反例 → 替代模板>."
}
```

- **`key`** = SVG 檔名去掉 `.svg`，下劃線小寫（如 `bullet_chart`）
- **`summary`** 是**選型句**，不是描述句。語法見 `meta.summaryGrammar`：先說什麼時候選它，再用 `Skip if ... (use <other_key>)` 指向最容易混淆的兄弟模板
- **`meta.total`** 同步 +1

> **不需要** `label` / `categories` / `quickLookup` / `keywords` —— 這些都已經移除。Strategist 全量讀取 summary 列表後語義匹配，不依賴任何預計算索引。**注意**：summary 是英文，但 source 檔案常含中文/行業術語（"中臺"、"架構圖"、"管道"），Strategist 自己負責語義翻譯再匹配。如果一個模板的命中強依賴某個中文短語，把它的英文等價物寫進 summary 的 Pick 子句裡。

### 9.2 反例

❌ 只寫"是什麼"：`"summary": "Bidirectional comparison chart for two datasets"`
✅ 寫"何時選"：`"summary": "Pick for two mirrored datasets sharing a common axis (age pyramid, A/B). Skip for >2 sides (use grouped_bar_chart)."`

❌ summary 過長（>400 字元）—— 選型時反而難抓重點，目標在 150-300 字元。

> **Why not stricter**：單一結構模板常需覆蓋多個商業框架/場景（如 `quadrant_text_bullets` 覆蓋 SWOT + Ansoff，`top_down_tree` 覆蓋 org + OKR），summary 需要列出關鍵詞錨點（"principles, key takeaways, action items" 這種）才能讓 Strategist 語義命中"非數字結構頁"，所以 100-180 字元的舊基線在結構-派命名後已經太緊。

---

## 10. 檢查清單

新增或修改圖表後，逐項檢查：

### 基礎校驗
- [ ] `xmllint --noout` 通過
- [ ] viewBox 為 `0 0 1280 720`
- [ ] 首行為白色背景 `<rect width="1280" height="720" fill="#FFFFFF"/>`

### 色彩
- [ ] 無舊色殘留（`grep` 驗證，見下方命令）
- [ ] 陰影 `flood-color` 為 `#0F172A`，opacity 小於等於 0.20
- [ ] 資料來源用 `#94A3B8`

### 排版
- [ ] 無 `font-size < 12` 的文本
- [ ] 所有 `<text>` 內容包裹 `<tspan>`
- [ ] 同一行多格式用內聯 `<tspan>`，**非**多個並排 `<text>`
- [ ] 內聯 `<tspan>` 不攜帶 `x` / `y` / `dy`
- [ ] 標題 34px、副標題 18px、來源 14px

### 結構
- [ ] 主要元素有語義化 `<g id="...">`
- [ ] 無 `<style>`、`class`、`<foreignObject>`、`mask`、`rgba()`
- [ ] `<g>` 標籤無 `opacity` 屬性
- [ ] 文本字元為原生 Unicode（`—` `©` `→` NBSP 等），無 HTML 命名實體（`&nbsp;` `&mdash;` `&copy;` 等）；裸 `& < >` 已轉義為 `&amp; &lt; &gt;`

### 陰影
- [ ] 使用 `feFlood` 方案（非 `feComponentTransfer`）
- [ ] 同頁陰影 `dx`/`dy` 方向一致
- [ ] 每頁帶陰影元素不超過 3 個

### 註冊（僅新增模板時）
- [ ] `charts_index.json` 的 `charts.<key>` 已登記 `summary` 欄位
- [ ] `summary` 寫成選型句（`Pick for ... Skip if ... (use <other>)`），不是描述句
- [ ] `summary` 長度控制在 150-300 字元（>400 字元要重寫）；如果模板覆蓋多個商業框架/場景，可放寬到 350 字元以塞下關鍵詞錨點
- [ ] `meta.total` 同步 +1

### 座標校準標記（calculator-supported 圖表必填）
- [ ] 矩形座標系圖表（bar / horizontal_bar / grouped_bar / stacked_bar / line / area / stacked_area / scatter / waterfall / pareto / butterfly）包含 `<!-- chart-plot-area: x_min,y_min,x_max,y_max -->` 標記
- [ ] Pie / donut / radar 圖表包含 `<!-- chart-plot-area: <type> | center: cx,cy | radius: r -->` 標記
- [ ] 標記位於 `<g id="chartArea">` 內、座標軸之後、資料元素之前
- [ ] 座標值與軸線的實際 SVG 座標一致

### 驗證命令
```bash
# 一键校验
f="your_chart.svg"
xmllint --noout "skills/ppt-master/templates/charts/$f" && echo "XML OK" || echo "XML FAIL"
echo "Old colors:" && grep -c '#2C3E50\|#7F8C8D\|#95A5A6\|#5D6D7E\|#000000' "skills/ppt-master/templates/charts/$f"
echo "Small fonts:" && grep -c 'font-size="[0-9]"' "skills/ppt-master/templates/charts/$f"
```

---

## 11. 卡片容器圖式 (Card Container Patterns)

容器卡是 PPT Master 中複用率最高的視覺單元（KPI 卡、分割槽卡、資訊卡）。下面三種圖式是經過驗證、與 PPTX 往返相容的"參考實現"，新增模板優先沿用，不要發明等價但實現髒的替代。

### 11.1 半圓角分割槽頭 (Half-Rounded Section Tab)

**用途**：給卡片或區塊加一個有色"標籤頭"，標識分類（S/W/O/T、Political/Economic、自我介紹/獲獎等）。比純文字大標題更易識別，比獨立標籤條更緊湊。

**兩種形態**——根據 tab 的"視覺錨點"在上還是在下選擇：

| 形態 | 形狀 | 視覺語義 | 典型場景 |
|------|------|---------|---------|
| **上圓下方** (圓頂角) | 頂部兩角圓，底部兩角直 | 從卡片"長出來"的標籤 | 分割槽卡頭部、quadrant 標題、資訊卡分類 |
| **上方下圓** (圓底角) | 頂部兩角直，底部兩角圓 | 從頁頭/章節條"懸掛下來"的吊牌 | 章節錨點、頁頭分隔條延伸、目錄跳轉標記 |

> 兩種形態的共同要求：**只圓一對角**，整條 path 直接畫出來。不要用"全圓角矩形 + 同色矩形蓋底/蓋頂"的 hack（往返到 PPTX 時會變成兩個獨立物件，編輯時顏色容易脫鉤）。

**實現一：上圓下方（預設）**

```xml
<!-- 模板：宽 W、高 H、圆角 R，左上原点 (x, y) -->
<path d="M {x+R} {y} h {W-2R} a {R} {R} 0 0 1 {R} {R} v {H-R} h -{W} v -{H-R} a {R} {R} 0 0 1 {R} -{R} Z"
      fill="#2563EB"/>

<!-- 实例：240×50, r=25, 起点 (245, 140) -->
<path d="M 245 140 h 190 a 25 25 0 0 1 25 25 v 25 h -240 v -25 a 25 25 0 0 1 25 -25 Z" fill="#2563EB"/>
```

**實現二：上方下圓（懸掛吊牌）**

```xml
<!-- 模板：宽 W、高 H、圆角 R，左上原点 (x, y) -->
<path d="M {x} {y} h {W} v {H-R} a {R} {R} 0 0 1 -{R} {R} h -{W-2R} a {R} {R} 0 0 1 -{R} -{R} Z"
      fill="#2563EB"/>

<!-- 实例：240×50, r=25, 起点 (245, 140) -->
<path d="M 245 140 h 240 v 25 a 25 25 0 0 1 -25 25 h -190 a 25 25 0 0 1 -25 -25 Z" fill="#2563EB"/>
```

**停用反例**（PEST/SWOT/comparison_columns 舊實現中常見）：

```xml
<!-- ❌ 不要这样写：用全圆角矩形 + 白色矩形覆盖一边圆角 -->
<rect width="260" height="120" rx="12" fill="#EFF6FF"/>
<rect y="100" width="260" height="20" fill="#EFF6FF"/>
```

底部覆蓋矩形在 SVG→PPTX 往返時會變成一個獨立的、跟頭部顏色繫結的矩形物件，PPT 裡編輯頭部顏色時容易漏改、視覺會"穿幫"。

### 11.2 巢狀卡片描邊 (Nested Card Border)

**用途**：讓卡片有"被描邊"的層次感，但避免 stroke。stroke 在 PPTX 中常被渲染為細線分層，且與陰影疊加易產生模板感。

**做法**：外層淺灰圓角 rect + 內層白色稍小圓角 rect，兩層之間留出 8–20px 縫即可形成"邊框"效果。

```xml
<!-- 外层"边框"层 -->
<rect x="60" y="140" width="560" height="255" rx="20" fill="#F1F5F9"/>
<!-- 内层白色内容卡（内缩 20px，半径变小） -->
<rect x="80" y="210" width="520" height="165" rx="12" fill="#FFFFFF"/>
```

**適用條件**：
- 當卡片上方還有 §11.1 的分割槽頭時，外層框充當頭部的"背板"
- 同頁只用 **一種** 描邊表達：外層框 OR stroke OR 陰影，不要同時用（參見 §3 陰影使用原則）

### 11.3 卡片網格作為內容頁骨架 (Card Grid as Page Skeleton)

**用途**：當一頁要並列展示 4 個平等的方面（pillar / aspect / quadrant），優先用 2×2 網格而非垂直疊加。

**網格尺寸建議**（1280×720 畫布）：

| 網格 | 單卡寬 × 高 | 間距 | 起始 (x, y) |
|------|-------------|------|-------------|
| 2×2 | 560 × 255 | 40 | (60, 140) (660, 140) (60, 420) (660, 420) |
| 2×3 (橫) | 370 × 260 | 25 | (50, 130) 行距 290 |
| 1×3 (橫長) | 400 × 540 | 30 | (60, 130) 列距 430 |
| 1×4 (頂) | 280 × 250 | 20 | (60, 150) 列距 300 |

**判定**："4 個並列方面" → 2×2；"3 個並列方面" → 1×3；"6 個能力點" → 2×3；"4 個關鍵指標" → 1×4。`page_rhythm` 標 `breathing` 的頁面 **不要** 用卡片網格（見 executor-base.md §2.1）。

### 11.5 傾斜虛線連線箭頭 (Diagonal Dashed Connector)

**用途**：表達"跨象限/跨層級"的關係——優先順序遷移、影響傳導、虛線彙報、對角趨勢。水平/垂直箭頭表達的是"流程進度"，傾斜虛線箭頭表達的是"關係或方向引導"，兩者語義不一樣。

**做法**：單條 `<line>` + `stroke-dasharray="6 5"` + `marker-end`。需要為這條線單獨定義一個 marker（不復用主流程圖的箭頭顏色，建議用 Slate 600 `#475569` 表達"建議性、非強制"的色調）。

```xml
<defs>
  <marker id="migrationArrow" markerWidth="12" markerHeight="12"
          refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
    <path d="M 0,0 L 10,6 L 0,12 Z" fill="#475569"/>
  </marker>
</defs>

<!-- 从 Q4 (右下) 指向 Q2 (左上) 的优先级迁移箭头 -->
<line x1="850" y1="605" x2="385" y2="200"
      stroke="#475569" stroke-width="2"
      stroke-dasharray="6 5" stroke-linecap="round"
      marker-end="url(#migrationArrow)"/>

<!-- 中段标签：白底胶囊压在箭头上，避免视觉打架 -->
<rect x="525" y="385" width="190" height="28" rx="14"
      fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
<text x="620" y="403" text-anchor="middle" font-size="12"
      font-weight="700" fill="#475569" letter-spacing="1">PRIORITY MIGRATION</text>
```

> **配對要求**：每條傾斜虛線箭頭必須配一箇中段標籤（小膠囊或一行文字），否則讀者會困惑"這條線在說什麼"。無標籤的箭頭只允許出現在水平/垂直流程中（如 `process_flow`）。

### 11.6 接地橢圓 (Ground Anchor Ellipse) — 非 filter 的深度表達

**用途**：讓"漂浮在卡片上的圓形/icon/人物頭像/獎盃/角色徽章"獲得"接觸地面"的視覺錨定，**但不使用 `<filter>` 陰影**。

**為什麼有用**：
1. PPTX 原生圓/橢圓物件，跨渲染器一致，不會被解析為 `<a:outerShdw>`（避免陰影顏色丟失或重排問題）
2. 跟 §3 「剋制陰影」呼應——一頁陰影預算上限 2-3 個，剩下需要"深度"的元素可以走這條路
3. 比 filter 陰影**更容易在 PPT 中二次編輯**（使用者可以直接拖、改色、刪除）

**做法**：在浮動元素**正下方**畫一個**橫扁橢圓**（`ry << rx`），低透明度，顏色用主體色或 Slate 900：

```xml
<!-- 头像/徽章下方的接地阴影板，cy 比头像底边低 10-15px -->
<ellipse cx="80" cy="172" rx="70" ry="5" fill="#0F172A" opacity="0.10"/>
<!-- 然后再画头像本体（顺序很重要，椭圆必须先画） -->
<circle cx="80" cy="80" r="80" fill="#E2E8F0"/>
```

**引數參考**：

| 浮動元素半徑 | 橢圓 rx | 橢圓 ry | opacity |
|-------------|---------|---------|---------|
| 30-50 px | r × 0.85 | 3-4 | 0.10-0.15 |
| 50-100 px | r × 0.85 | 5-6 | 0.10-0.12 |
| 100+ px | r × 0.85 | 7-9 | 0.08-0.10 |

顏色：預設 `#0F172A`（中性深灰），可改為主體色的深色變體（如人物頭像下用 `#1E3A8A`）表達"品牌色陰影"。

**停用**：不要把橢圓畫成正圓或近正圓（`ry/rx > 0.25` 就顯得失真）。也不要疊在`<filter>` 陰影上——挑一種就夠。

### 11.7 雙向互動箭頭 (Bidirectional Interaction Arrows)

**用途**：表達"請求/響應"、"推/拉"、"上行/下行"、"供給/需求"等成對關係。區別於單向流程箭頭。

**做法**：兩條平行的 `<line>` + 不同顏色的 `marker-end`，方向相反，**每條線都必須帶動作標籤**：

```xml
<defs>
  <marker id="reqArrow" markerWidth="10" markerHeight="10" refX="9" refY="5"
          orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L10,5 L0,10 Z" fill="#3B82F6"/>
  </marker>
  <marker id="respArrow" markerWidth="10" markerHeight="10" refX="9" refY="5"
          orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L10,5 L0,10 Z" fill="#10B981"/>
  </marker>
</defs>

<!-- 请求：左到右，蓝色 -->
<line x1="380" y1="250" x2="926" y2="250" stroke="#3B82F6" stroke-width="2.5"
      marker-end="url(#reqArrow)"/>
<rect x="500" y="216" width="280" height="26" rx="11" fill="#FFFFFF"
      stroke="#3B82F6" stroke-width="1"/>
<text x="640" y="234" text-anchor="middle" font-size="14" font-weight="700"
      fill="#3B82F6">① Login Request · POST /auth/login</text>

<!-- 响应：右到左，绿色 -->
<line x1="926" y1="290" x2="384" y2="290" stroke="#10B981" stroke-width="2.5"
      marker-end="url(#reqArrow)"/>
<!-- ...同样配标签... -->
```

**配色約定**：請求側（initiator）用藍色 `#3B82F6`、響應側（responder）用綠色 `#10B981`。如果是對等關係（如 A↔B 協同），統一用 Slate 600 `#475569` 不區分顏色。

**停用**：不允許畫"裸線"——雙向箭頭**每條都必須帶標籤**說明動作；否則讀者無法分辨方向語義。

### 11.8 參考實現

| 圖式 | 參考模板 |
|------|---------|
| §11.1 半圓角分割槽頭（上圓下方） | `quadrant_text_bullets.svg`, `labeled_card.svg`, `vertical_pillars.svg`, `comparison_columns.svg` |
| §11.2 巢狀卡片描邊 | `labeled_card.svg` |
| §11.3 2×2 卡片網格 | `kpi_cards.svg`, `quadrant_text_bullets.svg`, `labeled_card.svg` |
| §11.3 2×3 卡片網格 | `icon_grid.svg` |
| §11.3 1×3/1×4 卡片網格 | `comparison_columns.svg`, `vertical_pillars.svg` |
| §11.5 傾斜虛線連線箭頭 | `matrix_2x2.svg` |
| §11.6 接地橢圓 | `team_roster.svg` |
| §11.7 雙向互動箭頭 | `client_server_flow.svg` |

