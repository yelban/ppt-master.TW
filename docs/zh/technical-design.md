# 技術路線

[English](../technical-design.md) | [中文](./technical-design.md)

---

## 設計哲學 —— AI 驅動工作流，人掌握最終判斷

PPT Master 交付的是一份**高質量、可繼續編輯的 PowerPoint 草稿**，而不是封閉的最終成品。工作流先推理資訊與論證，再設計頁面，並按照明確的路線合同創作或保留 PowerPoint 原生物件。使用者負責確認方向，並在 PowerPoint 中掌握最後一公里的判斷。後續工作應當是對真實 deck 的精修，而不是從整頁圖片或淺層可編輯外殼重新搭建。

工作流提供簡報專用的推理、狀態、合同與質量門；確定性工具負責轉換、校驗、打包和可重複檔案操作。**最終質量上限仍由所選模型決定**，使用者的審美與判斷則負責評審和收尾。

### SVG 是專案的規範中間語言

PPT Master 不以“任意 SVG 都能轉成 PPTX”為目標。`svg_output/` 使用的是**專案規範化 SVG 中間語言**：它借用 SVG 的 XML 語法和二維圖形模型，但允許的元素、屬性、單位、metadata、結構合同與 DrawingML 對映都由專案規範封閉定義。這裡的方向是 **SVG 適應 PPT Master，而不是 PPT Master 追隨整個 SVG 標準擴張**。

這套中間語言區分三種輸入狀態：

| 狀態 | 定義 | 處理方式 |
|---|---|---|
| 規範創作輸入 | 提示詞、模板和示例應生成的唯一推薦表達 | 按註冊對映校驗和編譯，不因表達別名產生 warning |
| 相容輸入 | 已明確登記、可確定且安全歸一化的歷史或人工寫法 | Checker 給出非阻塞 warning；轉換器確定性歸一化後編譯，不把別名反向擴散到提示詞 |
| 非法或不支援輸入 | 缺少對映、存在歧義、破壞結構合同，或可能生成非法 DrawingML / PPTX 的表達 | Checker 報 error 並阻斷標準流程；轉換器在自身預檢或 package 校驗命中同一非法條件時失敗 |

例如，專案字號統一採用 SVG px 語義，規範寫法是有限的無單位數值（如 `font-size="24"`）；其他單位只有在轉換器已有確定性換算、Checker 也按相容輸入放行時才可保留，不能成為生成提示詞的新寫法。相容讀取是一條受控遷移邊界，不是放寬創作語言的理由。

三層職責必須分開，不能用其中一層替代另一層：

| 層級 | 單一職責 | 不承擔的職責 |
|---|---|---|
| 提示詞、模板與示例 | 精確表達專案規範寫法，從源頭減少偏差和 warning | 不作為正確性或安全邊界 |
| `svg_quality_checker.py` | 在作者狀態上執行專案合同；error 阻塞，非阻塞 warning 放行 | 不靜默改寫頁面，也不猜測設計意圖 |
| `svg_to_pptx.py` | 對編譯對映與 package 執行防禦校驗；歸一化已支援的相容形式；把前置 SVG 質量報告關聯進 postflight | 不重跑完整 `svg_quality_checker.py`，也不以“檔案已生成”替代前置質量門 |

---

## Generate PPTX 路線架構

下圖描述 Generate PPTX 路線，也包含其 `beautify-pptx` profile。Create Template 有獨立的工作區生命週期；Fill Native PPTX 與 Enhance Native PPTX 直接操作 OOXML。本文後續路線表會覆蓋全部四條頂層路線。

```
用户输入 (PDF/DOCX/XLSX/PPTX/URL/Markdown/主题文本)
    ↓
[源内容处理与事实充分性检查] → source_to_md.py 按类型分派转换器；topic-only 或关键事实缺口进入 topic-research
    └── 原始或转换后内容就绪；研究分支形成补充 Markdown 与 facts provenance，随后作为来源导入项目
    ↓
[创建项目] → project_manager.py init <项目名> --format <格式>
    ↓
[归档来源与项目级分析（有来源文件时；纯对话文本跳过）] → project_manager.py import-sources <项目路径> <来源...>
    ├── 先按所有权边界把传入文件 move/copy 到 sources/
    ├── 再对已归档 PPTX 执行 intake，写入 analysis/<stem>.identity.json、<stem>.slide_library.json、source_profile.json
    ├── 若缺少同 stem 的规范 Markdown，再对该归档 PPTX 运行 ppt_to_md.py
    └── sources/ 内容型文件成为内容契约
    ↓
[模板 / 品牌 / 布局（可选）] — 默认跳过，直接自由设计
    仅在用户明确提供符合当前合同的 Brand/Layout/Deck 工作区根路径时触发：可以是全局模板库条目根，也可以是项目工作区根
    原生 PPTX 模板请求进入 template-fill；可复用 SVG 模板需先通过 create-template 创建
    ↓
[Strategist] 策略师 - 三阶段策略师确认与设计规范 → design_spec.md + spec_lock.md
    ↓
[Image Acquisition] 图片获取（当资源列表中有需要 AI 生成、网络搜索或切片的图片时）
    ↓
[Executor] 执行师
    ├── 生成开始前启动 live preview，并在生成期间保持可用
    ├── 先生成 P01 → svg_quality_checker.py --stage first-page --json
    ├── 把 P01 作为方法样本分类完整 issue set；消除全部 blocking error，并处理选定的 advisory warning
    ├── P02 至末页连续生成项目规范化 SVG 页面 → svg_output/（中途不再运行 checker）
    ├── [Quality Check] svg_quality_checker.py --stage final --json（强制通过，0 错误；warning 非阻塞）
    └── 讲稿生成：完整讲稿 → notes/total.md
    ↓
[图表校准（条件触发）] → verify-charts 工作流（含数据图表的 deck 必须在此步骤校准坐标）
    ↓
[视觉自检（可选，opt-in）] → visual-review 工作流（仅在用户明确请求时触发）
    ↓
[后处理] → total_md_split.py（拆分讲稿）→ finalize_svg.py → svg_to_pptx.py（防御校验后编译）
    ↓
输出：
    svg_final/
    └── *.svg                                           ← 强制派生的视觉预览；尝试内联受支持图片，EMF/WMF 保留外链例外

    exports/
    ├── <project_name>_<timestamp>.pptx                       ← 默认原生形状版（DrawingML）
    ├── <project_name>_<timestamp>_native_charts_tables.pptx  ← 显式 --native-charts-and-tables 变体
    └── <project_name>_<timestamp>_narrated.pptx              ← --recorded-narration 或 --narration-audio-dir 变体

    validation/
    ├── svg_quality_report.json                      ← blocking / introduced / inherited / source-import 分类结果
    └── <output_stem>.report.json                    ← 关联最终 SVG 质量报告的 package / 资源审计

    # 默认流程（未指定 -o）先创建备份目录，再 best-effort 复制作者源
    backup/<timestamp>/
    └── svg_output/                            ← 成功复制时可由冻结作者源重建 pptx
```

未顯式指定 `-o` 時，native 與 narration 標記可以組合成 `<project_name>_<timestamp>_native_charts_tables_narrated.pptx`；顯式 `-o` 則保留呼叫者給定的檔名。

### SVG 是受約束的頁面設計語言

凡是通過 SVG 創作或重新設計頁面的工作流，`svg_output/` 都是完整的頁面設計權威，但這裡的 SVG 專指通過專案合同校驗的專案規範化 SVG，而不是任意瀏覽器可渲染的 SVG。最終幻燈片中應出現的文字、圖片、形狀、圖示、圖表 / 表格 fallback、背景和模板派生布局元素，都必須已經存在於對應頁面 SVG 中，或被它明確引用。模板、`design_spec.md` 和 `spec_lock.md` 負責指導 SVG 創作；匯出器不能把它們當成第二層畫面來源，在匯出階段補入 SVG 缺失的頁面內容。

最小語義標記不會削弱這條閉包。自由設計、brand-only 和 `template_reuse_scope: style` 頁面使用 `pptx_structure.mode: flat`：所有已表達物件保持 Slide 本地，不創作任何 Master/Layout 身份、分層或 placeholder metadata。匯出器根據當前配色/字型 lock 生成一個屬於本專案的乾淨 Master 和一個 Blank Layout，刪除 title/body 等內建內容佔位符與未使用的內建 Layout，僅保留標準日期、頁尾和頁碼能力鉤子，但不提升任何 Slide 內容。只有 `template_reuse_scope: mirror|layout` 使用 structured 路線，每張新頁面從第一版 SVG 起就宣告 Master/Layout 身份。固定 Master/Layout 視覺是根節點直接原子元素；可複用內容槽位是頂層 group，帶顯式設計區域 bounds 和一個相容 carrier；複合 `object` 區域走顯式 proxy 降級，Layout 也允許零槽。`data-pptx-role` 只補充專用 metadata 尚未表達的少量頁面框架、package 或動畫行為。帶舊結構語義的模板包不能原地升級，也不能作為 Step 3 的 structured 輸入：先通過 `create-template` 建立新工作區；原生 PPTX 只提供包內仍然存在的事實，舊 SVG 只作為視覺參考；隨後由 Generate PPTX 路線按照 AI 推導的應用計劃創作新頁面。flat 專案是有意不帶 mapping，不算 legacy。匯出器不推斷、修補或遷移 Master/Layout 結構與 placeholder。

| 領域 | 權威來源 |
|---|---|
| SVG 創作路線中的可見頁面內容與佈局 | `svg_output/` 中的最終頁面 SVG |
| 專案規範化 SVG 的語法、相容形式與對映邊界 | 由 [`references/shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 選擇的拆分權威集 |
| Master/Layout/Slide 打包與原生物件對映 | SVG 到 PPTX 的翻譯；可以重組 SVG 已表達的內容，但不能創造新的可見內容 |
| 動畫、轉場、講稿和旁白 | 各自的 sidecar / 資源與 PPTX package 後處理 |
| 直接原生 PPTX 編輯 | 所選原生工作流自己的 PPTX / OOXML 契約 |

這是一條“頁面設計閉包”規則，不代表 SVG 要描述完整 PPTX package。相關驗收是：完成的頁面 SVG 能重建對應幻燈片的可見設計；不要求僅憑 SVG 重建講稿、音訊、計時、relationships 或直接原生編輯結果。

`svg_final/` 不改變這條邊界。Step 7 必須從 `svg_output/` 派生視覺預覽：受支援的點陣圖 / SVG 資源會內聯，EMF/WMF 為 native passthrough 保留外部引用；無法解析的普通圖片會保留原引用，當前 finalizer 只統計這類處理錯誤，並不據此讓整次處理失敗。這組檔案供 IDE、瀏覽器檢視，也可由使用者手動作為 SVG 圖片插入 PowerPoint；它不是第二條 PPTX 匯出路線，也不承擔 PowerPoint 手工“轉換為形狀”的相容性。需要可編輯形狀時，唯一受支援的路徑是專案轉換器把 `svg_output/` 翻譯為原生 DrawingML PPTX。

已有 PPTX 請求按修改模型分流：兩條原生工作流繞過 SVG，`beautify-pptx` 則仍是 Generate PPTX 內部通過 SVG 重做可見設計的 profile：

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
| 只有主題，或現有材料缺少實現使用者目標所需的事實 | Generate PPTX Step 1 內執行 `topic-research` | 只有主題時立即研究；有材料時先轉換 / 閱讀，只補已識別的事實缺口 |
| 有原始檔或對話文本，deck 結構可以重想 | Generate PPTX | Strategist 可以拆分、合併、刪除、重排和重設計 |
| PPTX 作為源材料，使用者允許重構故事和頁結構 | Generate PPTX，經 `ppt_to_md` + `pptx_intake` | PPTX 身份和幾何是事實與候選，不是復刻約束 |
| 原生 PPTX 模板 + 新材料 / 新主題 | Fill Native PPTX（`template-fill-pptx`） | 克隆並填充原生頁面；不生成 SVG |
| 現有 PPTX，頁數 / 頁序 / 措辭 1:1 保留，只改善排版 | Generate PPTX + `beautify-pptx` profile | 通過 SVG 重新生成；內容和分頁鎖定 |
| 已完成 PPTX，保持內容 / 佈局穩定，只加講稿、音訊、計時、轉場 | Enhance Native PPTX（`native-enhance-pptx`） | 直接 OOXML patch；不重新設計 |
| 使用者想從一個或多個 PPTX/SVG、圖片/PDF、檔案/網站、品牌資產、直接文字或混合參考材料包構建可複用模板工作區 | Create Template（`create-template`） | 固定入口讀取每個適用證據通道，只分派一個 Create Brand、Create Layout 或 Create Deck 子工作流，再返回供 Generate Step 3 使用的工作區根目錄；結構型子工作流可匯出審閱 PPTX |
| 使用者提供符合當前合同的明確模板路徑 | Generate PPTX Step 3 | Brand/Layout/Deck 工作區解析 `templates/design_spec.md`；平鋪根目錄可解析直接 `design_spec.md`；語義舊包會被拒絕，並通過 Create Template 替換 |
| 使用者要求調整物件級動畫順序 / 效果 / 計時 | Generate PPTX + `customize-animations` 階段 | 通過 `animations.json` 控制可選匯出策略 |
| 使用者要求預覽、選擇、註解或重匯出瀏覽器編輯 | Generate PPTX + `live-preview` 階段 | 註解只在規定交接點應用 |

“最佳化這份 PPT”這類含糊請求歸約為一個判定點：是否保留原始頁數、頁序和逐頁措辭。兩者都屬於 Generate PPTX；保留時選擇 `beautify-pptx` profile，允許重構時使用普通 profile。

---

## 技術流程

**核心流程：AI 生成 SVG → 後處理轉換為 DrawingML（PPTX）。**

整個流程分為三個階段：

**第一階段：內容理解與設計規劃**
原始檔（PDF/DOCX/XLSX/PPTX/URL/Markdown/主題文本）會被轉換成 Strategist 所需的內容事實與分析事實。Strategist 先確認開放式溝通契約，再由此推導完整 PPT 方案、解決生產機制，最終輸出完整設計規格。

**第二階段：AI 視覺生成**
Executor 角色逐頁生成簡報的視覺內容，輸出為 SVG 檔案。這個階段的產物是**設計稿**，而非成品。

**第三階段：工程化轉換**
後處理指令碼將受支援的 SVG 向量元素轉換為 DrawingML。文本和向量形狀會保持為 PowerPoint 原生物件——可點選、可編輯、可改樣式；點陣圖資源則複製為 PPT picture media，而不是把整頁壓平成一張圖片。

---

## 產物流

Artifact 的來源 / 派生所有權以 [`artifact-ownership.md`](../../skills/ppt-master/references/artifact-ownership.md) 為準；本節只把同一資料流視覺化成架構說明。

維護這套系統時，把資料夾理解成資料流會比“這些目錄剛好存在”更清楚：

```text
sources/<content files> ────────┐
sources/*.facts.json ───────────┤
analysis/source_profile.json ───┼─> Strategist -> design_spec.md + spec_lock.md
analysis/image_analysis.csv ────┘

design_spec.md + spec_lock.md + images/ + icons/ + templates/
    └─> Executor -> svg_output/
          ├─> 规划产物与引用保留在有效的当前上下文中
          ├─> project_manager.py page-context <project> P<NN> [按需]
          │     └─> --record-usage -> analysis/page-context/P<NN>.usage.json
          ├─> svg_quality_checker.py -> validation/svg_quality_report.json
          ├─> finalize_svg.py -> svg_final/
          └─> svg_to_pptx.py -> exports/<name>_<ts>.pptx + validation/<output_stem>.report.json
                                       backup/<ts>/svg_output/ [默认输出路径；目录创建后复制为 best-effort]

直接 OOXML 路由：
analysis/<stem>.slide_library.json + 源 PPTX + fill_plan.json
    └─> template_fill_pptx.py -> exports/*.pptx
源 PPTX 项目归档副本 + 增强计划 + 讲稿/音频/计时资产
    └─> native_enhance_pptx.py -> exports/*.pptx
```

關鍵切分是：`svg_output/` 是作者狀態，`svg_final/` 是派生視覺預覽，`exports/` 和 `backup/` 是派生的交付或歸檔狀態。模糊這條線，會讓校驗、重匯出和人工修復都更難推理。

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

這張表只展示概念對應關係，不是對整個 SVG 標準的承諾，也不承諾所有對映語義無損。每項受支援能力都必須在 [`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 路由到的適用模組中擁有明確對映，說明專案規範寫法、允許的相容輸入、目標 DrawingML 表達、保真度和拒絕條件；涉及 PPTX 回導的能力還要說明來源 PPTX / OOXML 語義。對映狀態可以是精確、確定性歸一化、顯式 fallback、sidecar 或 unsupported；講稿、動畫、relationships 等 package 語義不必強行塞進 SVG，但必須明確由哪條路線承載。

如需從 PowerPoint 功能出發逐項檢視這些關係，請參閱 [PowerPoint 功能 ↔ 專案 SVG 對映指南](./powerpoint-svg-mapping.md)。該檔案負責公開能力與 PPTX 匯入語義對映；由 `shared-standards.md` 路由的權威集負責生成 SVG 創作。

主生成路線採用**規範窄寫入、受控相容讀取**。新生成的 `svg_output/` 與可複用模板只使用專案規範寫法，例如不透明的六位大寫 `#RRGGBB`，透明度放在對應的 `fill-opacity`、`stroke-opacity`、`stop-opacity`、`flood-opacity` 或原子元素 `opacity` 中。歷史或人工輸入只有在相容合同明確登記、轉換結果唯一且輸出合法時才可繼續匯出；Checker 對這類寫法給出非阻塞 warning，轉換器在編譯邊界統一歸一化。任何需要猜測、沒有對映或可能產生損壞 PPTX 的表達都必須報 error。

因此，轉換不是在任意 SVG 和 DrawingML 之間做格式猜測，而是在專案規範化 SVG 與 DrawingML 之間執行有登入檔、有保真度說明、可測試的編譯。

SVG 也是唯一同時滿足流程中所有角色需要的格式：**AI 能可靠地生成它，人能在任意瀏覽器裡直接預覽和除錯，指令碼能按明確的相容合同轉換它**——在生成任何 DrawingML 之前，設計稿就已經完全透明可見。

---

## 源內容轉換

原始檔（PDF / DOCX / EPUB / XLSX / PPTX / 網頁）會在 Strategist 開始前完成歸一化，但當前架構已經不是“全部轉成 Markdown 後其他資訊都不重要”的單通道模型。現在有兩條事實通道，各自擁有明確職責：

| 通道 | 產物 | 所有者 | 用途 |
|---|---|---|---|
| 內容契約 | `sources/` 內容型檔案（以 `<stem>.md` 為主） | `source_to_md/*` 轉換器 + `import-sources` | 文本、表格、圖表數值、SmartArt 節點文字、引用和源材料敘事 |
| 結構化分析 | `analysis/*.json` / `analysis/*.csv` | intake 與分析工具 | PPTX 身份資訊、頁面幾何、原生表格/圖表、SmartArt 關係，以及圖片尺寸、比例、引用次數、媒體型別與渲染能力等可測量事實 |

對 PPTX 原始檔，`project_manager.py import-sources` 先按所有權邊界把原件 move/copy 到專案 `sources/`，再以歸檔後的路徑執行 `pptx_intake.py`；只有沒有同 stem 的顯式或既有規範 Markdown 時，才在最後呼叫 `ppt_to_md.py`。因此正常首次匯入會得到兩條事實通道，但去重路徑可跳過重複 Markdown 轉換，intake 失敗也會記錄為匯入 note，而不是偽造分析產物。Markdown 仍然是主生成流水線的內容源；成功的 intake bundle 會寫出 `<stem>.identity.json`、`<stem>.slide_library.json`，並把緊湊的多 deck 索引合併到 `analysis/source_profile.json`。Strategist 預設讀取這個緊湊索引來獲取源事實；只有特定工作流需要原始細節時，才打開單個 deck 的原始 artifact。這個邊界很重要：主流水線可以重構頁數和敘事，而 `template-fill` 與 `beautify` 會把同一批 intake 事實中的一部分提升為更強約束。

轉換器生成的圖片資產也會被歸一化。伴隨的 `<stem>_files/` 目錄會匯入專案級 `images/` 池，`image_manifest.json` 按檔名合併；當匯入後目錄名發生變化時，Markdown 中的資源引用會被重寫。Office 向量圖（`.emf` / `.wmf`）是一等執行時資產：intake 階段不柵格化它們，`finalize_svg.py` 為 native 路徑保留外部引用，`svg_to_pptx.py` 以 Office 向量媒體嵌入，避免 CJK 字型替換和向量細節損失。

兩個轉換器設計選擇仍然成立：

**Native-Python 優先，外部二進位制兜底。** 常見格式由純 Python wheel 處理，pandoc 僅在長尾小眾格式時才被呼叫。讓每個使用者都去裝一份可能沒有許可權裝的系統級二進位制是一種可用性稅，而大多數輸入是 docx / pdf / html / pptx，這種稅不值得。

**TLS 指紋模擬應對高安全站點。** 網頁抓取預設走 Python 版 `web_to_md.py`，並在可用時依賴 `curl_cffi` 做類 Chrome TLS 指紋模擬。微信公眾號和不少 CDN 會直接遮蔽 Python 預設握手；把這件事留在 Python 轉換路徑裡，避免讓 Node 抓取器成為主架構。

---

## 專案結構與生命週期

`project_manager.py init` 建立固定的專案工作目錄；預設匯出隨後建立帶時間戳的備份目錄，再嘗試複製 `backup/` 快照。完整生命週期結構如下：

| 目錄 | 職責 |
|---|---|
| `sources/` | 原件歸檔、歸一化 Markdown、轉換器伴隨檔案 |
| `analysis/` | 機器抽取事實：PPTX intake bundle 與按需重算的圖片分析 |
| `images/` | 單一執行時圖片池：使用者圖、抽取圖、公式圖、網路圖、AI 圖、切片圖、EMF/WMF |
| `icons/` | 由 `icon_sync.py` 複製的專案級圖示集；匯出時的全域性庫回退僅用於 legacy compatibility |
| `templates/` | 複製進專案的模板 spec / SVG reference / 非圖片模板資產 |
| `svg_output/` | 唯一手寫 SVG 源目錄 |
| `svg_final/` | 強制派生的視覺預覽 SVG；嘗試內聯受支援點陣圖 / SVG，保留 EMF/WMF 外鏈例外；服務 IDE / 瀏覽器，也可手動作為 SVG 圖片插入 PowerPoint |
| `live_preview/` | 預覽服務狀態、直接編輯歷史和註解日誌 |
| `notes/` | `total.md` 與拆分後的逐頁講稿 |
| `validation/` | SVG 質量報告與 PPTX postflight 審計報告 |
| `exports/` | 帶時間戳的 native PPTX 交付物 |
| `backup/<timestamp>/` | 預設匯出先建立時間戳目錄，再嘗試複製凍結的 `svg_output/`；複製失敗不令匯出失敗，但目錄建立失敗當前不會降級處理 |

CLI 支援 `--move`、`--copy` 和自動預設，但共享同一條固定的所有權邊界：只有倉庫 `projects/` 目錄下的原始檔可以 move 到目標專案的 `sources/`；其他本地路徑一律 copy 並保留原檔案，即使顯式傳入 `--move` 也不例外。`--copy` 用於要求保留的 projects-local 輸入。Generate PPTX 使用自動模式，因此倉庫正式檔案和外部使用者檔案不會在匯入時被移除。

---

## 架構不變數

可執行的 artifact ownership 不變數以 [`artifact-ownership.md`](../../skills/ppt-master/references/artifact-ownership.md) 為準；本節解釋這些邊界為什麼在架構上重要。

這些不變數強於普通實現偏好。如果某個改動破壞了其中一條，它很可能是在改變架構，而不是做重構。

| 不變數 | 實際後果 |
|---|---|
| `sources/` 內容型檔案是主流水線內容契約 | 主 SVG 路線中的文本、表格和圖表數值來自 `sources/` 內容型檔案（Markdown 為主，`.txt` / `.csv` / `.json` / `.yaml` 等同樣計入）；已知 sidecar（`*.conversion_profile.json`、`*_files/image_manifest.json`）排除在外 |
| `analysis/` 存機器事實，不存設計契約 | `source_profile.json` 和 intake artifact 輔助 Strategist；除非工作流明確規定，否則不鎖定頁數 / 頁序 |
| `design_spec.md` 解釋設計；`spec_lock.md` 執行設計 | 兩者始終是權威產物；按需投影不會取代它們 |
| 規劃上下文有效時持續複用 | 連續執行直接使用完整 Design Spec、lock 與已觸發引用；fresh/resumed/restarted 或壓縮後才重新讀取一次 |
| `page-context` 按需呼叫 | 只讀投影器用於診斷、確定性路由檢查和可選的用量統計，不是逐頁門禁 |
| `svg_output/` 是唯一手寫 SVG 目錄 | 質量檢查、手工編輯、重匯出和 `update_spec.py` 都面向作者源 |
| `svg_final/` 是派生產物 | 它必須能從 `svg_output/` 重建，只負責視覺預覽；受支援資源儘量內聯，EMF/WMF 保留外鏈例外，不應成為 native 匯出的事實源 |
| native PPTX 標準匯出讀取 `svg_output/` | 唯一受支援的可編輯形狀路線由專案轉換器執行；它要在 finalize 重寫前保留圖示、`preserveAspectRatio`、圓角矩形和原生圖片裁剪語義 |
| PowerPoint 手工“轉換為形狀”不屬於相容性契約 | `svg_final/` 可以作為 SVG 圖片插入，但轉換後的結構與視覺結果不做保證，也不反向約束 SVG 允許能力 |
| 直接 OOXML 路由不進入 SVG 流水線 | 保留型工作流直接 patch 原生 PPTX parts |
| 圖片事實來自重算後設資料 | `analysis/image_analysis.csv` 從即時 `images/` 目錄重算；Strategist 先用源文上下文，只在圖片語義或安全放置仍無法確定時檢視那一張具體圖片；Executor 不重新讀取源影畫素 |
| 原生 PPTX 模板不是 Step 3 模板 | Step 3 只消費可複用模板目錄 |

---

## Canvas 格式系統

PPT Master 不只服務 PPT——同一套 SVG → DrawingML 流水線還能產出方形海報、9:16 故事、A4 印刷品。各格式特定的約定（比例、安全區、品牌區等）住在 [`references/canvas-formats.md`](../../skills/ppt-master/references/canvas-formats.md)。

值得標註的架構選擇：**viewBox 是畫素，不是絕對單位。** 畫素空間讓 AI Executor 思考佈局沒有歧義（`x="100"` 就是左緣 +100px），人類在瀏覽器裡檢查也直接。到 EMU 的換算只在匯出時發生一次——選畫素意味著流水線的其餘環節（Strategist、Executor、質量檢查、後處理）永遠不需要在 EMU 思維下工作，那對 AI 生成和人類除錯都是敵對的。

---

## 模板系統與可選路徑

模板是**可選項，不是預設**。Strategist 預設走自由設計——AI 完全憑源內容創造視覺系統。模板路徑只在使用者明確提供目錄路徑時啟用。

**為什麼預設自由設計。** 模板是地板，但很容易變成天花板：它會把整個 deck 鎖進模板自有的視覺慣用語，無視內容本身想要怎樣被呈現。自由設計的佈局從源內容的結構推導而來，而不是從一套固定語法套上去——視覺節奏跟著內容走，而不是跟內容打架。約束模式在窄場景裡確實更好（品牌鎖定的 deck、強型別場景如學術答辯或政府報告），所以它一直在；但 AI 不主動去抓，是使用者去抓。

**機械觸發，不做語義匹配。** 像 `presentation_core` 這樣的裸名字、品牌提及，或“麥肯錫風格”這類風格短語，即使庫裡存在相似目錄，也不會觸發 Step 3。Step 3 只消費顯式路徑。當前 Brand/Layout/Deck 工作區均解析 `templates/design_spec.md`；平鋪目錄只有在 SVG 已滿足當前合同時，才相容從根目錄讀取 `design_spec.md`。目錄形態從不授權結構遷移；帶舊 Master/Layout/placeholder 語義的包必須先替換為新建的模板工作區，才能進入 Step 3。發現性交給模板索引和顯式問答（“有哪些模板可以用？”），不交給執行時 fuzzy matching。

當前 Brand/Layout/Deck 都採用同一工作區路由合同；Brand 不含 SVG roster，空的可選目錄直接省略：

```text
<template_workspace>/
├── templates/   # design_spec.md；Create Layout / Create Deck 另含 SVG 原型
├── images/      # 可选；位图素材，SVG 统一引用 ../images/<name>
├── icons/
│   └── imported/ # 可选；导入向量素材的唯一规范副本
└── exports/     # 可选、按需生成的审阅文件；全局库下由 Git 忽略
```

`<template_workspace>` 可以是 `skills/ppt-master/templates/<kind>/<id>/`，也可以是 `projects/<name>/`。Step 3 接收這個根目錄。工作區可在兩個位置之間遷移而不改形；唯一的範圍差異是全域性索引註冊。空的可選目錄不建立，`exports/` 也不會複製進新專案。

對 Create Layout / Create Deck，`standard` 與 `fidelity` 會重新創作 SVG 和新的 Master/Layout/slot 系統；來源拓撲只作為視覺證據，不保留、也不蒸餾。`mirror` 把來源包內實際存在且已驗證的頁序、Master/Layout 身份與父子關係、placeholder 事實和受支援視覺物化到新工作區，不做語義歸納或缺口補造。只有被保留的來源本身已經品牌中立且應用中立時，Layout mirror 才合法；否則應重新創作 Layout，或把這些事實保留為 Deck。由於結構層不能是 `<g>`，固定結構層的來源 group wrapper 只允許機械展開成直接原子，同時保持歸屬、paint order 和視覺一致。Create Brand 只分析並物化身份片段，不進入這些結構複製策略，也不生成 SVG roster。

三類別範本擁有不同的設計契約片段：

| Kind | 擁有的片段 | 典型內容 | 對 Strategist 的影響 |
|---|---|---|---|
| `brand` | 身份片段 | 配色、字型、logo、語氣、圖示風格 | 鎖定身份；結構保持自由 |
| `layout` | 品牌中立的結構片段 | 畫布、頁面結構、語義文字角色/空間行為、頁面型別、SVG roster | 提供結構能力；身份與溝通應用仍由下游決定 |
| `deck` | 應用段 + 一體化身份/結構 | 重複場景、受眾與結果、代表性頁面角色、身份和真實 SVG roster | 提供描述性語境和原型；Strategist 將其與獨立確認的 Stage-1 契約及當前內容對照，再推導應用計劃 |

Theme、Slide Master、Slide Layout 與 Placeholder 是編譯生成的 PowerPoint 原生物件，不是新的模板 kind。Layout 決定拓撲、位置、語義文字角色與空間行為，Brand 決定身份值與資產。`template_reuse_scope: layout` 會結合已確認的閱讀模式和字號體系解析最終 placeholder 格式；`mirror` 則保留來源的字面格式與文字拓撲。兩類規則都可編譯進同一套原生 Master/Layout 圖譜。

當使用者提供多個路徑時，融合是**片段級**而不是欄位級：brand 覆蓋身份片段，layout 覆蓋結構片段，deck 提供應用段。只有 Layout 的頁面角色和槽位能夠表達 Deck 的必需敘事/內容角色時，才能覆蓋 Deck 結構，否則必須顯式提出合成衝突。專案內 Brand + Layout 組合的應用語境來自 Stage 1，不會自動升級成可註冊的 Deck。同類衝突也會顯式列出，而不是按輸入順序默默決定。這樣融合後的 spec 能明確說明每個片段來自哪裡，便於審計和復現。

**原生 PPTX 不能直接作為 Step 3 工作區。** 普通 Generate 可以把 PPTX 作為源材料使用，`beautify-pptx` 也可以在頁數、頁序和逐頁措辭 1:1 的邊界下重新設計；這兩種情況都不會把原始 PPTX 當作 Step 3 模板。把原生 PPTX 作為模板或頁面殼、再用新材料填充時，預設進入 Fill Native PPTX；若請求允許拆分、合併、刪頁、重排或敘事重構，則仍屬於 Generate。只有當目標是建立可複用模板工作區、並在 SVG 路線的 Step 3 中重複使用其設計系統時，才先執行 Create Template，再傳入生成的工作區根目錄。

**佈局是 opt-in，圖表和圖示不是。** 這種不對稱不是矛盾——*佈局*正是鎖定視覺慣用語的那一層（地板/天花板問題），而圖表和圖示是不會施加 deck 級風格約束的複用原語。同一個 `templates/` 目錄，但在視覺契約裡扮演的角色不同。

---

## 角色系統：單一流水線中的專業模式

PPT Master 用的是**單主代理內的角色切換**，不是並行子代理。Strategist、Image_Generator、Executor，以及各路線中的 child workflow / profile / stage，本質上都是按需載入的指令作用域；它們不是帶著各自過期 deck 狀態的獨立 agent。這個選擇有三條互相支撐的理由：

**為什麼是單代理而非並行子代理。** 頁面設計依賴完整的上游上下文——Strategist 的色彩選擇、圖片資源是否成功獲取（還是失敗被替代）、之前幾頁的視覺節奏。子代理拿到的只能是這個上下文的過期區域性快照，產出的 deck 視覺會逐頁漂。同一邏輯也禁止分批生成（比如一次 5 頁）：分批加速上下文壓縮，deck 的視覺一致性下降速度比節省的速度更快——不划算。

**為什麼是角色專屬 reference 而不是一個超大 prompt。** Strategist 跑的是「跟使用者協商」模式（開放式、對話式、可以回退），Executor 跑的是「產出嚴格 XML」模式：不得重選上游方案或漏掉必需屬性，但在 Design Spec 留出的範圍內仍擁有幾何、構圖、層級和視覺處理的實現權。把兩者塞進同一個 prompt，強迫模型在同一個 turn 裡持守相互矛盾的紀律——所有混合模式的 prompt 工程病灶都會出現。按角色拆開，每個角色只加載它需要的、扔掉其他。

**策略師確認階段是預設連續路線中的主要使用者設計決策 gate。** Strategist 階段以一個按依賴排序的三階段 gate 作為核心決策點。第一階段確認開放式溝通契約與畫布。`delivery_context` 在同一個開放文本欄位中區分演講者主導、讀者主導、混合、錄製/自動播放，明確主要場景並記錄可選的次要用途；混合場景不能只寫“混合”而不說明由哪一種主導。其中的文本框仍承載可編輯推薦，且沒有任何一項要求非空：確認時按當前文本原樣儲存，清空後的值保持為空，不會回退到推薦內容。第二階段只從該契約計算一次並確認完整 PPT 方案：閱讀模式、敘事 mode、頁數、成套視覺系統、圖片來源和生成圖渲染。存在模板時，Strategist 還會根據真實工作區和當前內容推導頁面/原型應用計劃，並以可編輯的自然語言文本展示；只有內部複用/遵循模式保持隱藏。閱讀模式決定資訊由頁面、視覺、講者和備註如何共同承擔，其選項卡不展示 px 數值。瀏覽器可以在本地執行確定性的「閱讀模式 → 正文基準 → 未鎖定角色字號」聯動；手動編輯字號即鎖定可見值，不會重新計算第二階段。第三階段也只計算一次，並且只處理生產機制：條件式 AI 圖片獲取路徑、公式策略、生成模式與 Design Spec 稽核開關。JSON 為相容保留 `delivery_purpose` 鍵，但使用者側統一稱為閱讀模式。生成圖直接繼承已選 PPT 色彩錨點，不再單設圖片調色選擇。最終狀態有兩個等價載體：預設 UI 路徑在最終等待返回後只讀取一次 `confirm_ui/result.json`；顯式 chat-only 或委託路徑保留等價的最終確認摘要，並可不產生 `result.json`。兩條路徑都先把全部最終值（含生產機制）固化到同一份 `design_spec.md` 並完成 Gate 1 fidelity。未開啟 refine 時立即進入 lock 編寫；`refine_spec: true` 時，流程會在 `spec_lock.md` 之前暫停，使用者可以通過正常聊天任意修改這同一份 Design Spec、迭代任意輪次，明確批准後才釋放 Gate 2 並編寫 lock。流程不會維護第二份 Design Spec 或並行 lock。正常的 lock 編寫與下游執行不再回讀確認通道。必需人工素材未就緒仍可能引入條件式阻塞點，因此這裡不是對所有 runtime gate 的排他宣告。專案校驗要求 `spec_lock.md ## communication` 下存在緊湊的 `audience` / `objective` / `core_message` 錨點，並要求 §IX 每個 Slide block 都有 `Audience move`。

**圖片分析以重算後設資料為先，Strategist 只保留小範圍視覺兜底。** 當專案裡存在圖片時，`analyze_images.py` 把可度量事實重算到 `analysis/image_analysis.csv`；該 CSV 是即時 `images/` 目錄的派生檢視，不是持久快取。Strategist 先根據圖片在源文中的位置與前後文、圖注 / alt / 標題、檔名、使用者說明、已有資源記錄和這些後設資料判斷。只有當某一張具體圖片在選用、事實身份、頁面角色、裁剪安全或焦點放置上仍有實質歧義時，才可單獨檢視它，絕不得掃描整個圖片目錄。結論寫入 Design Spec §VIII 後，Executor 只消費該計劃與幾何資料，不會重新開啟源圖進行語義探索。使用者圖、抽取圖、網路圖、AI 圖、公式圖和切片圖仍統一匯入同一張可度量事實表。

**保留的規劃上下文**負責跨頁連續性；按需逐頁投影只承擔下文所述的診斷用途。

---

## 執行紀律

Generate 執行以 [`workflows/generate-pptx.md`](../../skills/ppt-master/workflows/generate-pptx.md) 為權威，該檔案擁有 Step 1–7 與 Generate 專屬規則；[`SKILL.md`](../../skills/ppt-master/SKILL.md) 只擁有全域性執行紀律，以及交接到 `routing.md` 的強制入口。這些規則整體看起來很官僚，但存在的理由是：LLM 預設行為是“讓我在這一 turn 裡把整個問題搞定”，而這恰好是序列流水線最不該有的形狀——序列流水線要求每一步的輸出都是有界、過 checkpoint、被下一步消費的。它們共同關閉了實際反覆出現的失敗模式：亂序執行、AI 代為做使用者設計決策、跨階段打包、前置條件未滿足、投機預先準備、子代理上下文丟失、分批漂移、長 deck 色彩字型漂移、指令碼批次生成 SVG 漂移，以及路由歧義。

全路由通用的停止 / 繼續規則以 [`failure-recovery.md`](../../skills/ppt-master/workflows/governance/failure-recovery.md) 為準；其中具體故障矩陣與續跑入口目前覆蓋 Generate PPTX。本節不復制這些規則。

其中三條邊界尤其關鍵。第一，Executor 頁面 SVG 必須由當前主代理逐頁手寫；禁止寫 Python / Node / shell 生成器批次吐 SVG，因為這種輸出會丟失跨頁判斷和視覺連續性。第二，生成節奏固定為 `P01 → first-page gate → 不间断生成其余页面 → final gate`。P01 不只是單頁樣張：執行者必須先輸出 `gate-signal`，區分 method-level、page-local 與未覆蓋的能力，再把已解決的方法規則帶入後續頁面；P02 到末頁之間不分批，也不插入 checker 呼叫。第三，路由是確定性的：原生 PPTX 模板、beautify、native enhancement、自定義動畫、live preview 等觸發條件已經在倉庫裡定義清楚時，不再額外拋給使用者一個開放式路線選擇題。

角色切換協議（切換模式前必須 `read_file references/<role>.md`）有兩個互相支撐的作用：把新鮮的角色指令載入上下文，覆蓋前一模式的漂移；對話 transcript 中的可見標記構成審計軌跡，讓使用者能看到 agent 何時切換了模式——回看一個具體決策為什麼這樣做時，這條線索很關鍵。

---

## 設計規範的傳播：spec_lock.md 作為上下文執行契約

Strategist 階段產出兩份看起來冗餘但服務不同物件的產物：

- `design_spec.md` —— 人類可讀敘述；deck 的「為什麼」（溝通意圖、受眾變化、敘事 / 模板 / 視覺理由、頁面大綱）
- `spec_lock.md` —— 機器可讀執行契約；包含緊湊的 `audience` / `objective` / `core_message` 溝通錨點，以及跨頁穩定的身份/複用角色和路由值（核心 HEX/字型角色、圖示庫、圖片資源與結構對映）

為什麼兩份都要？`design_spec.md` 儲存完整的確認方案與理由；`spec_lock.md` 只命名必須跨頁穩定或參與路由的子集。它根據 Design Spec 與頁面/資源/模板上下文編寫，不再逐欄位複製 UI JSON 或聊天摘要等確認通道原始載荷。[Generate PPTX Step 6](../../skills/ppt-master/workflows/generate-pptx.md#step-6-executor-phase) 在有效執行上下文中只保留並複用這兩份產物。fresh/resumed/restarted、上下文壓縮或只剩摘要時重新完整讀取一次；未變化的連續上下文不重複讀取。區域性色階、漸變/效果色與零星的非結構性展示字型屬於頁面判斷；一旦重複出現或形成穩定語義，就必須先提升為上游 lock 角色。

該檢視省略 Executor core 已經恆定載入的通用 SVG/圖示禁令，只保留專案專屬 forbidden 行。圖片從當前頁 brief、圖片資源表中的顯式頁分配和 mirror 原型引用中選擇；已分配給其他頁面的圖片會被排除，仍無法歸屬的 legacy 圖片保留在相容子集中，只有所有鎖定圖片都能確定歸屬到其他頁面時才記錄 `confirmed-none`。

這份 lock 同時也是逐頁路由表。除了全域性配色和字型，它還承載 `page_rhythm`（`anchor` / `dense` / `breathing`）、`page_charts`（某頁選中的圖表目錄參考；它只觸發讀取對應 SVG 與 §VII Usage，不鎖定最終圖表型別或幾何）、帶放置/裁剪契約的圖片行，以及決定載入哪些執行規則檔案的 `mode` / `visual_style`。選定 custom 方向時，lock 還承載已消解的 `mode_behavior` / `visual_style_behavior`；當它確實綜合或借鑑已有目錄項時，再用可選的 `mode_references` / `visual_style_references` / `image_rendering_references` 記錄全部精確 id，執行階段會先讀取每個對應檔案再綜合。真正全新的 custom 不寫參考欄位。`template_reuse_scope: mirror|layout` 專案的 lock 還承載 `page_layouts`（每頁繼承哪個輸入模板 SVG）、唯一的 `pptx_masters` / `pptx_layouts` 定義，以及 `page_pptx_layouts` 頁面分配；`template_reuse_scope: style`、自由設計和 brand-only 專案使用 `pptx_structure.mode: flat`，那些段整段省略，而不是寫成空值。其餘欄位的空值本身仍是訊號：沒有圖表、沒有圖片，很多時候是設計選擇，而不是漏填。

`page-context v2` 保留為按需投影器。每次呼叫都會輸出繫結 `lock_source.sha256` 的緊湊全域性錨點、當前 §IX/資源/路由 delta，以及大型引用的帶 scope 路徑/SHA 指紋；該投影既不是顏色/字型白名單，也不是替代權威。只有明確的診斷/統計需求，或頁面/模板/圖表的路徑-SHA 問題仍未解決時才呼叫。有效且未壓縮的上下文中做有界精確回修，可以只回讀修改片段並校驗；fresh、已壓縮、外部、來源不明、結構性或投影不符的修改必須完整讀取 Design Spec 與 lock。flat 頁面沒有原型引用；structured 頁面使用權威完整 SVG。manifest 與 text-slot sidecar 只保留為派生工具診斷，不注入頁面創作上下文。

`--record-usage` 在 `analysis/page-context/` 下為實際呼叫的頁面寫入派生快照，記錄輸入 hash 和緊湊 stdout 的實測大小。token 計數按需載入 `o200k_base`；沒有安裝 `tiktoken` 時寫入 `tokens: null`，但不阻塞執行。`page-context-report` 排除過期快照，彙總已有快照並列出唯一引用指紋；統計可以只覆蓋部分頁面。一次載入的大型引用 payload 與其他會話上下文有意不納入統計。

`update_spec.py` 用兩個協調步驟傳播一次有意的 deck 級錨點修改：把新值寫入 `spec_lock.md`，然後字面替換到每一份 `svg_output/*.svg`。工具的範圍**故意收得很窄**——只支援 `colors.*`（HEX 值，大小寫不敏感替換）和 `typography.font_family`（屬性級）。其他欄位（字號、圖示、圖片、畫布）**有意不支援**——它們的替換需要屬性級或語義級理解，風險/收益不值得做批次傳播。當重複出現的上下文值被明確提升為具名語義角色時，反向回寫 lock 同樣合理；但不能只為了清空 checker 的資訊提示而擴充 lock。其他欄位應修改其權威產物並重做受影響頁面。

工具拒絕做備份：依賴 git 回滾。加備份機制只是重複 git 的工作，還會留下過時快照。

---

## 材料 → 規劃 → 實現：餐廳合同

“做飯”不是臨時解釋，而是生成流程的正式所有權模型：

| 餐廳角色 | PPT Master 對應項 | 決策權 |
|---|---|---|
| 顧客與初始食材 | 使用者確認與使用者提供的原材料/素材 | 決定事實、意圖、排除項、材料補充許可，以及要求具體到什麼程度 |
| 選單策劃與備料負責人 | Strategist、`design_spec.md`、`spec_lock.md` 及其負責的材料獲取階段 | 判斷材料是否充分；補齊獲準補充的事實；選定內容、資源、頁面清單、圖表參考 key / 模板版式 key、字型、色板錨點、圖示和裁剪邊界；記錄可選的能力 / 表達建議；在執行前備齊專案級材料清單 |
| 廚師 | Executor | 只使用專案中已備好的材料，以幾何、構圖、層級、間距和視覺處理實現方案；不得改變所選“菜品”，也不得自行找料、換料；可以調整明確標為 suggestion 或 Reference 的欄位 |

**備料有兩個時點。** Topic Research 在最終確認前補充規劃所需的事實：只有主題時立即執行；已有材料時先轉換 / 閱讀，僅在仍有關鍵事實缺口時補齊，而且不獲取任何圖片。AI / web / slice 圖片只能在最終確認以及完整的 `design_spec.md §VIII` / `spec_lock.md` 之後獲取，並在 Executor 開始前進入終態。Strategist 還會在編寫最終方案時解析、同步並驗證圖示 inventory。Image_Generator、Image_Searcher 與圖示同步工具只是 Strategist 負責的備料機制，不是獨立決策者。

**專案中已備好的材料就是邊界。** 圖片和其他宣告型資源，仍須由 Strategist 選定、寫入規劃產物，並保證專案路徑可解析或明確標為 `Needs-Manual`。圖示 SVG 只要已位於 `<project>/icons/` 就屬於已備材料；`spec_lock.icons.inventory` 記錄 Strategist 計劃選用的內建圖示，但不是窮盡式執行白名單。其他目錄中的檔案不構成使用許可。缺料必須返回上游；Executor 不得搜尋、生成、下載、同步或替換資源。

**具體程度決定自由度。** “做麻婆豆腐”鎖定成品身份：火候、口感和擺盤可以發揮，但不能換成番茄炒蛋或豆腐湯。“做一道豆腐菜”則保留了品類內選擇空間。Strategist 可以把這個開放要求收斂成具體方案；如果 Design Spec 有意保留某個維度的開放性，Executor 可以在該範圍內實現。一旦 Design Spec 已經選定具有約束力的結果，執行階段不得重新開啟選擇。明確標為 suggestion 或 Reference 的欄位——包括頁面級首選圖片 pattern——仍是表達建議；Executor 可以在不改變內容、資源、身份和顯式約束的前提下調整。

**點綴只能保持區域性。** 零星的頁面級字型或顏色可以用於增加層級、區分和氛圍，但不能發展成第二套視覺系統。結構性或重複出現的字型、色板角色、資源與跨頁身份 pattern 仍屬於 Strategist 決策；複用前必須先更新 Design Spec/lock。頁面級 §VIII 圖片 pattern 仍是首選構圖參考。

**提示詞重構不變數。** 壓縮提示詞時，必須繼續區分初始材料、使用者確認、Strategist 負責的備料、策略規劃和執行自由。把材料獲取下放給 Executor、把許可變成配額、把靈活實現變成靜默更換資源 / 身份，或把精確的約束計劃降級成近似目標，均屬於語義迴歸。執行時權威位於 [`strategist.md`](../../skills/ppt-master/references/strategist.md) 與 [`executor-base.md`](../../skills/ppt-master/references/executor-base.md)，提示詞編寫規則位於 [`prompt-style.md`](../rules/prompt-style.md)。

---

## 圖片獲取與嵌入

這一階段有多項架構層面的決策：

**provider 專屬 config key，不用通用 `IMAGE_API_KEY`。** 每個 backend 用自己的 `OPENAI_API_KEY` / `MINIMAX_API_KEY` 等等，當前 backend 由顯式的 `IMAGE_BACKEND=<name>` 選定。統一的 `IMAGE_API_KEY` 欄位第一眼看著乾淨，但當使用者同時配了多個 provider 又不確定哪個在生效時會造成靜默混亂——這種 fault 通常只表現為「影像生成結果怪怪的」，找不到清晰失敗點。強制 per-provider key 讓「我現在用的是哪個 backend」從推理變成可讀配置。

**預設寬鬆 license 過濾，配以嚴格模式應對沒法放致謝的版面。** 網路圖片搜尋預設允許 CC BY / CC BY-SA 加內聯致謝——大部分幻燈片都有視覺空間放一個致謝元素。`--strict-no-attribution` 是給全屏 hero image 和緊湊構圖的逃生口，那些場景沒法放致謝又不打破設計。NC（CC BY-NC*）和 ND（CC BY-ND*）自動拒絕，因為 PPT Master 的典型產物會用於商用或修改場景；寬鬆預設 + 這個底線正好對應使用者實際想要的 fail-mode。

**Manifest-first 獲取。** 流水線內的 AI 圖片生成永遠先寫 `images/image_prompts.json`，並渲染旁路 `image_prompts.md`，哪怕只有一張圖。`image_gen.py "prompt"` 這種位置引數形式只保留給一次性除錯，因為它沒有 manifest / sidecar 審計軌跡。網路圖片獲取也類似：多行 web 資源寫入 `images/image_queries.json` 批次執行，並用 `image_sources.json` 追蹤來源和致謝資訊。

**圖片執行路徑以 Design Spec 為權威。** UI 或聊天中的最終確認都先固化為 `design_spec.md §I` 的 `AI Image Acquisition Path`；Image_Generator 根據該值選擇 API、host-native 或 manual，不能在執行階段重新決定。`image_gen.py --manifest` 只屬於 API Path A。當前 CLI 仍保留一個讀取 UI `result.json` 的防誤呼叫 guard，用於在該檔案明確記錄 `host-native` / `manual` 時阻止誤跑 Path A；它不是權威來源，不覆蓋 chat-only，也不能替代 Design Spec 的路線判斷。這是當前程式碼與上游權威鏈尚未閉合的實現差異，不能當作正常消費路徑。

**相關小插畫用一張統一 sheet。** 當 deck 需要三個或更多同風格小插畫時，資源計劃使用一個 AI illustration sheet 行，再用若干 `slice` 行派生元素，而不是分別生成多張小圖。`slice_images.py` 把 sheet 切成具名透明元素，這些派生檔案進入 `images/`，隨後重跑 `analyze_images.py`，讓 Executor 看到真實尺寸。這既是成本規則，也是風格一致性規則：一張 sheet 會強迫這些小元素來自同一種視覺手法。

**Executor 前必須進入終態。** 需要獲取的資源行必須落到 `Generated`、`Sourced` 或 `Needs-Manual`；`Pending` 和 `Failed` 不能漏進 Executor。`Needs-Manual` 可以作為已知佔位 / 依賴繼續進入 SVG 生成，但 Step 7 會在最終匯出前重新檢查必需檔案是否已經存在。

**開發期外部引用，下游分叉成預覽與原生匯出兩套嵌入策略。** 在 `svg_output/` 裡編輯時，圖片是外部檔案引用——快速迭代、單點替換。隨後分成兩種表達：`svg_final/` 對普通點陣圖和受支援的 SVG 資源執行 Base64 內聯，EMF/WMF 則保留外部引用供 native PPTX passthrough；個別資源內聯失敗會計入處理錯誤，但不會回寫作者源或讓 finalizer 整體失敗。native PPTX 則把點陣圖或 Office vector 複製進 PPTX 的 media 資料夾，用 `<a:srcRect>` 表達受支援的點陣圖裁剪。分叉的理由是職責不同：前者服務視覺預覽，後者服務專案轉換器生成的可編輯 DrawingML。`svg_final/` 不是無條件脫離專案資產即可搬運的交換格式，也不作為 PowerPoint 手工“轉換為形狀”的相容源。

**一份渲染鎖、繼承 PPT 色彩錨點、逐圖確定構圖。** 當 deck 包含 AI 生成圖片時，Stage 2 會在每套成套設計方向中確認 deck 級 `rendering`。圖片顏色不再形成第二次使用者決策：Image_Generator 從 `spec_lock.md colors` 的核心 HEX 角色出發，再結合完整 Design Spec 與每項資源按用途推導的 `type` 或 hero-page 構圖。渲染可以在不改變核心角色語義的前提下，按上下文派生色階、材質色、明暗過渡與氛圍色；不得用一套無關的圖片專屬調色替換 deck 身份。重複使用的派生色可以提升為具名 lock 角色。

---

## 圖文版式：Primary 主結構 + Modifier 修飾層

「圖片**怎麼放上幻燈片**」的詞表（完整詞彙在 [`references/image-layout-patterns.md`](../../skills/ppt-master/references/image-layout-patterns.md)）把 81 條穩定編號技法拆成兩層、自由組合：

- **Primary 主結構**（容器佈局 / 圖作畫布 + 原生覆蓋 / 多圖組合）—— 頁面的骨架。一頁可一個也可多個；跨 Primary 的組合，如「側邊對比 + 圖作畫布的註解卡」，是合規的。
- **Modifier 修飾層**（非矩形裁剪 / 遮罩與疊加 / 紋理 / 特殊技法）—— 裝飾層。一頁可疊任意多個，附著在 Primary 之上。

**為什麼顯式允許複合，而不設「一頁一個 Primary」配額。** 這份詞表用於擴充套件構圖選擇，不是層數指標。一頁可以由一個或多個 Primary 構成，並按需要疊加任意數量的 Modifier；每一層都必須對當前敘事或視覺層級有貢獻。需要警惕的是整套 deck 反覆退化為裸的 `#2` / `#3` / `#5` / `#6` 且完全不使用 Modifier，而不是要求每一頁都必須複合。

**為什麼物理拆分兩層，而不是隻打標籤。** 詞表被重排成「Primary 全部在前，Modifier 全部在後」——Strategist 或 Executor 讀一次目錄，就能從結構上內化「兩層」心智模型。編號是穩定 id（`#38` 永遠是「圖作畫布 + 註解卡」，不論它在檔案裡的物理位置），所以 `spec_lock.md`、`design_spec.md §VIII`、歷史 executor 輸出、過往示例裡所有 `#<id>` 引用照樣解析。

**為什麼組合走 Strategist 資源列表，而不是到繪製時才第一次發現。** `§VIII 图片资源列表` 的 `Layout pattern` 列接受 `#<id> + #<id> ...` 表示式——Primary id 加可選 Modifier id；`Crop Policy` 則記錄 `adaptive` 或 `no-crop`。Strategist 必須在 SVG 生成前完整檢視目錄，寫出具體的首選構圖和資訊完整性邊界，並通過 lock 投影讓兩者在 session 重入後繼續存在。Executor 再決定實際表達：它可以調整尺寸、位置、流向與權重，也可以換成另一個目錄 pattern 或普通構圖。資源身份、必用 / 內容義務、`no-crop` 和顯式使用者 / 模板約束仍具有約束力；只有改變這些邊界才需要先更新 Design Spec。

**為什麼真正的硬約束留在上游。** 跨切的 SVG 創作與 PPTX 相容性例外屬於 [`shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 路由的權威集。版式詞表只指向該路由，不再複述合同；每條規則仍只有一個所屬模組，詞表裡也不會留下過期副本。

---

## 專案規範化 SVG 與相容性邊界

SVG 與 DrawingML 的表達模型並不等價，因此主編譯路徑不把“瀏覽器可以渲染”視為“專案可以匯出”。只有在 [`references/shared-standards.md`](../../skills/ppt-master/references/shared-standards.md) 路由到的適用模組中登記了專案規範表達或顯式相容形式，並且擁有確定 DrawingML 對映的詞彙，才屬於可接受輸入。該拆分權威集負責語法、結構、單位、metadata、相容別名、保真度和拒絕條件；本架構檔案只定義分層原則，不復制具體規則。

**為什麼本地複用是編譯期複用，不是 PowerPoint 保留物件。** 接受的創作形式由權威合同定義、共享校驗器執行。校驗通過後，流水線會遞迴實體化引用子樹並重寫克隆區域性 ID 後再匯出；PPTX 回導因此只返回展開後的原語，不重建創作期複用圖。

值得在架構層標記的理由：

- **為什麼需要封閉對映，而不是預設接受普通 SVG。** 專案規範化 SVG 是編譯器中間語言，不是瀏覽器相容層。新增元素、屬性或取值必須同時補齊匯入語義、匯出對映、校驗規則和迴歸驗證；未登記能力預設不進入主編譯路徑。
- **為什麼相容輸入不等於創作許可。** 已登記的歷史別名可以由轉換器確定性歸一化，並由 Checker 給出非阻塞 warning；提示詞、模板和示例仍只生成專案規範寫法。相容面只能服務遷移和人工輸入，不能反向擴大生成語法。
- **為什麼 warning 可以放過。** warning 只表示合法輸出前提下的推薦寫法、確定性歸一化、已知保真度下降或視覺質量風險。它不改變頁面語義，不要求 Executor 回改，也不阻斷髮布；如果某項必須修正才能交付，它就應被定義為 error。
- **為什麼是經驗性，不是從規範推導。** 相容性邊界從真實的 PPT 匯出失敗長出來，不是讀 OOXML 規範推匯出來的。有些理論上能表達的效果跨 PowerPoint 版本仍不可靠，因此合同反映的是實際能交付的子集。
- **XML 良構性仍是前置條件。** SVG 一旦不是合法 XML，尚未進入 DrawingML 相容性階段就會失敗。接受的創作形式集中在權威合同中，避免架構與提示檔案分別維護後發生漂移。
- **相容性校驗在後處理之前執行。** `svg_quality_checker.py` 在 `svg_output/` 上執行；後處理會重寫 SVG，可能掩蓋源級別違規。阻斷性 error 由 Executor 重新寫，warning 不觸發回改。Generate 路線只允許在 final Checker 達到 0 error 後進入匯出；轉換器不重跑完整 Checker，而是獨立校驗編譯對映、ZIP、頁數和 package 結構，並把前置質量報告的階段、阻塞計數與 SVG 源指紋寫入 postflight。

---

## 質量門

**為什麼需要這道檢查器。** LLM 生成的 SVG 不是確定性的——相容性違規會在長 deck 中悄悄混入，只在 `svg_to_pptx` 中途崩或 PowerPoint 靜默丟元素時才暴露。檢查器把「PowerPoint 在第 14 頁匯出失敗」轉化為「第 14 頁違反 SVG 相容性合同」，診斷速度提升一個數量級——這正是讓長 deck 在經濟上可迭代的關鍵。

**為什麼放在後處理之前，而不是之後。** 後處理會重寫 SVG（圖示嵌入、圖片內聯），會掩蓋源級別違規。直接讀 `svg_output/` 抓的是 Executor 的實際輸出，先於任何可能掩蓋 bug 的清理動作。

**為什麼有 first-page 與 final 兩道檢查。** P01 gate 把第一張頁面當作方法樣本：先區分 method-level、page-local 與未覆蓋能力，完整審閱該輪 issue set，再在合併修復迴圈中消除全部 blocking error，並處理選定的 advisory warning。通過後，P02 到末頁連續生成且不插入 checker；final gate 才對完整作者源做釋出前檢查。前者校準方法，後者驗證全集，不能互相替代。

**嚴重性模型：error 阻塞、warning 不阻塞，且有意沒有 auto-fix。** 嚴重性不按“是否符合推薦寫法”劃分，而按“能否確定、合法地對映”劃分：

| 嚴重性 | 判定條件 | 流水線行為 |
|---|---|---|
| `error` | 結構合同被破壞；輸入無對映或有歧義；必要 metadata 缺失；數值非法；轉換後可能違反 DrawingML / PPTX 約束；或可能導致 PowerPoint 修復檔案 | Executor 必須重寫並重新校驗；Generate 路線不得在 final 報告仍有阻塞錯誤時進入匯出。若匯出器讀到帶阻塞錯誤的 final 報告，postflight 標記 `quality_gate=failed`，該產物不得被宣告為成功交付 |
| `warning` | 已有唯一、安全、合法的轉換結果，但輸入不是專案規範寫法，或存在已知的確定性歸一化、保真度下降、視覺質量風險 | 記錄診斷後允許釋出；不要求逐條確認或強制回改 |

質量門沿用設計哲學中定義的三層職責。這裡有意不提供 auto-fix：機械修補可能靜默覆蓋有效的設計意圖，也可能交付一個更差的頁面。

**當前實現邊界。** `svg_to_pptx.py` 會先生成 PPTX，再寫 postflight；`quality_gate=failed` 會得到失敗報告，但這一狀態目前不會單獨讓 CLI 返回非零，也不會刪除已經生成的檔案。缺失、非 final、過期或無法驗證的質量報告會以對應 `quality_gate` 出現在回執中，並使報告進入 `passed-with-warnings`；當前 Step 7 允許這類產物在讀取回執並披露實質 warning 後完成。因而 PPTX 檔案存在或命令退出 `0` 都不等於成功：`failed` 報告絕不能交付，`passed-with-warnings` 則必須結合具體 `quality_gate` 和 warning 判斷、披露。匯出器尚未把 `quality_gate=failed` 獨立收口為非零退出或回滾，這是當前防禦缺口，而不是放寬 error 語義。

如果同一種 warning 持續出現在新生成頁面中，應優先修正提示詞、模板示例或規範說明，使預設輸出回到專案規範寫法；這屬於生成質量問題，不需要把本來安全的相容輸入升級成阻塞錯誤。反過來，如果實踐證明某個 warning 可能產生非法檔案或不確定語義，就必須把合同和 Checker 同步升級為 error。

**為什麼圖表座標驗證掛在同一道 gate。** 圖表頁面有幾何正確性需求（柱高、餅圖扇角、座標軸刻度位置），這些不是結構問題，SVG 合法性規則也抓不到。最自然的捕捉位置就是已經要求 AI 回看自己輸出的那道 gate——把「看一眼你剛生成的東西然後修」的認知上下文打包到一個階段，比把結構和幾何審查分到兩輪 review 更高效。

---

## 後處理流水線

> 工程化轉換階段中每一份產物和每一個模組為何存在，刪除它會破壞哪些工作流。在考慮簡化 `svg_final/` / `finalize_svg.py` / `svg_to_pptx.py` 之前，先讀這一節。

### 後處理產物與工作流

後處理與匯出階段嚴格區分創作源、校驗、預覽、交付與歸檔產物。每一份都服務於一種流水線中無法替代的工作流。

| 產物 | 服務的工作流 | 為何無可替代 |
| --- | --- | --- |
| `svg_output/` | 唯一源、手工編輯入口、`update_spec.py`、`svg_quality_checker.py` | 流水線中唯一**手寫**而非派生的目錄 |
| `svg_final/` | IDE 內即時預覽（VSCode/Cursor 直接開啟 `.svg`）、瀏覽器單頁預覽、手動作為 SVG 圖片插入 | `.pptx` 在 IDE 裡打不開；`svg_output/` 因圖示 / 圖片是外部引用，IDE 中渲染不完整。普通資源儘量內聯，EMF/WMF 保留外鏈；PowerPoint 手工“轉換為形狀”不在支援範圍 |
| `exports/<name>_<ts>.pptx`（native） | 預設主交付物——PowerPoint 中以 DrawingML 形狀形態可編輯 | 預設 DrawingML 物件模型；原生 Chart/Table 與旁白變體同樣可編輯，但擁有不同的物件或播放行為 |
| `validation/svg_quality_report.json` | 機器可讀的最終 SVG 門禁 | 把阻斷錯誤、新增提示、原型繼承項和來源匯入損失分開，併為受檢 SVG 位元組生成指紋 |
| `validation/<output_stem>.report.json` | 已釋出 PPTX 的 postflight 與資源審計 | 記錄實際 ZIP/package part 數量；重新檢查 ZIP 與正式頁數；把內部關係、結構化包、轉場和動畫如實標為構建期強制校驗；只有 SHA-256 指紋與匯出輸入一致時才接受質量報告關聯，同時暴露未解析變數、外部圖片和純通用字型棧 |
| `exports/<name>_<ts>_native_charts_tables.pptx`（需 `--native-charts-and-tables` 顯式開啟） | 讓帶 `data-pptx-replace-with` 標記的 SVG 派生形狀圖表/表格替換為 PowerPoint 原生 Chart/Table 物件 | 帶資料來源和圖表/表格專屬控制的物件；預設 DrawingML shape 本身仍可獨立編輯 |
| `exports/<name>_<ts>_narrated.pptx`（經 `--recorded-narration` 或 `--narration-audio-dir` 生成） | 嵌入匹配到的旁白音訊；完整錄製模式可直接服務自動放映與 PowerPoint 影片匯出 | `--recorded-narration` 要求每頁匹配音訊，並寫入“時長 + padding”的自動推進；低層 `--narration-audio-dir` 允許部分或零覆蓋，只有另加 `--use-narration-timings` 才寫自動推進 |
| `exports/<narrated_stem>.mp4`（可選，經 `powerpoint_video.py`） | Windows PowerPoint 2016+ 下保留動畫與旁白的影片交付物 | 委託 PowerPoint 原生編碼器並等待完成；它是 PPTX 後處理整合，不是第二套 deck 渲染器 |
| `backup/<ts>/svg_output/`（僅預設輸出路徑；目錄建立後複製為 best-effort） | 在不重跑 LLM 的前提下從凍結 SVG 源重建 pptx | 轉換成功後先建立備份目錄再嘗試複製；顯式 `-o` 不建立，複製失敗不阻斷匯出，非 quiet 模式列印 warning，postflight 的 `backup_path` 為空，但目錄建立失敗仍會中斷 |

校驗 JSON 是冷審計產物，不是常規模型輸入。匯出器在程式內部讀取 SVG 質量報告，並在預設非 quiet 流程列印緊湊的 `[POSTFLIGHT]` 回執，包含狀態、質量門結果、Slide 數量、warning 類別計數和產物路徑。成功流程只消費該回執，不載入兩份完整 JSON；只有失敗排查或使用者明確要求審計時才定向提取報告欄位。

### SVG 前處理器有**兩種使用形態**

這是讀程式碼時容易忽略的關鍵事實。共享清理模組、本地引用展開器和 inline geometry materializer 一方面寫盤生成 `svg_final/`，另一方面在 native 轉換中以記憶體形式複用。Checker、編輯器和結構解析器也共享部分幾何解釋，但不屬於本節的產物消費者。

**寫盤消費者** —— `finalize_svg.py` 每次執行都把 `svg_output/` → `svg_final/` 寫到磁碟一次，同時展開專案圖示佔位符和合規的本地 `<use>` 引用。`svg_final/` 隨後供 IDE / 瀏覽器視覺預覽及手工 SVG 圖片插入使用。

**記憶體消費者** —— native pptx 直接讀 `svg_output/`（不經磁碟中轉），依次物化作者 SVG 的 inline geometry、展開專案圖示佔位符、再次物化圖示註入的 geometry、展開合規的本地 `<use>`，最後處理定位文本 run：

| 記憶體呼叫點 | 前處理器 | native pptx 為何需要 |
| --- | --- | --- |
| `svg_to_pptx/drawingml/converter.py` | `svg_to_pptx.geometry_properties` | inline style 中的幾何宣告要先物化為 XML 屬性；圖示展開後需再執行一次 |
| `svg_to_pptx/use_expander.py` | `svg_finalize.embed_icons` | DrawingML 不識別 `<use data-icon="...">`；不展開圖示會靜默丟失 |
| `svg_to_pptx/use_expander.py` | 靜態本地引用展開 | DrawingML 不保留 SVG `<use>` 例項圖；合規子樹必須實體化並獲得例項級獨立 ID |
| `svg_to_pptx/tspan_flattener.py` | `svg_finalize.flatten_tspan` | DrawingML 文本塊無法在段落中跳位置；`dy` 堆疊的多行 `<tspan>` 會塌成一行，`x` 錨定的 tspan 會跑到錯誤的列 |

### 各模組消費者一覽

| 模組 | 寫盤消費者 | 記憶體消費者 | 刪除影響 |
| --- | --- | --- | --- |
| `geometry_properties.py` | `finalize_svg.py` 在複製後及圖示展開後呼叫 | `drawingml/converter.py`；Checker、編輯器與 template structure parser 共享同一解釋 | inline style 幾何屬性無法穩定轉為 XML geometry，預覽、校驗和 native 轉換可能產生不同結果 |
| `embed_icons.py` | `finalize_svg` 的 `embed-icons` 步驟（隨後展開本地 use） | `svg_to_pptx/use_expander.py` | native pptx 丟失全部圖示，`svg_final/` 也失去受支援圖示的視覺閉包 |
| `svg_to_pptx/use_expander.py`（本地引用） | `finalize_svg` 的 `embed-icons` 步驟 | native 轉換器預檢 | finalize/native 匯出失去實體化合規本地複用的能力 |
| `flatten_tspan.py` | `finalize_svg` 的 `flatten-text` 步驟 | `svg_to_pptx/tspan_flattener.py` | **native pptx 中 `dy` 堆疊的多行文本塌成一行** |
| `align_embed_images.py` | `finalize_svg` 的 `align-images` 步驟 | — | `svg_final/` 失去圖片嵌入 → IDE / 瀏覽器預覽和手工插入的 SVG 圖片缺圖 |
| `crop_images.py` / `embed_images.py` / `fix_image_aspect.py` | 被 `align_embed_images.py` import | — | `align_embed_images` `ImportError`，整條鏈路 broken |
| `svg_rect_to_path.py` | — | — | 僅保留為歷史診斷工具，不屬於 `finalize_svg` 或受支援匯出流程；不得據此承諾 PowerPoint 手工“轉換為形狀”相容性 |

---

## 直接 OOXML 路由

不是所有 PPTX 相關請求都應該重新生成頁面。PPT Master 現在為“原生 deck 本身就是編輯物件”的場景提供直接 OOXML 路由。

`template_fill_pptx.py` 是 `scripts/template_fill_pptx/` 包的薄 CLI 入口。analyzer 抽取帶文本槽位、表格、圖表和幾何資訊的 slide library；fill plan 選擇源頁面並確認替換內容；applier 克隆幻燈片並直接 patch XML parts。這條路線故意繞開 SVG：使用者提供 PowerPoint 模板時，通常期望原生母版、佔位符、表格和圖表繼續保持 PowerPoint-native。

`native_enhance_pptx.py` 是已完成 deck 原生增強的穩定入口。它委託 `native_enhance_pptx_core.py`，在專案歸檔副本上直接 patch PPTX package：講稿、頁面轉場、錄製旁白媒體、頁面計時和相關後設資料。舊名稱 `native_narration_pptx.py` 僅保留為精簡的 CLI 相容包裝器。它的契約是保留：已有內容、佈局和格式不重新生成。

這些直接路線會和主流水線共享部分分析原語，但複用深度不同：Template Fill 消費標準 PPTX intake 的 slide library；Native Enhance 只用 `ppt_to_md.py` 理解內容，並從歸檔 package 生成自己的輕量 `slide_index.json`。兩者都不共享 SVG 作者階段和後處理階段。這個分離是有意的：SVG 生成是設計合成路徑；直接 OOXML 編輯是保留路徑。

---

## Native PPTX 轉換器內部

`svg_to_pptx.py` 執行設計哲學中定義的最終防線；本節只解釋這條受約束編譯路線的內部結構。

**為什麼是逐元素派發而不是整體翻譯。** SVG 的層級模型乾淨地對映到 DrawingML 的 group / shape / picture 型別——不需要一個全域性最佳化器去重新規劃幻燈片。每種形狀都有自己窄的翻譯器，簡單到能單獨除錯和單元測試。一張幻燈片的最終質量等於這些獨立區域性轉換之和；這個性質在整體翻譯下脆弱，在元素派發下穩健。

**為什麼匯入型與生成型 metadata 分層。** 匯入 PPTX 時，完整 SVG 可以攜帶高階形狀所需的 metadata、隱藏 carrier 和預覽指紋，因此作為原生載荷後備留在臨時分析工作區且保持不可變。`svg_authoring_view.py` 生成模板建立所用的可編輯 IR：輕量 SVG 通過檔案內 source ref 標識物件，`authoring_manifest.json` 只記錄路徑與初始 hash，不重複儲存原始載荷。`standard` / `fidelity` 創作專案規範化 SVG，只有精確匹配已登記 preset 時才使用 compact authored-preset 組。Mirror 從 IR 物化通過校驗的模板，只為未改且 hash 匹配的 Slide-local/slot ref 重新接入轉換器已支援的 metadata；固定結構層保持直接原子，不支援或已修改的物件保留當前 SVG fallback，IR 專用 ref 不進入最終模板 SVG。

**為什麼只有一條 PPTX 編譯路線。** Native 匯出把作者 SVG 中受支援的元素逐個翻譯成 DrawingML 形狀。常規 deck 路線讀取 `svg_output/`；使用者需要時，create-template 對通過校驗的模板原型呼叫同一 structured 編譯器，生成 `exports/<id>_template_preview.pptx` 作為審閱證據。專案不會把整頁 SVG 媒體或另一套點陣圖渲染打包成第二類 PPTX。`svg_final/` 仍由常規 deck 的強制後處理生成，但只承擔派生視覺預覽和 SVG 圖片插入，不為 PowerPoint 手工“轉換為形狀”提供相容兜底。

**為什麼結構化複用路線必須在視覺生成前確定結構。** Master 和 Layout 不是後處理階段才發現的結果。使用 `template_reuse_scope: mirror|layout` 時，Strategist 在 SVG 生成前寫出唯一 Master/Layout 定義和完整頁面分配；Executor 在構圖時同步寫入這些身份、固定原子元素和槽位，匯出器只編譯宣告。`template_reuse_scope: style`、自由設計與 brand-only deck 做的是相反的取捨：保持 `mode: flat`，所有物件留在 Slide 本地，不寫任何結構 metadata，匯出時只獲得一個屬於本專案的乾淨 Master/Blank-Layout 殼。舊輸入可以為新的 `create-template` 工作區提供參考，但不存在原地升級結構的路線；兩種生成模式都不會觸發啟發式 Master/Layout 提升或 placeholder 推斷。

**為什麼 Master/Layout 視覺必須原子化。** 一個 Master 或固定 Layout 物件必須是根節點的直接子元素。匯入 PPTX 時，group 的 transform、opacity、style 和 z-order 會下推到各個原子物件。這個選擇有意放棄來源 group 的整體編輯層級，換取簡單、可比較、可確定重建的結構歸屬，避免巢狀結構歧義。

**為什麼 Layout 槽位使用 group。** 一個可複用槽位是頂層 `<g>`，攜帶語義型別和設計區域 bounds。普通槽位恰好包含一個相容 carrier；匯出時 carrier 被解包並繫結成真實 Slide placeholder。無法由單一 placeholder 表示的複合 `object` 區域走顯式 proxy 降級：可見 group 保持普通 Slide 物件，隱藏透明 placeholder 負責 PowerPoint 繫結。Layout 也可以零槽，因此純視覺頁面無需製造假全頁槽位。

**為什麼可複用 bounds 是設計區域，不是量出來的文本框。** bounds 來自安全區、分欄、面板內框或圖片框，而不是字形寬度、行數或當前內容緊包圍盒。當前 Slide 保留自己的 carrier 幾何，因此只要語義構圖相同，4:6、3:7、5:5 的例項都可複用同一 Layout。文本長度不會意外拆分或改變可複用合同。

**為什麼內部應用計劃保留兩個欄位。** Strategist 推導 `template_reuse_scope`，記錄字面映象複用、結構化版式複用或 flat 風格參考；structured 計劃再推導 `template_adherence: strict|adaptive`。`page_layouts` 記錄完整創作原型，`pptx_masters` / `pptx_layouts` 記錄唯一可複用定義，`page_pptx_layouts` 記錄頁面分配。strict 保持宣告的原型合同；adaptive 保持原型 Master，只有固定 Layout 原子或槽位 topology/bounds 改變時，Strategist 才可宣告新 Layout。若製作過程暴露出這一需求，執行必須退回上游，待 Strategist 更新、回讀並校驗定義與分配後才能繼續；匯出器不會事後推斷。這些是匯出器內部值，不是使用者確認選項。模板定義即使暫時沒有頁面使用，也能註冊進最終檔案。layout 的皮膚由專案控制；mirror 還要保持字面視覺與文位元組點拓撲。`style` 不帶 adherence 或結構 mapping。

**為什麼顯式版式把文字預設值分在 Master 與 Layout 兩層。** Flat 與 structured 匯出都會把鎖定的 title 字號和確定性的九級 body 層級寫入 Master 文本預設值，同時保留原有縮排與專案符號設定；在 structured 路線上，每個 Layout 文字槽位還會把 carrier 首個 run 的字號寫入一級預設值，同時保留提示文字的直接字號。這樣，插入或重置 placeholder 時仍能繼承 Layout 特定尺度，而生成 Slide 上的直接 run 不變。

**為什麼 structured 輸出要在釋出前回讀。** 後設資料預檢不能證明 package 序列化保留了所有 relationship 與註冊資訊。匯出器會重新開啟臨時 PPTX，把已釋出 Slide 與完整 Master/Layout roster 分開校驗，包括沒有任何 Slide 使用的定義；同時核對 Presentation → Master → Layout → Slide 註冊鏈、物理 part/content-type roster、選擇器身份、固定物件順序、placeholder 型別/有效索引/bounds、carrier 繫結、隱藏 proxy 與零槽 Layout，只有通過後才釋出。

**為什麼 Create Layout / Create Deck 分為創作模式和保留模式。** `pptx_template_import.py` 輸出分層 Master/Layout/Slide 參考和 native 結構事實。`standard` / `fidelity` 把這些素材和視覺當參考，再按照確認後的可複用行為創作新拓撲。Mirror 則把已驗證的來源 roster 與拓撲一對一物化到新工作區，只允許顯式 structured 合同要求的機械歸一化，不補造缺失事實。原始 PPTX 保持為不可變分析證據，不成為最終模板依賴。Create Brand 沒有結構複製策略。

**為什麼 create-template 在兩種範圍都使用同一工作區路由。** `create-template` 仍以寫入索引的 `library` 為預設，也可寫入已初始化專案。兩種根目錄都要求 `templates/`；`images/`、`icons/` 和按需生成的 `exports/` 只有存在真實內容時才出現，已有 SVG 素材的引用規則也一致。因此工作區可直接遷移和複用，不需要全域性庫專用 package 分支或縮減的專案分支。唯一範圍差異是全域性索引註冊；兩種範圍共享同一可遷移工作區合同，但只有 Layout / Deck 擁有 structured SVG 合同，Brand 仍是 identity-only。

**為什麼模板 SVG 保持完整卻仍能編譯成原生結構。** 模板 SVG 會重複攜帶繼承的 Master/Layout 視覺和示例 Slide 內容，因此可獨立開啟。生成時由 `page_layouts` 選擇該原型，輸出 SVG 仍保持視覺閉包。匯出器移除重複繼承原子、生成真實 Master/Layout part，並把槽位 carrier 與 Slide-local 內容留在 Slide。

**為什麼 PowerPoint 原生 Chart/Table 重建使用顯式替換 marker，而不是自動替換物件。** 獨立的 `pptx_to_svg.py` 匯入器只為已驗證的表格 / 圖表子集輸出可見 SVG fallback、`data-pptx-replace-with` 與 `<metadata type="application/json">`。生成型 deck 只在 Strategist 將 §IX 頁面塊標為 `Native-ready: yes` 時準備這組內容；§VII 只儲存正向 catalog reference，catalog marker 只是能力示例，不替專案做決策。父組 marker 決定 payload schema；普通 shape 與 connector 不使用該合同。表格匯入覆蓋精確的物理行列 topology、slave 為空的規範矩形 merge、安全的 solid/no-fill 逐邊 border、純文本多段落，以及封閉的 run 級富文本段落。富文本段落包含非空 `runs`；每個 run 必須有 `text`，並且只能使用 `bold`、`italic`、`underline`、`strike`、`color`、`font_size`、單一 `font_family`、`lang` 和 `alt_lang`。不含非空 `effectLst` / `effectDag` 的來源展示型 run XML 會歸一化到該 schema；表格單元格 run 效果則會停用原生替換，並新增阻塞效果診斷。帶 relationship 的文本、擴充套件節點、換行、欄位、tab、專案符號、破損文本 topology、非規範 merge、不安全 border 與非純色填充仍保持 fallback-only。表格樣式 `{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}` 的規範化 fallback 會解析 `wholeTbl`、`firstRow`、橫向帶狀行、主題顏色 / 字型和直接格式覆蓋；這不代表完整 built-in/custom style registry。

受支援的柱 / 條 / 折線 / 面積、餅 / 圓環、散點 / 氣泡圖在沒有 baked preview 時會生成確定性、可讀的 SVG fallback，並標記 `data-pptx-fallback-kind="normalized"`。匯入器還覆蓋已驗證的柱 / 折線 / 面積組合圖、規範四系列 OHLC stock、數值日期軸面積圖、採用封閉 `axes.x` / `axes.y` 合同的散點 / 氣泡圖、radar、安全的 `of_pie` `serLines`、座標軸 / 標題 / 圖例歸一化，以及有界的柱 / 條圖 gap/overlap 場景。`gapWidth` 只接受 `0..500` 內的單個整數，`overlap` 只接受 `-100..100` 內的單個整數；這兩個表現欄位在 native 輸出中有意歸一化，非法、重複或越界輸入 fail closed。組合圖可保留主 / 次 plot 各自的 category cache 與 workbook range。XY 匯入根據各系列一致的有效 line/marker/smooth 狀態推導 `scatter_style`。封閉的 category/value 與 XY 軸合同為 native read-back 保留 kind、position、visibility、label position、number format、min/max/major unit、reverse 和 major gridlines；規範化 XY fallback 只消費兩個 `major_gridlines` 開關。

ChartEx 匯入被有意限制為 7 個已驗證資料模型：`treemap`、`sunburst`、`histogram`、`pareto`、`box_whisker`、`waterfall` 與 `funnel`。其受支援的層級 / 分類 / 數值 / 系列 / 小計資料 topology 可經 native 輸出再匯入回讀。數值 cache 必須非空且有限，count/index 必須是規範非負整數，並滿足精確連續的 point topology。來源 ChartEx 的樣式、座標軸、標籤與 binning 可能歸一化；這不代表任意 ChartEx 匯入或表現層保真。C4/C5 不擴充套件 normalized renderer，因此 renderer 外的有效 active 型別在沒有源 preview 時仍使用 `data-pptx-fallback-kind="placeholder"`。完整 `AxisSpec`、任意 ChartEx 家族、任意富文本 OOXML、旋轉 / 翻轉 / 3D 圖表、未驗證的 combo/stock/date-axis 變體及其他未建模語義仍不在 active 匯入子集內。native replacement 仍可能歸一化 payload 外的表現細節，並保留資料模型優先 warning。預設匯出把 fallback 子元素作為可編輯 DrawingML shape；只有 `--native-charts-and-tables` 才啟用帶資料來源和物件專屬編輯模型的 PowerPoint 原生 Chart/Table。每個 active 匯入 marker 都帶有 `data-pptx-import-source="pptx"` 與 `data-pptx-fallback-sha256`：可見 fallback、可達 SVG definition/reference 或 marker transform 變更後，native replacement 會 fail，而不是丟棄 SVG 編輯；仍保留匯入來源標記但沒有 hash 的舊匯入 marker 相容並給出 warning。生成型創作會同時省略匯入來源和靜態 baseline，且不產生 warning。該 importer/exporter 組合只用於重建，不替代 `template-fill-pptx` 或 `native-enhance-pptx` 的保留型路線。

---

## 動畫與轉場模型

值得講的設計選擇是動畫**錨點**，不是效果列表。

**為什麼把物件動畫錨在頂層 `<g>` group。** PowerPoint 的動畫時序基於
形狀 ID——每個被動畫的物件都需要穩定的 shape ID。給單個原語做動畫會產出
每頁 30+ 個分別運動的原子，只給整頁做動畫又會損失視覺敘事。頂層 group
本來就是 Executor 標記邏輯內容塊的自然粒度，因此進入、強調、動作路徑和退出
可以共用同一套語義單元。

**為什麼頁面結構自動跳過。** 頂層 group 只要帶有 `data-pptx-layer`，就被視為不可動畫的結構層；當前實現也把任何顯式 `data-pptx-placeholder` 視為靜態頁框，`background` / `header` / `footer` / `decoration` / `watermark` / `page-number` 等 role 再補齊其餘頁面 chrome。ID token 回退不是按整份 SVG 啟停，而是僅對同時缺少 layer、role 和 placeholder 的單個頂層 group 生效，因此新舊標記混合的 SVG 仍可能只在未標記 group 上使用 legacy ID 判斷。另有一個有界的原語相容回退：只有整頁沒有頂層 group、尚未找到任何動畫目標且根原語候選為 1–8 個時，才把這些根原語作為錨點。這是當前掃描器的真實作用域；動畫 reference 中“僅 marker-free legacy SVG”這一整頁口徑仍需另行與實現對齊。

**為什麼物件級動畫用 sidecar，而不是 SVG 屬性。** SVG 繼續作為靜態視覺源。自定義 PPTX 動畫屬於匯出策略，所以物件級覆蓋放在可選的 `animations.json`，按 slide stem 和頂層 group id 關聯。這樣不會把 PowerPoint 專用後設資料塞進 SVG，同時仍能在預設全域性動畫不夠用時調整順序、效果、延遲和時長。

**為什麼錄製旁白讓自動推進時長跟著片段時長走。** 錄製旁白模式面向影片匯出，影片裡沒有演講者去點選。該模式會逐頁探測音訊實際時長，並把自動推進設定為“音訊時長 + `--narration-padding`”；padding 預設是 0.5 秒，用於避免音訊尾部被切斷。它不使用估算朗讀速度或固定每頁時長。

**為什麼錄製旁白拒絕 on-click 物件動畫。** PowerPoint 可以在真實排練時記錄
點選計時，但 PPT Master 不合成物件級點選事件。錄製旁白路徑只寫頁面級音訊和
頁面自動推進計時，所以單擊觸發的物件效果會讓匯出依賴額外的 PowerPoint 人工
排練。使用 `--recorded-narration` 匯出的 deck 必須採用無點選物件動畫
（`after-previous` 或 `with-previous`）。

**為什麼原生影片匯出保持獨立命令。** 音訊合成和 PPTX 打包屬於跨平臺專案操作；PowerPoint 影片編碼則是 Windows 桌面整合。`powerpoint_video.py` 接收最終帶旁白 PPTX，呼叫 `CreateVideo` 並輪詢 `CreateVideoStatus`，對呼叫方呈現同步結果，同時避免把 Office 自動化耦合進 TTS backend。

---

## 維護邊界：不要合併什麼

下面這些“簡化”都有明確代價。除非要有意識地重新設計周邊架構，否則應把它們視作反向契約。

| 不要合併或新增 | 原因 |
|---|---|
| 不要把模板名或風格短語模糊匹配到庫路徑 | Step 3 必須確定性觸發；選錯模板比自由設計更難恢復 |
| 不要把原生 PPTX 模板當作 Step 3 模板 | 作為模板 / 頁面殼時應走原生克隆與填充；作為來源、1:1 beautify 或可重構材料時分別走對應 Generate 邊界，而不是把 PPTX 直接交給 Step 3 |
| 不要把 `template-fill-pptx`、`beautify-pptx`、`native-enhance-pptx` 合成一個“PPTX 最佳化”路線 | 三者的保留契約不同：原生填充、1:1 重排、直接增強是三種操作 |
| 不要用指令碼批次生成 Executor SVG 頁面 | 跨頁設計判斷依賴主代理逐頁連續創作 |
| 不要把 `image_analysis.csv` 當持久快取 | `images/` 是即時工作目錄；事實必須按需重算 |
| 不要讓 `svg_final/` 成為 native PPTX 預設輸入 | `svg_final/` 為視覺預覽而重寫資源，native 轉換需要 `svg_output/` 的高保真語義 |
| 不要把 `svg_final/` 當作可還原形狀或無外部依賴的交換格式 | 它服務視覺預覽和 SVG 圖片插入，但 EMF/WMF 保留外鏈例外；PowerPoint 手工“轉換為形狀”不在支援範圍 |
| 不要預設開啟物件級動畫 | 頁面轉場是預設；物件動效是顯式匯出策略 |
| 不要把 visual review、旁白、圖表校準或動畫定製預設塞進每次執行 | 這些工作流觸發範圍窄，且有額外依賴 |
| 不要用檔案複製替代 `finalize_svg.py` | finalize 會嵌入圖示 / 圖片、展開特殊文本並準備預覽產物 |
| 不要在主流水線裡把 `analysis/<stem>.slide_library.json` 當作第二份圖表數值來源 | Markdown 擁有內容數值；除非直接 PPTX 工作流接管，否則 intake 圖表 / 表格條目只是結構摘要 |

---

## 頂層路線與支撐檔案

[`workflows/index.md`](../../skills/ppt-master/workflows/index.md) 是僅供維護者使用的目錄，不進入任務載入鏈。執行時路線選擇以 [`workflows/routing.md`](../../skills/ppt-master/workflows/routing.md) 為權威。PPT Master 只有四條頂層產物路線：Generate PPTX、Create Template、Fill Native PPTX、Enhance Native PPTX。使用者請求只能進入其中一條；任何支撐檔案都不與它們競爭。

支撐檔案保持拆分，只是為了收緊路線合同，並在需要時載入可選上下文：

| 分類 | 檔案 | 歸屬路線 |
|---|---|---|
| 生成 profile | `beautify-pptx` | Generate PPTX；逐字措辭、頁數與頁序 1:1 凍結 |
| 模板子工作流 | `create-brand`、`create-layout`、`create-deck` | Create Template 在“僅身份 / 品牌中立且應用中立的結構 / 應用契約與身份結構一體化”中只分派一個 |
| 模板輸入階段 | `apply-template-workspace` | Generate PPTX Step 3；只在顯式工作區根目錄觸發時載入 |
| 生成階段 | `topic-research`、`resume-execute`、`refine-spec`、`verify-charts`、`visual-review`、`live-preview`、`customize-animations` | Generate PPTX 中各自定義的 intake、planning、editing、quality 或 post-processing 節點 |
| 共享階段 | `generate-audio` | Generate PPTX 後處理，或 Enhance Native PPTX 的旁白整合 |
| 治理檔案 | `failure-recovery` | 四條頂層路線的全域性停止 / 繼續規則；Generate PPTX 的具體故障矩陣與續跑入口 |

這種分類是職責邊界，不是檔案命名偏好。只有出現不同的產物生命週期和修改模型時，才新增頂層路線；Create Template 內按模板型別區分的執行歸入子工作流，路線內的可選行為歸入 profile 或 stage，跨路線政策歸入 governance。
