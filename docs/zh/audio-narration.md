# 音訊旁白與影片匯出

[English](../audio-narration.md) | [Chinese](./audio-narration.md)

---

PPT Master 可以把演講者備註轉成逐頁音訊旁白（預設基於 [`edge-tts`](https://github.com/rany2/edge-tts) —— 微軟 Edge 的線上神經網路語音；也可配置 ElevenLabs、MiniMax、Qwen TTS、CosyVoice 使用高質量或復刻音色）。Edge 路徑還會從同一次 TTS 流中寫出該頁的 SRT；音訊可繼續嵌入 PPTX，供 PowerPoint 使用原生影片匯出。

## 你會得到什麼

- 每頁一個音訊檔案，存放於 `<project_path>/audio/`，檔名與 SVG 對齊（`01_cover.mp3`、`02_market_landscape.mp3` …）。
- 使用 Edge 時，每頁還有一個同名字幕檔案，存放於 `<project_path>/notes/subtitles/`（`01_cover.srt`、`02_market_landscape.srt` …）。每個檔案使用以 `00:00:00,000` 為原點的頁內時間軸，時間來自 Edge 的詞邊界。
- 提供 SVG 到 SRT 的計時計劃後，還會重建 `animations.json`：無點選物件動畫會等待相關字幕 cue；同時生成與最終 PPTX 時間軸一致的 `<project_path>/notes/subtitles/total.srt`。PowerPoint 匯出影片後，還可用同一命令根據影片音軌校準每頁起點，得到幀級對齊的外掛字幕。
- 可選重新匯出：在 `exports/` 生成新版 PPTX，每頁對應的 `m4a` / `mp3` / `wav` 音訊已嵌入到該頁，且頁面切換時間按音訊長度自動設定——無人值守自動播放和影片匯出都不用再手動調時間。
- Windows 下可選原生影片匯出：`powerpoint_video.py` 把最終帶旁白 PPTX 交給 PowerPoint 2016+，並等待其原生 MP4 編碼成功或失敗。
- 演講者備註原樣保留。

## 它是怎麼做到的

1. **備註本身就是為 TTS 寫的口播稿**。PPT Master 的 notes 規範刻意產出適合朗讀的散文——沒有 `[过渡]` / `[停顿]` 這種舞臺標記，也沒有 `要点：` / `时长：` 這種 meta 行——念出來的內容就是頁面上的內容。
2. **AI 替你選音色**。當你提出生成旁白時，AI 根據 deck 的主語言（`zh-TW` / `en-US` / `ja-JP` / `ko-KR` / …）和所選 provider 拉取或解釋可用音色，挑出候選並給每個寫一句中文調性說明（如"穩重男聲·適合財報"）。語速/風格也會基於 notes 資訊密度給出推薦值。
3. **一次問完，一次回答**。AI 在一條訊息裡同時確認 provider、音色、語速、是否嵌入 PPTX，以及是否繼續匯出影片；每項都標推薦值。回"好"接受全部預設，或者只說要改的部分（如"音色 2，語速 -5%"）。
4. **執行**。使用 Edge 時，指令碼從同一次流中把每頁 MP3 和 SRT 分別寫到 `audio/` 與 `notes/subtitles/`；雲端 provider 目前仍只寫音訊。對於 Generate PPTX，AI 將當前 SVG 內容組對映到編號後的 SRT cue，重建無點選動畫，再匯出帶音訊的 PPTX；最後從該 PPTX 讀回實際計時併合並逐頁 SRT。若使用者選擇自動影片匯出且本機 Windows PowerPoint 相容，則繼續呼叫 PowerPoint 原生編碼器，等 MP4 完成後再校準交付字幕。不支援長音訊匯入或自動拆分。

字幕保持為外部 SRT 檔案：PPT Master 不把字幕嵌入 PPTX，也不燒錄進 MP4。自動影片匯出委託給本機 Windows PowerPoint，並不是另一套渲染器。

共享階段見 [`workflows/stages/generate-audio.md`](../../skills/ppt-master/workflows/stages/generate-audio.md)。

## 兩條嵌入路徑

| 命令 | 用途 |
|---|---|
| `--recorded-narration audio` | 準備 PowerPoint 的"錄製的計時和旁白"。要求每頁都有音訊，並寫入頁面自動推進時間。用於旁白影片匯出。重匯出檔案儲存為 `exports/<name>_<timestamp>_narrated.pptx`。 |
| `--narration-audio-dir audio` | 底層音訊嵌入能力。只嵌入匹配到的檔案，允許部分頁面有音訊。用於測試或後續手工整理。匯出檔案同樣帶 `_narrated` 字尾。 |

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

# 2A. 用 edge-tts 生成 MP3/SRT 对（默认，无需 API Key）
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --voice zh-TW-YunjianNeural --rate +0%

# 2B. 用 ElevenLabs 生成 MP3（需要 ELEVENLABS_API_KEY）
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider elevenlabs \
  --voice-id <elevenlabs-voice-id> \
  --elevenlabs-model eleven_multilingual_v2

# 2C. 用 MiniMax 生成 MP3（支持系统音色或复刻 voice_id）
export MINIMAX_API_KEY="your-minimax-api-key"
# 默认使用国内地址；海外访问可设置 MINIMAX_TTS_BASE_URL=https://api.minimax.io/v1/t2a_v2
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider minimax \
  --voice-id <minimax-voice-id> \
  --minimax-model speech-2.8-hd

# 2D. 用 Qwen TTS 生成音频（系统音色或复刻音色）
export DASHSCOPE_API_KEY="your-dashscope-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider qwen \
  --voice-id <qwen-voice> \
  --qwen-model qwen3-tts-flash \
  --qwen-language-type Chinese

# 2E. 用 CosyVoice 生成 MP3（系统音色或复刻/设计音色）
export COSYVOICE_API_KEY="your-dashscope-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --provider cosyvoice \
  --voice-id <cosyvoice-voice> \
  --cosyvoice-model cosyvoice-v3-flash

# 3. 输出整套 SRT 的指纹，再对照每页当前 SVG 内容组与 SRT cue，编写
#    <project_path>/narration_timing.json；没有对应口播的组不写 cue，
#    后续按正常动画顺序出现。
python3 skills/ppt-master/scripts/narration_sync.py fingerprint <project_path>

# 4. 根据正式 SRT 重建无点击对象动画计时
python3 skills/ppt-master/scripts/narration_sync.py animations <project_path> \
  --narration-padding 0.5 --force

# 5. 重新导出 PPTX 嵌入音频
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> \
  -o <final_narrated_pptx> --no-merge --recorded-narration audio \
  --narration-padding 0.5

# 6. 按最终 PowerPoint 计时合并逐页 SRT
python3 skills/ppt-master/scripts/narration_sync.py subtitles <project_path> \
  --pptx <final_narrated_pptx> --force

# 7. Windows 可选：通过 PowerPoint 导出视频并等待完成
python3 skills/ppt-master/scripts/powerpoint_video.py --check
python3 skills/ppt-master/scripts/powerpoint_video.py \
  <final_narrated_pptx> -o exports/<final_video>.mp4

# 8. 根据导出音轨校准每页起点，生成与视频同名的外挂 SRT
python3 skills/ppt-master/scripts/narration_sync.py subtitles <project_path> \
  --pptx <final_narrated_pptx> --video <powerpoint_exported_video> \
  -o exports/<powerpoint_exported_video_stem>.srt --force
```

edge 模式下 `--voice` 是必填項，可用 `--list-voices --locale <locale>` 檢視音色。
Edge 預設同時生成最多 3 頁音訊/SRT。可用 `--concurrency <N>` 調整；
排查連線問題時可設為 `--concurrency 1`。雲端 provider 仍保持序列。

Edge 命令會從同一次流式請求中生成 `audio/<stem>.mp3` 與 `notes/subtitles/<stem>.srt`。句末標點必定結束一條字幕；單條超過預設 20 個可見字元時，優先在逗號、分號或冒號處拆分，仍然過長才在最近的詞邊界拆分。可用 `--subtitle-max-chars` 調整上限。相鄰字幕最多允許 100 毫秒的計時重疊：後一句起點會移到前一句終點；超過該範圍則報錯。每頁 SRT 使用從零計時的頁內時間基準，並保留 Edge `WordBoundary` 的實際時間（包括首條字幕前的靜音）；雲端 provider 命令目前只生成音訊。

`narration_timing.json` 與 `animations.json` 刻意分離：前者記錄整套有序 SRT 的 SHA-256、旁白 padding、有序 SVG 組 ID 和可選的 1-based cue 編號。`narration_sync.py animations` 會拒絕過期的 SRT 指紋，用當前 SVG 校驗組 ID，並用 PowerPoint 支援的欄位完整替換動畫 sidecar。`narration_sync.py subtitles` 從最終 PPTX 讀取真實頁面關係順序、毫秒級頁面推進與轉場時間，因此 `total.srt` 使用原生 PPTX 時間軸。相對 `--pptx` 路徑按 `<project_path>` 解析。

PowerPoint 的影片編碼器可能把每個頁面 / 媒體段落量化到輸出幀時鐘；即使 PPTX 計時值正確，這些很小的分頁誤差仍可能逐頁累積。把最終 `.mp4` / `.wmv` / `.mov` 通過 `--video` 傳入後，指令碼會用歸一化音訊相關性在影片音軌中定位每頁原始旁白。它只改頁級偏移，Edge 的字幕文本和頁內 `WordBoundary` 時間保持不變；這是影片匯出後的字幕校準步驟，不會改寫影片。

最終帶旁白的 SVG 匯出固定使用 `--no-merge`。讓每條 SVG 文本行保持獨立文本框，可以保留作者座標；合併段落會讓 PowerPoint 重新計算多行文本幾何，可能造成肉眼可見的偏移。

```json
{
  "version": 1,
  "srt_sha256": "<sha256 of the ordered page-local SRT set>",
  "narration_padding": 0.5,
  "slides": {
    "01_title": {
      "groups": [
        { "id": "page-title", "cue": 1 },
        { "id": "supporting-visual" }
      ]
    }
  }
}
```

ElevenLabs 模式下 `--voice-id` 是必填項，可從賬戶中列出音色：

```bash
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
python3 skills/ppt-master/scripts/notes_to_audio.py --provider elevenlabs --list-voices
```

MiniMax、Qwen 與 CosyVoice 使用 `--voice-id` 傳入對應平臺的系統音色或復刻音色 ID。聲音復刻本身先在對應平臺控制台 / API 中完成，`notes_to_audio.py` 使用得到的 voice ID 生成逐頁旁白。

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
- **Provider 保留策略** —— 只要該音色仍存在於你的 provider 賬戶中，就可以繼續複用對應 `voice_id`；保留、刪除與過期規則以各平臺政策為準。

## 依賴

```bash
python3 -m pip install edge-tts
```

已寫入 `skills/ppt-master/requirements.txt`。`edge-tts` 呼叫微軟的線上 TTS 服務，**生成時**需要聯網；生成後的音訊是本地檔案，PowerPoint 播放和影片匯出都不依賴網路。雲端 TTS provider 不需要額外 Python 包，直接通過 HTTPS 呼叫；按 `.env.example` 配置對應 API Key 即可。

自動 MP4 匯出不增加 Python 依賴，但要求 Windows PowerPoint 2016+ 與 Windows PowerShell；macOS 或沒有相容 PowerPoint 的機器保留帶旁白 PPTX，改用手動匯出。

## 經驗值

- **語速**：在 Generate PPTX 路線上，PPT Master 會根據最終 SVG 中的獨立資訊組調整講稿長度；每頁 2–5 句只是常見節奏，並非上限。可先使用 `+0%`，較密且刻意保留細節的講稿可嘗試 `-5%`。
- **改某一頁**：改對應的 `notes/<page>.md`，再跑一次 `notes_to_audio.py`（指令碼會重新生成全量 MP3，整套 deck 跑一遍成本很低）。
- **混合語言 deck**（中文裡夾英文術語等）：主流 locale 的神經語音對嵌入的外語詞處理得不錯——按主語言挑音色，先用一頁試聽再批次。

---

## 匯出為影片

帶旁白的 PPTX 在 `exports/` 裡就緒後，Windows PowerPoint 2016+ 可通過下面的介面自動匯出：

```bash
python3 skills/ppt-master/scripts/powerpoint_video.py \
  <final_narrated_pptx> -o <final_video.mp4>
```

命令使用錄製的計時和旁白，預設輸出 1080p/30fps，並在 PowerPoint 明確成功或失敗後才返回。嵌入音訊作為逐頁旁白播放，頁面自動推進時間控制影片節奏。`--recorded-narration` 會拒絕 `on-click` 物件動畫，因為 PPT Master 不生成物件級點選計時。

**PowerPoint 手動回退（Windows / Mac，Office 2016+）**：

1. 開啟 `exports/` 裡那份帶旁白的 `.pptx`。
2. **檔案 → 匯出 → 建立影片**。
3. 選清晰度以及"使用錄製的計時和旁白"。
4. **建立影片** → 儲存為 `.mp4`（Windows 也支援 `.wmv`）。
5. 若要讓外掛字幕最貼合最終影片，再執行上面的 `narration_sync.py subtitles --video ...`，把生成的同名 SRT 與影片放在一起。

PowerPoint for Mac 可以手動匯出 MP4/MOV，但微軟明確說明其影片匯出不會播放動畫效果。需要動畫保真時，應使用 Windows 自動匯出路徑。

**Keynote（Mac）**：開啟 deck → **檔案 → 匯出到 → 影片…** ——Keynote 同樣會讀取嵌入的音訊和分頁計時，輸出 `.m4v` / `.mov`。

**經驗值**：

- **不需要麥克風、不需要錄製環節**——音訊是合成的，重跑可重現。
- **Windows 動畫保真**：PowerPoint 的 Windows 影片匯出會保留 PPT Master 的原生頁間轉場和無點選物件動畫；Mac 影片匯出存在上面的限制。詳見 [轉場與動畫](./animations.md)。
- **單頁改音訊**：改對應 `notes/<page>.md`，再跑一遍 `notes_to_audio.py` + 嵌入步驟，再重新匯出影片——單頁迭代通常不到一分鐘。
- **檔案大小**：20 頁全高畫質 deck 通常是 30–80 MB，取決於圖片量。需要小檔案分享時降到高畫質就行。
