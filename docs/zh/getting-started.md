# 快速入門

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
| **就要這份 deck,換成新內容** | 套模板(template fill) | 挑出合適的頁面,把文字 / 表格 / 圖表資料直接寫回原檔案。設計、版式、圖片、動畫都保留;輸出就是同一份 deck,原生可編輯。最快;但受限於現有頁面。 |
| **基於這份 deck 的風格生成新 deck** | create-template | 把 `.pptx` 解析成可複用的風格資產包,再走 SVG 管線**重新生成**——結構自由、頁數任意。更靈活;完整重建。 |

前者:把 `.pptx` 連同素材(或一個主題)給 AI,說「套模板」——見 [套模板工作流](../../skills/ppt-master/workflows/template-fill-pptx.md)。本節其餘部分講 create-template。

**想基於某份現成 PPT 的風格重新生成 deck,必須顯式走 create-template 流程——別直接丟個 `.pptx` 指望 AI 自動處理。** AI 預設走自由設計,不會主動切進建立模板的流程;不顯式啟動它,生成過程就容易錯亂。先用 create-template 把那份 `.pptx` 復刻成 PPT Master 模板:

```
你：用 /create-template 把这个复刻成模板：projects/brand/our_deck.pptx
```

這會跑 `pptx_template_import.py`,把檔案重建成可複用的資產包——版式 SVG + `design_spec.md` + 抽取出的主題色、字型、圖片。生成時引用的就是這個資產包。

復刻出的模板可以放在兩個位置之一:

| 位置 | 路徑 | 說明 |
|---|---|---|
| **註冊進 skill 庫** | `skills/ppt-master/templates/layouts/<id>/` | 全域性,所有專案可複用;跑 `register_template.py` 後,問"有哪些模板"時會被列出來 |
| **放進專案裡** | `projects/<project>/templates/` | 專案本地;給路徑即用,無需註冊 |

無論放哪,生成時都靠在對話裡給出它的**目錄路徑**來引用——工作流只認顯式路徑,絕不認裸模板名:

```
你：用 sources/report.pdf 做 deck,模板用 skills/ppt-master/templates/layouts/academic_defense/
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

完整說明 → [即時預覽工作流](../../skills/ppt-master/workflows/live-preview.md)

---

## 轉場與動畫

匯出的 deck 自帶**頁間轉場**和**頁內元素入場動畫**,輸出為真正的 OOXML——不是嵌入影片。預設元素進入頁面時自動級聯入場,無需設定,在 PowerPoint 和 Keynote 中原生播放,無需額外工具。只有當你想要特定順序、效果或時序時,才需要定製。

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
| AI 跑偏或漏了步驟 | 讓它重新讀 `skills/ppt-master/SKILL.md`。 |
| 視覺質量不理想 | 換成大上下文 Claude 模型 + `gpt-image-2`——harness 決定下限,模型決定上限。 |
| 文字溢位或元素重疊 | 重跑那一頁,或用即時預覽修;詳見 [FAQ](./faq.md)。 |
| 沒有生圖 API key | 零配置的網路圖片搜尋仍可作為兜底;見 [FAQ](./faq.md)。 |
| 動畫或部分效果在別的軟體裡不對 | 檔案是標準 `.pptx`,PowerPoint / Keynote / WPS / LibreOffice 都能開啟;元素動畫在 PowerPoint 2016+ 和 Keynote 還原最完整,更老的 Office 會把部分效果降級為 Appear。 |
| 擔心長 deck 撐爆上下文 | 生成可走分段模式;詳見 [FAQ](./faq.md)。 |

模型選擇、費用、圖表可編輯性、自定義模板等,都在 [FAQ](./faq.md) 裡。
