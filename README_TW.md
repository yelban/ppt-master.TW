# PPT Master — AI 生成原生可編輯 PPTX，支援任意檔案輸入

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
<summary>本專案由 <a href="https://www.packyapi.com/register?aff=ppt-master">PackyCode</a>、<a href="https://apikey.fun/register?aff=PPT-MASTER">APIKEY.FUN</a>、<a href="https://runapi.co/register?aff=WMLJ">RunAPI</a>、<a href="https://www.compshare.cn/coding-plan?ytag=GPU_YY-git_pptmaster0624">優雲智算</a> 等贊助方支援，得以持續免費開源。</summary>

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

> **AI 生成 PPT，不是 AI 套模板。** PPT Master 是一套在 AI IDE（Claude Code / Cursor / VS Code + Copilot 等）裡執行的工作流：把 PDF / DOCX / 網頁等材料交給 AI，它在你本機生成一份真正的 PowerPoint——每個元素都能在 PowerPoint 裡點開修改，資料不出本地，不鎖定任何平臺和模型。工作原理與能力邊界 → [產品定位](#產品定位)。

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

丟進原材料，拿回的這份 PPT **不只是能改**：它有 PPT 原生的轉場與入場動畫，演講者備註能直接合成音訊旁白，圖表和表格還能以帶資料的 PowerPoint 原生物件形式匯出，也能參考你自己的 PPT 模板來設計——一份能直接拿去講、回頭還能改的成品。每項能力怎麼用 → [快速入門](./docs/zh/getting-started.md)。

## 產品定位

**一個檔案如果在 PowerPoint 裡打不開、改不動，就不該被叫做 PPT。** 市面上的 AI PPT 工具大致分四類，PPT Master 只做最後一類：

| 型別 | 產物形態 | 能在 PowerPoint 裡逐元素改嗎 |
|---|---|:---:|
| 模板填空 | 套模板的 PPTX | 部分可以，受模板限制 |
| 圖片式 | 一頁一張大圖拼成 PPTX | ❌ 整頁是圖片 |
| HTML 演示 | 網頁演示 | ❌ 不是 PPTX |
| **原生可編輯（PPT Master）** | **真 DrawingML 形狀、文本框、圖表** | ✅ 每個元素都能點開改 |

形態上，它不是網站也不是 App，而是一套在 AI IDE（Claude Code / Cursor / VS Code + Copilot / Codebuddy 等）裡執行的工作流（一個 "skill"）：你在 IDE 的對話方塊裡說"用這份 PDF 做一份 PPT"，AI 按這套工作流在你本機生成真正可編輯的 `.pptx`。你不寫任何程式碼，要做的只有三件事——裝 Python、裝一個 AI IDE、把資料放進來。

這個形態換來三個別的工具很難同時給出的承諾：

- **成本透明可控** — 工具免費開源，唯一成本是你自己的 AI 模型用量，你用多少付多少，不在此之外增加任何訂閱費用
- **資料不出本地** — 你的檔案不應該為了做一份 PPT 就被上傳到別人的伺服器。除與 AI 模型的對話外，全流程在你的電腦上完成
- **不鎖定平臺** — 你的工作流不應該被任何一家公司綁架。Claude Code、Cursor、VS Code Copilot 等均可驅動；Claude、GPT、Gemini、Kimi 等模型均可使用

> [!IMPORTANT]
> ### 這是一個工具，不是一個許願池
> `harness + model = agent`——PPT Master 只負責工作流，產出上限由模型決定。推薦 **Claude 大上下文視窗（~100 萬 token）+ AI 生圖（`gpt-image-2`）**；其他模型能跑通流程，但有質量差距。
>
> 也別指望一把就拿到完美成品。它的價值是幫你把大部分枯燥的活兒幹掉，剩下的打磨交給你——做原生可編輯的 PPT，本就是為了讓你接著改，而不是甩給你一張改不動的圖。模型越便宜，要補的人工就越多；效果不理想，先升級模型，再對照[快速入門](./docs/zh/getting-started.md)和示例工程檢查用法。

---

## 關於作者

我是何雨果（Hugo He），投融資領域從業者（註冊會計師 · 資產評估師 · 諮詢工程師（投資）），工作中經常審閱和修改 PPT。我希望 AI 生成的幻燈片仍然能在 PowerPoint 裡繼續編輯，而不是被壓成一張張圖片——所以做了這個。

未來，使用 Python 和 AI agent 的能力會越來越重要，這個專案也想展示：僅憑這兩樣，你能走多遠。零基礎上手有一段學習曲線，但走完這段，你就接上了未來——做 PPT 只是個藉口，我真正想推廣的是 Python 和 agent。

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

> **模型推薦**：追求最佳效果選 **Claude Opus**，搭配 `gpt-image-2` 生圖；**Gemini 3.5 Flash** 目前綜合價效比很高，尤其速度很快，值得一試。

**🔑 想用 Claude / GPT / Gemini 但還沒有渠道？** 本專案贊助商 **[PackyCode](https://www.packyapi.com/register?aff=ppt-master)**、**[APIKEY.FUN](https://apikey.fun/register?aff=PPT-MASTER)** 與 **[RunAPI](https://runapi.co/register?aff=WMLJ)** 均支援按量呼叫 Claude、GPT、Gemini 等主流模型，無需訂閱、支援國內支付，併為本專案使用者提供專屬優惠（詳情見頁首）。

**🔀 手上有多個渠道？** 拿到多家的 API Key 後，[cc-switch](https://github.com/farion1231/cc-switch)（跨平臺桌面應用）可以一鍵切換 Claude Code、Codex、Gemini CLI 等工具的 API 供應商，免去手動改配置。

### 3. 配置專案

**方式 A — 下載 ZIP**（無需安裝 Git，適合快速體驗）：
[GitHub](https://github.com/hugohe3/ppt-master) → **Code → Download ZIP** · [AtomGit](https://atomgit.com/hugohe3/ppt-master) → **克隆/下載 → 下載ZIP**（國內網速更快）

如果你打算長期使用並持續更新，推薦使用下面的 Git clone 方式。

**方式 B — Git clone**（推薦；需先安裝 [Git](https://git-scm.com/downloads)）：

```bash
# GitHub
git clone https://github.com/hugohe3/ppt-master.git
# AtomGit（国内网速更快）
git clone https://atomgit.com/hugohe3/ppt-master.git
cd ppt-master
```

然後安裝依賴：

```bash
pip install -r requirements.txt
```

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

> **輸出說明：** 原生形狀版 `.pptx`（可直接編輯）儲存至 `exports/<name>_<timestamp>.pptx`；`svg_output/` 始終映象到 `backup/<timestamp>/svg_output/`，便於歸檔或後續重跑。加 `--svg-snapshot` 時，額外在 `exports/` 內並排生成 SVG 快照版 pptx（詳見[常見問題](./docs/zh/faq.md)）。需要 Office 2016+。圖表和表格預設匯出為 SVG 派生的形狀（在 PowerPoint / Keynote / WPS 間畫素一致）；加 `--native-objects` 則改為匯出**帶資料、可直接編輯的 PowerPoint 原生圖表 / 表格物件**（跨軟體渲染可能略有差異），儲存為 `exports/<name>_<timestamp>_native_charts.pptx`。

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
| 🆚 | [為什麼選 PPT Master](./docs/zh/why-ppt-master.md) | 與 Gamma、Copilot 等工具的對比 |
| 🪟 | [Windows 安裝指南](./docs/zh/windows-installation.md) | Windows 使用者手把手安裝教程 |
| 📖 | [SKILL.md](./skills/ppt-master/SKILL.md) | 核心流程與規則 |
| 📐 | [畫布格式](./skills/ppt-master/references/canvas-formats.md) | PPT 16:9、小紅書、朋友圈等 10+ 種格式 |
| 🛠️ | [指令碼與工具](./skills/ppt-master/scripts/README.md) | 所有指令碼和命令 |
| 💼 | [示例](./examples/README.md) | 所有示例專案 |
| 🏗️ | [技術路線](./docs/zh/technical-design.md) | 架構、設計哲學、為什麼選 SVG |
| ❓ | [常見問題](./docs/zh/faq.md) | 模型選擇、費用、排版問題排查、自定義模板 |

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

## Star History

<a href="https://star-history.com/#hugohe3/ppt-master&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=hugohe3/ppt-master&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=hugohe3/ppt-master&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=hugohe3/ppt-master&type=Date" />
 </picture>
</a>

---

## 贊助與支援

PPT Master 目前主要由我開發維護。每個新模板、Bug 修復、檔案更新都需要持續的資源投入，目前由以下贊助方和個人支持者共同分擔。

**企業贊助方**

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

[⬆ 回到頂部](#ppt-master--ai-生成原生可編輯-pptx支援任意檔案輸入)
