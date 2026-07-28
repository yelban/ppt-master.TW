# PPT Master — AI 生成原生 PowerPoint，支援任意檔案輸入

[![Version](https://img.shields.io/github/v/release/hugohe3/ppt-master?label=version&color=blue)](https://github.com/hugohe3/ppt-master/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/hugohe3/ppt-master.svg)](https://github.com/hugohe3/ppt-master/stargazers)
[![AtomGit stars](https://atomgit.com/hugohe3/ppt-master/star/badge.svg)](https://atomgit.com/hugohe3/ppt-master)
[![The Agentic Leaderboard](https://www.theagenticleaderboard.com/badges/ppt-master.svg)](https://www.theagenticleaderboard.com/agent/?q=ppt-master)

<p align="center">
  <a href="https://trendshift.io/repositories/25760?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-25760" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/25760" alt="hugohe3%2Fppt-master | Trendshift" width="250" height="55"/></a>
</p>

[English](./README.md) | 正體中文 | [简体中文](./README_CN.md)

<details open>
<summary>本專案由 <a href="https://www.kimi.com/code/?aff=ppt-master">Kimi</a>、<a href="https://www.packyapi.com/register?aff=ppt-master">PackyCode</a>、<a href="https://apikey.fun/register?aff=PPT-MASTER">APIKEY.FUN</a>、<a href="https://runapi.co/register?aff=WMLJ">RunAPI</a>、<a href="https://www.compshare.cn/coding-plan?ytag=GPU_YY-git_pptmaster0624">優雲智算</a> 等贊助方支援，得以持續免費開源。</summary>

<p align="center">
  <a href="https://www.kimi.com/code/?aff=ppt-master"><img src="https://gcdn.moonshot.cn/growth-cdn/sponsor/kimi-zh.png" alt="Kimi" width="100%"></a>
</p>

感謝 [Kimi](https://www.kimi.com/code/?aff=ppt-master) 贊助本專案！[Kimi K3](https://platform.kimi.com/docs/guide/kimi-k3-quickstart) 是全球首個開源 3T 級模型，擁有原生視覺能力與 100 萬 Token 上下文。搭配 PPT Master，K3 可以理解 PDF、DOCX、網頁等原始資料，提煉重點、規劃演示邏輯，並生成可在 PowerPoint 中繼續修改的原生可編輯 PPTX。

**立即體驗 [Kimi Code](https://www.kimi.com/code/?aff=ppt-master)，或通過 Kimi 開放平臺（[中文站](https://platform.kimi.com?aff=ppt-master)｜[Global](https://platform.kimi.ai?aff=ppt-master)）使用 API。**

<hr>

<table>
  <tr>
    <td width="180"><a href="https://www.packyapi.com/register?aff=ppt-master"><img src="docs/assets/sponsors/packycode.png" alt="PackyCode" width="150"></a></td>
    <td>感謝 PackyCode 贊助了本專案！PackyCode 是一家穩定、高效的 API 中轉服務商，提供 Claude Code、Codex、Gemini 等多種中轉服務。PackyCode 為本專案的使用者提供了特別優惠，使用<a href="https://www.packyapi.com/register?aff=ppt-master">此連結</a>註冊並在充值時填寫"ppt-master"優惠碼，可以享受 9 折優惠。</td>
  </tr>
  <tr>
    <td width="180"><a href="https://apikey.fun/register?aff=PPT-MASTER"><img src="docs/assets/sponsors/apikey-fun.png" alt="APIKEY.FUN" width="150"></a></td>
    <td>感謝 APIKEY.FUN 贊助了本專案！APIKEY.FUN 是一家專業的企業級 AI 中轉站，致力於為企業和開發者提供穩定、高效、低成本的 AI 中轉服務。平臺支援 Claude、OpenAI、Gemini 等主流熱門模型，價格低至官方原價的 <strong>7%</strong>。通過<a href="https://apikey.fun/register?aff=PPT-MASTER">本專案專屬連結</a>註冊，還可享受最高 <strong>永久充值 95 折</strong> 專屬優惠。</td>
  </tr>
  <tr>
    <td width="180"><a href="https://runapi.co/register?aff=WMLJ"><img src="docs/assets/sponsors/runapi.png" alt="RunAPI" width="150"></a></td>
    <td>感謝 RunAPI 贊助了本專案！RunAPI 是一個高效穩定的 API 平臺，一個 API Key 即可訪問 OpenAI、Claude、Gemini、DeepSeek、Grok 等 150+ 主流模型，價格低至官方原價的 <strong>1 折</strong>，極其穩定，可無縫相容 Claude Code 等工具。RunAPI 為 PPT Master 使用者提供專屬福利：通過<a href="https://runapi.co/register?aff=WMLJ">本專案專屬連結</a>註冊並聯系管理員，即可領取 <strong>￥7 的免費額度</strong>。</td>
  </tr>
  <tr>
    <td width="180"><a href="https://www.compshare.cn/coding-plan?ytag=GPU_YY-git_pptmaster0624"><img src="docs/assets/sponsors/youyun.png" alt="優雲智算" width="150"></a></td>
    <td>感謝優雲智算贊助了本專案！優雲智算是 UCloud 旗下 AI 雲平臺，一站式提供國內外主流模型的 API 服務，一個 Key 即可呼叫所有模型。主打高價效比國產模型 CodingPlan 套餐（GLM5.2、Deepseek-v4 等），同時提供官方轉發的穩定海外模型通道，滿足多場景開發需求。已相容 Claude Code、Codex 等主流 AI 程式設計工具及通用 API 呼叫，支援企業級高併發、7×24 技術支援和自助開票。通過<a href="https://www.compshare.cn/coding-plan?ytag=GPU_YY-git_pptmaster0624">此連結</a>註冊，最高可獲得 <strong>¥10 免費體驗金</strong>。該專案已製作成 Agent【PPT 製作大師】，無需本地部署即可使用。</td>
  </tr>
</table>

</details>

> **可編輯早已是及格線——真正拉開差距的是原生深度。** PPT Master 交給你的是一份真正的 PowerPoint：母版、原生形狀、資料驅動的圖表與表格，而不是一堆扁平文本框，也不是套模板填空的結果。它還不止把幻燈片排得好看——先替你把邏輯理順，再談視覺；而這份原生深度在**持續向 PowerPoint 本身靠攏**，逐版本補齊更多原生能力。形態上，它是一套在有 Agent 能力的 AI 工具裡執行的工作流：把你的主題或材料交給 AI，就在你本機生成，資料不出本地，不鎖定任何平臺和模型。工作原理與能力邊界 → [產品定位](#產品定位)。

<p align="center">
  <a href="https://hugohe3.github.io/ppt-master/"><strong>線上預覽</strong></a> ·
  <a href="./examples/"><strong>示例下載</strong></a> ·
  <a href="./docs/zh/faq.md"><strong>常見問題</strong></a> ·
  <a href="./docs/zh/roadmap.md"><strong>路線圖</strong></a>
</p>

<h3 align="center">下載這份<a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_attention_is_all_you_need/exports/attention_is_all_you_need_narrated.pptx">帶音訊旁白的 <em>Attention Is All You Need</em> 論文精讀 deck</a>，在 PowerPoint 裡直接放映，每一頁都會自己"讀"給你聽 —— 這只是 PPT Master 能力的冰山一角。</h3>

<table>
  <tr>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_pritzker_2026"><img src="docs/assets/screenshots/preview_pritzker_2026.png" alt="雜誌風 — 普利茲克獎 2026" /></a><br/>
      <sub><b>雜誌風</b> — 建築攝影 + 排版網格，冷靜剋制的編輯感<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_pritzker_2026">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_pritzker_2026/exports/pritzker_2026.pptx">下載 .pptx</a></sub>
    </td>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_global_ai_capital_2026"><img src="docs/assets/screenshots/preview_global_ai_capital.png" alt="新聞風 — 2026 全球 AI 資本格局" /></a><br/>
      <sub><b>新聞 / 財經資料風</b> — 深色儀表盤，圖表驅動，彭博風<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_global_ai_capital_2026">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_global_ai_capital_2026/exports/global_ai_capital_2026.pptx">下載 .pptx</a></sub>
    </td>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_swiss_grid_systems"><img src="docs/assets/screenshots/preview_swiss_grid.png" alt="瑞士風 — 網格系統入門" /></a><br/>
      <sub><b>瑞士風</b> — 嚴格柵格，剋制字型，紅色點綴<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_swiss_grid_systems">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_swiss_grid_systems/exports/swiss_grid_systems.pptx">下載 .pptx</a></sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_glassmorphism_demo"><img src="docs/assets/screenshots/preview_glassmorphism_demo.png" alt="毛玻璃風 — AI Agent 工程化 Demo" /></a><br/>
      <sub><b>毛玻璃 SaaS</b> — 半透明疊層，漸變景深，產品 UI 感<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_glassmorphism_demo">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_glassmorphism_demo/exports/glassmorphism_demo.pptx">下載 .pptx</a></sub>
    </td>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_sugar_rush_memphis"><img src="docs/assets/screenshots/preview_sugar_rush_memphis.png" alt="孟菲斯風 — Sugar Rush 音樂節" /></a><br/>
      <sub><b>孟菲斯波普</b> — 高飽和原色，幾何圖形，俏皮活力<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_sugar_rush_memphis">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_sugar_rush_memphis/exports/sugar_rush_memphis.pptx">下載 .pptx</a></sub>
    </td>
    <td align="center" width="33%">
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_indie_bookstore_zine_guide"><img src="docs/assets/screenshots/preview_indie_bookstore_zine.png" alt="Zine 風 — 獨立書店指南" /></a><br/>
      <sub><b>Risograph Zine</b> — 雙色印刷質感，手作書店文化<br/>
      <a href="https://hugohe3.github.io/ppt-master/viewer.html?project=ppt169_indie_bookstore_zine_guide">線上翻頁</a> · <a href="https://raw.githubusercontent.com/hugohe3/ppt-master/main/examples/ppt169_indie_bookstore_zine_guide/exports/indie_bookstore_zine_guide.pptx">下載 .pptx</a></sub>
    </td>
  </tr>
</table>

<p align="center">
  <sub>以上示例均為一次性生成、未經精修（生成模型：Claude Opus 4.7 + <code>gpt-image-2</code>）。下載任意一份 .pptx 在 PowerPoint 裡開啟，是感受真實產出水平最快的方式。<br/><a href="https://hugohe3.github.io/ppt-master/">線上翻看全部示例 →</a> · <a href="./examples/"><code>examples/</code> 目錄</a> · <a href="./docs/zh/why-ppt-master.md">為什麼選 PPT Master？</a></sub>
</p>

<p align="center">
  更多端到端例項：<a href="https://space.bilibili.com/111258938/lists/8144072"><strong>合集·PPT-Master 能力展示</strong></a>（B 站）
</p>

---

丟進原材料，拿回的不是一張能改的靜態版面，而是**一份帶完整 PowerPoint 行為的成品**：原生頁間轉場、可按需開啟的入場動畫（預設關閉）、演講者備註一鍵合成音訊旁白乃至影片、圖表和表格可作為帶資料的原生物件匯出，也能沿用你自己的 PPT 模板來設計——直接拿去講，回頭還能接著改。每項能力怎麼用 → [快速入門](./docs/zh/getting-started.md)。

## 產品定位

**可編輯如今只是及格線——真正要緊的是你能拿到多少 PowerPoint。** PPT Master 交付的是 PowerPoint 的原生物件模型本身，而且有深度：帶調節手柄的原生形狀與連線符、按需的資料驅動圖表與表格、完整的文本 / 圖片 / 填充 / 效果，點開任意元素都作為原生 PowerPoint 物件繼續編輯；走模板 / 結構化路線時，它還能為你產出帶真正母版與版式（`p:sldMaster` / `p:sldLayout` 繼承）的 deck。

而且這份深度是**一個前進方向，不是一張固定清單。** PPT Master 的北極星是持續向 PowerPoint 本身靠攏：不斷開發、整合更多 PowerPoint 原生能力，一個版本接一個版本，縮小「AI 能替你生成的」和「你在 PowerPoint 裡手工能做出的」之間的差距。[PowerPoint ↔ SVG 對映指南](./docs/zh/powerpoint-svg-mapping.md) 逐條、誠實地記錄了這份能力今天覆蓋到哪——SmartArt 是刻意的排除，不是缺口。

形態上，它是一套在有 Agent 能力的 AI 工具裡執行的工作流（一個 "skill"）：你在對話方塊裡說"用這份 PDF 做一份 PPT"，它就按流程在你本機生成、匯出原生可編輯的 `.pptx`。你不寫任何程式碼，只做三件事——裝 Python、裝一個 AI 工具、把材料放進來。

從源材料生成新 deck 是主管線，但不是唯一路線：PPT Master 還能從你的參考資料中提煉可複用的品牌 / 版式 / 成品模板，把新內容填進你已有的 `.pptx` 並保留其設計，或為成品 deck 追加原生轉場、動畫和旁白——每條路線都有明確的保留契約。

在這份原生深度之上，這個形態還帶來三個承諾：

- **成本透明可控** — 工具免費開源，唯一成本是你自己的 AI 模型用量，不在此之外增加任何訂閱費用
- **資料不出本地** — 除與 AI 模型的對話外，全流程在你的電腦上完成
- **不鎖定平臺** — 任何具備 agent 能力的 AI IDE 均可驅動；Claude、GPT、Gemini、Kimi 等模型均可使用

為什麼選它、以及它不適合的場景 → [為什麼選 PPT Master](./docs/zh/why-ppt-master.md)；這些承諾背後的長期能力邊界 → [專案定位與能力邊界](./docs/zh/project-positioning.md)。

> [!IMPORTANT]
> ### 這是一個工具，不是一個許願池
> `harness + model = agent`——PPT Master 只負責工作流，產出上限由模型決定。推薦 **Kimi K3（或 Claude）大上下文視窗（~100 萬 token）+ AI 生圖（`gpt-image-2` 或 Google `gemini-3.1-flash-image`）**；其他模型能跑通流程，但有質量差距。
>
> 也別指望一把就拿到完美成品。它的價值是幫你把大部分枯燥的活兒幹掉，剩下的打磨交給你——做原生可編輯的 PPT，本就是為了讓你接著改，而不是甩給你一張改不動的圖。模型越便宜，要補的人工就越多；效果不理想，先升級模型，再對照[快速入門](./docs/zh/getting-started.md)和示例工程檢查用法。

---

## 關於作者

我是何雨果（Hugo He），投融資領域從業者（註冊會計師 · 資產評估師 · 諮詢工程師（投資）），工作中經常審閱和修改 PPT。我希望 AI 生成的幻燈片仍然能在 PowerPoint 裡繼續編輯，而不是被壓成一張張圖片——所以做了這個。

未來，使用 Python 和 AI agent 的能力會越來越重要，這個專案也想展示：僅憑這兩樣，你能走多遠。零基礎上手有一段學習曲線，但走完這段，你就接上了未來——做 PPT 只是個藉口，我真正想推廣的是 Python 和 agent。

---

## 你可能也感興趣

### <a href="https://github.com/microsoft/ResearchStudio">ResearchStudio-<img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/figures/reel-wordmark.png" alt="Reel" height="16"></a>

> 微軟開源專案，我最近也參與其中——從**論文**到**演講影片**、**海報**與**部落格**，自動化科研傳播的**最後一公里**。
>
> 📦 **倉庫：**[microsoft/ResearchStudio](https://github.com/microsoft/ResearchStudio) · 📄 **論文：**[arXiv:2607.04438](https://arxiv.org/abs/2607.04438)

<table align="center">
<tr>
<td align="center" valign="middle" width="53%">
  <a href="https://aka.ms/ResearchStudio">
    <img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/figures/reel_demo.gif" width="100%"
    alt="ResearchStudio-Reel 演示" />
  </a>
</td>
<td align="center" valign="middle" width="47%">
  <a href="https://aka.ms/ResearchStudio">
    <img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/examples/latent_diffusion_landscape/poster.png" width="100%" alt="ResearchStudio-Reel 生成的海報" />
  </a>
</td>
</tr>
</table>

<details>
<summary><strong>BibTeX</strong> —— 如果你在研究中使用了 ResearchStudio-Reel</summary>

```bibtex
@article{xiao2026researchstudioreel,
  title   = {ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog},
  author  = {Lingao Xiao and Yalun Dai and Yangyu Huang and Qihao Zhao and Wenshan Wu and Hugo He and Ruishuo Chen and Jin Jiang and Qianli Ma and Jiahuan Zhang and Xin Zhang and Ying Xin and Yang Ou and Yan Xia and Scarlett Li and Longbo Huang and Zhipeng Zhang and Yang He and Yap Kim Hui and Yan Lu},
  journal = {arXiv preprint arXiv:2607.04438},
  year    = {2026},
  url     = {https://arxiv.org/abs/2607.04438}
}
```

</details>

---

## 快速開始

### 1. 前置條件

**只需安裝 [Python](https://www.python.org/downloads/) 3.10+。** 其餘依賴在第 3 步下載好專案後，用一行 `pip install -r requirements.txt` 裝齊。

<details>
<summary><strong>Windows</strong> — 請看專門的<a href="./docs/zh/windows-installation.md">手把手安裝指南</a> ⚠️</summary>

Windows 需要一些額外步驟（PATH 設定、執行策略等）。我們為 Windows 使用者寫了一份**手把手安裝指南**：

**📖 [Windows 安裝指南](./docs/zh/windows-installation.md)** — 從零到跑通第一份 PPT，10 分鐘搞定。

簡要流程：從 [python.org](https://www.python.org/downloads/) 下載 Python → **安裝時勾選 "Add to PATH"** → 完成，依賴安裝見第 3 步。
</details>

<details>
<summary><strong>macOS / Linux</strong> — 安裝即用</summary>

```bash
# macOS
brew install python

# Ubuntu / Debian
sudo apt install python3 python3-pip
```
</details>

<details>
<summary><strong>邊緣場景備用方案</strong> — 99% 的使用者用不到</summary>

**Pandoc** — 只在需要轉小眾格式時才裝：`.doc`、`.odt`、`.rtf`、`.tex`、`.rst`、`.org`、`.typ`。`.docx`、`.html`、`.epub`、`.ipynb` 已由 Python 原生處理，不需要 pandoc。

```bash
# macOS
brew install pandoc

# Ubuntu / Debian
sudo apt install pandoc
```
</details>

### 2. 選擇一個 Agent

PPT Master 在**任何具備 agent 能力**（可讀寫檔案、執行命令、持續多輪對話）的工具裡都能跑。

沒用過這類工具也不用擔心：它們在本專案裡只扮演一個角色——一個能讀寫檔案的 AI 聊天視窗。從下表任選一款裝好即可，全程只用它的聊天面板，不需要寫任何程式碼。

> **作者最推薦：[Claude Code](https://claude.ai/code)** ——本專案開發與測試最充分的環境，CLI 與 VS Code / JetBrains 擴充套件均可。

| 型別 | 代表工具 | 說明 |
|---|---|---|
| **IDE 內建 agent** | • VS Code 架構（含 [VS Code](https://code.visualstudio.com/) 本體及分支與衍生）：[Cursor](https://cursor.sh/)、Trae、Codebuddy IDE、[Windsurf](https://codeium.com/windsurf) 等<br>• 其他架構：[Zed](https://zed.dev/) 等 | 編輯器原生整合 agent |
| **IDE 外掛 / 擴充套件** | [Claude Code](https://claude.ai/code)（VS Code / JetBrains 擴充套件）、[GitHub Copilot](https://github.com/features/copilot)、[Cline](https://cline.bot/)、通義靈碼 等 | 裝在 VS Code / JetBrains 等宿主裡使用 |
| **CLI agent** | [Claude Code](https://claude.ai/code) CLI、[Codex CLI](https://github.com/openai/codex)、Gemini CLI 等 | 終端裡執行，適合指令碼化 / 遠端 / 伺服器場景 |

> **模型推薦**：追求最佳效果，語言模型選 **[Kimi K3](https://www.kimi.com/code/?aff=ppt-master)**（或 Claude）驅動流程，搭配 AI 生圖 —— **`gpt-image-2`**（OpenAI）或 **`gemini-3.1-flash-image`**（Google）。本專案贊助商 Kimi Code 支援按量呼叫，很適合上手。

**🔑 想用 Claude / GPT / Gemini 但還沒有渠道？** 本專案贊助商 **[PackyCode](https://www.packyapi.com/register?aff=ppt-master)**、**[APIKEY.FUN](https://apikey.fun/register?aff=PPT-MASTER)** 與 **[RunAPI](https://runapi.co/register?aff=WMLJ)** 均支援按量呼叫 Claude、GPT、Gemini 等主流模型，無需訂閱、支援國內支付，併為本專案使用者提供專屬優惠（詳情見頁首）。

**🔀 手上有多個渠道？** 拿到多家的 API Key 後，[cc-switch](https://github.com/farion1231/cc-switch)（跨平臺桌面應用）可以一鍵切換 Claude Code、Codex、Gemini CLI 等工具的 API 供應商，免去手動改配置。

### 3. 配置專案

**方式 A — Git clone**（推薦；需先安裝 [Git](https://git-scm.com/downloads)）：首選這種方式，因為 clone 可以隨時拉取最新版本。

```bash
# GitHub
git clone https://github.com/hugohe3/ppt-master.git
# AtomGit（中国大陆地区网速更快）
git clone https://atomgit.com/hugohe3/ppt-master.git
cd ppt-master
```

然後安裝依賴：

```bash
pip install -r requirements.txt
```

**方式 B — 下載 ZIP**（無需安裝 Git，適合快速體驗）：
[GitHub](https://github.com/hugohe3/ppt-master) → **Code → Download ZIP** · [AtomGit](https://atomgit.com/hugohe3/ppt-master) → **克隆/下載 → 下載ZIP**（中國大陸地區訪問 GitHub 下載不便時用這個，網速更快）；解壓後同樣用 `pip install -r requirements.txt` 裝依賴。ZIP 沒有 Git 歷史，不能自動 `git pull`（更新見下）。

如果完整倉庫下載失敗、或嫌體積太大，可以改到 [Releases](https://github.com/hugohe3/ppt-master/releases) 頁面下載純技能包 `ppt-master-skill-*.zip`（約 50 MB，功能完整，但不含內建示例 deck）。

#### 日常更新

**Git clone 安裝：**

```bash
python3 skills/ppt-master/scripts/update_repo.py
```

指令碼會拉取最新版；如果 `requirements.txt` 有變化，會自動同步 Python 依賴。

**下載 ZIP 安裝：**

ZIP 目錄沒有 Git 歷史，不能自動 `git pull`。更新時請重新下載最新版 ZIP，解壓到新目錄，然後把舊目錄裡的 `.env` 和 `projects/` 複製過去，再執行：

```bash
pip install -r requirements.txt
```

> **方式 C — Skill marketplace**：倉庫已新增 `.claude-plugin/marketplace.json` 後設資料，可通過 [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) 生態一行安裝：
>
> ```bash
> # 跨 agent CLI（Claude Code、Cursor、Codex 等）
> npx skills add hugohe3/ppt-master
>
> # 或在 Claude Code 內
> /plugin marketplace add hugohe3/ppt-master
> /plugin install ppt-master@ppt-master
> ```
>
> 上述兩種安裝方式都只會拉取 skill 檔案本身（不含完整倉庫），後處理指令碼仍需在安裝目錄跑 `pip install -r requirements.txt`。

### 4. 開始創作

**先在 Agent 裡開啟專案資料夾：** 目標是讓 AI 工作在上一步解壓 / 克隆出來的 `ppt-master` 目錄裡——IDE 類工具通過選單 **檔案 → 開啟資料夾**（File → Open Folder）開啟它，AI 聊天面板通常在側邊欄；CLI 類工具先 `cd ppt-master` 再啟動。之後的一切都在聊天裡完成。

**提供原始材料（推薦）：** 將 PDF、DOCX、圖片等檔案放入 `projects/` 目錄下，在 AI 聊天面板中告訴它使用哪些檔案。獲取路徑的最快方式：在檔案管理器或 IDE 側邊欄中右鍵檔案 → **複製路徑**（Copy Path / Copy Relative Path），直接貼上進聊天框。

```
你：请用 projects/q3-report/sources/report.pdf 这份文件生成一份 PPT
```

**直接輸入內容：** 也可以把文字內容直接貼上進聊天視窗，AI 會根據這些內容生成 PPT。

```
你：请根据以下内容制作成 PPT：[粘贴你的文字内容...]
```

兩種方式下 AI 都會先確認設計規範：

```
AI：好的，先确认设计规范：
   [模板] B) 自由设计
   [格式] PPT 16:9
   [页数] 8-10 页
   ...
```

AI 全程處理——內容分析、視覺設計、SVG 生成、PPTX 匯出。

> **輸出說明：** SVG 管線統一由專案轉換器讀取 `svg_output/`，生成可直接編輯的原生 DrawingML `.pptx`，儲存至 `exports/<name>_<timestamp>.pptx`。正式交付流程會生成自包含預覽 `svg_final/`，並把 `svg_output/` 映象到 `backup/<timestamp>/svg_output/`；PowerPoint 手工“轉換為形狀”不在支援範圍。明確用於臨時測試的少量自包含頁面可改用[快速測試模式](./skills/ppt-master/workflows/profiles/quick-test.md)：只寫 SVG 頁面和一個 PPTX，不生成規劃、預覽、講稿、驗證報告或備份。圖表和表格預設匯出為 SVG 派生、可逐形狀編輯的 DrawingML 物件，優先保證 PowerPoint / Keynote / WPS 間的視覺一致性；加 `--native-charts-and-tables` 則把符合合同的組替換為帶資料來源和物件專屬編輯能力的 PowerPoint 原生 Chart/Table 物件，跨軟體渲染可能略有差異，儲存為 `exports/<name>_<timestamp>_native_charts_tables.pptx`。兩條路線都可編輯，區別在於 PowerPoint 物件模型，而不是“能否編輯”。

> **已有一份想複用的 `.pptx`？** 把那份 deck 連同素材給 AI，說「套模板」即可——它會把新內容（文字、表格、圖表資料）填進你現有的設計，只匯出你挑選的頁面，且保持原生可編輯。詳見 [常見問題](./docs/zh/faq.md) 與 [套模板工作流](./skills/ppt-master/workflows/template-fill-pptx.md)。

> **遇到問題？** AI 迷失上下文時，讓它先讀 `skills/ppt-master/SKILL.md`；其他問題檢視 **[常見問題](./docs/zh/faq.md)** — 涵蓋模型選擇、排版問題、匯出異常等，基於真實使用者反饋持續更新。

### 5. 圖片獲取（可選）

非使用者自帶圖片有兩條路徑，可在同一份 deck 裡按圖混用：

**A) AI 生圖** — `image_gen.py`。設定 `IMAGE_BACKEND` 和對應 `*_API_KEY`（`OPENAI_API_KEY`、`GEMINI_API_KEY` 等），流程會自動呼叫。`python3 skills/ppt-master/scripts/image_gen.py --list-backends` 檢視完整後端清單。`gpt-image-2` 目前綜合質量最佳。

**B) 網路圖片搜尋** — `image_search.py`。**零配置**可用；建議配置 `PEXELS_API_KEY` / `PIXABAY_API_KEY`（都免費申請）以獲得穩定的高質量結果：

- 不配置時只使用 Openverse / Wikimedia Commons，適合作為兜底，但容易出現構圖隨意、清晰度不穩定的圖片
- 配置後預設搜尋鏈會追加 Pexels / Pixabay，現代商業攝影、人物、辦公、生活方式和插畫類圖片質量明顯更穩定
- 許可自動處理：預設把 CC0、公有領域、Pexels / Pixabay 免署名許可、CC BY、CC BY-SA 一起納入候選；選中需署名的圖片時，Executor 會在該幻燈片自動新增小字署名。只有明確不能出現署名時，才使用 `--strict-no-attribution` 限制為免署名圖片
- 對視覺要求高的封面、產品圖、人物圖和品牌場景，優先順序建議：使用者自帶高畫質素材 / AI 生圖 > 配置 Pexels / Pixabay 的網路搜尋 > 零配置網路搜尋

上面提到的 API Key 統一通過 `.env` 配置。clone 安裝可以用 `cp .env.example .env`；skill marketplace 安裝建議使用持久的使用者級配置：

```bash
mkdir -p ~/.ppt-master
cp /path/to/installed/ppt-master/.env.example ~/.ppt-master/.env
```

PPT Master 會優先讀取當前程式環境變數，然後按順序讀取第一個存在的 `.env`：當前工作目錄、skill 安裝目錄（如 `~/.agents/skills/ppt-master/.env`）、clone 倉庫根目錄、`~/.ppt-master/.env`。

> 完整說明：[`image-generator.md`](./skills/ppt-master/references/image-generator.md)（AI）·[`image-searcher.md`](./skills/ppt-master/references/image-searcher.md)（網路）。

---

## 檔案導航

| | 檔案 | 說明 |
|---|------|------|
| 📘 | [快速入門](./docs/zh/getting-started.md) | 三步做出第一份 deck，外加模板、即時預覽、動畫、旁白、聲音復刻的用法（**新使用者從這裡開始**） |
| 🆚 | [為什麼選 PPT Master](./docs/zh/why-ppt-master.md) | 為什麼選它、以及它不適合的場景 |
| 🧭 | [專案定位與能力邊界](./docs/zh/project-positioning.md) | 長期定位、產品承諾與能力邊界 |
| 🪟 | [Windows 安裝指南](./docs/zh/windows-installation.md) | Windows 使用者手把手安裝教程 |
| 📖 | [SKILL.md](./skills/ppt-master/SKILL.md) | 核心流程與規則 |
| 📐 | [畫布格式](./skills/ppt-master/references/canvas-formats.md) | PPT 16:9、小紅書、朋友圈等 10+ 種格式 |
| 🛠️ | [指令碼與工具](./skills/ppt-master/scripts/README.md) | 所有指令碼和命令 |
| 💼 | [示例](./examples/README.md) | 所有示例專案 |
| 🏗️ | [技術路線](./docs/zh/technical-design.md) | 架構、設計哲學、為什麼選 SVG |
| ❓ | [常見問題](./docs/zh/faq.md) | 模型選擇、費用、排版問題排查、自定義模板 |

<sub>完整檔案索引 → [`docs/zh/`](./docs/zh/README.md)</sub>

---

## 貢獻

詳見 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 開源協議

[MIT](LICENSE)

## 致謝

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(author))（CRAP 設計原則）

## 相關工具

[cc-switch](https://github.com/farion1231/cc-switch) —— 一鍵切換 Claude Code / Codex / Gemini CLI 等工具的 API 供應商。

## 聯絡與合作

歡迎合作交流、將 PPT Master 整合到你的工作流，或者單純提問：

- 💬 **提問與分享** — [GitHub Discussions](https://github.com/hugohe3/ppt-master/discussions)
- 🐛 **Bug 反饋與功能建議** — [GitHub Issues](https://github.com/hugohe3/ppt-master/issues)

---

## 贊助與支援

PPT Master 目前主要由我開發維護。每個新模板、Bug 修復、檔案更新都需要持續的資源投入，目前由以下贊助方和個人支持者共同分擔。

**企業贊助方**

<a href="https://www.kimi.com/code/?aff=ppt-master"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/assets/sponsors/kimi-dark.svg"><img src="docs/assets/sponsors/kimi-light.svg" alt="Kimi" height="40" /></picture></a>
&nbsp;
<a href="https://www.packyapi.com/register?aff=ppt-master"><img src="docs/assets/sponsors/packycode.png" alt="PackyCode" height="40" /></a>
&nbsp;
<a href="https://apikey.fun/register?aff=PPT-MASTER"><img src="docs/assets/sponsors/apikey-fun.png" alt="APIKEY.FUN" height="40" /></a>
&nbsp;
<a href="https://runapi.co/register?aff=WMLJ"><img src="docs/assets/sponsors/runapi.png" alt="RunAPI" height="40" /></a>
&nbsp;
<a href="https://www.compshare.cn/coding-plan?ytag=GPU_YY-git_pptmaster0624"><img src="docs/assets/sponsors/youyun.png" alt="優雲智算" height="40" /></a>
&nbsp;
<a href="https://m.do.co/c/547f129aabe1"><img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/PoweredByDO/DO_Powered_by_Badge_blue.svg" alt="Powered by DigitalOcean" height="40" /></a>

**個人贊助**

如果 PPT Master 幫到了你，任何金額的個人贊助都能幫助專案持續更新、保持免費開源。

<a href="https://paypal.me/hugohe3"><img src="https://img.shields.io/badge/PayPal-赞助-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="通過 PayPal 贊助" /></a>

<img src="docs/assets/alipay-qr.jpg" alt="支付寶收款碼" width="220" />

---

Made with ❤️ by [何雨果 Hugo He](https://www.hehugo.com/) — 如果這個專案對你有幫助，請給一個 ⭐，也歡迎[贊助支援](#贊助與支援)。

<sub>官方釋出渠道：<a href="https://github.com/hugohe3/ppt-master">GitHub</a>（主倉庫）· <a href="https://atomgit.com/hugohe3/ppt-master">AtomGit</a>（映象）。其他平臺轉發版本均為非官方版本。MIT 協議，使用需保留署名。</sub>

[⬆ 回到頂部](#ppt-master--ai-生成原生-powerpoint支援任意檔案輸入)
