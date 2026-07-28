# 常見問題

[English](../faq.md) | [中文](./faq.md)

---

## Q: PPT Master 支援哪些原始檔格式？

幾乎所有常見格式都支援：**PDF**、**DOCX**、**PPTX**、**EPUB**、**HTML**、**LaTeX**、**RST**、**網頁連結**（包括微信公眾號文章）、**Markdown**，或者直接在對話中貼上文字內容。AI 代理會自動將源材料轉換為 Markdown 後再生成幻燈片。

## Q: 只有一個主題或想法、沒有任何資料，也能生成嗎？

可以。直接告訴 AI 你想做的主題或場景（如"做一個關於宮崎駿的 PPT"、"介紹我們公司新產品"），Generate PPTX 路線會執行 **topic-research 階段**，補齊規劃所需的事實基礎與來源記錄。已有部分材料時，只補實現使用者目標仍缺少的事實；如果使用者要求只使用原材料，則不做外部補充。圖片由 Strategist 在規劃中選定，並且只在最終確認後獲取。

效果取決於公開網頁的覆蓋度。如果你已有專業資料（論文、內部檔案），直接把檔案給 AI 比聯網檢索更準。

## Q: 除了 PPT 還能生成其他格式嗎？

可以。除了標準的 **16:9** 和 **4:3** 簡報格式，PPT Master 還內建了社交媒體和營銷類格式：

| 格式 | 適用場景 |
|------|----------|
| 小紅書 3:4 | 圖文分享、知識帖 |
| 微信朋友圈 / IG 1:1 | 方形海報、品牌展示 |
| Story / 抖音 9:16 | 豎版故事、短影片封面 |
| 微信文章頭圖 | 公眾號文章封面 |
| A4 印刷 | 印刷海報、傳單 |

建立專案時指定格式即可（如 `--format xhs`）。輸出仍然是包含原生形狀的 `.pptx` 檔案。

## Q: PPT Master 支援哪些 AI 工具？

PPT Master 可以在任何能讀取檔案和執行命令、支援 Agent 的 AI 工具中執行——**Claude Code**（CLI / VS Code / JetBrains / Web）、**VS Code Copilot**、**Codex** 等均可使用。不同工具的使用成本可參考下方的費用對比。

## Q: 我下載過舊版本，怎麼更新到最新版？

看你當時怎麼安裝：

| 安裝方式 | 更新方式 |
|---|---|
| Git clone | 在 `ppt-master` 目錄執行 `python3 skills/ppt-master/scripts/update_repo.py` |
| Download ZIP | 重新下載最新版 ZIP，解壓到新目錄；把舊目錄裡的 `.env` 和 `projects/` 複製過去；再執行 `pip install -r requirements.txt` |
| Skill marketplace | 用對應的 marketplace / skills 工具重新安裝或更新 |

長期使用建議用 Git clone。ZIP 適合快速體驗，但沒有 Git 歷史，不能自動 `git pull`。

如果不確定自己是哪種安裝方式，可以讓 AI 在專案目錄裡執行：

```bash
python3 skills/ppt-master/scripts/update_repo.py
```

如果當前目錄不是 Git clone 版本，指令碼會提示你按 ZIP 方式遷移。

## Q: 倉庫超過 1 GB，skills 工具下載直接失敗——能只拿 skill 嗎？

可以。完整倉庫確實很大（Git 歷史，加上內建的示例 deck 及其素材），而且這個體積是寫進歷史裡的——在不破壞已有大量 fork 的前提下沒法瘦身。如果你只想要 skill、不需要完整倉庫，用下面的輕量方式：

- **Marketplace CLI**：`npx skills add hugohe3/ppt-master`，或 Claude Code 裡的 `/plugin install`，都只拉取 skill 檔案（見 README 的「開始設定」一節）。
- **手動下載**：到 [Releases](https://github.com/hugohe3/ppt-master/releases) 頁面下載 `ppt-master-skill-*.zip`——只含 skill 檔案（約 50 MB），無需 clone 完整倉庫。

兩種方式裝好後，都要在安裝目錄跑 `pip install -r requirements.txt`，後處理指令碼才能工作。

這兩條路徑都不帶 `.git` 目錄，`git describe` 查不到版本。已安裝的版本記錄在 skill 自身 `SKILL.md` frontmatter 的 `metadata.version` 欄位裡。

中國大陸地區訪問 GitHub 下載不便的話，完整倉庫在 [AtomGit](https://atomgit.com/hugohe3/ppt-master) 也有映象（clone 或下載 ZIP）；1 GB 出頭的體積在中國大陸地區網路下載一般沒問題。

## Q: 能用 AI 生成配圖嗎？

可以。PPT Master 內建了圖片生成指令碼，支援多個供應商（Gemini、OpenAI、FLUX、通義千問、智譜等）。在策略師階段選擇"AI 生圖"方案後，流程會根據內容自動生成配圖。你也可以使用自己的圖片——只需放到專案的 `images/` 目錄下即可。

## Q: 沒有生圖 API Key，還能配圖嗎？

可以——在策略師的"圖片方案"步驟選擇"網路圖片"。PPT Master 內建了零配置的 `image_search.py`，在 Openverse 和 Wikimedia Commons 中搜索可商用的開放許可圖片（無需 API Key）。零配置搜尋適合作為兜底：能直接用，但圖片質量不穩定，容易出現普通使用者上傳、構圖隨意、清晰度一般的素材。

如果想要更現代的商業風照片，建議在 `.env` 裡設定 `PEXELS_API_KEY` 和/或 `PIXABAY_API_KEY`（都是免費申請）。搜尋會自動納入 Pexels / Pixabay，人物、辦公、生活方式、產品和插畫類圖片質量通常會明顯更穩定。兩種路徑可以在同一份 deck 裡混用（比如 hero 圖用 AI 生成、團隊照片用網路搜尋）；如果選中的圖片需要署名，Executor 會在該幻燈片自動新增就地小字署名。

要清楚一點：**網路搜尋只負責「找到一張相關、可下載、授權合規的圖」，並不保證它在這一頁裡好看或貼切**——排序只看文字後設資料，看不到畫面。生成時多模態模型會讀一份縮圖自查、不合適會重搜；但**要真正高質量，最可靠的還是你自己去搜**：在任何來源找到更合適的圖，把連結給 AI，它會用 `image_search.py --from-url <链接>` 直接下載替換（記為手動來源、版權由你把關）。換圖隨時能做——生成途中或在即時預覽裡都行，不會打斷流程。簡而言之：把網路搜尋當「兜底佔位」，把人工挑圖當「精修」。

## Q: 生成的 PPT 可以編輯嗎？

可以。SVG 管線統一由專案轉換器讀取 `svg_output/` 並生成原生 DrawingML `.pptx`；文字、圖形和顏色無需額外轉換即可編輯，檔案以時間戳命名儲存至 `exports/`。在正式交付流程中，Executor 的原始 SVG 源（`svg_output/` 副本）會映象到 `backup/<timestamp>/svg_output/`，便於歸檔或基於該版重跑 `finalize_svg → svg_to_pptx` 重建 PPTX，無需再走 LLM。

正式交付的 Step 7 仍會強制生成 `svg_final/`。其中每頁都是自包含的視覺預覽 SVG，可直接在瀏覽器或 IDE 中開啟，也可作為 SVG 圖片手動插入 PowerPoint；顯式快速測試會跳過預覽和備份產物。專案只保證 `svg_final/` 作為預覽或圖片顯示，不保證 PowerPoint 手工“轉換為形狀”後的結果。需要可編輯形狀時，請使用 `exports/` 中由專案轉換器生成的原生 PPTX。

## Q: 為什麼一段正文被拆成了好幾個文本框？能不能一段一個文本框？

預設會把可合併的正文段落匯出成一個可編輯的 PowerPoint 文本框，內部保留多個段落。**拉伸框時文字會在框內自動重排**。

如果你需要嚴格保持逐行版式，重新匯出時加上 `--no-merge`：

```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> --no-merge
```

使用 `--no-merge` 時，SVG 裡的每一視覺行都會變成一個獨立的 PowerPoint 文本框。這樣能**逐畫素保留 SVG 的版式**，適合封面、圖表、表格、以及任何對版式精度敏感的頁面。

**代價**：預設合併會保留一個可編輯文本框和原始視覺行邊界；只有需要讓每一視覺行都能單獨移動時才使用 `--no-merge`。判定足夠保守——非段落型 `<text>` 會自動落回按行拆框路徑。

跟 AI 對話時也可以直接說："這個頁面要嚴格保持逐行版式" —— AI 重新匯出時會加上 `--no-merge`。

## Q: 字號為什麼用 px 不是 pt？匯出後字號會變嗎？

PPT Master 內部**全程只用 px**（無單位畫素）——確認頁、`spec_lock.md`、SVG 都是 px，沒有 pt 這一層。原因是 SVG 畫布本身就是 1280×720 px，px 是真正的排版/執行單位；只用一個單位，能避免「確認時說 20pt、寫進 SVG 又變成另一個數」這類單位混淆導致整套字號偏差。

PowerPoint 最終顯示的是 pt，所以**匯出時**自動把 px 換成 pt（`pt = px × 0.75`，保留 1 位小數）。例如正文 `24px` 匯出後是 `18pt`、標題 `42px` 是 `31.5pt`。所以你在 PowerPoint 裡看到 `13.5pt`、`31.5pt` 這種非整數是**正常的、有意的**，不是 bug——字號算出來是多少就是多少，不再強行湊成整數或半磅。

正文基準按**閱讀模式**固定取值（不是區間）。它控制閱讀距離與資訊密度，與開放式溝通意圖是兩條獨立軸：

| 閱讀模式 | 正文 px | ≈ 匯出 pt |
|---|---|---|
| `text` 文字型（近讀：報告 / 資料） | 20px | 15pt |
| `balanced` 均衡（預設：路演 / 評審） | 24px | 18pt |
| `presentation` 展示型（投影 / 釋出） | 32px | 24pt |

標題、副標題、腳註等其它角色按比例從正文派生，並取整潔偶數 px。你在確認頁可以手動覆蓋任何角色的 px 值。

## Q: PPT Master 怎麼確定演示的風格？

在第 d 項確認時鎖定兩個獨立維度：

- **Mode（怎麼講）**：`pyramid` / `narrative` / `instructional` / `showcase` / `briefing` —— 見 `references/modes/`
- **Visual style（長什麼樣）**：`swiss-minimal` / `editorial` / `soft-rounded` / `dark-tech` … + `custom` —— 見 `references/visual-styles/`

任意 mode 可與任意 visual style 自由組合。

## Q: 用 PPT Master 做 PPT 貴嗎？

PPT Master 本身免費開源，唯一的成本來自你自己的 AI 模型用量。

目前主流 AI 工具都已轉向按量計費——用多少付多少。PPT Master 天然契合這一模型：不需要額外訂閱 PPT 平臺、沒有專有積分、沒有按人頭收費的演示工具費用。

而且它跑在程式設計 agent 裡：走固定月費的訂閱套餐，就能在套餐額度內多做 deck 而不額外多花錢；走 API 直連、按 token 計費則是另一種價格結構——由你選。無論走哪條，PPT Master 都不會在你的 AI 支出之外再加一層自己的費用。

## Q: 生成的圖表可以編輯資料嗎？

預設情況下，圖表以**自定義設計的 SVG 圖形**形式渲染，轉換為原生 PowerPoint 形狀——形狀級別完全可編輯（移動、改色、改文字、調樣式）。預設不用 Excel 驅動的圖表物件是有意為之：PowerPoint 預設圖表樣式陳舊、視覺受限於固定模板。SVG 圖表則提供出版物級的視覺質量，可以在 PowerPoint 中直接精修，且在 PowerPoint / Keynote / LibreOffice / WPS 間畫素一致。

如果你的工作流明確需要 Excel 驅動的資料編輯或 PowerPoint 的圖表/表格專屬控制，匯出時加 `--native-charts-and-tables`：受支援的資料圖表和純文本表格會以**帶資料來源的 PowerPoint 原生 Chart / Table 物件**形式匯出（儲存為 `exports/<name>_<timestamp>_native_charts_tables.pptx`，並保留這份 deck 自己的配色，而不是套用 PowerPoint 預設主題）。預設 SVG fallback 同樣會轉換成可編輯 DrawingML shape，但不具備圖表資料工作簿或圖表/表格物件模型。原生物件在 PowerPoint / Keynote / LibreOffice / WPS 間可能略有差異，因此形狀路線仍是視覺穩定性的預設選擇。

## Q: 頁面切換和元素動畫可以調嗎？

可以。頁間轉場預設開（`fade` 0.4s），頁內元素物件動畫**預設關**——翻到
一頁時整頁一次性呈現，不會自動逐個級聯。兩者都通過 `svg_to_pptx.py` 的
引數控制：`-t/--transition` 控制頁級，`-a/--animation` 控制元素級。物件
登入檔已經包含進入、強調、動作路徑和退出效果。

```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t push       # 换转场效果
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t none       # 关闭转场
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto       # 开启页内元素入场（按 group id 自动映射效果）
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation entrance_fade # 开启并改用单一规范效果
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation emphasis_spin # 原生强调效果
python3 skills/ppt-master/scripts/pptx_animations.py --list             # 完整分类效果清单
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto --animation-trigger on-click   # 单击触发，演讲者控制节奏
```

`on-click` 適合現場演示。通過 `--recorded-narration` 做旁白/影片匯出時會拒絕它，因為 PPT Master 只寫頁面級計時，不生成物件級點選計時；帶旁白的 deck 請使用 `after-previous` 或 `with-previous`。

常用命令、Start 模式選擇與物件級自定義見[轉場與動畫](./animations.md)；精確效果與校驗行為由其中連結的執行規範維護。

## Q: 推薦用什麼 AI 模型？

**Claude**（Opus / Sonnet）是推薦且測試最充分的模型。SVG 排版本質上是在絕對座標系中做精確的數學計算（字號 x 字數 x 容器寬度），Claude 在這方面表現明顯優於其他模型。

**GPT 系列**早期版本排版問題較多——文字超出容器、元素錯位、座標計算失誤。較新的版本（如 GPT-5.5）在這方面已有明顯進步，實際效果可以接受；如果遇到問題，可以告知 AI 修正具體頁面。

其他模型（Gemini、GLM、MiniMax 等）效果參差不齊。總體來說，前端/視覺能力越強的模型，生成效果越好。

## Q: 有人說 PPT Master "只是個玩具"——這個評價準確嗎？

不準確。PPT Master 是簡報工作流，不是模型，也不是完整 agent。它提供簡報專用的推理、合同、專案狀態、確定性轉換與質量門；最終質量上限仍由所選模型決定。用弱模型或小上下文視窗來評價這套工作流，就好比掛著一檔開跑車然後說它跑不快。

**發揮完整實力的組合：**

- **Claude 大上下文視窗**（推薦 ~100 萬 token 級別）：大上下文讓 Executor 在同一個會話裡看到全部已生成頁面，在不拆分執行的前提下保持整份 deck 的視覺一致性。上下文不足時被迫走拆分模式，兩段之間會出現明顯的風格漂移。
- **AI 生圖，推薦 `gpt-image-2`**（或同等質量）：配圖水平是 deck 整體觀感的最大變數。用佔位級的網路圖片和用真正貼合內容的 AI 生成圖，視覺效果完全是兩個量級。

如果你看到的效果差強人意，先對照以下幾點檢查你的配置，再下結論：用的什麼模型？上下文開了多大？有沒有接入圖片生成 API？同樣的工作流，Claude Opus 配 100 萬 token 上下文配 `gpt-image-2` 的結果，和小引數開源模型配零配置的結果，是截然不同的體驗。

> **沒有 Claude 渠道？** 本專案贊助商 [PackyCode](https://www.packyapi.com/register?aff=ppt-master) 提供 Claude 及其他主流模型的按量付費接入——無需訂閱，無需境外信用卡，支援國內支付，開箱即用。充值時填寫優惠碼 **`ppt-master`** 享 9 折。

最後再說一句：這是一個免費、個人維護的開源專案。合用就用，能幫到你我很高興；不合用，換個工具就好。真誠的反饋與建議始終歡迎——這也是專案一點點變好的方式。

## Q: 文字超出邊框 / 元素錯位怎麼辦？

原因取決於偏差出現在哪一層。如果源 SVG 本身已經溢位或錯位，通常屬於創作 / 排版問題：模型需要準確計算座標、字型度量和容器尺寸。如果 SVG 預覽正確、匯出的 PPTX 卻不同，則可能是轉換器或渲染器問題，應連同兩份產物一起反饋。

**解決辦法**：
1. 對比 `svg_output/` 中的頁面與匯出 PPTX，先區分創作問題和轉換問題
2. 告訴 AI 哪一頁有問題、具體是什麼問題——它可以單獨重新生成某一頁
3. 如果 SVG 本身持續出錯，換更強的模型，或讓 AI 直接修正座標
4. 記住：生成的 PPTX 是**高質量、可編輯的草稿**，不是封閉的最終成品——在 PowerPoint 中做少量收尾是正常的

## Q: 生成一份 PPT 要多久？

一份典型的 10–15 頁 PPT 大約需要 **10–20 分鐘**（使用吞吐較快的模型）。生成流程是**故意序列的**（逐頁生成），這樣才能保持前後頁面的視覺一致性——並行生成方案曾經測試過，結果是各畫各的、缺乏整體觀。

如果感覺生成很慢，檢查一下模型的 token 吞吐速度。瓶頸通常在模型的輸出速度，而不是指令碼本身。

## Q: 臨時測試幾頁 PPT，可以走快速模式嗎？

可以。請明確說明這是一次**快速測試**，並給出少量、固定、自包含的頁面清單。Generate 路線會啟用 [`quick-test` profile](../../skills/ppt-master/workflows/profiles/quick-test.md)：AI 直接手寫 `svg_output/`，隨後呼叫測試專用的直接匯出器。

該模式只產出 SVG 頁面和一個 PPTX；不會做原始檔轉換、事實研究、策略師規劃與確認、模板套用、素材獲取、Live Preview、質量報告、講稿、`svg_final/`、備份、動畫或旁白。正式交付、需要事實或原始檔、依賴外部素材/模板/原生圖表表格，或要求複用時，仍走標準流程。

## Q: 長 PPT 一次生成會不會上下文爆掉？

預設推薦**一次性連續生成**——10–15 頁的 deck 在 200K 上下文視窗下完全夠用，跨頁視覺一致性也最好（Executor 看到前幾頁 SVG 後會主動對齊風格、字號、節奏）。

只有訊號偏重的場景（頁數 ≥ 18 / 源材料很厚 / 走過 topic-research 累積大量 web 抓取），AI 才會在策略師階段給出**拆分模式**的可選提示：規劃會話（策略師確認階段 + 圖片獲取）結束後停止當前對話；你新開聊天視窗，輸入 `继续生成 projects/<项目名>` 進入執行會話（SVG 生成 + 匯出）。新會話從磁碟重新載入 `design_spec` / `spec_lock` / `sources` / `images` 繼續執行。

兩段式是**折中方案**——新會話需付出過載 Generate 權威檔案與必需執行引用的固定成本，但可丟棄規劃會話噪聲，並把節省下來的視窗空間用於主動重讀 `sources/` 做內容增稠。**訊號正常時不需要**，提示也不會出現；使用者隨時可以忽略提示，走預設連續模式。

## Q: 能在匯出前預覽或修正某一頁嗎？

可以。你可以**隨時中斷工作流**——前幾頁生成後就可以檢視並反饋意見。AI 可以根據你的意見重新生成特定頁面，不需要等到全部完成再修改。

生成後的修正也一樣簡單，直接告訴 AI："第 3 頁佈局有問題——標題和圖表重疊了"，它會修正那個特定的 SVG。

## Q: 我手上有一份現成的 PPT，想基於它做東西，該走哪條路？

把「用一份已有 PPT」拆成兩個問題：**留不留它的內容**、**留不留它的設計（版式 + 視覺）**。四種組合對應三種生成路徑，以及直接保留原檔案這一種無需生成的結果：

| 意圖 | 路線 | 固定不變的東西 |
|---|---|---|
| 留內容 + 重做版式 | **Generate PPTX + beautify profile** | 頁數、頁序、每頁文字、圖表/表格資料 |
| 換內容 + 留設計 | **Fill Native PPTX** | 原生頁面設計；可選擇、亂序、複用源頁 |
| 只留內容，設計與分頁都重來 | **Generate PPTX** | 源事實；故事結構和頁數都可重構 |
| 留內容 + 留設計 | 不必生成 | 直接用原檔案 |

使用 **beautify profile** 的前提是：原 PPT 的分頁本身就是輸出要求的一部分。文字逐字不動、頁數頁序 1:1 保留，只重排版式、層級和留白，並繼承原配色字型。典型說法是「把這份 PPT 美化一下 / 重新排版，內容別動」。見 [beautify profile](../../skills/ppt-master/workflows/profiles/beautify-pptx.md)。

用 **主管線** 的前提是：原 PPT 只是內容材料。流程會用 `ppt_to_md` 抽成 Markdown，並讀取 `analysis/` 裡的 PPTX intake 事實，再由 Strategist 自由重構大綱（合頁 / 拆頁 / 換序）。典型說法是「用這份 PPT 的內容重做一份更好的」或「提煉成 10 頁高管彙報」。

beautify 和主管線的一句話判別：**原來的分頁是要保留的資訊，還是隻是前一作者的結構、可以推翻？** 保留 → beautify；推翻 → 主管線。落到硬判據就是**頁數 / 頁序**：只要它有任何變化——拆頁、合頁、刪頁、換序，乃至「一字不改、只把某張太擠的頁拆開排得更好看」——都屬於重分頁，走主管線。beautify 嚴格 1:1。

如果使用者說法含糊，比如「把這份 PPT 做得更專業一點」「最佳化一下這個 deck」，AI 應先問一句：**要保留原頁數、頁序和每頁文字，只做美化；還是把 PPT 當素材，重新梳理成一份新故事？**

還有一條正交的路：如果你不是要現在產出一份 deck，而是想把這套設計**收成可複用模板**供以後反覆用，走 **create-template**（見下面「如何製作自定義模板」）。

---

## Q: 我已經有一份做好的 `.pptx`，能不能複用它的設計、只填新內容？

可以——這就是 **套模板（template fill）** 路徑，獨立於 SVG 生成管線。把你現成的 `.pptx` 連同素材（或一個主題）給 AI，說「套模板 / 把這些填回去」。它會把你的 deck 當作原生頁面庫，只挑適合新內容的頁面（可亂序、可重複），把新文字——以及原生表格單元格、圖表資料——直接寫回原始 OOXML。

輸出仍是 100% 原生可編輯的 PowerPoint：原設計、母版、圖片、動畫都保留，且只匯出選中的頁面。它刻意**不**改版式、不加頁、不換圖——一份 deck 的頁面結構本身承載著邏輯（總分、對比、遞進），所以應挑選結構本就契合內容的頁面，而不是硬塞進去。若需要全新結構或不同頁數，請改用 create-template（見下一問）。完整步驟：[套模板工作流](../../skills/ppt-master/workflows/template-fill-pptx.md)。

---

## Q: 如何製作自定義模板？

想把自己喜歡的 PPT 模板製作成 PPT Master 可呼叫的模板？按以下步驟操作：

**第一步 — 準備參考材料**

**最推薦的方式是直接給原始 `.pptx` 檔案**。PPT Master 會提取包內實際存在且受支援的主題色、字型、Master/Layout、placeholder type/idx、原生形狀資訊和可複用圖片資源。`standard` 與 `fidelity` 把來源當作視覺參考，重新設計 SVG roster 和新的 Master/Layout/slot 系統，不保留、也不蒸餾來源拓撲。`mirror` 則把這些已驗證的來源事實物化到新工作區，不做語義歸納或缺口補造。由於結構層禁止 `<g>`，來源 Master/Layout 的 group wrapper 只允許機械展開成直接原子。

完整匯入 SVG 可以保留高階 PowerPoint 形狀所需的 metadata、隱藏 carrier 和預覽指紋，並作為載荷後備留在臨時分析工作區且保持不可變。模板建立使用帶檔案內 source ref 和緊湊路徑/hash manifest 的輕量可編輯 IR。`standard` / `fidelity` 創作專案規範化 SVG，只有精確匹配已登記 preset 時才使用 compact authored-preset 組。Mirror 從 IR 物化最終模板，只為未改且 hash 匹配的 Slide-local/slot ref 重新接入轉換器已經支援的載荷；不支援或已修改的物件保留當前 SVG fallback。

沒有源 PPTX 時，截圖集也能跑（`cover.png` / `toc.png` / `chapter.png` / `content.png` / `closing.png`），但保真度會明顯下降。建議優先找原始 PPTX。

**第二步 — 讓 AI 建立模板**

使用支援 Agent 的 AI 工具（Claude Code、Codex 等），要求它使用 **PPT Master 的 `/create-template` 工作流**，將這些參考材料轉換成模板。提供的資訊越詳細，效果越好，例如：

- 模板名稱和適用場景（如政府彙報、高階諮詢、產品宣講等）
- 期望的風格基調和配色（如"現代剋制、深藍主色調"）
- 類別偏好（`brand` 品牌 / `general` 通用 / `scenario` 場景 / `government` 政務 / `special` 特殊）
- 畫布格式（預設 16:9，如需其他格式請註明）
- 輸出範圍：進入索引的 `library`（預設）或一個已經初始化的 `project`；兩者使用相同路由並省略空的可選目錄

不需要一次提供所有細節——AI 代理會通過對話追問補齊缺失資訊（輸出範圍、模板 ID、主題模式等）。

**第三步 — 等待完成**

AI 代理會自動完成後續工作——分析參考、構建佈局定義並驗證模板。如果你明確需要 PowerPoint 審閱檔案，它還會按需生成 `exports/<id>_template_preview.pptx`。兩種範圍都要求 `templates/`，並使用可選的 `images/`、`icons/` 與 `exports/`：`library` 寫入 `skills/ppt-master/templates/<kind>/<id>/` 並完成全域性註冊；`project` 寫入 `projects/<name>/` 並跳過註冊；空的可選目錄直接省略。把這個工作區根目錄交給 Step 3 即可，Step 3 不會複製 `exports/`，全域性庫的預覽匯出也由 Git 忽略。根目錄平鋪 `design_spec.md` 的工作區只有在 SVG 已滿足當前合同時才相容；語義舊包必須通過 `create-template` 替換，不能原地升級。

> **提示**：對風格和使用場景描述得越具體，生成的模板就越符合你的預期。

---

> 更多問題可先檢視 [skills/ppt-master/SKILL.md](../../skills/ppt-master/SKILL.md) 與 [AGENTS.md](../../AGENTS.md)
