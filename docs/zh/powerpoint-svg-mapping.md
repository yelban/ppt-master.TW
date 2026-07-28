# PowerPoint 功能 ↔ 專案 SVG 對映指南

[English](../powerpoint-svg-mapping.md) | [Chinese](./powerpoint-svg-mapping.md)

---

## 目的與權威邊界

本指南從 PowerPoint 使用者的視角回答一個問題：**對於某項 PowerPoint 功能，專案中由什麼表達承載，匯出或回導時能保留什麼？** 因此，PowerPoint 語義是唯一主索引，SVG 元素只作為某項 PowerPoint 能力的具體實現出現。

這是一份公開的能力與匯入行為對映表，不是第二份生成 SVG 語法規範，也不承諾轉換任意 SVG 或任意 OOXML。規範生成合同由 [`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 路由到拆分權威集；生成語法出現差異時，以適用模組為準。PPTX 匯入的容錯模式與使用者可見降級由本文 §11 和[轉換命令檔案](../../skills/ppt-master/scripts/docs/conversion.md)負責，精確 parser 行為仍以實現程式碼為真值。本指南未列出的功能不會因此被預設為受支援。

主路線編譯的是**專案規範化 SVG**，而不是通用瀏覽器 SVG：

```text
PowerPoint 意图
    ↔ 项目规范化 SVG 或显式 sidecar
    ↔ DrawingML / PPTX 包语义
```

有些 PowerPoint 功能沒有誠實的 SVG 等價表達。對於這些功能，本指南會明確標為 sidecar/打包層功能、直接 PPTX 保留功能或不支援，而不是強行塞進裝飾性 SVG metadata。

## 如何閱讀表格

每行只對應一項 PowerPoint 能力。對映的基數不一定是一個物件對一個物件：一個 SVG 文本節點可能生成多個 PowerPoint run，一個原生圖表 marker 組可能收斂為一個 `p:graphicFrame`，一個匯入的 PowerPoint 物件也可能重建為多個 SVG 元素。

| 術語 | 含義 |
|---|---|
| `Native-stable` | 在檔案化邊界內，匯出使用對應的可編輯 DrawingML 屬性或物件。 |
| `Native-normalized` | 匯出結果仍可編輯，但源表達會被歸一化為等價的 DrawingML 結構。 |
| `Approximate` | PowerPoint 沒有完全對應的能力；效果具有實質意義時必須複核生成的 PPTX。 |
| `Bake-required` | 必須預渲染為圖片，或使用受支援的顯式幾何重建。 |
| `Sidecar/package` | 該能力屬於專案 sidecar 或 PPTX 打包器，而不是 SVG 頁面設計。 |
| `Direct preservation` | 直接 PPTX 工作流可以保留源 OOXML；主 SVG 編譯器不重建它。 |
| `Unsupported` | 主生成路線沒有已登記對映，不得猜測。 |

下文中的“回導”是指 PPTX-to-SVG 路線生成的語義投影，不是恢復原始 SVG 語法或補造缺失設計意圖。它不承諾原始 `<defs>` 圖、`<use>` 結構、path 命令或 `<tspan>` 排版。

## 1. 簡報、幻燈片與座標模型

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 簡報頁面尺寸 | 根 SVG `viewBox="0 0 W H"`，通過專案畫布合同選擇 | 簡報寬高；96 DPI 下 `1 SVG px = 9,525 EMU` | `Native-stable`；回導的自定義 PPTX 尺寸可使用相容的正小數 | 數值必須有限、原點為零且尺寸為受支援的正值；所有公開頁和內部 Layout 原型必須匹配鎖；禁止根 transform |
| 幻燈片 | 一個完整的 `svg_output/<slide>.svg` 頁面 | 一個 `p:sld` 及其 relationships | 重建為一張完整 SVG 頁面 | SVG 是可見頁面權威；備註和包行為單獨承載 |
| 物件位置與尺寸 | SVG 絕對座標與元素邊界 | `a:xfrm` 偏移和範圍 | 經座標換算後為 `Native-normalized` | 數值必須有限，並使用已登記座標語法 |
| Z 順序 | SVG 原始碼順序，由後到前 | PowerPoint shape tree 順序 | 按 shape tree 順序重建 | 不得依賴瀏覽器專屬堆疊行為 |
| 旋轉、縮放、平移與映象 | 受支援的 SVG transform 形式 | DrawingML transform 或歸一化幾何 | `Native-normalized`；matrix 可能被分解 | 已登記 transform 合同以外的傾斜與錯切不可接受 |
| 主題顏色與字型 | `spec_lock.md` 鎖定的角色；規範 SVG 使用解析後的值 | 當精確匹配鎖定角色時保留 theme token，否則寫直接 DrawingML 值 | 已登記角色為 `Native-stable` | 新頁面不得自行發明未鎖定顏色、字型或字號 |
| PowerPoint 包身份 | `spec_lock.md` 結構宣告與打包器 | Presentation、Master、Layout、relationship 與 content type 註冊 | 從包結構讀回，不從頁面外觀推斷 | 最終包讀回必須與宣告的 roster 一致 |

受支援的畫布見 [`canvas-formats.md`](../../skills/ppt-master/references/canvas-formats.md)，根 `viewBox` 的規範合同見 [`shared-standards-core.md` §4.1](../../skills/ppt-master/references/shared-standards-core.md#41-semantic-svg-marker-contract)。

## 2. Master、Layout、背景與佔位符功能

**路線邊界**：主 SVG 流程中的自由生成與 brand-only 專案從規劃到匯出始終使用 `pptx_structure.mode: flat`；`flat` 不是等待匯出器自動升級的臨時狀態。即使多個頁面出現相同 Logo、頁尾或排版，匯出器也不得據此切換到 `structured`，不得自動提升到 Master/Layout，也不得推斷佔位符或去重。若輸出需要可複用的原生 Master、Layout 或佔位符，Step 3 必須消費一個已校驗的 deck/layout 模板工作區；沒有該工作區時，先走 [`create-template`](../../skills/ppt-master/workflows/create-template.md)，再返回主流程。flat 匯出建立的最小 Master 和 Blank Layout 只是 PPTX 格式必需的包結構，不是從頁面總結出的設計母版。直接使用原始 PPTX 模板填充新內容仍走 [`template-fill-pptx`](../../skills/ppt-master/workflows/template-fill-pptx.md)。

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 自由設計簡報結構 | `pptx_structure.mode: flat`；頁面內容保持 Slide-local | 一個乾淨的專案 Master 和一個 Blank Layout，已表達物件留在 Slide | flat 路線包拓撲為 `Native-stable` | 禁止編寫 Master/Layout/layer/placeholder metadata |
| 基於模板的簡報結構 | `pptx_structure.mode: structured` 加顯式 Master/Layout/頁面分配 | 宣告的 `p:sldMaster`、`p:sldLayout`、註冊與 Slide 父子關係 | 在顯式結構合同內為 `Native-stable` | 匯出器絕不猜測 Master、Layout 或佔位符拓撲 |
| 幻燈片母版 | 根 Master 身份加原子級 `data-pptx-layer="master"` 物件；一個校驗通過的 compact authored-preset `<g>` 計為一個 semantic atom | 可複用 Master part 與 picker 身份 | Create Template mirror 可把來源包中已驗證的事實保留到新工作區；創作模式使用新身份 | Master atom 必須為直接、穩定物件，並在所屬頁面間一致；普通組或 expanded authored 組不具備該資格 |
| 幻燈片版式 | 根 Layout 身份加原子級 `data-pptx-layer="layout"` 物件；一個校驗通過的 compact authored-preset `<g>` 計為一個 semantic atom | 某個 Master 下的可複用 Layout part | Create Template mirror 可把已驗證的源 Layout 保留到新工作區；Strategist 的 adaptive 計劃可宣告新 Layout | 僅當固定 atom 和 slot 合同完全相同時才複用 Layout key；普通組或 expanded authored 組不具備該資格 |
| 回導的繼承圖形可見性 | 分層分析記錄規範化源布林值；物化後的 structured mirror 在根寫入精確小寫的 `data-pptx-show-inherited-shapes` 與 `data-pptx-show-master-shapes` | 把已宣告來源值寫入 `p:sld@showMasterSp` 與 `p:sldLayout@showMasterSp` | `Native-stable`：Slide 為 false 時隱藏 Layout 與 Master 圖形；Layout 為 false 時只隱藏 Master 圖形 | 省略即 true；使用同一 Layout key 的頁面必須使用相同 Layout 值。背景、Slide-local 物件、佔位符繼承、part 與父子關係保持不變 |
| strict 模板 Layout | 選中的原型合同 | 保留現有已宣告 Layout 拓撲 | 頁面遵循原型時為 `Native-stable` | 不得改變固定 Layout atom 和 slot 結構 |
| adaptive 模板 Layout | 選定 Master 加 Strategist 顯式宣告的當前或新 Layout | 可複用結構變化時建立已宣告的新 Layout 身份 | Strategist 更新計劃與 lock 對映、執行恢復後為 `Native-stable` | 製作中發現變化須退回上游；絕不在下游改變已複用 Layout key |
| structured 模式以外的 Slide 背景填充 | 第一個合格的全幅 `<rect>`，可直接位於根下或位於簡單單子組中，使用已登記純色、線性/徑向漸變或預設圖案填充 | Slide 的原生 `p:bg` | 保真度遵循下文對應 paint 行 | transform、filter、clip、圓角、可見 stroke 或未對映 fill 會阻止提升 |
| structured 模式的 Master/Layout/Slide 背景填充 | 宣告結構層中一個直接鋪滿畫布的純色 `<rect>` | Master、Layout 或 Slide 層級的原生 `p:bg` | `Native-stable` | 顯式 scoped background 所有權有意只支援純色 |
| structured 模式的漸變或圖案背景形狀 | 宣告在 Master/Layout 層的普通漸變/圖案 `<rect>`，或 Slide-local 內容 | 所屬 part 上的可編輯 shape | 保真度遵循下文對應 paint 行 | structured 匯出關閉通用背景提升；不得使用 `data-pptx-layer="slide"` |
| 圖片背景 | 宣告在 Master/Layout 層的普通專案 `<image>`，或 Slide-local 內容 | 所屬 part 上的可編輯 `p:pic` | 保真度遵循下文 picture 對應行 | image 元素絕不提升為 `p:bg` |
| 標題佔位符 | 含一個文本 carrier 的結構化 slot 組 | Layout 和 Slide 的 `title` 型別 `p:ph` | `Native-stable` | carrier 數量、邊界、型別與有效 index 必須與 Layout 合同一致 |
| 副標題佔位符 | 含一個文本 carrier 的結構化 slot 組 | `subTitle` 型別 `p:ph` | `Native-stable` | 與標題相同的 slot 規則 |
| 正文佔位符 | 含一個文本 carrier 的結構化 slot 組 | `body` 型別 `p:ph` | `Native-stable` | 多行 carrier 仍必須是一個文本框 |
| mirror 回導文本佔位符的 Slide frame | slot 的 `<text>` carrier 保留正數源 `data-pptx-frame="x y width height"`，並與 slot 的可複用 bounds 分開 | Slide carrier 保持該精確 `a:xfrm`；文字仍可編輯，源硬換行保留為顯式段落 | 在受支援回導文本範圍內為 `Native-stable` | `data-pptx-bounds` 仍只定義 Layout 預設 frame，二者可以不同；standard/fidelity 創作不得為複製 bounds 而新增此 frame |
| 日期、頁尾與頁碼佔位符 | 結構化文本 slot | `dt`、`ftr` 與 `sldNum` 型別 `p:ph`，帶匹配的 Layout 頁首/頁尾標誌 | `Native-stable` | 佔位符 index 必須唯一且合法 |
| 圖片佔位符 | 含一個圖片或受支援 crop carrier 的結構化 slot | `pic` 型別 `p:ph` | 在圖片合同內為 `Native-stable` | slot 必須恰好含一個相容的直接 carrier |
| 圖表或表格佔位符 | 含一個匹配原生物件 carrier 的結構化 slot | `chart` 或 `tbl` 型別 `p:ph` | 僅原生 Chart/Table 匯出時為 `Native-stable` | 需要合法 JSON metadata 與 `--native-charts-and-tables` |
| 通用物件佔位符 | 一個相容 carrier（可為一個校驗通過的 compact authored-preset `<g>`），或顯式複合 proxy binding | `obj` 型別 `p:ph` | 原生 binding；複合可見內容仍為普通 shape | 複合 slot 必須使用已登記 proxy 降級方案；expanded authored 組不能作為單物件 carrier |
| 媒體佔位符 | 一個圖片或受支援 crop carrier | `media` 型別 `p:ph` | 僅為原生佔位符 binding | 不會從裝飾性 SVG 內容生成影片或音訊 |
| 空文本佔位符 | 空或僅空白的已標記 text carrier | 使用合法 1 pt 下限的不可見 U+200B run，生成一個原生文本 shape | `Native-stable` | 不得新增假破折號、小於 1 pt 的文字或與背景同色的可見字元 |
| cover/content/ending 等頁面角色 | flat 路線根 `data-pptx-page-role` 編譯提示 | 路由/校驗提示；不是 PowerPoint 原生頁面型別 | 沒有獨立 OOXML 物件 | structured 頁面改用顯式 Master/Layout 身份 |
| 幻燈片節與自定義放映 | 無 SVG 對映 | 主生成路線不編寫 | 當源保留工作流擁有該語義時為 `Direct preservation` | 不得編碼為可見 metadata |

精確的結構 metadata 與 slot 語法見 [PPTX 結構介面](../../skills/ppt-master/references/pptx-structure-interface.md#1-pptx-structure-routing)。

內部識別符號與 PowerPoint 顯示名稱是兩件事：Master 和 Layout key 使用專案受限 ASCII 識別符號語法，picker 名稱可以含空格。每個 Layout 定義還必須指定父 Master 與一個顯式原型來源。精確行語法由 PPTX 結構介面擁有。

## 3. PowerPoint 形狀與繪圖物件

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 矩形 | `<rect>` | 可編輯 `p:sp` 與 `a:prstGeom prst="rect"` | `Native-stable`；可能時回導為原語 | 僅使用已登記 paint、line 與 transform 屬性 |
| 對稱圓角矩形 | 圓角半徑相等且受支援的 `<rect>` | `a:prstGeom prst="roundRect"` 加 adjustment | `Native-stable` | 不對稱圓角按 freeform 行處理 |
| 圓或橢圓 | `<circle>` 或 `<ellipse>` | `a:prstGeom prst="ellipse"` | `Native-stable` | 需要時，bounds 和 radius 必須有限且為正 |
| 直線 | `<line>` | 可編輯 line/freeform shape | `Native-normalized` | 拒絕瀏覽器專屬 line 效果 |
| 帶箭頭的線 | 帶已登記 triangle、stealth、arrow、diamond 或 oval 起點/終點 marker 的 `<line>` 或受支援 path | 原生 DrawingML 線首/線尾 | `Native-normalized`；marker 大小為近似 | marker 定義必須遵循條件 marker 合同 |
| 原生連線符 | 帶 connector metadata 和直接可見 path 的專案創作 compact preset 組 | `p:cxnSp` | 匯入 connector 保留源拓撲往返所需的 expanded 證據 | 已登記 preset/connector schema 內為 `Native-stable` |
| 任意多邊形 | `<path>` | 帶 `a:custGeom` 的 `p:sp` | 匯入自定義幾何重建為 path | `Native-normalized`；SVG arc 轉為三次曲線段 |
| 已物化的合併形狀結果 | `shape_boolean_svg.py` 輸出的普通 `<path>`；“拆分”返回多個同級 path | 每個返回 path 對應一個帶 `a:custGeom` 的 `p:sp` | `Native-normalized`；回導為最終自由形狀幾何，不保留可重放的操作歷史 | 僅接受受支援的閉合 operands；第一個 source 決定樣式與順序，且不輸出 clip、mask 或顯式 fill rule |
| 多邊形 | `<polygon>` | 閉合自定義幾何 | `Native-normalized` | points 必須有限且合法 |
| 折線 | `<polyline>` | 開放自定義幾何 | `Native-normalized` | points 使用與其他生成幾何相同的有限、已登記語法 |
| PowerPoint 預設形狀 | 由 registry 生成的 compact `<g>`，由該組承載 preset 意圖與基礎 paint，並直接包含可見 `<path>` 子元素 | 一個可編輯 preset `p:sp` | preset 身份與 adjustment 可以經匯入/匯出保留 | 質檢與匯出動態重渲染 registry；規範創作表達不含隱藏 carrier、preview wrapper 或已儲存 preview hash |
| 匯入的預設形狀 | 含隱藏原生 carrier、可見 preview 證據與新鮮度 metadata 的 expanded 匯入/往返組 | payload 合法且未改變時重新接入 preset | 在匯入合同內為 `Native-stable` | 不支援的 preset 保留為顯式診斷 fallback，不猜測幾何 |
| 動作按鈕形狀 | compact authored `actionButton*` preset 組 | 僅生成可見 preset 幾何 | 形狀幾何可往返 | 不建立單擊動作、導航目標或超連結 |
| 組 | `<g>` | `p:grpSp`，或對特殊 carrier 執行檔案化的 flatten/collapse | 分組內容可重建為 `<g>` | 結構 atom 與 placeholder 合同優先於普通分組 |
| 複用本地 symbol | 已登記的同文檔 `<use>` 合同或專案 icon placeholder | 在生成 Slide 中展開為可編輯 shape | 回導不承諾恢復原 symbol 圖 | 拒絕外部 use、不受支援的 symbol 能力和結構 metadata 複用 |
| 圖示 / 匯入向量 | 由專案圖示管線解析的 `<use data-icon="library/name">`；create-template 匯入統一使用 `imported/<name>` | 展開後的可編輯向量原語/組 | 重建幾何，不恢復原圖示庫引用 | 標識區分大小寫；匯入素材僅在工作區根目錄 `icons/imported/<name>.svg` 保留一份 |
| SmartArt / DiagramML | 無主 SVG 物件對映 | 主重設計路線可以用普通 shape 重建語義 | 原生/模板路線中為 `Direct preservation`，否則為 preview 或顯式 fallback | 不得將裝飾性組標記為原生 SmartArt |

專案創作 preset 有意採用 compact 表達，而 PPTX 匯入繼續保留無損往返裁決所需的 expanded 證據。精確機器合同仍屬於 [`shared-standards-core.md`](../../skills/ppt-master/references/shared-standards-core.md)，preset 選擇與創作行為見 [`native-shape-authoring.md`](../../skills/ppt-master/references/native-shape-authoring.md)。

## 4. PowerPoint 文本功能

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 文本框 | `<text>` | 帶 `p:txBody` 的可編輯 `p:sp` | 重建為 `<text>`，需要時含 `<tspan>` | 文本必須是良構 XML，且僅使用已登記屬性 |
| 行內混合格式 | 不帶定位的 `<tspan>` run | 同一文本框內的 DrawingML run | `Native-normalized`；已登記 run 格式仍可編輯 | 改變文本框幾何的定位可能會拆分結果 |
| 多段落 | 可合併的 text/tspan 結構 | 同一文本框內的多個 `a:p` 段落 | `Native-normalized` | 嚴格獨立定位的行可保持為獨立文本框 |
| 有意義的文本空白 | `<text>`/`<tspan>` 上精確的 `xml:space="default"` 或 `xml:space="preserve"` | 可編輯 DrawingML run 中歸一化或保留的 U+0020 文本 | `Native-normalized`；保留行內 run 所有權 | 使用專案 Chromium/SVG2 合同：LF/TAB 轉為空格，`default` 跨 run 摺疊，`preserve` 全部保留，Unicode 間隔字元保持字面值；CSS `white-space` 與 SVG 1.1 遺留換行刪除不在對映內 |
| 字型 | 根據專案 lock 解析的規範 `font-family` | 直接 typeface 或已登記 theme font | 在安裝字型/替換邊界內為 `Native-stable` | 校驗會報告未鎖定或不可用字型 |
| 字號 | 有限、無單位的 SVG px，例如 `font-size="24"` | DrawingML 百分之一磅；`1 px = 0.75 pt` | 單位轉換後為 `Native-stable` | 生成創作只使用無單位 px；已登記歷史單位是會產生 warning 的相容輸入，未知單位為 error；DrawingML 下限為 1 pt |
| 字重 | `<text>`/`<tspan>` 上已登記的 `font-weight` | DrawingML 常規/粗體 run 開關 | `Native-normalized`；數值字重會摺疊到 DrawingML 布林邊界 | 精確取值語法與別名屬於 [`svg-effects.md` §6.7](../../skills/ppt-master/references/svg-effects.md#67-advanced-text-treatments) |
| 斜體、下劃線與刪除線 | `<text>`/`<tspan>` 上已登記的 `font-style` / `text-decoration` | DrawingML 斜體、下劃線與刪除線 run 屬性 | 已登記 token 為 `Native-stable` | 拒絕未知 token；精確語法屬於 [`svg-effects.md` §6.7](../../skills/ppt-master/references/svg-effects.md#67-advanced-text-treatments) |
| 文本填充與透明度 | 規範 fill 加 run alpha | DrawingML run fill 與 alpha | `Native-normalized` | 使用語義 alpha 通道，不使用未登記 CSS 效果 |
| 文本輪廓 | 文本上已登記 stroke | DrawingML run outline | `Native-normalized` | 輪廓承載精細視覺意義時需複核 |
| 文本對齊 | 已登記的 `text-anchor` 與段落語義 | 段落對齊加歸一化文本框位置 | `Native-normalized` | 不支援 run 級錨定與瀏覽器 baseline 啟發式；精確放置屬於 [`svg-effects.md` §6.7](../../skills/ppt-master/references/svg-effects.md#67-advanced-text-treatments) |
| 文本框垂直對齊 | 無規範生成 SVG 控制；生成文本框使用頂部對齊 | 頂部對齊的 DrawingML text body | 匯入的垂直文本可能被歸一化，但主路線不公開通用創作控制 | 不得從 SVG baseline 或瀏覽器排版行為推斷垂直對齊 |
| 字元間距 | 已登記 `letter-spacing` | DrawingML 字元間距 | `Native-normalized` | 按 [`svg-effects.md` §6.7](../../skills/ppt-master/references/svg-effects.md#67-advanced-text-treatments) 拒絕不受支援的 CSS 排版、超出 DrawingML 範圍的間距，以及導致生成 run advance 或文本框 extent 非正的負字距 |
| 專案符號段落 | 已識別的前導專案符號形式 | 原生 DrawingML bullet | `Native-normalized` | 僅提升已登記 bullet 語法 |
| 旋轉文本 | 文本物件上受支援的 transform | 旋轉文本 shape | `Native-normalized` | 傾斜文本與瀏覽器專屬 transform 不受支援 |
| 文本陰影或發光 | 受支援 filter/effect 合同 | 一個原生外陰影或發光 | `Approximate` | 僅支援一個已登記效果圖；實質效果需複核 |
| WordArt、文本變形或沿路徑文本 | 無已登記主路線對映 | 不生成原生 WordArt | `Bake-required` 或使用普通文本/幾何重建 | 瀏覽器可渲染不代表 PowerPoint 受支援 |

## 5. PowerPoint 圖片功能

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 圖片 | 具有顯式正尺寸且只含一個專案資產或圖片 data URI 源的 `<image>` | `p:pic`、media part 與 relationship | 重建為 `<image>` | 源必須可解析、採用已登記格式，並包含與 MIME/副檔名相符的可解碼位元組；非法 frame 或媒體會在封裝前失敗 |
| 顯式複雜 SVG 圖片 | `create-template` 歸一化期間，由 `extract_svg_pictures.py` 從一個精確 `<g id>` 生成緊邊界、自包含 `.svg`，再以直接 `<image>` 引用 | 一個以 SVG media 為源的 `p:pic` | 回導為一個 `<image>`；內部 path 不會提升成獨立 PowerPoint 形狀 | 僅允許 `standard` / `fidelity` 顯式選擇；匯入、重複檢測、Master/Layout、finalize 與 export 均不得自動把組轉換成這種表達 |
| 圖片拉伸填滿框 | `preserveAspectRatio="none"` | 原生拉伸 picture frame | `Native-stable` | `none` 必須單獨出現；它會有意改變源寬高比 |
| 圖片裁剪填充 | 一個已登記對齊值加顯式 `slice` | 原生 `a:srcRect` 裁剪 | 源尺寸可讀時為 `Native-stable` | 對齊值區分大小寫；未知模式與額外 token 為 error |
| 圖片適應框 | 省略時使用預設值，或一個已登記對齊值加顯式 `meet` | 原生 fitted picture frame | `Native-normalized` | 僅寫對齊值是相容輸入，Checker 會給出規範化建議 |
| 圖片透明度 | 原子 image `opacity` | 原生 `a:alphaModFix` | `Native-stable` | 值必須有限，並在可接受 opacity 語法內 |
| 圖片裁成形狀 | 作用於 image/crop wrapper 且只含一個 SVG 名稱空間形狀的已登記 `clip-path` | picture preset 或 custom geometry | `Native-normalized` | circle/ellipse/rect preset 必須覆蓋完整圖片 frame；區域性或偏移輪廓使用 path/polygon；不接受任意 mask 或依賴繞組規則（winding rule）的輪廓 |
| 匯入的裁剪圖片 | 匯入器產生的精確 SVG 名稱空間巢狀 crop wrapper，在可視根/`g` 樹中內含一個直接 unit-frame image | 重新匯出為原生 signed `a:srcRect` | crop 合同內為 `Native-stable`，包括負裁剪值 | 拒絕通用巢狀 viewport、非可視或僅渲染所屬容器、額外可視子元素、不可表示的 crop window、無裁剪的冗餘 wrapper，以及無法解析的 clip-marker 配對 |
| 圖片重著色、藝術濾鏡、模糊或複雜 mask | 無通用創作對映 | 使用受支援 overlay 重建或預渲染 | `Bake-required` | 任意 SVG filter 和 blend mode 違反主合同 |

## 6. PowerPoint 填充、線條與效果功能

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 無填充 | `fill="none"` | `a:noFill` | `Native-stable` | 生成 SVG 使用小寫規範拼法 |
| 純色填充 | 已鎖定規範 `fill="#RRGGBB"` | `a:solidFill`；當鎖定角色可精確複用時使用 theme token | `Native-stable` | 相容顏色拼法可產生 warning；格式錯誤或生成未鎖定值失敗 |
| 填充透明度 | 不透明 fill 加 `fill-opacity` | 原生 alpha | `Native-stable` | 生成值為 0 到 1 的有限無單位數 |
| 線性漸變填充 | `<defs>` 中已登記 `<linearGradient>` | 原生 `a:gradFill` | `Native-normalized` | stop、座標、transform 與引用必須遵循封閉合同 |
| 徑向漸變填充 | 已登記 `<radialGradient>` | 居中圓形 DrawingML 漸變 | `Approximate` | 對焦點/半徑敏感的設計需複核 |
| 圖案填充 | 帶註解的專案 pattern 定義 | 原生 `a:pattFill` | `Native-normalized` | 僅支援已登記 PowerPoint 預設 pattern |
| 無輪廓 | `stroke="none"` 或已登記線預設 | `a:ln` 內的 `a:noFill` | `Native-stable` | 不得用零線寬模糊 CSS 模擬預設 |
| 實線輪廓 | 已登記 `stroke` 與寬度 | 原生 `a:ln` | `Native-stable` | 寬度與 paint 必須使用規範單位/語法 |
| 複合輪廓線 | 無已登記的單一 SVG stroke 表達 | 顯式幾何替代或烘焙資產 | 複合線身份為 `Bake-required` | 容錯回導省略不支援的輪廓並報告；嚴格回導拒絕非 `sng` 的 `cmpd` |
| 內側對齊輪廓 | 無已登記的普通 SVG stroke 表達 | 顯式內縮幾何或烘焙資產 | 精確輪廓對齊為 `Bake-required` | 容錯回導省略不支援的輪廓並報告；嚴格回導拒絕非 `ctr` 的 `algn` |
| 圖案、圖片或組派生輪廓 paint | 無已登記的線條 paint SVG 對映 | 顯式幾何替代或烘焙資產 | `Bake-required` | 容錯回導省略不支援的輪廓並報告；嚴格回導拒絕該輸入，不虛構純色線 |
| transform 下的輪廓縮放 | 精確的 `vector-effect="none"` 或 `vector-effect="non-scaling-stroke"` | 選擇被解析為原生線寬 | `Native-normalized` | 拒絕其他取值；生成拼法必須精確且為小寫 |
| 虛線或點線輪廓 | 已登記 dash array | 預設或自定義 DrawingML dash | `Native-normalized` | 拒絕不支援的 dash 語義 |
| 線端與連線樣式 | 已登記 cap/join 值 | 原生 line cap/join 屬性 | 固定 join 合同內為 `Native-stable` | 回導僅接受一個 join；miter 必須精確使用 `lim="800000"` |
| 線條箭頭 | 已登記起點/終點 marker | 原生 head/tail end 屬性 | marker 大小為 `Approximate` | 僅 triangle、stealth、arrow、diamond、oval 遵循條件 marker 合同 |
| 外陰影 | 一個受支援 shadow filter 圖 | `a:effectLst` 中的原生外陰影 | `Approximate`；僅當非零偏移仍可穩定分類時，才重建單一 shape/connector 來源 `outerShdw` | 零偏移來源陰影和不支援的圖結構不會被靜默改成其他效果 |
| 發光 | 一個受支援 glow filter 圖 | `a:effectLst` 中的原生髮光 | `Approximate`；單一 shape/connector 來源發光保持已登記的半徑換算 | 發光承載語義強調時需複核 |
| 匯入的文字 run 效果 | 邏輯 shape 上未變更的 `metadata[data-pptx-part="txbody"]`；繼承自 Layout/Master 的列表樣式以及豎排、含關係引用、表格單元格降級路徑使用僅限匯入的阻塞效果狀態 | `p:txBody` 內原始的 slide-local 原生 run 效果 | 僅在原始 slide-local payload 仍可用時為 `Native-stable`；繼承效果、編輯或降級路徑若會丟失非空 run `effectLst` / `effectDag` 則被阻斷 | 不是公開創作語法；表格單元格 run 效果還會停用原生 Table 替換 payload |
| 整個物件透明度 | 原子元素 `opacity` | alpha 分發至受支援原生通道 | `Native-normalized` | 除非整個原子物件需要淡出，否則優先通道專屬 alpha |
| 組透明度 | 相容 `<g opacity>` | 後代歸一化近似 | `Approximate`，併產生 warning | 生成 SVG 應優先後代 alpha |
| 內陰影、柔化邊緣、倒影、模糊、湍流、混合模式或任意 mask | 無已登記原生對映 | 顯式幾何替代或柵格資產 | `Bake-required`；PPTX 回導保留基礎物件，並對不支援的 shape/connector 效果、圖片/組效果 DAG 及非空圖片/組效果列表產生阻塞診斷 | 已處理的物件效果不能被改成其他型別或靜默省略；文字 run 安全邊界見上方未變更 `txBody` 行 |

## 7. PowerPoint 表格

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 視覺繪製表格 | 普通 SVG shape、line 與 text | 相互獨立的可編輯 PowerPoint shape | 保真度遵循各元件對應行 | 它不是原生表格，也沒有 PowerPoint 表格編輯模型 |
| PowerPoint 原生表格 | 一個帶 `<metadata type="application/json">` 和可見 fallback 的 `<g data-pptx-replace-with="table">` | 啟用原生 Chart/Table 替換時產生含 `a:tbl` 的 `p:graphicFrame` | 匯入受支援表格重建 fallback 加替換 metadata | metadata 必須形成已登記矩形 schema；需要 `--native-charts-and-tables` |
| 合併表格單元格 | 規範原生表格 merge metadata | 原生水平/垂直合併語義 | 封閉 schema 內為 `Native-stable` | 拒絕重疊、歧義或非矩形合併 |
| 表格單元格格式 | 已登記原生表格單元格格式欄位 | 原生單元格 fill、border、text 與 alignment | `Native-normalized` | 不猜測封閉 schema 以外的欄位；匯入的非空 run 效果會阻斷，而不是歸一化成無效果單元格 |
| 不受支援的原生表格功能 | SVG fallback 或直接源保留 | 保留可見 fallback，或在直接路線保留源 OOXML | 顯式 fallback / `Direct preservation` | 不得臨時擴充套件 JSON |

PowerPoint 原生 Chart/Table 物件是可選功能。預設匯出保留 SVG fallback，並轉換為仍可獨立編輯的 DrawingML shape，以保持視覺穩定；原生匯出改為提供物件的資料來源以及圖表/表格專屬編輯模型，並可能歸一化外觀。

匯入的圖表組使用 `data-pptx-fallback-kind="source-preview|normalized|placeholder"` 對可見 fallback 分類；其中 `placeholder` 自身即表示僅用於重建的 fallback。`data-pptx-replacement-status` 則記錄 fallback-only 圖表或表格匯入無法提出有效替換宣告的原因。該合同下的匯入組均使用 `data-pptx-import-source="pptx"`，有效宣告還可攜帶 `data-pptx-fallback-sha256` 防止陳舊 metadata 覆蓋後續視覺編輯。舊 `data-pptx-native*`、`data-pptx-visual-status` 和 `data-pptx-route-status` 寫法仍可讀，但不再是規範創作格式。

## 8. PowerPoint 圖表

| PowerPoint 功能 | 專案表達 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 視覺繪製圖表 | 普通 SVG 幾何與文本 | 相互獨立的可編輯 PowerPoint shape | 保真度遵循各元件對應行 | 沒有“編輯資料”工作簿 |
| PowerPoint 原生經典圖表 | 一個帶 `<metadata type="application/json">` 已登記 JSON 資料和可見 fallback 的 `<g data-pptx-replace-with="chart">` | `p:graphicFrame`、經典 chart part 與嵌入工作簿 | 受支援的匯入重建 fallback 加替換 metadata | chart type 與資料必須匹配封閉 schema；需要 `--native-charts-and-tables` |
| 原生 ChartEx 圖表 | 具有受支援 ChartEx family 的相同 marker 介面 | `cx:chart` part 與嵌入工作簿 | 受支援 family 可按語義重建 | 僅接受已登記 family/field 組合 |
| 圖表標題、圖例、座標軸、標籤與系列格式 | 已登記原生圖表 metadata | 原生 chart 屬性 | `Native-normalized` | 精確欄位與受支援 family 仍以 `native-data-interface.md` 為規範 |
| 圖表說明、來源或腳註 | replacement marker 之外的普通伴隨 SVG text | 圖表旁邊可編輯的 Slide 文本框 | 作為文本時為 `Native-stable` | 不得把 Slide 文案隱藏在 chart JSON 裡 |
| 已編輯 SVG fallback 與過期替換 metadata | 更新後的可見 SVG 加過期 hash | 預設匯出保留可見 SVG；原生替換失敗 | 顯式安全行為 | 編譯器絕不默默丟棄更新的視覺編輯 |
| 不支援的 3D 或延後圖表 family | SVG 繪製圖表、烘焙資產或直接源保留 | 不猜測原生圖表 | fallback / `Direct preservation` | 不支援的 alias 必須使原生校驗失敗 |

完整圖表/表格 schema 和受支援 family 列表有意僅保留在[原生資料介面替換合同](../../skills/ppt-master/references/native-data-interface.md#2-powerpoint-native-chart--table-replacement-markers-opt-in)中。

## 9. PowerPoint 播放與打包功能

這些能力屬於 PPTX 包語義。它們不出現在頁面 SVG 中是有意設計。

| PowerPoint 功能 | 專案中的所有者 | PPTX 結果 | 回導與保真度 | 校驗邊界 |
|---|---|---|---|---|
| 演講者備註 | `notes/<slide>.md` sidecar | Notes Slide part 與 relationship | `Sidecar/package` | 備註不是 SVG 文本，不影響頁面幾何 |
| 幻燈片切換 | CLI 選項或 `animations.json` | `p:transition` | `Sidecar/package` | 未知效果或非法時長失敗；不默默 fallback 到 `fade` |
| 物件動畫（進入 / 強調 / 動作路徑 / 退出） | `animations.json`，目標為穩定的頂層 SVG group ID | 根 `p:timing` 動畫樹 | `Sidecar/package`；group ID 僅為目標錨點 | 靜態結構層與佔位符不可動畫 |
| 旁白音訊 | `audio/` 資產加 recorded-narration 匯出選項 | media relationship、audio carrier 與 timing | `Sidecar/package` | 必須校驗資產、Slide 關聯與時序 |
| 幻燈片自動換頁 | 顯式 transition timing 或旁白派生時長 | `advTm`/換頁行為 | `Sidecar/package` | 單擊驅動動畫與錄製旁白不相容 |
| 超連結或動作 | 無主 SVG 編譯器對映 | 不由頁面 SVG 建立 | 原生路線保留源 OOXML 時為 `Direct preservation` | action-button preset 只提供可見幾何 |
| 批註或審閱執行緒 | 無 SVG 或生成側對映 | 不編寫 | 僅在其他路線明確擁有時為 `Direct preservation` | 不自動將審閱 metadata 轉為可見 Slide 內容 |
| 不屬於已對映功能的 relationship | 無通用 SVG 逃生口 | 不生成 | 適用時為 `Direct preservation` | 不支援任意 relationship 注入 |

sidecar 工作流見[轉場與動畫](./animations.md)（技術規範源為 [`references/animations.md`](../../skills/ppt-master/references/animations.md)）與 [`audio-narration.md`](./audio-narration.md)。

## 10. 其他 PowerPoint 原生功能

| PowerPoint 功能 | 主路線狀態 | 受支援的替代方案 | 邊界 |
|---|---|---|---|
| SmartArt / DiagramML | 無原生 SVG 編譯器對映 | 使用 shape 重建語義，或通過原生/模板路線保留 | 截圖或 fallback 必須是顯式的 |
| OLE 或嵌入 Office 物件 | SVG 路線不支援 | 直接保留或渲染 preview | 不得通過 SVG metadata 製造包 relationship |
| 原生公式 / OMML | SVG 路線不支援 | 渲染公式資產或直接保留原生 OOXML | 渲染公式是圖片，不是可編輯公式 |
| 影片 | 不支援作為 SVG 創作媒體物件 | 直接保留，或本合同之外的顯式封面/連結工作流 | `media` 佔位符不建立影片 |
| 3D 模型 | 不支援 | 直接保留或烘焙 preview | 不將瀏覽器 SVG 近似當作原生 3D |
| 宏 / VBA | 不支援 | 僅通過感知宏的直接工作流保留 | 普通生成 `.pptx` 路線不生成 VBA |
| 任意 Office 擴充套件 XML | 不支援 | 由擁有該語義的原生工作流直接保留 | SVG 編譯器不提供通用 OOXML 透傳 |

## 11. 反向對映：PPTX 到專案 SVG

匯入器將受支援的 PowerPoint 語義重建為與匯出相同的專案詞彙：

| PowerPoint 源物件 | 專案 SVG 重建 |
|---|---|
| 預設形狀 | 受支援時重建為含原生 carrier 與可見 preview 證據的 expanded preset 組 |
| 自定義幾何 | `<path>` |
| 文本體 | `<text>` 與 `<tspan>` run/段落 |
| 圖片 | `<image>`，或已登記巢狀 crop 表達 |
| 同時帶柵格相容預覽的 SVG 圖片 | 優先使用 `asvg:svgBlip` relationship 重建 `<image>`；僅當 SVG relationship 或 media part 不可用時才使用普通 `a:blip` relationship |
| 連線符 | expanded 線/path preview 加 connector/frame/topology 證據 |
| 組 | `<g>` |
| 受支援原生表格/圖表 | 可見 fallback 加原生物件 metadata |
| 不支援的 graphic frame 或 SmartArt | 顯式 preview、placeholder 或 unsupported 狀態 |

這是語義投影，不是語法往返。只有 Create Template mirror 可把來源包中已驗證的 Master/Layout 事實保留到新工作區；普通視覺匯入不會從 Slide 外觀推斷可複用拓撲。

### 匯入執行模式與錯誤恢復邊界

`pptx_to_svg.py` 預設採用容錯匯入，因為輸入來自使用者或第三方 PPTX。`--strict` 用於 parser 開發、合同核驗和復現第一個原始檔違規點。生成 SVG 的嚴格校驗與匯出邊界保持不變。

| 原始檔情況 | 預設容錯匯入 | `--strict` | 診斷結果 |
|---|---|---|---|
| 可識別顏色語義帶無關源 metadata | 規範化已識別顏色與 modifier | 拒絕非規範結構 | warning；可用時包含 part、Slide 與 shape 上下文 |
| 不支援的填充、輪廓、效果、圖片填充、文字型或樣式屬性 | 保留物件，只省略不支援的屬性或功能 | 在第一個違規點停止 | warning 說明省略內容與 fallback |
| 無法按屬性對映的不支援物件 | 只把該物件替換為可見診斷佔位；沒有可用 frame 時才省略 | 在第一個違規點停止 | warning 標識源物件 |
| 不支援的 Slide 或 part 背景 | 省略該背景，繼續當前頁面/part | 在第一個違規點停止 | warning 標識所屬 part |
| 損壞的包/XML 或缺失必需包結構 | 停止；不存在安全的頁面級容錯 | 停止 | 整潔的命令錯誤，不輸出裸 Python traceback |

每次成功轉換都會寫入 `<output>/conversion-report.json`。報告記錄執行模式、Slide 與 warning 數量、穩定原因碼、源錯誤訊息、採用的 fallback、包 part，以及可用時的 Slide 序號和 shape id/name/kind。因此，容錯匯入不是靜默吞錯：它儘可能保留可用輸出，同時讓每一次合同降級都可複核。

## 12. 校驗職責

四層有意承擔不同職責：

| 層 | 職責 |
|---|---|
| 提示詞、模板與示例 | 對每項 PowerPoint 功能只生成規範表達 |
| `svg_quality_checker.py` | 拒絕非法/不支援對映；對已登記相容拼法或保真風險給出 warning 但允許繼續 |
| `svg_to_pptx.py` 與最終包讀回 | 歸一化相容輸入、編譯 DrawingML，並拒絕任何會產生歧義、結構不一致或非法結果的輸出 |
| `pptx_to_svg.py` | 預設容錯模式在最窄安全邊界保留可用 deck 並報告源內容降級；`--strict` 模式在第一個不支援或格式錯誤的源結構處停止 |

生成 SVG 的 warning 不是猜測許可。它只適用於擁有唯一結果的受支援對映，但其拼法或保真度值得注意的情況。缺失對映、非法單位、格式錯誤 metadata、破損的結構合同，以及可能觸發 PowerPoint 修復的生成 DrawingML 仍是 error。匯入診斷描述對源內容的顯式丟失或規範化，絕不授權匯入器虛構不支援的語義。

## 13. 新增或修改對映

應將對映變更視為編譯器變更，而不是寬鬆 SVG parser 調整：

1. 命名 PowerPoint 能力與預期的可編輯 DrawingML 結果。
2. 在 [`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 路由到的適用權威模組中定義一種規範專案 SVG 或 sidecar 表達。
3. 將可接受相容輸入與生成創作分開宣告。
4. 實現匯出；僅當支援語義重建時實現匯入。
5. 增加 Checker 分類：非法/歧義輸入為 error，只有結果確定的相容或近似輸入可為 warning。
6. 對生成 SVG、PPTX 包、PowerPoint 渲染，以及適用時的反向匯入執行聚焦迴歸驗證。
7. 同步更新本指南中對應的英文與中文行。

實現入口：

- 匯出：[`svg_to_pptx.py`](../../skills/ppt-master/scripts/svg_to_pptx.py) 與 `scripts/svg_to_pptx/`
- 匯入：[`pptx_to_svg.py`](../../skills/ppt-master/scripts/pptx_to_svg.py) 與 `scripts/pptx_to_svg/`
- 校驗：[`svg_quality_checker.py`](../../skills/ppt-master/scripts/svg_quality_checker.py)
- 權威路由：[`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md)
