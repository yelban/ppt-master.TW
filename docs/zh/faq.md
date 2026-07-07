# 常見問題

[English](../faq.md) | [中文](./faq.md)

---

## Q: PPT Master 支援哪些原始檔格式？

幾乎所有常見格式都支援：**PDF**、**DOCX**、**PPTX**、**EPUB**、**HTML**、**LaTeX**、**RST**、**網頁連結**（包括微信公眾號文章）、**Markdown**，或者直接在對話中貼上文字內容。AI 代理會自動將源材料轉換為 Markdown 後再生成幻燈片。

## Q: 只有一個主題或想法、沒有任何資料，也能生成嗎？

可以。直接告訴 AI 你想做的主題或場景（如"做一個關於宮崎駿的 PPT"、"介紹我們公司新產品"），AI 會自動啟動 **topic-research 工作流**——通過網頁搜尋抓取權威來源（Wikipedia / 官網 / 機構釋出），整理成 Markdown 資料檔案 + 配圖集後再走主流程生成幻燈片。

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

PPT Master 可以在任何能讀取檔案和執行命令的 AI 程式設計代理中執行——**Claude Code**（CLI / VS Code / JetBrains / Web）、**VS Code Copilot**、**Codex** 等均可使用。不同工具的使用成本可參考下方的費用對比。

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

## Q: 能用 AI 生成配圖嗎？

可以。PPT Master 內建了圖片生成指令碼，支援多個供應商（Gemini、OpenAI、FLUX、通義千問、智譜等）。在策略師階段選擇"AI 生圖"方案後，流程會根據內容自動生成配圖。你也可以使用自己的圖片——只需放到專案的 `images/` 目錄下即可。

## Q: 沒有生圖 API Key，還能配圖嗎？

可以——在策略師的"圖片方案"步驟選擇"網路圖片"。PPT Master 內建了零配置的 `image_search.py`，在 Openverse 和 Wikimedia Commons 中搜索可商用的開放許可圖片（無需 API Key）。零配置搜尋適合作為兜底：能直接用，但圖片質量不穩定，容易出現普通使用者上傳、構圖隨意、清晰度一般的素材。

如果想要更現代的商業風照片，建議在 `.env` 裡設定 `PEXELS_API_KEY` 和/或 `PIXABAY_API_KEY`（都是免費申請）。搜尋會自動納入 Pexels / Pixabay，人物、辦公、生活方式、產品和插畫類圖片質量通常會明顯更穩定。兩種路徑可以在同一份 deck 裡混用（比如 hero 圖用 AI 生成、團隊照片用網路搜尋）；如果選中的圖片需要署名，Executor 會在該幻燈片自動新增就地小字署名。

要清楚一點：**網路搜尋只負責「找到一張相關、可下載、授權合規的圖」，並不保證它在這一頁裡好看或貼切**——排序只看文字後設資料，看不到畫面。生成時多模態模型會讀一份縮圖自查、不合適會重搜；但**要真正高質量，最可靠的還是你自己去搜**：在任何來源找到更合適的圖，把連結給 AI，它會用 `image_search.py --from-url <链接>` 直接下載替換（記為手動來源、版權由你把關）。換圖隨時能做——生成途中或在即時預覽裡都行，不會打斷流程。簡而言之：把網路搜尋當「兜底佔位」，把人工挑圖當「精修」。

## Q: 生成的 PPT 可以編輯嗎？

可以。主 `.pptx`（原生 PowerPoint 形狀，文字、圖形、顏色均可直接編輯，無需轉換）以時間戳命名儲存至 `exports/`。Executor 的原始 SVG 源（`svg_output/` 副本）始終映象到 `backup/<timestamp>/svg_output/`，便於歸檔或基於該版重跑 `finalize_svg → svg_to_pptx` 重建 pptx，無需再走 LLM。加 `--svg-snapshot` 會額外在 `exports/` 內並排生成 SVG 快照版 pptx，便於跨平臺單檔案分發；預設關閉——日常開發/診斷場景中 live preview 已經提供了 SVG 視覺參考。需要 **Office 2016** 或更高版本。

## Q: 為什麼一段正文被拆成了好幾個文本框？能不能一段一個文本框？

預設會把可合併的正文段落匯出成一個可編輯的 PowerPoint 文本框，內部保留多個段落。**拉伸框時文字會在框內自動重排**。

如果你需要嚴格保持逐行版式，重新匯出時加上 `--no-merge`：

```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> --no-merge
```

使用 `--no-merge` 時，SVG 裡的每一視覺行都會變成一個獨立的 PowerPoint 文本框。這樣能**逐畫素保留 SVG 的版式**，適合封面、圖表、表格、以及任何對版式精度敏感的頁面。

**代價**：預設段落合併後，PowerPoint 自動換行的行數可能與原 SVG 不一致。預設更適合正文密集型頁面（abstract、多段落章節、參考文獻等）；版式敏感頁面使用 `--no-merge`。判定足夠保守——非段落型 `<text>` 會自動落回按行拆框路徑。

跟 AI 對話時也可以直接說："這個頁面要嚴格保持逐行版式" —— AI 重新匯出時會加上 `--no-merge`。

## Q: 字號為什麼用 px 不是 pt？匯出後字號會變嗎？

PPT Master 內部**全程只用 px**（無單位畫素）——確認頁、`spec_lock.md`、SVG 都是 px，沒有 pt 這一層。原因是 SVG 畫布本身就是 1280×720 px，px 是真正的排版/執行單位；只用一個單位，能避免「確認時說 20pt、寫進 SVG 又變成另一個數」這類單位混淆導致整套字號偏差。

PowerPoint 最終顯示的是 pt，所以**匯出時**自動把 px 換成 pt（`pt = px × 0.75`，保留 1 位小數）。例如正文 `24px` 匯出後是 `18pt`、標題 `42px` 是 `31.5pt`。所以你在 PowerPoint 裡看到 `13.5pt`、`31.5pt` 這種非整數是**正常的、有意的**，不是 bug——字號算出來是多少就是多少，不再強行湊成整數或半磅。

正文基準按**交付目的**固定取值（不是區間）：

| 交付目的 | 正文 px | ≈ 匯出 pt |
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

作為對比，Gamma 訂閱 $8–20/月，Beautiful.ai $12–45/月——無論用多少都得付這個底價。PPT Master 在你現有 AI 支出之外不增加任何額外成本。

## Q: 生成的圖表可以編輯資料嗎？

預設情況下，圖表以**自定義設計的 SVG 圖形**形式渲染，轉換為原生 PowerPoint 形狀——形狀級別完全可編輯（移動、改色、改文字、調樣式）。預設不用 Excel 驅動的圖表物件是有意為之：PowerPoint 預設圖表樣式陳舊、視覺受限於固定模板。SVG 圖表則提供出版物級的視覺質量，可以在 PowerPoint 中直接精修，且在 PowerPoint / Keynote / LibreOffice / WPS 間畫素一致。

如果你的工作流明確需要 Excel 驅動的資料編輯，匯出時加 `--native-objects`：受支援的資料圖表和純文本表格會以**帶資料、可直接編輯的 PowerPoint 原生圖表 / 表格物件**形式匯出（儲存為 `exports/<name>_<timestamp>_native_charts.pptx`，並保留這份 deck 自己的配色，而不是套用 PowerPoint 預設主題）。代價是跨軟體渲染——原生物件在 PowerPoint / Keynote / LibreOffice / WPS 間可能略有差異，所以 SVG 形狀仍是預設路徑。

## Q: 頁面切換和元素動畫可以調嗎？

可以。頁間轉場預設開（`fade` 0.4s），頁內元素入場動畫**預設關**——翻到一頁時整頁一次性呈現，不會有元素一個個自動級聯出來（那種沒人要的自動連播正是「AI 味」最重的地方）。兩者都通過 `svg_to_pptx.py` 的引數控制——`-t/--transition` 控制頁級，`-a/--animation` 控制元素級。想要頁內動畫時顯式開啟即可：

```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t push       # 换转场效果
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t none       # 关闭转场
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto       # 开启页内元素入场（按 group id 自动映射效果）
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation fade        # 开启并改用单一效果
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto --animation-trigger on-click   # 单击触发，演讲者控制节奏
```

`on-click` 適合現場演示。通過 `--recorded-narration` 做旁白/影片匯出時會拒絕它，因為 PPT Master 只寫頁面級計時，不生成物件級點選計時；帶旁白的 deck 請使用 `after-previous` 或 `with-previous`。

完整效果列表、`<g id="...">` 錨點機制、降級行為、限制：見 [轉場與動畫](./animations.md)。

## Q: 推薦用什麼 AI 模型？

**Claude**（Opus / Sonnet）是推薦且測試最充分的模型。SVG 排版本質上是在絕對座標系中做精確的數學計算（字號 x 字數 x 容器寬度），Claude 在這方面表現明顯優於其他模型。

**GPT 系列**早期版本排版問題較多——文字超出容器、元素錯位、座標計算失誤。較新的版本（如 GPT-5.5）在這方面已有明顯進步，實際效果可以接受；如果遇到問題，可以告知 AI 修正具體頁面。

其他模型（Gemini、GLM、MiniMax 等）效果參差不齊。總體來說，前端/視覺能力越強的模型，生成效果越好。

## Q: 有人說 PPT Master "只是個玩具"——這個評價準確嗎？

不準確。PPT Master 是一個 **harness**，不是完整的 agent——`harness + model = agent`，輸出上限完全由模型決定，而不是由 harness 本身決定。用弱模型或小上下文視窗來評價 PPT Master，就好比掛著一檔開跑車然後說它跑不快。

**發揮完整實力的組合：**

- **Claude 大上下文視窗**（推薦 ~100 萬 token 級別）：大上下文讓 Executor 在同一個會話裡看到全部已生成頁面，在不拆分執行的前提下保持整份 deck 的視覺一致性。上下文不足時被迫走拆分模式，兩段之間會出現明顯的風格漂移。
- **AI 生圖，推薦 `gpt-image-2`**（或同等質量）：配圖水平是 deck 整體觀感的最大變數。用佔位級的網路圖片和用真正貼合內容的 AI 生成圖，視覺效果完全是兩個量級。

如果你看到的效果差強人意，先對照以下幾點檢查你的配置，再下結論：用的什麼模型？上下文開了多大？有沒有接入圖片生成 API？同樣的工作流，Claude Opus 配 100 萬 token 上下文配 `gpt-image-2` 的結果，和小引數開源模型配零配置的結果，是截然不同的體驗。

**harness 決定工作流上限，model 決定質量上限。** 如果 agent 能力不達預期，請先升級模型，再來評價 harness。

> **沒有 Claude 渠道？** 本專案贊助商 [PackyCode](https://www.packyapi.com/register?aff=ppt-master) 提供 Claude 及其他主流模型的按量付費接入——無需訂閱，無需境外信用卡，支援國內支付，開箱即用。充值時填寫優惠碼 **`ppt-master`** 享 9 折。

最後再說一句：這是一個免費、個人維護的開源專案。合用就用，能幫到你我很高興；不合用，換個工具就好。真誠的反饋與建議始終歡迎——這也是專案一點點變好的方式。

## Q: 文字超出邊框 / 元素錯位怎麼辦？

這幾乎都是模型能力問題，不是 PPT Master 的 bug。SVG 排版是純手動絕對定位——模型必須準確計算座標、字型度量和容器尺寸。

**解決辦法**：
1. 切換到 **Claude**（Opus 或 Sonnet），如果你用的是其他模型
2. 告訴 AI 哪一頁有問題、具體是什麼問題——它可以單獨重新生成某一頁
3. 直接開啟 SVG 原始檔，讓 AI 修正座標
4. 記住：生成的 PPTX 是**高質量起點**，不是最終成品——在 PowerPoint 中做少量調整是正常的

## Q: 生成一份 PPT 要多久？

一份典型的 10–15 頁 PPT 大約需要 **10–20 分鐘**（使用吞吐較快的模型）。生成流程是**故意序列的**（逐頁生成），這樣才能保持前後頁面的視覺一致性——並行生成方案曾經測試過，結果是各畫各的、缺乏整體觀。

如果感覺生成很慢，檢查一下模型的 token 吞吐速度。瓶頸通常在模型的輸出速度，而不是指令碼本身。

## Q: 長 PPT 一次生成會不會上下文爆掉？

預設推薦**一次性連續生成**——10–15 頁的 deck 在 200K 上下文視窗下完全夠用，跨頁視覺一致性也最好（Executor 看到前幾頁 SVG 後會主動對齊風格、字號、節奏）。

只有訊號偏重的場景（頁數 ≥ 18 / 源材料很厚 / 走過 topic-research 累積大量 web 抓取），AI 才會在策略師階段給出**拆分模式**的可選提示：規劃會話（策略師確認階段 + 圖片獲取）結束後停止當前對話；你新開聊天視窗，輸入 `继续生成 projects/<项目名>` 進入執行會話（SVG 生成 + 匯出）。新會話從磁碟重新載入 `design_spec` / `spec_lock` / `sources` / `images` 繼續執行。

兩段式是**折中方案**——付出約 6K tokens 的 SKILL.md 重讀成本，換得 60–200K 的規劃會話噪聲丟棄，並把節省下來的視窗空間用於執行會話主動重讀 `sources/` 做內容增稠。**訊號正常時不需要**，提示也不會出現；使用者隨時可以忽略提示，走預設連續模式。

## Q: 能在匯出前預覽或修正某一頁嗎？

可以。你可以**隨時中斷工作流**——前幾頁生成後就可以檢視並反饋意見。AI 可以根據你的意見重新生成特定頁面，不需要等到全部完成再修改。

生成後的修正也一樣簡單，直接告訴 AI："第 3 頁佈局有問題——標題和圖表重疊了"，它會修正那個特定的 SVG。

## Q: 我手上有一份現成的 PPT，想基於它做東西，該走哪條路？

把「用一份已有 PPT」拆成兩個問題：**留不留它的內容**、**留不留它的設計（版式 + 視覺）**。四種組合對應四條路：

| 意圖 | 路線 | 固定不變的東西 |
|---|---|---|
| 留內容 + 重做版式 | **beautify（美化 / 重排）** | 頁數、頁序、每頁文字、圖表/表格資料 |
| 換內容 + 留設計 | **template-fill（套模板）** | 原生頁面設計；可選擇、亂序、複用源頁 |
| 只留內容，設計與分頁都重來 | **主管線** | 源事實；故事結構和頁數都可重構 |
| 留內容 + 留設計 | 不必生成 | 直接用原檔案 |

用 **beautify** 的前提是：原 PPT 的分頁本身就是輸出要求的一部分。文字逐字不動、頁數頁序 1:1 保留，只重排版式、層級和留白，並繼承原配色字型。典型說法是「把這份 PPT 美化一下 / 重新排版，內容別動」。見 [beautify 工作流](../../skills/ppt-master/workflows/beautify-pptx.md)。

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

**最推薦的方式是直接給原始 `.pptx` 檔案**。當前的 PPTX 匯入管線能做到接近高保真還原——PPT Master 會從 PPTX 中提取主題色、字型、母版/版式結構、可複用圖片資源（包括精靈圖裁剪關係），再用這些素材重建出乾淨可維護的模板。封面、章節、裝飾繁複的頁面都能穩定還原，這是目前最靠譜的派生路徑。

沒有源 PPTX 時，截圖集也能跑（`cover.png` / `toc.png` / `chapter.png` / `content.png` / `closing.png`），但保真度會明顯下降。建議優先找原始 PPTX。

**第二步 — 讓 AI 建立模板**

使用 AI 程式設計代理（Claude Code、Codex 等），要求它使用 **PPT Master 的 `/create-template` 工作流**，將這些參考材料轉換成模板。提供的資訊越詳細，效果越好，例如：

- 模板名稱和適用場景（如政府彙報、高階諮詢、產品宣講等）
- 期望的風格基調和配色（如"現代剋制、深藍主色調"）
- 類別偏好（`brand` 品牌 / `general` 通用 / `scenario` 場景 / `government` 政務 / `special` 特殊）
- 畫布格式（預設 16:9，如需其他格式請註明）

不需要一次提供所有細節——AI 代理會通過對話追問補齊缺失資訊（模板 ID、主題模式等）。

**第三步 — 等待完成**

AI 代理會自動完成後續工作 — 分析截圖、構建佈局定義、註冊模板，使其出現在 PPT Master 工作流的模板選項中。

> **提示**：對風格和使用場景描述得越具體，生成的模板就越符合你的預期。

---

> 更多問題可先檢視 [skills/ppt-master/SKILL.md](../../skills/ppt-master/SKILL.md) 與 [AGENTS.md](../../AGENTS.md)
