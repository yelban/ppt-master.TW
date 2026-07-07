# Roadmap

[English](../roadmap.md) | [中文](./roadmap.md)

---

> PPT Master 是單人維護的開源專案，按**優先順序**而非時間表推進。這份 roadmap 用來統一對外預期：已經做了什麼、在持續維護演進什麼、暫時不打算做什麼。優先順序會隨使用者反饋和實際使用訊號調整，不承諾時間視窗。
>
> 專案當前定位：**AI 從零生成 SVG → DrawingML 原生可編輯 PPTX**。這條路線的核心是「跨四渲染器的位置保真 + 真原生形狀」，所有方向都圍繞這條主軸展開。

---

## 近期能力演進

近兩個月的能力面擴張。只列結構性的，單 flag / 增量最佳化看 commit log。

### 2026-03（真原生 PPTX 路線成型）

- **直接匯出原生可編輯 PPTX** — `svg_to_pptx` 補齊 glow / rotate / text-decoration / stroke-linejoin，整條 SVG → DrawingML 鏈路開始可用
- 圖表 / 佈局模板 JSON 索引上線，AI 選型路徑打通

### 2026-04（管線規模化）

- **無源生成**：`topic-research` 工作流支援「只給主題、不給原始檔」
- **PPTX 匯出質變**：SVG clipPath → DrawingML picture geometry、marker → 原生箭頭、輸出歸集到 `exports/`
- **圖表庫 70 個 + 圖示三庫**（simple-icons / phosphor-duotone / brand-logo）
- **`spec_lock.md` 機器可讀契約**：Strategist 鎖定後 Executor 每頁強制重讀，跨頁一致性有了保證
- **元素級動畫預設開啟** + 旁白音訊 / 影片匯出([`workflows/generate-audio.md`](../../skills/ppt-master/workflows/generate-audio.md))

### 2026-05（視覺編輯 + AI 圖系統化）

- **Live Preview 進入主流程**（[`workflows/live-preview.md`](../../skills/ppt-master/workflows/live-preview.md)） — 瀏覽器即時預覽 + 點選元素寫要求 + 「apply my annotations」讓 AI 重做該區域（基於 [@WodenJay](https://github.com/WodenJay) [PR #85](https://github.com/hugohe3/ppt-master/pull/85)）
- **任意 PPTX 復刻為模板**（[`workflows/create-template.md`](../../skills/ppt-master/workflows/create-template.md)） — PPTX → SVG 逆向 + OOXML 主題 / 母版 / 版式 / 資源提取
- **AI 圖三維繫統** rendering × palette × type + Strategist h.5 鎖定，下游消費固定契約
- **AI 圖 `hero_page` 雙檔** — 區域性插圖 + 整頁主角圖共存
- **品牌身份預設子系統**（[`workflows/create-brand.md`](../../skills/ppt-master/workflows/create-brand.md)） — 提取並複用品牌色板 / 字型 / Logo / 語調
- **視覺自檢工作流**（[`workflows/visual-review.md`](../../skills/ppt-master/workflows/visual-review.md)） — 按 rubric 逐頁自查 AI 生成的 SVG
- **AI 圖 Type 概念邊界澄清** — Type 收窄回「local 資訊圖的內部幾何骨架」(11 個真骨架);原 4 個偽 type (hero/background/portrait/typography) 折回 `page_role: hero_page` + 4 條構圖通則(single-subject / portrait / typographic / atmospheric);hero_page 文字分層規則(關鍵視覺詞 embedded、可改文字走 SVG)
- **Brutalist AI 報章示例 deck 交付**（[`examples/ppt169_brutalist_ai_newspaper_2026/`](../../examples/ppt169_brutalist_ai_newspaper_2026/)） — P0 三檔第一檔落地：滿版小字 + 不規則欄寬 + halftone 黑白圖 + 單點紅 + 真原生 shape，10 頁編輯部年報實壓「文字位置精度 + 跨頁一致性」
- **Kubernetes Blueprint 示例 deck 交付**（[`examples/ppt169_kubernetes_blueprint_2026/`](../../examples/ppt169_kubernetes_blueprint_2026/)） — P0 三檔第二檔落地：等距工程圖美學 + 藍圖青/琥珀色板 + 全手寫 SVG 幾何（無 raster 圖）+ 自定義"逐筆繪製"動畫，10 頁 Kubernetes 架構走讀實壓「幾何形狀泛化 + chart 結構擴充套件性」
- **AI 圖 `custom` 兜底出口** — `rendering` / `palette` / hero 構圖三處允許宣告 `custom` + 一段 `*_behavior` prose，替換原"找不到匹配就硬塞 vector-illustration / cool-corporate"的假兜底；端到端契約：[`image-renderings/_index.md`](../../skills/ppt-master/references/image-renderings/_index.md) §1.5 + [`image-palettes/_index.md`](../../skills/ppt-master/references/image-palettes/_index.md) §2 + Strategist h.5 hard-rule（每維 ≤1 custom，單候選可雙 custom）+ spec_lock 欄位 + Image_Generator Step 2 消費分支
- **Template 架構三分類收口**（[`docs/zh/templates-architecture.md`](./templates-architecture.md)） — brand / layout / deck 三獨立目錄 + 每類獨立 schema + 段級合成 + git-style 衝突解決；SKILL.md Step 3 按 kind 分支處理，觸發規則仍是「顯式路徑才觸發」
- **Pattern 填充 PPTX 安全網** — `svg_quality_checker.py` 現在對未標 `data-pptx-pattern` 的 `<pattern>` 元素髮 warning（會靜默回退 `ltUpDiag` 斜紋）、對超出 OOXML `ST_PresetPatternVal` 列舉的值發 error（schema 校驗失敗 PPT 無法開啟）；`shared-standards.md §7` 落地了完整 preset 清單和 `<rect fill="<bg>"/>` 子元素約定
- **LaTeX 數學公式渲染上線**（[`scripts/latex_render.py`](../../skills/ppt-master/scripts/latex_render.py)） — Strategist 在 Typography 確認中鎖定 `mixed` / `render-all` / `text-only` 三檔策略，顯式寫 `images/formula_manifest.json`；指令碼走 codecogs → quicklatex → mathpad → wikimedia 四源 fallback chain，輸出透明 PNG 進 §VIII 表的 `Acquire Via: formula` / `Status: Rendered` 行；公式密集型 deck（學術 / 工程 / 教學）首次擁有原生渲染路徑，規則面禁止掃原始檔 `$...$` 自動渲染（公式選取是 Strategist 決策）
- **即時預覽直接編輯 — L1 / L2 / L3**（[`workflows/live-preview.md`](../../skills/ppt-master/workflows/live-preview.md)） — 瀏覽器編輯器新增無需 AI 往返的確定性就地編輯：文字內容（L1）、fill / stroke / font-size 等樣式屬性（L2）、以及畫布上的幾何操作（L3）——在選中元素上拖拽即移動、方向鍵微調（`Shift` = 10px）、多選、加右鍵重疊選擇器選取堆疊元素。編輯支援 `Ctrl+Z` 撤銷 + 合併，點 **Apply changes** 寫回 `svg_output/`；移動經 finalize / 匯出保位（移動的 text、提升的多行 tspan、重定位的 icon 都在 PPTX 中如實再現）。重新匯出仍由對話觸發；畫布上的縮放手柄尚未實現（縮放走幾何輸入框）

### 2026-06（mode/視覺風格雙 catalog + PPTX 入口與內容策略擴充套件）

- **任意 PPTX 復刻設計 → 內容回填路線**（[`workflows/template-fill-pptx.md`](../../skills/ppt-master/workflows/template-fill-pptx.md)） — 使用者給一份現成 `.pptx` 加新材料 / 主題、要求「複用這套 deck 的設計 / 把內容填回去」時，走這條獨立工作流直接編輯 PPTX，不進 SVG 生成管線。輸出仍是原生可編輯 PPTX（複用原 slide 的形狀 / 版式而非截圖回填），過程做私有部件隔離、暴露圖表資料、容量校驗；觸發同模板規則——顯式要求複用既有 deck 才進，刻意不做改版式 / 加頁 / 換圖（那是從零生成主路線的活）。與下文 Non-goals 的 #53 區分見該節
- **三個 executor 退役 → mode + visual-style 雙 catalog**（[`references/modes/`](../../skills/ppt-master/references/modes/) + [`references/visual-styles/`](../../skills/ppt-master/references/visual-styles/)） — 原三個 `executor-*.md`（general / consultant / consultant-top）把「領域 · 受眾 · 說服 · 敘事」捆在一條線；拆成兩個正交 catalog（照 `image-renderings` 範式：扁平目錄 + `_index` + 按需讀 + Strategist 鎖一個）。**mode** = 講解骨架（`pyramid` / `narrative` / `instructional` / `showcase`，consultant + top 因敘事核心相同合併為 pyramid）；**visual-style** = SVG 排版美學（`swiss-minimal` / `editorial` / `soft-rounded` / `dark-tech`，各 paired 一個 image-rendering，**零 HEX**——顏色真值守在 confirmation e + image-palettes）。Strategist `§d` 雙層獨立鎖定 `mode` + `visual_style` 進 `spec_lock`，Executor 載入兩個 locked 檔案；任意 mode × 任意 style 自由組合，渲染座標仍留 `templates/charts/`
- **提示詞約束強度三檔解耦**（[`docs/rules/prompt-style.md`](../rules/prompt-style.md) §4） — 規則（`Hard rule` / `Forbidden`）/ 預設（`Default — … may override`）/ 參考（`Reference — not a constraint`）三檔顯式化 + 「客觀失敗 vs 品味」判據 + checker 邊界，讓模型對「該守 vs 可破」一目瞭然；visual-style catalog 全程用 Reference 強度
- **visual-style catalog 擴充至 18 個，與 image-renderings 對齊 + 示例庫回收** — 先從[示例庫](../../examples/)提煉 4 個（`brutalist` / `blueprint` / `memphis` / `zine`），再補齊 [`image-renderings`](../../skills/ppt-master/references/image-renderings/) 裡有排版對應物的手繪 / 紋理風格 6 個（`sketch-notes` / `ink-notes` / `chalkboard` / `paper-cut` / `vintage-poster` / `pixel-art`），再回收示例庫裡仍未覆蓋的獨立氣質：`ink-wash`（新中式水墨留白，源 藏拙 / 李子柒）· `glassmorphism`（深底磨砂玻璃 + 流光，源 glassmorphism_demo，從 soft-rounded 獨立）· `photo-editorial`（滿版攝影主導、文字點題，源 Pritzker / fashion_weekly）· `data-journalism`（Bloomberg/Economist 新聞資訊圖，多欄微圖表 + 資料側欄，源 global_ai_capital）。catalog 重組為 5 組（企業產品 / 編輯出版 / 表現印刷 / 手繪筆觸 / 特殊）。**關鍵判據**：一個 rendering 升 visual-style 的前提是它定義「整頁版面語言」而非「插入圖的樣子」——故 corporate-photo「攝影主導版面」該建（photo-editorial），而 nature / warm-scene / fantasy-animation 等純氛圍 rendering 仍只配對、不單建。全程零 HEX、Reference 強度
- **mode catalog 擴檔至 5 個：加 `briefing`** — 補上「中性資訊平鋪」這一格：無論點 / 無故事 / 不教學 / 不衝擊，topic 標題、等權鋪事實、完整可掃讀，服務週報 / 參考冊 / 目錄 / 會議材料 / FAQ 這類「只告知不論證」的 deck。五個 mode 自此更接近 MECE 地切分**表達意圖**：說服（pyramid）· 講故事（narrative）· 教會（instructional）· 震住（showcase）· 只告知（briefing）。`_index` 加了 `briefing` vs `pyramid` 的灰區判據（「要不要造個 thesis 才塞得進 pyramid → 那就是 briefing」）。五個預設之外加一個 `custom` 兜底，承接預設蓋不住的 bespoke 方向（特殊節奏 / 多 mode 融合 / 特定姿態）——使用者點名**或策略師推薦**皆可，與所有鎖一樣由使用者確認；一份 deck 永遠只鎖一個值，融合=一個 custom 描述多幕。唯一要避免的是「預設明明貼合卻圖省事甩 custom」。這與「使用者自帶大綱 / 方向覆蓋 mode」是同一條真值優先原則
- **mode / visual-style 體系真實 deck 驗證完成 + 四項校準收緊落地** — 5 mode + 18 visual-style + `custom` 逃生艙在 5 份覆蓋性 deck 上跑過驗證（briefing×data-journalism / narrative×photo-editorial / instructional×chalkboard / showcase×glassmorphism / custom×zine，其中 narrative 一份走 AI 圖生成分支）：**選型零誤判**（四對 Close-calls 灰區引力全被觸發且全抗住）、**紀律全落實**（零 HEX / Reference 強度 / 整頁版面語言）、**custom 機制可用**（`mode_behavior` 散文段落撐過 10 頁生成、能講成大白話讓使用者確認）、**mode ⟂ visual_style 正交成立**（任意組合無串味，含「keynote/釋出會=mode 不是 style」路由正面驗證）、匯出 5/5 deck × 全頁 0 失敗。據真實訊號收緊四處：`strategist §e` 按 visual_style 預判中性檔位一次鎖全（消除連續三份的 Executor 中途補色）、`executor-base §1` 套模板頁重皮到當前 visual_style（模板供結構不供皮，映象模板仍按 §1.1 逐字保留）、`briefing §1` 的 `core_message` = 本頁覆蓋什麼而非證明什麼（briefing 專屬例外，全域性 §IX 論斷語義保留給 narrative/instructional/pyramid）、`svg_quality_checker` 修字型 drift 誤報（按定界符匹配 + font-stack 歸一化）+ 放寬 showcase mode 與 poster 類 visual-style 的字號上限
- **可選 spec 複核環節上線**（[`workflows/refine-spec.md`](../../skills/ppt-master/workflows/refine-spec.md)） — 策略師確認階段後新增一個 opt-in 停頓點：使用者明確要求時（預設 OFF），Strategist 先產出完整 `design_spec.md` + `spec_lock.md`，停下來讓使用者對 spec 任意部分（大綱 / 配色 / 排版 / 版式 / 圖片策略 / page rhythm）深入討論修改，改完同步兩個檔案再進生成。與 split-mode 同構——不主動觸發、預設管線零變化，僅在策略師確認階段裡多一行 opt-in 提示。複核視角（邏輯清晰度 / 資訊密度 / 焦點 / 口語化 / 感染力 / 章節配比 + 各設計維度）只給方向、不落任何數字閾值（`Reference` 強度）。啟發自 [@cuberoocp](https://github.com/cuberoocp) [issue #173](https://github.com/hugohe3/ppt-master/issues/173)
- **互動式視覺化策略師確認頁（Step 4）**（[`scripts/confirm_ui/server.py`](../../skills/ppt-master/scripts/confirm_ui/server.py)，欄位 schema [`scripts/docs/confirm_ui.md`](../../skills/ppt-master/scripts/docs/confirm_ui.md)） — 策略師確認階段從純聊天升級為瀏覽器視覺化頁面，Step 4 預設自動拉起：可列舉欄位（canvas / mode / visual_style / 圖示 / 圖片用法 / 公式與生成策略）從 `catalogs.json` 出常用項、生成型欄位擺候選——配色 swatch、字型即時預覽（CJK / Latin 各自獨立）、AI 圖 rendering × palette 候選；並支援自定義 HEX 即時 swatch 反饋、配色 × 字型組合的即時合成預覽、canvas 尺寸聯動建議正文字號區間。與 Step 6 Live Preview **共用 `5050` 埠**（永不同時跑，確認頁在 Step 4 末尾自動 `--shutdown` 讓出埠；埠被佔則自動順延到下一個空閒口）。原則上**聊天始終是 canonical 通道、確認頁只是便利層**：頁面寫出的 `result.json` 對推薦值具權威性、由下游就地消費（圖片計劃 / `image_strategy` / 字型 / split 與 refine-spec 開關都從中讀取），任何打不開 / 超時 / 無 GUI 的情況都無損回退到聊天總結路徑
- **原始檔轉換保真度提升一批** — 源材料進管線時更少丟資訊：`doc_to_md` 把 Word 裡的 OMML / Office Math 公式轉成內聯 LaTeX、`pdf_to_md` 識別 `Figure N |` 豎線分隔的圖注、`ppt_to_md` 保留源 deck 已有的超連結（run 級外鏈 `[text](url)` / slide 內部跳轉 `[text](#slide-N)` / shape 級點選，含危險 scheme 過濾與錨文本 Markdown 轉義）並把原生圖表資料轉寫成 Markdown 表格（數值隨轉換存活，不再只剩一張圖）。圖注識別基於 [@suay1113](https://github.com/suay1113) [PR #191](https://github.com/hugohe3/ppt-master/pull/191)，超連結保留提煉自 [@ZhaoZuohong](https://github.com/ZhaoZuohong) [PR #155](https://github.com/hugohe3/ppt-master/pull/155)

- **內容保真的 PPT 美化 / 重排版上線**（[`workflows/beautify-pptx.md`](../../skills/ppt-master/workflows/beautify-pptx.md)） — 與 `template-fill` 互為映象：template-fill 複用某份 deck 的設計換新內容，beautify 反過來保留內容、重做版面。給一份現成 PPTX，**全部文字逐字保留（不增 / 不刪 / 不改寫）**，從源 deck 提取並**繼承其視覺身份（配色 / 字型，`theme` 或 `observed` 兩套候選過確認頁）**，只重做版面 / 層級 / 留白；嚴格 1:1 頁數頁序，圖表 / 表格從抽取資料原生重繪（資料凍結）、源配圖重新排布。技術上仍走從零生成原生 PPTX 管線（`ppt_to_md` 抽內容 → 主管線 → 全新 deck），不補丁原檔案，因此不碰 Non-goals #53。新增 `beautify_identity.py` / `beautify_inventory.py`，confirm 頁全欄位按源 seed 後使用者複核。v1 天花板（誠實標註）：不緩解資訊過載（擠頁只在頁內改，真要重排分頁屬主管線）、不保證座標級 paste-back、combo / dual-axis / waterfall 圖丟未捕獲的繪圖層

- **PPTX intake 多 deck 支援 + `analysis/` 源名字首** — 主管線專案現在可把多份源 deck 合併進來：每份寫 `<stem>.identity.json` / `<stem>.slide_library.json`，各自 digest 內聯進單一索引 `source_profile.json` 的 `decks[]`（保住"Strategist 必讀 `source_profile.json`"單入口契約，單 deck 即一條、多 deck 列多條；同 stem 重導覆蓋該條）。`beautify` / `template-fill` 仍是 1:1 單 deck，按 stem 讀自己那份 `<stem>.*`

- **材料發散度（§c 受眾下的自由文字項）** — 主管線在 §c 受眾文本框下加一個**純文字**小問：使用者用自己的話寫要多貼源、還是多放開重塑（留空＝平衡預設）。刻意不做固定檔位、不按源訊號替使用者推薦、不聯動頁數——就是問使用者本人意圖。無論寫得多放開都**事實守源**：只對源內內容重組 / 重框 / 展開 / 連結，絕不引入源外事實（那是 `topic-research` 的活）。Strategist 寫 §IX 大綱時讀這段 prose 消費、記 `design_spec §I`，**不進 spec_lock**（Executor 不讀）；`mode` 與發散度正交。beautify / template-fill 內容凍結，不暴露此項

- **一批預設行為與入口標準化** — 逐元素入場動畫預設關（只留轉場 `fade`；元素動畫改 opt-in `-a auto` / `animations.json`），消除"自動級聯入場"的 AI 味；per-project `icons/` 在選擇時把選中圖示複製進專案、嵌入優先本地；`analysis/` 確立為機器抽取事實的 canonical 必讀層（PPTX intake bundle + `image_analysis.csv`）；主管線把源 deck 的身份（配色 / 字型 / 版式）當**參考而非約束**（可繼承可重設，由策略師判斷，預設從零設計）；confirm 頁支援自定義配色輸入

- **AI 插畫大圖 → 切片點綴插畫管線**（[`scripts/slice_images.py`](../../skills/ppt-master/scripts/slice_images.py)） — 當一份 deck 需要若干同一家族的點綴插畫時，不再一格一次 AI 呼叫，而是**一次生成一張多格插畫大圖**（單次呼叫鎖住整組風格 / 色板、成本遠低於逐格生成），再由 `slice_images.py` 確定性按 `RxC` 網格切成獨立元素檔案；`--trim` 按每格內容包圍盒緊裁、`--alpha` 摳掉平整底色，讓每個元素以**透明剪影**落到異色頁面而非帶可見方框。資源契約（§VIII）雙行落地：一行 `ai` Illustration Sheet（生成但永不直接放置、不進 `spec_lock.md` images）+ 每格一行 `slice` 元素（實際放置、進 spec_lock）；Step 5 生成大圖後切片並重跑 `analyze_images`，Step 7 readiness gate 在離線場景列出大圖 + 元素目標讓使用者手動放圖再切。要不要用點綴插畫是 Strategist 在 `image_usage` source 邊界內的判斷（不單獨成確認欄位；`image_usage: none` 永遠壓過插畫意圖），使用者看不到內部 sheet/slice 實現。`svg_quality_checker` 加了對應校驗，[`image-layout-patterns.md`](../../skills/ppt-master/references/image-layout-patterns.md) 補了圖主導的促銷 / 宣傳版式範式

- **點綴插畫：從「能切出來」到「會用、成體系」** — 在切片管線之上補齊決策層 + 收緊切片質量，讓 deck 真正用好插畫而非只是技術上能生成。①**切片質量**：`slice_images.py` 的 `--alpha` 改軟蒙版抗鋸齒 + 1px 去光暈、底色取樣改 2px 邊框環中位數、色距改最大通道差；`svg_quality_checker` 對 Generated `slice` 行校驗檔案存在性。②**觸發傾向繫結 `visual_style`**：每個風格標 `core` / `supportive` / `sparse` 插畫傾向（[`visual-styles/_index.md`](../../skills/ppt-master/references/visual-styles/_index.md) 加 `Illus.` 列 + 各檔案 §6），core 預設推薦用、sparse 預設不用；優先順序鏈 `image_usage:none` → 使用者顯式意圖（雙向覆蓋）→ 風格傾向 → none。③**貫穿母題 through-line**：deck 傾向用插畫時，封面錨點 / 章節分隔 / 頁內散點出自同一母題家族（共享 h.5 rendering+palette+主題世界），讀成一套設計系統而非孤立散點；AI 母題僅在 `image_usage` 含 ai 時生成，provided/web 僅沿用本已成同族的素材。④**插畫角色決策地圖**：Strategist §h 加「角色 × 何時 × 機制 × source」導航表（散點 / 主角錨點 / 章節分隔 / 氛圍背景 / 母題）。全程不設配額、不把品味數字化（同尺寸瓷磚檢測評估後不做，留給 §4.3 placement 散文 + 執行判斷）

- **影像變換矩陣端到端保真 + host-native 生成路徑** — `svg_to_pptx` 的 DrawingML 圖片匯出現在如實尊重 SVG 的 transform 矩陣（旋轉 / 斜切 / 複合變換不再在巢狀 `<g transform>` 下錯位或塌回原點），把「跨四渲染器位置保真」主軸補到 raster 圖層；`image_gen.py` 增加 host-native 生成路徑，在宿主自帶影像生成能力時走原生通道。兩者均屬修復 / 增量補強，細節見 commit log

- **網路配圖改為「最佳圖 + 可複核 + 人工換圖」** — web 圖來源不再預設靜默下載一池候選，而是**預設只下最佳匹配圖**，候選池退化成 `--save-candidates` 的顯式升級路徑（預設 4 張）；每張下載圖生成 ≤1024px review 副本（`images/.review/`，放置 / promote 仍全解析度）。合適性複核做成 **model-agnostic**：多模態模型讀 review 副本自查，非多模態則把 `source_page_url` 交人工判斷——不假設模型有視覺。新增 `image_search.py --from-url <链接>`：把人找到的任意圖片 URL 下載並替換目標（記 `license_tier: manual`、繼承頁面上下文），作為通用人工換圖通道；`--promote` 改為從被選候選重算署名（不沿用舊圖 credit）。全程在 Step 5 內、不合適轉 `Needs-Manual` + 佔位，**不阻塞主流程**。定位上 web 搜尋是「兜底取圖、不保證質量」，真要高質量靠 AI 生圖或自己手動挑圖換入

- **Web 配圖實體安全門（精確主體不再被「高畫質錯圖」贏走）** — 承上條 web 配圖：給 web 候選加 `required_terms` 實體門控，擋住「後設資料相關但主體錯誤」的圖（一張精修的羅馬紀念碑贏下「重慶地標」行）。`required_terms` 各組之間 AND、組內 `A|B` 給別名（跨語言 `Chongqing|重庆`），匹配做小寫 / 分隔符歸一 / 空白壓縮以相容多詞與 CJK 名；命中實體即視作相關訊號（零 query 詞重疊不再否決，CJK 標題地標可在英文 query 下通過，無 `required_terms` 時舊的否決邏輯照舊）。像素面積從主導分（cap 5000）降級為 tie-breaker（cap 1500）+ 標題命中加權，讓實體準確性與相關性壓過純解析度（避免高畫質錯主體贏）。CLI `--require-terms`（可重複，逗號 / `|`）、批次 `required_terms`、`--from-url` 均繼承，記入 `image_sources.json` 備審；門控形同虛設（弱 `required_terms`）會發 warning。定位是與 `.review` 視覺複核配對的**後設資料門**，不是視覺分類器

- **原生 PPTX 匯出圖片媒體大小封頂** — 保持生成 deck 可編輯、不嵌入巨幅源圖：新增原生圖片尺寸模式——`cap`（預設）只對超大源圖限制最大邊長，`display` 按渲染 SVG 框尺寸做更激進壓縮；原生匯出保留完整嵌入畫素，SVG/PPT 顯示裁剪仍走可編輯的 picture-crop 後設資料；`finalize_svg` 保留原有 slice/meet 行為，另加預設按渲染尺寸下采樣以產出緊湊 SVG 快照。檔案落地 `cap` / `display` 兩模式與 `--no-image-optimize` 逃生艙

### 2026-07（分階段確認 UI + 原生圖表 / 表格成熟）

- **Step 4 確認 gate 重構為三階段嚮導 + 視覺化預覽** — 原來單次「八項確認」gate 拆成一個瀏覽器會話內的三階段流程（方向錨點 → 設計系統 → 圖片 / 執行方式），每個下游階段都從使用者**實際已確認**的上游選擇重新推導，而非 AI 原始推薦——於是圖片策略天然吻合已確認的配色系統。確認頁為難以憑名字判斷的選項補上視覺輔助：18 個 `visual_style` 每個一張專屬 real-SVG 頁面縮圖、真實圖示庫樣本、AI 圖參考圖預覽。`recommendations.json` 改用規範的 `stage` 選擇器（`tier` 僅作內部向後相容讀取），使用者可見措辭統一為「階段」；聊天 fallback 映象同樣的分階段順序

- **`--native-objects` 從休眠 marker 硬化為可用級 opt-in** — 那條窄「原生物件」例外（見下文 Non-goals）現在匯出的圖表與純文本表格會**保留 deck 自己的設計**，不再塌回 PowerPoint 的白底預設主題。classic 原生圖表顯式寫入 chart-area / plot-area / 軸線 / 網格線 / 標籤文字顏色——從可見的 SVG fallback 推斷（最大面板型 `<rect>` → 背景、fallback 文字 → 標籤、fallback 描邊 → 軸線/網格），或用 `style` 顯式覆蓋（`chart_area_fill` / `plot_area_fill` / `text_color` / `axis_color` / `grid_color`，`"none"` 表透明）；顏色解析把命名色、`#RGB` 簡寫、`rgb()` / `rgba()` 歸一為 OOXML hex；bar/column 系列關掉負值反色，負值柱保持系列色。啟用匯出命名為 `<name>_<ts>_native_charts.pptx` 以與預設壓平形狀匯出區分。**預設路線不變**——圖表/表格仍以 SVG 派生的 DrawingML 形狀匯出以保跨渲染器保真；原生物件仍是下文 Non-goals 裡那條刻意的 opt-in 取捨

---

## 進行中 / 下一步

明確在做或下一步要做的方向，不承諾時間視窗。

- **多 deck intake 與材料發散度的真實使用校準（剛落地）** — 多 deck 合併 intake（`<stem>` 字首 + `decks[]` 合併索引）與材料發散度自由文字項（§c 受眾下）均已上線（見上「2026-06」），接下來按真實使用訊號校準：多份源 deck 同名（stem 衝突）的處理目前是後者覆蓋前者，是否需要去重 / 加序號待訊號；發散度的自由文字讓 Strategist 判得準不準、放開寫時「事實守源」邊界守不守得住，待真實生成驗證。兩者都不預先加機械閾值
- **插畫能力（機制 + 部署層）的真實 deck 校準（剛落地）** — 切片管線、邊緣質量收緊，以及決策層（風格傾向 / 貫穿母題 / 角色地圖，見上「2026-06」）均已上線，接下來按真實使用訊號校準：一次大圖切多格的風格 / 色板一致性與 `--alpha` 軟蒙版對格內不規則構圖的魯棒性、離線 readiness gate 的手動放圖 + 重切體驗、風格傾向是否翻對了該翻的風格、母題在真實 deck 上讀成「設計系統」還是「過度裝飾」、以及 source 邊界（provided/web 不靜默生成 AI）守得住否。不預先加機械閾值 / 配額；同尺寸瓷磚若真反覆出現再考慮更窄的 lint
- 其餘：mode / visual-style 體系的驗證與校準已收口（見上「2026-06」），結構（5 mode + 18 visual-style + custom）定型、四對近鄰消歧併成一張 Close-calls 表、四項校準收緊已落地。後續方向由真實使用訊號與反饋驅動；長期改進見下「持續維護方向」，已評估不做的見「明確不做」

---

## 持續維護方向

不承諾時間視窗的長期改進項。只列真方向，具體修復 / 單 flag 看 commit log。

- **Prompt 精簡** — 在不降質量的前提下壓縮各角色 prompt 的 token 佔用、提升快取命中率，帶來間接的成本 / 速度改善。與下面「純速度最佳化」一節互補：做間接最佳化，不做犧牲質量的提速。

---

## 明確不做（Non-goals）

下面這些方向被多次提過，已經評估並決定**不做**。列出來不是否定需求價值，而是說明它們與本專案主路線不匹配；如果你剛好需要這些能力，建議看其他工具或 fork 本專案走自己的路。

### 讀取任意 PPTX 模板 → 僅填充文字

**對應 Issue**：[#53](https://github.com/hugohe3/ppt-master/issues/53)、[#118](https://github.com/hugohe3/ppt-master/issues/118)

PPT Master 主路線是「AI 從零生成 SVG → DrawingML」，整條管線圍繞完全可控的形狀/文字/版式構建。「解析既有 PPTX 佔位符 + 僅回填文字」是另一種產品形態，需要處理任意來源的母版 / 主題 / 佔位符體系，與現有架構發力點正交。

**基礎訴求其實很簡單**：如果只是「固定位置替換 Excel 資料到 PPT 模板」，直接讓 AI 寫一段 `python-pptx` 指令碼即可，幾行程式碼搞定，不需要本專案這套管線。

> **與 `template-fill-pptx` 路線的區別**：「複用某份 deck **自己的**設計、把新內容回填進去」是已支援的能力（見上「2026-06」），輸出仍原生可編輯。這裡拒的是另一種形態——解析**任意第三方**模板的母版 / 主題 / 佔位符體系並僅做文字替換；兩者發力點不同，別混為一談。

### 改用原生 PowerPoint 圖表（Excel-native chart）

**對應 Issue**：[#99](https://github.com/hugohe3/ppt-master/issues/99)、[#100](https://github.com/hugohe3/ppt-master/issues/100) 類

跨四渲染器（PowerPoint / Keynote / LibreOffice / WPS）的位置保真是專案主軸。把預設路線改成 PowerPoint 原生圖表會讓「畫素級一致性」破功——同一個 PPTX 在不同渲染器裡圖表會顯示不同佈局。圖表預設用 SVG 是 **by design**，不是能力缺失。

窄例外是 `data-pptx-native` marker：受支援的資料圖表與純文本網格表格在生成時攜帶原生物件後設資料，匯出加 `--native-objects` 才啟用——供主動用跨渲染器保真換取 PowerPoint 內可編輯性的使用者使用；啟用後的物件現在會保留 deck 的 chart-area / plot / 軸線 / 網格線 / 標籤顏色與原生表格格式，不再塌回 PowerPoint 預設主題（見上文 2026-07）。預設匯出路徑與 SVG 圖表 / 表格系統不變。

### uv 作為預設 / 必需依賴

**對應 Issue**：[#111](https://github.com/hugohe3/ppt-master/issues/111)

`pip + requirements.txt` 是唯一官方安裝路徑，因為它在所有 Python 環境下都可用、不需要額外學習成本。uv 是好工具，但「讓 uv 成為預設」會抬高新使用者的入門門檻。如果你個人偏好 uv，完全可以在 fork 裡用，不影響主線。

### 純速度最佳化

**對應 Issue**：[#97](https://github.com/hugohe3/ppt-master/issues/97)

成本 / 速度 / 質量三角下，本專案選擇**質量優先**。20 分鐘生成一個高質量 PPTX 是當前的合理點。

會做：通過 prompt 精簡 / 快取命中率提升帶來的間接改善；
不會做：以犧牲質量為代價的「隨便幾頁應付交差」式提速。

如果對速度敏感且能接受質量下降，Gamma / 美圖 AI 等競品更合適。

### CLI / SaaS / 桌面 App 形態

產品形態明確為 **chat-driven AI IDE skill**（Claude Code / Cursor / VS Code + Copilot / Codebuddy）。

不會做：獨立 CLI（`ppm` 之類）、SaaS Web 服務、Electron 桌面殼。所有「讓它脫離 chat 獨立執行」的提案都會被拒。chat 是互動核心，不是包裝層。

---

## 反饋渠道

- **Issues**：[github.com/hugohe3/ppt-master/issues](https://github.com/hugohe3/ppt-master/issues) — 報告 Bug / 提建議
- **Discussions**：[github.com/hugohe3/ppt-master/discussions](https://github.com/hugohe3/ppt-master/discussions) — 用法討論 / 經驗分享
- **郵箱**：heyug3@gmail.com

提需求前先掃一眼上面的 **Non-goals**；如果你的需求落在那一節，多半不會被採納，但歡迎討論是否還有別的路徑解決你的真實問題。
