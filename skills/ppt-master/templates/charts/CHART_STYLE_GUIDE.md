# Chart Template Authoring Guide

`templates/charts/` 的模板負責視覺化結構、資料編碼和資訊關係，不負責最終專案風格。模板必須保持原始碼可讀、獨立可渲染，並允許 Executor 根據專案 Design Spec 與 `spec_lock.md` 重做字型、配色和裝飾。

## 0. 上游規範

**Hard rule**: 本指南只定義 Chart 模板庫的結構與中性預覽合同。通用 SVG 語法、效果、原生資料介面和 PowerPoint 結構分別由以下權威檔案定義：

| 合同 | 權威檔案 |
|---|---|
| 通用 SVG | [`shared-standards.md`](../../references/shared-standards.md) |
| 效果與相容輸入 | [`svg-effects.md`](../../references/svg-effects.md) |
| Native Chart/Table | [`native-data-interface.md`](../../references/native-data-interface.md) |
| 畫布格式 | [`canvas-formats.md`](../../references/canvas-formats.md) |

**Forbidden — second SVG specification**: 不在本指南複述或放寬上游語法。發生衝突時以上游權威檔案為準。

---

## 1. 所有權邊界

### 1.1 模板與專案

| Chart 模板擁有 | 專案擁有 |
|---|---|
| 視覺化型別與資料到圖形的對映 | 專案字型與字號體系 |
| 節點、連線、軸、系列和標籤關係 | 專案調色盤與品牌色 |
| 視覺化型別、構圖骨架和閱讀順序 | 實際分組、框架數量、專案數量與容量適配 |
| 必要的狀態與語義區分 | 頁面背景、頁頭、頁尾和品牌 chrome |
| 獨立預覽所需的中性樣式 | 最終強調策略與頁面級視覺層級 |

**Hard rule**: Executor 適配模板時保留視覺化型別、資訊關係和資料準確性；最終視覺必須來自當前專案，而不是繼承模板的示例審美。

**Reference — not a constraint**: 模板的分組、框架數、專案數和示例容量用於展示結構，不是專案上限。Executor 可按實際內容調整，但不能改變已選視覺化型別、關係或資料語義。

### 1.2 保留判斷

對每個視覺元素按順序判斷：

| 判斷 | 處理 |
|---|---|
| 刪除後會改變資料含義、關係、狀態或閱讀順序 | 保留 |
| 刪除後會弱化分組、層級、邊界或文本容量 | 保留結構表達；只簡化不承載資訊的樣式層 |
| 只讓示例顯得更精緻、立體、品牌化或“高階” | 作為簡化候選；通過文本與前後渲染核對後再刪除 |
| 只對某個專案風格成立 | 交給 Executor 重建 |

**Default — structure first (may override when semantics require it)**: 優先使用清楚的線、面、標籤和留白。裝飾不能成為理解結構的前提。

### 1.3 保真優先

**Hard rule — fidelity before slimming**: 模板瘦身不得改寫或刪除原有可見標題、標籤、說明、數值、單位、狀態、來源、順序、容量和關係。佔位內容保持原文；只有明確重複的資訊可以刪除，並記錄理由。

**Hard rule — structural frames survive**: 框線、底色、分隔、標籤頁或面板只要表達真實的資訊單元、父子層級、階段範圍、繪圖區或輸出區，就屬於結構。可以減少疊加效果，但不得為了 token 數字把有效層級壓平。

**Forbidden — compression by rewriting**: 不用縮寫、概括、換詞或刪句降低 token。體積最佳化來自屬性繼承、重複樣式合併和非語義效果簡化，不來自內容編輯。

---

## 2. 中性預覽

### 2.1 獨立可渲染

**Hard rule**: 每個模板保持完整 `<svg>`、`viewBox="0 0 1280 720"` 和一個直接的白色全畫布背景，使檔案無需外部樣式即可開啟審閱。

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="1280" height="720"
     font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang TC', 'Microsoft JhengHei', sans-serif">
    <rect width="1280" height="720" fill="#FFFFFF"/>
    <!-- semantic content -->
</svg>
```

白色背景是預覽基線，不是專案背景指令。Executor 必須按當前頁面風格處理最終背景。

### 2.2 中性參考色

以下色值只保證模板獨立展示時清晰。它們不是最終專案調色盤：

| 角色 | 中性參考值 | 使用邊界 |
|---|---|---|
| 主文本 | `#0F172A` | 標題、關鍵值 |
| 正文 | `#475569` | 描述、圖例 |
| 次文本 | `#64748B` | 軸標籤、輔助說明 |
| 弱線 | `#CBD5E1` / `#E2E8F0` | 網格、邊界、分隔 |
| 參考強調 | `#2563EB` | 第一系列、當前狀態或結構焦點 |
| 正向語義 | `#059669` | 僅表示上升、完成、達標 |
| 負向語義 | `#E11D48` | 僅表示下降、異常、未達標 |
| 警示語義 | `#D97706` | 僅表示風險或待處理 |

**Hard rule**: 多系列資料必須可區分；正負、完成/計劃等語義狀態必須可辨認。顏色承擔這些資訊時保留，顏色只承擔裝飾時移除。

**Forbidden — fixed catalog palette**: 不要求每個卡片、步驟或能力點使用不同 Tailwind hue。專案配色不從模板示例反向推導。

### 2.3 頁面 chrome

| 元素 | 模板行為 |
|---|---|
| 標題/副標題 | 可用簡短佔位文本展示層級和可用空間；不附帶裝飾條、徽章或品牌圖形 |
| 資料來源 | 僅當該視覺化結構需要來源/腳註槽時保留；不是每個模板的固定頁尾 |
| 頁碼、Logo、部門名 | 省略 |
| 進度徽章、狀態膠囊 | 只有狀態本身屬於資訊時保留，移除純裝飾外殼 |

---

## 3. 裝飾與效果

### 3.1 減少冗餘效果

**Default — one clear treatment (may override when structure requires depth)**: 中性模板避免陰影、發光、紋理、漸變和多層框同時疊加；保留能幫助讀者識別真實邊界、重疊或空間關係的最少效果。

| 效果 | 預設 | 允許條件 |
|---|---|---|
| 陰影/filter | 有描邊或底色已能分組時省略 | 重疊、浮層或空間深度本身屬於結構 |
| 漸變 | 只承擔審美時可換成實色 | 連續色階、流量、深度面或方向確實承載編碼 |
| 透明光暈 | 省略 | 透明度本身編碼範圍或不確定性 |
| 圓角卡片 | 保留真實資訊單元的一層邊界 | 圓角值與最終外觀由專案適配 |
| 圖示底板 | 非預設 | 需要明確圖示槽位或狀態邊界 |

**Hard rule**: Heatmap 色階、Sankey 流量寬度、系列區分、Isometric 面向關係和真實模組邊界屬於資訊編碼或結構。普通卡片陰影、氣泡高光、無含義色帶和不承擔順序的大號淡色編號通常不屬於；刪除前仍需確認沒有弱化層級。

### 3.2 容器剋制

**Hard rule**: 每個真實資訊單元保留至少一種清楚的邊界表達：留白、分隔線、描邊或底色。通常只需一種；父級區域與子級內容確實表達兩個層級時可以保留兩層。不要同時疊加無語義的描邊、陰影、漸變和多層圓角框。

**Reference — not a constraint**: 專案最終可能採用強裝飾風格。那是 Executor 根據 Design Spec 重建的專案決策，不是共享模板的預設形態。

---

## 4. 原始碼可讀性與體積

### 4.1 語義壓縮

**Hard rule**: 縮小模板時保留正常換行、縮排、語義 `id` 和必要分割槽註釋。壓縮目標是減少重複資訊，不是把 XML 變成一行。

| 做法 | 要求 |
|---|---|
| 字型繼承 | 公共 `font-family` 放在根 `<svg>` 或清楚的父 `<g>` |
| 屬性繼承 | 同組重複的 `fill`、`stroke`、字號或錨點可提升到父組 |
| 註釋 | 保留結構、語義和機器標記；刪除色名、營銷解釋和重複說明 |
| 文本 | 普通單行直接寫在 `<text>`；只有多 run/多行需要 `<tspan>` |
| 座標 | 頁面座標使用必要精度；按上游合同執行 `compact_svg_coordinates.py` |
| ID | 使用 `chart-area`、`series-1`、`card-1` 等結構名稱，避免示例業務名 |

### 4.2 禁止的壓縮

**Forbidden — opaque source**:

- 單行 minify、隨機縮寫 ID 或刪除結構註釋。
- 為省字元把核心構圖拆成難以追蹤的深層 `<symbol>/<use>` 圖。
- 把模板必要資訊藏進外部 CSS、指令碼或未登記依賴。
- 用 Base64、壓縮字串或生成器說明替代可讀的可視幾何。

靜態同文檔 `<use>` 只在重複原語保持清晰、且滿足上游條件合同時使用；它不是預設瘦身手段。

### 4.3 文本可讀性

| 角色 | 中性範圍 |
|---|---|
| 頁面標題 | `30–36`，`700–800` |
| 區域標題 | `18–24`，`600–700` |
| 正文/標籤 | `13–16` |
| Caption/軸刻度 | `12–14` |

**Hard rule**: 所有文本 `font-size >= 12`，使用有限無單位數值。需要成為一個 PowerPoint 文本框的多格式邏輯行使用一個 `<text>` 加非定位 `<tspan>`；獨立文本框使用獨立 `<text>`。

---

## 5. 結構與邊界

### 5.1 語義分組

**Hard rule**: 使用描述性頂層 `<g id>` 表達頁面級邏輯單元，例如 Header、Chart、Legend、Card Grid 或 Process。不要為每條文字、圖示或資料點建立一個直屬根組。

| 頂層組 | 典型內容 |
|---|---|
| `header` | 標題與副標題 |
| `chart-area` / replacement carrier | 軸、資料系列、標籤、必要 metadata |
| `legend` | 系列或狀態說明 |
| `card-1` / `feature-card-1` | 一個完整資訊單元 |
| `timeline-track` | 時間軸與階段標籤 |
| `milestone-cards` | 同一結構的一組裡程碑卡片 |

### 5.2 `data-pptx-bounds`

**Hard rule**: 每個可見直屬根 `<g>` 都宣告正數、根座標系的 `data-pptx-bounds="x y width height"`。即使該組已有 native chart/table frame，也保留 bounds。

```xml
<g id="header" data-pptx-bounds="60 40 1160 72">
    <text x="60" y="74" font-size="32">Title</text>
</g>

<g id="card-1" data-pptx-bounds="60 150 560 250">
    <!-- complete card -->
</g>
```

| 邊界要求 | 行為 |
|---|---|
| 座標系 | 使用根 `viewBox` 座標，不使用區域性 transform 後坐標 |
| 範圍 | 覆蓋該邏輯單元允許使用的佈局子畫布，不從示例文字緊包圍盒推斷 |
| 精度 | 最多兩位小數 |
| 巢狀組 | 不寫；Checker 忽略巢狀 bounds |
| 背景/defs | 直接背景 primitive 與非可見定義不需要 bounds |

**Forbidden — bounds noise**: 不給每個巢狀 `<g>`、圖示、資料點或實現碎片新增 bounds。

### 5.3 Shape-first

| 物件 | 模板表達 |
|---|---|
| 基礎節點/容器 | `<rect>`、`<circle>`、`<ellipse>` |
| 直線關係/分隔/引線 | `<line>` |
| 預設可精確表達的彎折/曲線關係 | 完整 compact authored `bentConnector*` / `curvedConnector*` `<g>`；端點不附著 |
| 標準塊箭頭/流程節點 | 僅在 preset 精確匹配時使用完整 compact authored-preset `<g>` |
| 單一預設不能表達、但封閉形狀可組合的物件 | 優先用 `shape_boolean_svg.py` 物化 Merge Shapes 結果 |
| 圖元、預設、Boolean 都不能表達的資料/語義/鎖定風格幾何 | `<path>`、`<polygon>`、`<polyline>` |
| 資料圖表 | 預設 Shape fallback；符合條件時附帶 native replacement marker |

**Forbidden — inferred native semantics**: 概念圖、流程圖和框架圖不新增 `data-pptx-replace-with="chart"`；普通關係線不新增 Connector attachment metadata。

---

## 6. 資料圖表合同

### 6.1 繪圖區標記

**Hard rule**: calculator-supported 資料圖表在 `<g id="chartArea">` 內、軸之後、首個資料元素之前保留精確機器註釋：

```xml
<!-- chart-plot-area: 140,150,1160,550 -->
```

Pie、Donut、Radar 使用對應中心和半徑格式。該註釋是工具輸入，不得作為“清理註釋”刪除。

### 6.2 Native Chart/Table

**Hard rule**: 只有 [`native-data-interface.md`](../../references/native-data-interface.md) 支援的真實資料圖表或純文本表格使用 replacement marker。JSON metadata 與可見 fallback 必須表達同一份資料。

```xml
<g id="line-chart"
   data-pptx-bounds="100 140 1080 460"
   data-pptx-replace-with="chart">
    <metadata type="application/json">...</metadata>
    <g id="chartArea">...</g>
</g>
```

**Hard rule**: 專案顏色適配時同步修改可見系列顏色和 metadata `style.colors`。預設 Shape 輸出與顯式 native 輸出都必須可驗證。

### 6.3 資料裝飾邊界

| 元素 | 分類 |
|---|---|
| 軸、刻度、網格、圖例 | 結構 |
| 系列顏色、正負語義色 | 資料編碼 |
| 資料點節點 | `lineMarker` 等型別需要時保留 |
| Area fill | 面積/累計量是資訊時保留；普通 line chart 僅在確認填充不承擔範圍、基線或強調含義後簡化 |
| 柱體漸變、節點高光、卡片陰影 | 只承擔審美時可簡化；若用於區分重疊、層級或狀態則保留結構作用 |
| 來源與註釋 | 內容需要時保留，不作為全庫固定 chrome |

---

## 7. 佔位內容與註冊

### 7.1 佔位內容

**Hard rule**: 模板佔位文本使用英文，展示真實文本容量和資料格式，但不承載具體專案事實。

| 應展示 | 示例 |
|---|---|
| 標題長度 | `Revenue Trend`、`Implementation Plan` |
| 資料格式 | `$245.5M`、`98.5%`、`2026 Q1` |
| 正常換行 | 2–3 行短描述 |
| 結構容量 | 真實建議數量範圍內的 series/items/nodes |

**Forbidden — placeholder storytelling**: 不寫長篇營銷文案、部門歸屬、真實品牌或無法複用的專案背景。

### 7.2 `charts_index.json`

新增模板必須登記 `<key>.summary`：

```json
"line_chart": {
  "summary": "Pick for 1-3 time-series on a continuous axis showing direction. Skip if cumulative volume matters (use area_chart)."
}
```

**Hard rule**: `summary` 是選型句，使用 `Pick for ... Skip if ...`，不是視覺描述；`key` 與檔名一致，`meta.total` 與 catalog 數量一致。

---

## 8. 遷移邊界

本指南是新建和修改模板的目標合同。當前目錄中的 76 個 SVG 均已納入該合同；後續不得以歷史檔案為由恢復無語義裝飾，也不得把中性化誤解為刪除結構邊界。

**Current reference set**:

| 模板 | 覆蓋結構 |
|---|---|
| `timeline.svg` | 時間、狀態和里程碑卡片 |
| `kpi_cards.svg` | KPI 值、單位與趨勢 |
| `labeled_card.svg` | 2×2 標籤卡片結構 |
| `icon_grid.svg` | 2×3 圖示槽與能力卡片 |
| `line_chart.svg` | 雙系列折線與 native chart metadata |
| `pipeline_with_stages.svg` | 分階段管線、貫通流程和輸出鏈 |
| `layered_architecture.svg` | 分層架構、能力輸出和底座 |
| `stacked_area_chart.svg` | 累計面積、圖例和統計卡片 |
| `heatmap_chart.svg` | 時間×日期矩陣、連續色階和統計側欄 |
| `bubble_chart.svg` | 三變數氣泡、象限、系列清單和尺寸圖例 |
| `quadrant_text_bullets.svg` | 二軸四象限、分割槽說明和行動標籤 |
| `financial_statement_table.svg` | 財務層級、數值列和強調合計行 |
| `box_plot_chart.svg` | 五數分佈、異常值、圖例和統計摘要 |
| `dual_axis_line_chart.svg` | 雙軸序列、階段帶和資料標註 |
| `stacked_bar_chart.svg` | 堆疊分類、總量標籤和洞察側欄 |
| `segmented_wheel.svg` | 中心主題、等權扇區和配對說明卡 |
| `sankey_chart.svg` | 零損耗流向、節點層級和流量編碼 |
| `roadmap_vertical.svg` | 縱向里程碑、狀態軌道和目標側欄 |
| `snake_flow.svg` | 多行蛇形長流程、順序節點和配對里程碑卡 |
| `concentric_circles.svg` | 同心優先順序、資源佔比和分層說明卡 |
| `scatter_chart.svg` | 雙系列散點、迴歸趨勢、置信區間和統計洞察 |
| `area_chart.svg` | 雙系列累計面積、月度趨勢和摘要指標 |
| `chevron_process.svg` | 連續階段箭頭、週期帶和階段交付物 |
| `radar_chart.svg` | 多維能力對比、系列面積和基準資料表 |
| `module_composition.svg` | 父模組邊界、三級處理鏈和端到端資料流 |
| `fishbone_diagram.svg` | 核心問題、六類原因分支和具體成因標籤 |
| `numbered_steps.svg` | 編號步驟、連線順序、任務卡和階段時長 |
| `pareto_chart.svg` | 80/20 分界、降序柱體、累計曲線和行動洞察 |
| `top_down_tree.svg` | 父子層級、彙報連線和末級節點摘要 |
| `butterfly_chart.svg` | 共用中軸、雙側映象系列和對稱刻度 |
| `chevron_chain_with_tail.svg` | 連續箭頭階段、支撐標籤和結果彙總尾塊 |
| `gauge_chart.svg` | 單項指標、目標區間、當前值和狀態說明 |
| `gantt_chart.svg` | 任務行、時間跨度、依賴關係和當前時間標記 |
| `waterfall_chart.svg` | 起始值、增減貢獻、連線基線和最終合計 |
| `hub_inward_arrows.svg` | 外圍輸入、向心關係和中心結論 |
| `treemap_chart.svg` | 層級面積編碼、分類色塊、標籤和解釋註記 |
| `hub_spoke.svg` | 中心樞紐、徑向連線、能力節點和參考環 |
| `matrix_2x2.svg` | 雙軸象限、點位分佈、象限標籤和優先順序說明 |
| `process_flow.svg` | 順序節點、連線關係、階段時長和狀態圖例 |
| `donut_chart.svg` | 環形佔比、中心總值、系列圖例和摘要指標 |
| `grouped_bar_chart.svg` | 多系列並列柱、共用分類軸和系列圖例 |
| `pyramid_isometric.svg` | 分層金字塔、等距深度面和層級說明 |
| `progress_bar_chart.svg` | 多項進度、目標標記、當前值和狀態分組 |
| `basic_table.svg` | 表頭、資料行、對齊列和狀態單元格 |
| `mind_map.svg` | 中心主題、放射分支、二級節點和分支骨架 |
| `comparison_columns.svg` | 並列方案列、價格層級、功能清單和推薦狀態 |
| `bullet_chart.svg` | 定性區間、實際值、目標線和多指標對照 |
| `comparison_table.svg` | 多方案表頭、橫向屬性行和結果強調 |
| `client_server_flow.svg` | 客戶端與服務端分割槽、請求響應和互動方向 |
| `dumbbell_chart.svg` | 雙狀態端點、變化連線、差值和專案排序 |
| `pyramid_chart.svg` | 遞進層級、分層容量和層級說明 |
| `vertical_pillars.svg` | 並列支柱、分類標題、要點列表和底部結論 |
| `journey_map.svg` | 階段軌道、使用者行動、情緒曲線和痛點卡片 |
| `consulting_table.svg` | 分層行列、指標數值、資料條和重點結論 |
| `pros_cons_chart.svg` | 正反雙欄、判斷軸、論據列表和建議結論 |
| `project_schedule_table.svg` | 任務表格、負責人、狀態和橫向排期 |
| `horizontal_bar_chart.svg` | 長標籤排名、橫向數值條和洞察側欄 |
| `funnel_chart.svg` | 遞減階段、轉化率、流失關係和摘要指標 |
| `isometric_stairs.svg` | 遞進臺階、階段標籤、空間順序和接地基線 |
| `pie_chart.svg` | 單層佔比、扇區標籤、圖例和總量摘要 |
| `circular_stages.svg` | 環形階段、迴圈方向、階段說明和中心主題 |
| `team_roster.svg` | 成員卡片、頭像槽、姓名職務和簡介容量 |
| `harvey_balls_table.svg` | 評價行列、分級圓點、評分圖例和彙總狀態 |
| `column_chart.svg` | 單系列分類柱、數值標籤、座標軸和基準線 |
| `arc_anchored_list.svg` | 弧線主軸、錨點節點、順序條目和配對說明 |
| `vertical_list.svg` | 縱向軌道、順序節點、內容卡片和階段狀態 |
| `sunburst_chart.svg` | 多層環形層級、父子佔比、葉子圖例和解釋面板 |
| `agenda_list.svg` | 編號議程、條目說明、時長資訊和縱向導軌 |
| `stock_chart.svg` | OHLC 蠟燭、日期軸、價格區間和指標摘要 |
| `feature_matrix_table.svg` | 功能行、產品列、二元狀態和方案對照 |
| `histogram_chart.svg` | 連續分箱、頻數柱、統計標記和分佈解釋 |
| `venn_diagram.svg` | 集合邊界、交集區域、關係標籤和結論說明 |
| `quadrant_bubble_scatter.svg` | 雙軸象限、氣泡位置、尺寸編碼和專案標籤 |
| `bar_of_pie_chart.svg` | 主餅佔比、長尾聚合、堆疊條明細和連線關係 |
| `pie_of_pie_chart.svg` | 主餅佔比、長尾聚合、次級餅明細和連線關係 |
| `word_cloud.svg` | 詞項權重、字號編碼、主題分佈和關鍵詞層級 |

**Hard rule**: 修改任一模板時先凍結可見文本、資料和結構層級，再簡化確認無語義的效果、補齊直屬根 bounds，並完成文本差異、獨立渲染與雙路線驗證。未經明確說明的文本刪除、改寫或結構邊界丟失都會阻斷變更。不要僅為追求 catalog 一次性整齊而批次重寫。

---

## 9. 檢查清單

### 9.1 結構與可讀性

- [ ] SVG 獨立可渲染，`viewBox` 為 `0 0 1280 720`。
- [ ] 原始碼有正常縮排、語義 ID 和必要結構註釋。
- [ ] 原有可見文本、數值、單位、來源、狀態和關係保持不變；刪除項只有稽核過的重複資訊。
- [ ] 真實資訊單元、父子層級、階段範圍和輸出區仍有清楚邊界。
- [ ] 每個可見直屬根 `<g>` 有準確的 `data-pptx-bounds`；巢狀組不濫加 bounds。
- [ ] 模板只保留結構、資料編碼和必要中性預覽。
- [ ] 字型在根或清楚父組繼承，文本字號不小於 12。

### 9.2 風格歸屬

- [ ] 無固定專案調色盤、品牌字型或品牌 chrome。
- [ ] 純裝飾效果已減少，但沒有以“去裝飾”為由刪除結構框線或壓平層級。
- [ ] 顏色差異確實表達 series、state、positive/negative 等語義。
- [ ] 標題、副標題和來源只用於展示必要結構或容量。

### 9.3 資料與 PowerPoint

- [ ] 資料圖表保留準確 `chart-plot-area` 標記。
- [ ] Eligible Chart/Table 的 metadata 與可見 fallback 資料一致。
- [ ] 預設 Shape-first 匯出通過。
- [ ] 存在 replacement marker 時，顯式 native Chart/Table 匯出通過。
- [ ] `svg_quality_checker.py` 無 error；warning 已人工判斷。

### 9.4 Catalog

- [ ] 新模板已登記 `charts_index.json`。
- [ ] 修改 key/summary 後通過 `chart_recall.py validate` 和 recall 煙測。
- [ ] 前後可見文本差異已審閱，非重複內容沒有意外丟失或改寫。
- [ ] 前後渲染對比確認結構仍可讀。
- [ ] 記錄 bytes/tokens 變化，但不以犧牲原始碼可讀性換取數字。

---

## 10. 驗證命令

```bash
# 单文件 SVG 合同
python3 skills/ppt-master/scripts/svg_quality_checker.py \
  skills/ppt-master/templates/charts/<key>.svg

# Catalog key
python3 skills/ppt-master/scripts/chart_recall.py validate <key>

# 可安全压缩的页面坐标（默认 dry-run）
python3 skills/ppt-master/scripts/compact_svg_coordinates.py \
  skills/ppt-master/templates/charts/<key>.svg
```

**Validation**: 修改後至少完成 XML 解析、獨立 SVG 渲染、Checker、預設 Shape-first 匯出，以及 marker 模板的 native Chart/Table 匯出。

---

## 11. 結構圖式相容索引

本節保留舊引用錨點，但所有圖式都受 §1 所有權邊界約束。

### 11.1 Attached Section Tab

**Reference — not a constraint**: 半圓標籤只在“標籤從屬於當前資訊塊”是結構資訊時使用。顏色、圓角和高度由專案適配；它不是卡片的預設裝飾。

**Forbidden — cover hack**: 不把“全圓角矩形 + 同色覆蓋矩形”作為兩個未合併物件疊放來偽造單側圓角。需要時優先以封閉的圓角矩形和矩形為 operands，通過 `shape_boolean_svg.py` 物化 Union 結果；只有 Boolean 仍不能忠實表達時才手寫可編輯 path。

### 11.2 Nested Card Border

**Default — single boundary (may override when hierarchy requires two levels)**: 中性模板優先一層描邊或留白。淺色外框 + 內層白卡屬於舊視覺配方，不再作為共享模板預設；只有外層與內層表達兩個真實層級時才保留。

### 11.3 Card Grid

卡片網格表達並列關係和容量，不決定最終卡片風格：

| 結構 | 典型容量 | 參考畫布分配 |
|---|---|---|
| 2×2 | 4 個平行方面/KPI | `560×255`，橫向間距約 40 |
| 2×3 | 6 個能力/服務 | `370×260`，橫向間距約 25 |
| 1×3 | 3 個平行支柱 | 每列約 `400×540` |
| 1×4 | 4 個緊湊指標 | 每列約 `280×250` |

**Hard rule**: `page_rhythm: breathing` 不因 catalog 示例自動變成卡片網格；最終結構仍服從頁面內容和專案節奏。

### 11.5 Diagonal Relationship Arrow

**Hard rule**: 傾斜虛線箭頭只表達跨象限遷移、影響或建議方向，並配一條簡短關係標籤。顏色與標籤外觀由專案決定。

### 11.6 Ground Anchor

**Default — omit (may override when depth is semantic)**: 接地橢圓是深度裝飾，不屬於中性模板預設。只有物體與地面/層級的空間關係本身有意義時保留；不得為了“漂浮感”普遍新增。

### 11.7 Bidirectional Interaction Arrows

**Hard rule**: 雙向關係使用兩條方向明確的線，每條線都有動作標籤。請求/響應的顏色只需可區分，最終對映由專案調色盤決定。
