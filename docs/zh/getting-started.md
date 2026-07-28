# 快速入門

[English](../getting-started.md) | [Chinese](./getting-started.md)

---

最快做出第一份 deck 的路徑、圍繞它的各項能力——模板、即時預覽、動畫、旁白、聲音復刻——以及出問題時去哪裡查。章節大致按你真實使用時遇到它們的順序排列。每節都是精簡版,需要細節就點 **完整說明 →** 連結。

- [用模板](#用模板)
- [做出第一份 deck](#做出第一份-deck)
- [即時預覽與視覺化修改](#即時預覽與視覺化修改)
- [轉場與動畫](#轉場與動畫)
- [旁白與影片](#旁白與影片)
- [使用復刻音色](#使用復刻音色)
- [遇到問題怎麼辦](#遇到問題怎麼辦)

---

## 用模板

**可選。** 預設走**自由設計**——不需要模板,可以直接跳到下一節。只有當 deck 必須複用一套固定版式或品牌時,才需要模板。

**複用現成 `.pptx` 有兩條路,取決於你想要什麼結果:**

| 你想要… | 路徑 | 會發生什麼 |
|---|---|---|
| **用這份 deck 的原生頁面殼承載新內容** | Fill Native PPTX | 克隆選中的源頁面，並在 OOXML 中直接改寫文字 / 表格 / 圖表資料。來源設計保持原生；輸出是受現有頁面殼約束的新回填 deck。 |
| **先建立可複用設計系統，再生成新 deck** | Create Template → Generate PPTX | 從參考材料建立經過驗證的 Brand、Layout 或 Deck 工作區，再創作一份新 deck。新故事、結構與頁數都可以不同於來源。 |

前者:把 `.pptx` 連同素材(或一個主題)給 AI,說「套模板」——見 [套模板工作流](../../skills/ppt-master/workflows/template-fill-pptx.md)。本節其餘部分講 create-template。

**想把某份現成 PowerPoint 做成可複用工作區，必須顯式請求 Create Template 路線。** 原生 `.pptx` 加新材料預設屬於 Fill Native PPTX，並不是 Generate PPTX Step 3 可以直接消費的模板。先建立工作區：

```
你：用 /create-template 从 projects/brand/our_deck.pptx 创建一个可复用 Deck 模板
```

Create Template 會分析參考材料，確認結果屬於 Brand、Layout 還是 Deck，再創作或物化一個經過驗證的新工作區。匯入器只提供來源證據；最終工作區擁有 `templates/design_spec.md`、所需 SVG 原型與配套素材。如果需要 PowerPoint 評審檔案，再顯式執行可選預覽匯出；它會按需建立 `exports/<id>_template_preview.pptx`。生成時引用的是工作區根目錄。

在 create-template 簡報中選擇 `library`（沿用原預設）或 `project`。兩種範圍都要求 `templates/`，並使用可選的 `images/`、`icons/` 和按需生成的 `exports/`；空的可選目錄直接省略。專案範圍要求給出已初始化的目標專案；只有全域性庫範圍會執行註冊。

復刻出的模板可以放在兩個位置之一:

| 位置 | 路徑 | 說明 |
|---|---|---|
| **註冊進 skill 庫** | `skills/ppt-master/templates/<kind>/<id>/` | 可移植工作區並執行全域性註冊；問“有哪些模板”時會被列出來 |
| **放在 projects 下** | `projects/<name>/` | 相同的可移植工作區，不執行全域性註冊 |

兩種結果都通過對話裡給出**工作區根目錄路徑**來引用。Step 3 會解析 `templates/design_spec.md`；為相容目錄形態，也接受 `design_spec.md` 直接位於所給根目錄、且 SVG 已滿足當前合同的平鋪工作區。create-template 可在同一對話裡把已驗證的精確工作區根目錄直接交給 Step 3。兩種情況都以路徑為準，絕不認裸模板名。完整工作區可以在全域性庫與 `projects/` 之間複製或遷移，無需調整目錄結構；只有全域性庫註冊不同。

```
你：用 sources/report.pdf 做 deck,模板用 skills/ppt-master/templates/layouts/presentation_core/
```

完整說明 → [模板指南](./templates-guide.md)

---

## 做出第一份 deck

整個流程就三步。先裝好環境——只需要 Python,見 [快速開始](../../README_CN.md#快速開始)。

1. **把源材料放進** `projects/` —— PDF、DOCX、Markdown、一個網址,或直接要貼上的文字。
2. **在對話裡告訴 AI** 要把什麼做成 deck(如果上面準備了模板,把它的路徑一起給;否則就是自由設計):
   ```
   你：用 projects/q3-report/sources/report.pdf 做一份 PPT
   你：把這份內容做成 PPT：<貼上你的文字>
   ```
3. **拿回可編輯的 `.pptx`**,位於 `exports/<名称>_<时间戳>.pptx` —— 真正的 DrawingML 形狀、文本框、圖表,在 PowerPoint / Keynote / WPS / LibreOffice 裡點開就能改。

開始前 AI 會先確認一份簡短的設計規格(模板、格式、頁數……);之後內容分析、排版、配圖、SVG 生成、匯出都由它完成——這就是其它能力圍繞的核心環節。

---

## 即時預覽與視覺化修改

生成過程中會自動開啟瀏覽器預覽 `http://localhost:5050`。

- **即時看著每頁渲染**出來。
- **直接改,無需 AI** —— 選中元素後在右欄改文字、顏色、字型、字號;拖拽即可移動,或用方向鍵微調(`Shift` = 10px),`Ctrl+Z` 撤銷。改動即時預覽,點 **Apply changes** 寫回 `svg_output/`。
- **或寫註解交給 AI** —— 點選元素寫一句要改成什麼,點 **Submit annotations**,再回對話說"應用註解"(或 "apply my annotations"),AI 會改寫那塊區域並重新匯出 PPTX。

PPT Master 最初是純對話設計;視覺化編輯是在很多使用者提出後融入的(建立在 [@WodenJay](https://github.com/WodenJay) 的 [PR #85](https://github.com/hugohe3/ppt-master/pull/85) 之上)。

完整說明 → [即時預覽階段](../../skills/ppt-master/workflows/stages/live-preview.md)

---

## 轉場與動畫

匯出的 deck 用真正的 OOXML 儲存**頁間轉場**和可選的**頁內元素物件動畫**，
不是嵌入影片。預設保留 `fade` 頁間轉場，頁內動畫為 `none`；只有顯式使用
`-a auto`、203 個原生 `entrance_*` / `emphasis_*` / `path_*` / `exit_*`
預設之一，或 `animations.json` 才會啟用物件動畫。29 箇舊短名稱只保留為相容
輸入；新的動畫選擇統一使用帶字首的規範名稱。未知效果、Start
模式、非法時序值或缺失物件引用會直接阻斷匯出，候選 PPTX 還會在釋出前回讀
動畫目標、效果和 timing 結構。Microsoft PowerPoint 是動效行為的主要驗證
目標；Keynote、WPS、LibreOffice 可能重新對映個別效果。

完整說明 → [轉場與動畫](./animations.md)

---

## 旁白與影片

把演講者備註按頁生成語音旁白,把音訊嵌回 PPTX,再用 PowerPoint 匯出帶旁白和轉場的 MP4——無需第三方工具。

```
你：给这个 PPT 生成音频,并把音频嵌回重新导出
你：给这个 PPT 生成音频
```

旁白預設用 `edge-tts`(約 90 種語區);需要更高質量音色可配置雲端 provider。AI 會按 deck 語言推薦音色,生成前只問你一次。

完整說明 → [音訊旁白與影片匯出](./audio-narration.md)

---

## 使用復刻音色

用 ElevenLabs / MiniMax / Qwen / CosyVoice 復刻你自己的聲音(或在授權前提下復刻演講者的聲音),讓整份 deck 用 *你的聲音* 念出來。在 provider 控制台復刻一次,把得到的 `voice_id` 傳進來,PPT Master 就會用這個音色逐頁朗讀備註並嵌回 PPTX。

完整說明 → [使用復刻音色](./audio-narration.md#使用復刻音色)

---

## 遇到問題怎麼辦

[常見問題(FAQ)](./faq.md) 是持續更新的排查真值——來自真實使用者反饋。最常見情況的快速指引:

| 情況 | 先試這個 |
|---|---|
| AI 跑偏或漏了步驟 | 讓它重新讀 `skills/ppt-master/SKILL.md`、`skills/ppt-master/workflows/routing.md` 和已選路線的權威檔案。 |
| 視覺質量不理想 | 換成大上下文 Claude 模型 + `gpt-image-2`——harness 決定下限,模型決定上限。 |
| 文字溢位或元素重疊 | 重跑那一頁,或用即時預覽修;詳見 [FAQ](./faq.md)。 |
| 沒有生圖 API key | 零配置的網路圖片搜尋仍可作為兜底;見 [FAQ](./faq.md)。 |
| 動畫或部分效果在別的軟體裡不對 | Microsoft PowerPoint 是動效行為的主要驗證目標。Keynote / WPS / LibreOffice 可以開啟 `.pptx`，但可能重新對映或省略個別效果或 Start 語義；動效關鍵交付應在 PowerPoint 中驗證。 |
| 擔心長 deck 撐爆上下文 | 生成可走分段模式;詳見 [FAQ](./faq.md)。 |

模型選擇、費用、圖表可編輯性、自定義模板等,都在 [FAQ](./faq.md) 裡。
