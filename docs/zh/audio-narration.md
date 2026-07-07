# 音訊旁白與影片匯出

PPT Master 可以把演講者備註轉成逐頁音訊旁白（預設基於 [`edge-tts`](https://github.com/rany2/edge-tts) —— 微軟 Edge 的線上神經網路語音；也可配置 ElevenLabs、MiniMax、Qwen TTS、CosyVoice 使用高質量或復刻音色），再把音訊嵌入回 PPTX，由 PowerPoint 自帶的"匯出影片"一鍵產出帶旁白和轉場的 MP4，全程無需第三方工具。

## 你會得到什麼

- 每頁一個音訊檔案，存放於 `<project_path>/audio/`，檔名與 SVG 對齊（`01_cover.mp3`、`02_market_landscape.mp3` …）。
- 可選重新匯出：在 `exports/` 生成新版 PPTX，每頁對應的 `m4a` / `mp3` / `wav` 音訊已嵌入到該頁，且頁面切換時間按音訊長度自動設定——無人值守自動播放和影片匯出都不用再手動調時間。
- 演講者備註原樣保留。

## 它是怎麼做到的

1. **備註本身就是為 TTS 寫的口播稿**。PPT Master 的 notes 規範刻意產出適合朗讀的散文——沒有 `[过渡]` / `[停顿]` 這種舞臺標記，也沒有 `要点：` / `时长：` 這種 meta 行——念出來的內容就是頁面上的內容。
2. **AI 替你選音色**。當你提出生成旁白時，AI 根據 deck 的主語言（`zh-TW` / `en-US` / `ja-JP` / `ko-KR` / …）和所選 provider 拉取或解釋可用音色，挑出候選並給每個寫一句中文調性說明（如"穩重男聲·適合財報"）。語速/風格也會基於 notes 資訊密度給出推薦值。
3. **一次問完，一次回答**。AI 在一條訊息裡同時問三件事——生成模式、音色、是否把音訊嵌入回 PPTX——每項都標了推薦值。回"好"接受全部預設，或者只說要改的部分（如"音色 2，語速 -5%"）。
4. **執行**。指令碼寫出逐頁音訊到 `audio/`，再（如果你保留嵌入）重新匯出帶音訊的 PPTX。不支援長音訊匯入或自動拆分。

完整流程見 [`workflows/generate-audio.md`](../../skills/ppt-master/workflows/generate-audio.md)。

## 兩條嵌入路徑

| 命令 | 用途 |
|---|---|
| `--recorded-narration audio` | 準備 PowerPoint 的"錄製的計時和旁白"。要求每頁都有音訊，並寫入頁面自動推進時間。用於旁白影片匯出。 |
| `--narration-audio-dir audio` | 底層音訊嵌入能力。只嵌入匹配到的檔案，允許部分頁面有音訊。用於測試或後續手工整理。 |

## 怎麼觸發

deck 匯出後，在聊天裡直接說就行：

```
你: 给这个 PPT 生成音频
你: 帮我用日语给这个 deck 配一个温柔女声的旁白
你: Generate narration for this deck and re-export with audio embedded.
```

剩下的 AI 全包。

## 支援的語言

凡是 `edge-tts` 支援的 locale 都行——大約 90 個，覆蓋中文全部主要變體（`zh-TW` 普通話 / `zh-TW` 臺灣普通話 / `zh-HK` 粵語）、英文（美/英/澳/印）、日語、韓語、法語、德語、西班牙語、葡萄牙語、俄語、阿拉伯語等。任何 locale 的全量音色清單都可以這樣查：

```bash
python3 skills/ppt-master/scripts/notes_to_audio.py --list-voices --locale ja-JP
```

## 進階：手動呼叫指令碼

如果你想跳過 AI 流程直接跑命令：

```bash
# 1. 确保备注已切分（后处理 Step 7.1）
python3 skills/ppt-master/scripts/total_md_split.py <project_path>

# 2A. 用 edge-tts 生成 MP3（默认，无需 API Key）
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --voice zh-TW-YunjianNeural --rate +0%

# 2B. 用 MiniMax 生成 MP3（支持系统音色或复刻 voice_id）
export MINIMAX_API_KEY="your-minimax-api-key"
# 默认使用国内地址；海外访问可设置 MINIMAX_TTS_BASE_URL=https://api.minimax.io/v1/t2a_v2
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider minimax \
  --voice-id <minimax-voice-id> \
  --minimax-model speech-2.8-hd

# 2C. 用 Qwen TTS 生成音频（系统音色或复刻音色）
export DASHSCOPE_API_KEY="your-dashscope-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider qwen \
  --voice-id <qwen-voice> \
  --qwen-model qwen3-tts-flash \
  --qwen-language-type Chinese

# 2D. 用 CosyVoice 生成 MP3（系统音色或复刻/设计音色）
export COSYVOICE_API_KEY="your-dashscope-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider cosyvoice \
  --voice-id <cosyvoice-voice> \
  --cosyvoice-model cosyvoice-v3-flash

# 3.（可选）重新导出 PPTX 嵌入音频
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> \
  --recorded-narration audio
```

edge 模式下 `--voice` 是必填項。雲端 provider 使用 `--voice-id` 傳入對應平臺的系統音色或復刻音色 ID。聲音復刻本身先在對應平臺控制台/API 中完成，`notes_to_audio.py` 使用得到的 voice ID 生成逐頁旁白。

進入 PPTX 的旁白音訊必須是 PowerPoint 可靠格式：`m4a`（AAC）、`mp3` 或 `wav`。內建生成路徑預設使用 `mp3`；如果 provider 產出 `pcm`、`opus` 或 `flac`，需要先轉碼再嵌入。

## 使用復刻音色

四個雲端 provider —— **ElevenLabs**、**MiniMax**、**Qwen**、**CosyVoice** —— 都支援用一段較短的音訊樣本復刻一個新音色，再用這個音色合成新語音。只要你能拿到 `voice_id`，PPT Master 就能用這個音色把整份 deck 念出來。（`edge` 不支援復刻。）

**職責切分**：聲音復刻本身在 provider 的控制台或 API 完成——你上傳一段樣本（一般 10 秒到幾分鐘的乾淨錄音），平臺給你返回一個 `voice_id`。PPT Master 在*消費*側：拿到 `voice_id` 後用這個音色逐頁朗讀備註。PPT Master 不會把你的樣本上傳到任何地方。

| Provider | 復刻入口 | 樣本時長 |
|---|---|---|
| ElevenLabs | [elevenlabs.io](https://elevenlabs.io) → Voices → Add Voice → Instant / Professional Voice Cloning | 1 分鐘（Instant）/ 30 分鐘以上（Professional） |
| MiniMax | [platform.minimaxi.com](https://platform.minimaxi.com) → 語音克隆 | 10 秒 – 5 分鐘 |
| Qwen TTS | [DashScope 控制台](https://dashscope.console.aliyun.com) → 語音合成 → 聲音復刻 | 10 秒 – 5 分鐘 |
| CosyVoice | [DashScope 控制台](https://dashscope.console.aliyun.com) → 語音合成 → 音色復刻 | 10 秒 – 5 分鐘 |

**復刻完之後怎麼用** —— 在聊天裡告訴 AI 即可，AI 會跳過音色推薦環節直接用你的 `voice_id`：

```
你: 用 MiniMax 我克隆的音色生成旁白，voice_id 是 xxxxxxx
你: 用我在 ElevenLabs 复刻的 voice id abc123 生成
```

也可以直接跑指令碼：

```bash
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider minimax --voice-id <你的复刻 voice id> \
  --minimax-model speech-2.8-hd
```

把 `--provider minimax` 換成 `elevenlabs` / `qwen` / `cosyvoice` 就能切到對應平臺；`--voice-id` 接收復刻音色和接收系統音色的方式完全一樣。

**注意**：

- **授權** —— 只復刻你自己擁有的、或拿到了明確授權的聲音。每個 provider 的服務條款都禁止冒用他人聲音。
- **語言覆蓋** —— 復刻出來的音色會繼承說話人的口音。對中英混合等多語 deck，建議挑一個對你樣本語言組合處理較好的 provider；ElevenLabs `eleven_multilingual_v2` 和 CosyVoice 通常最寬容。
- **一次復刻、長期複用** —— `voice_id` 不過期。復刻一次，可以給任意多份 deck 配旁白。

## 依賴

```bash
python3 -m pip install edge-tts
```

已寫入 `skills/ppt-master/requirements.txt`。`edge-tts` 呼叫微軟的線上 TTS 服務，**生成時**需要聯網；生成後的音訊是本地檔案，PowerPoint 播放和影片匯出都不依賴網路。雲端 TTS provider 不需要額外 Python 包，直接通過 HTTPS 呼叫；按 `.env.example` 配置對應 API Key 即可。

## 經驗值

- **語速**：PPT Master 預設每頁 2–5 句備註，`+0%` 聽感最自然。如果某頁特別密集（長技術段落），可以試 `-5%`。
- **改某一頁**：改對應的 `notes/<page>.md`，再跑一次 `notes_to_audio.py`（指令碼會重新生成全量 MP3，整套 deck 跑一遍成本很低）。
- **混合語言 deck**（中文裡夾英文術語等）：主流 locale 的神經語音對嵌入的外語詞處理得不錯——按主語言挑音色，先用一頁試聽再批次。

---

## 匯出為影片

帶旁白的 PPTX 在 `exports/` 裡就緒後，PowerPoint 自帶"建立影片"功能可以直接把它匯出成 MP4——不需要任何第三方工具。嵌入的音訊會作為每頁旁白播放；頁間切換時間已經由 PPT Master 在嵌入時按音訊長度自動設好（用 `--recorded-narration audio` 重新匯出時），所以影片節奏和旁白完全同步。`--recorded-narration` 會拒絕 `on-click` 物件動畫，因為 PPT Master 不生成物件級點選計時。

**PowerPoint（Windows / Mac，Office 2016+）**：

1. 開啟 `exports/` 裡那份帶旁白的 `.pptx`。
2. **檔案 → 匯出 → 建立影片**。
3. 選清晰度（4K / 全高畫質 / 高畫質 / 標準）以及"使用錄製的計時和旁白"——PPT Master 已經替你錄好了。
4. **建立影片** → 儲存為 `.mp4`（Windows 也支援 `.wmv`）。

**Keynote（Mac）**：開啟 deck → **檔案 → 匯出到 → 影片…** ——Keynote 同樣會讀取嵌入的音訊和分頁計時，輸出 `.m4v` / `.mov`。

**經驗值**：

- **不需要麥克風、不需要錄製環節**——音訊是合成的，重跑可重現。
- **動畫保留**：PPT Master 的頁間轉場和無點選頁內元素入場動畫是真正的 OOXML 動畫，匯出影片後正常播放。詳見 [轉場與動畫](./animations.md)。
- **單頁改音訊**：改對應 `notes/<page>.md`，再跑一遍 `notes_to_audio.py` + 嵌入步驟，再重新匯出影片——單頁迭代通常不到一分鐘。
- **檔案大小**：20 頁全高畫質 deck 通常是 30–80 MB，取決於圖片量。需要小檔案分享時降到高畫質就行。
