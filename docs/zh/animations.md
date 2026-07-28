# 頁間轉場與元素動畫

[English](../animations.md) | [中文](./animations.md)

---

PPT Master 會把**頁間轉場**和可選的**元素物件動畫**寫成真正的 PowerPoint
OOXML，而不是嵌入影片。物件動畫包括進入、強調、動作路徑和退出。本文只說明
使用者需要做的選擇和常用命令；精確效果對映、完整 sidecar schema、錨點規則與
封包校驗統一由[動畫執行規範](../../skills/ppt-master/references/animations.md)維護。

## 預設行為

| 層級 | 預設 | 含義 |
|---|---|---|
| 頁間轉場 | `fade`，0.4 秒 | 頁面之間使用剋制的視覺過渡 |
| 元素物件動畫 | **`none`（關閉）** | 每頁一次性完整出現；只有當動效確實有助於表達時才開啟 |

修改動畫設定不需要重新生成頁面，只需對同一份 `svg_output/` 重跑 `svg_to_pptx.py`。

## 常用操作

| 目標 | 命令 |
|---|---|
| 保持預設設定 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project>` |
| 更換頁間轉場 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t push` |
| 關閉視覺轉場 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -t none` |
| 每 5 秒自動翻頁 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --auto-advance 5` |
| 開啟自動元素入場 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto` |
| 全部使用同一種入場效果 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation entrance_fade` |
| 全部使用同一種原生強調效果 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation emphasis_spin` |
| 全部使用同一種原生動作路徑 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation path_circle` |
| 全部使用同一種原生退出效果 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> --animation exit_fade` |
| 單擊逐個揭示元素 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto --animation-trigger on-click` |
| 所有元素同時入場 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto --animation-trigger with-previous` |
| 放慢逐步揭示節奏 | `python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -a auto --animation-duration 0.5 --animation-stagger 0.8` |

48 個規範頁間切換標識已經覆蓋當前 PowerPoint 效果庫的三個完整分組：

- 細微：平滑 `morph`、淡入/淡出 `fade`、推入 `push`、擦除 `wipe`、
  分割 `split`、顯示 `reveal`、切入 `cut`、隨機線條 `random_bars`、
  形狀 `shape`、揭開 `uncover`、覆蓋 `cover`、閃光 `flash`。
- 華麗：跌落 `fall_over`、懸掛 `drape`、簾式 `curtains`、風 `wind`、
  上拉帷幕 `prestige`、折斷 `fracture`、壓碎 `crush`、剝離 `peel_off`、
  頁面捲曲 `page_curl`、飛機 `airplane`、日式摺紙 `origami`、溶解
  `dissolve`、棋盤 `checkerboard`、百葉窗 `blinds`、時鐘 `clock`、
  漣漪 `ripple`、蜂巢 `honeycomb`、閃耀 `glitter`、渦流 `vortex`、
  碎片 `shred`、切換 `switch`、翻轉 `flip`、庫 `gallery`、立方體
  `cube`、門 `doors`、框 `box`、梳理 `comb`、縮放 `zoom`、隨機
  `random`。
- 動態內容：平移 `pan`、摩天輪 `ferris_wheel`、傳送帶 `conveyor`、
  旋轉 `rotate`、視窗 `window`、軌道 `orbit`、飛過 `fly_through`。

舊標識 `strips`、`circle`、`diamond`、`newsflash`、`plus`、`pull`、
`wedge`、`wheel` 只保留為相容輸入；新 sidecar、計劃、軌跡和輸出只使用規範
標識。相容輸入會反糖化為一個原生效果及其效果選項，例如 `diamond` 會變成
`shape` 加 `shape: diamond`，`wedge` 會變成 `clock` 加 `style: wedge`。

原生 PowerPoint 效果選項寫在 `transition.effect_options` 中。方向、形狀、
圖案、Morph 範圍、黑場、卷頁數量和彈跳等引數都會按所選效果嚴格校驗。執行
`python3 skills/ppt-master/scripts/pptx_animations.py --describe-transition <effect>`
可檢視精確取值。`-t none` 只關閉視覺效果，不會移除顯式設定的自動翻頁計時。

## 選擇 Start 模式

| Start 模式 | 行為 | 適用場景 |
|---|---|---|
| `on-click` | 每次單擊顯示一個內容組 | 由演講者控制節奏的現場演示 |
| `with-previous` | 頁面出現時所有內容組同時入場 | 一次協調完成的整體入場 |
| `after-previous`（預設） | 各內容組無需點選，按順序自動出現 | 展廳迴圈、錄屏走查和旁白 deck |

`--recorded-narration` 不支援 `on-click`；帶旁白或用於影片匯出的 deck 應使用 `after-previous` 或 `with-previous`。

## 選擇動畫效果

| 選擇 | 適用場景 |
|---|---|
| `auto` | 讓 PPT Master 根據內容組角色選擇合適效果；這是開啟元素動畫時的推薦選項 |
| 原生 `entrance_*` | 使用 PowerPoint 的 53 個原生進入預設之一 |
| 原生 `emphasis_*` | 讓已顯示物件獲得關注或改變外觀 |
| 原生 `path_*` | 讓物件沿 PowerPoint 的 64 條動作路徑之一移動 |
| 原生 `exit_*` | 讓物件在動畫序列中退出頁面 |
| `mixed` | 使用相容模式名，在規範 PowerPoint 預設中確定性輪換 |
| `random` | 從同一規範預設池中穩定地生成變化 |
| `none` | 關閉元素動畫 |

規範登入檔包含 203 個 PowerPoint 原生標識：53 個進入、33 個強調、64 條
動作路徑、53 個退出。現在新選擇、sidecar、自動決策、轉換軌跡和示例都只使用
帶類別字首的規範名稱。29 箇舊短名稱只保留為相容輸入，寫入前會歸一化，不再
維護第二套動畫行為。舊 Fly 方向名統一對映到 `entrance_fly`，舊 Wipe 方向名
統一對映到 `entrance_wipe`；方向會保留為引數，而不會形成新的規範預設。舊
`wheel` 保留四輻語義。執行
`python3 skills/ppt-master/scripts/pptx_animations.py --list` 可檢視完整分類清單。
4 個媒體播放命令需要媒體或書籤目標，仍由音影片工作流負責。

## 自定義具體物件

只有當整份 deck 的統一設定不夠用時才需要 `animations.json`，例如標題先出現、圖表第二個出現、結論最後出現。最簡單的方式是從真實頁面分組生成完整 scaffold，修改後校驗並匯出：

```bash
python3 skills/ppt-master/scripts/animation_config.py scaffold <project>
python3 skills/ppt-master/scripts/animation_config.py validate <project>
python3 skills/ppt-master/scripts/svg_to_pptx.py <project>
```

生成的 sidecar 以穩定的頂層 `<g id="...">` 內容組為目標。常用物件級欄位如下：

| 欄位 | 用途 |
|---|---|
| `effect` | 覆蓋物件動畫效果；設為 `none` 可讓該物件保持靜態 |
| `order` | 調整揭示順序，不改變頁面圖層順序 |
| `delay` | 在 `after-previous` 中或單擊 `trigger_shape` 後增加等待時間 |
| `duration` | 覆蓋該物件的動畫排程時長 |
| `effect_options` | 設定效果適用的 `direction`、`amount`、`color`、`font_name`、`relative` 或 `size` |
| `trigger_shape` | 單擊另一個頂層內容組時觸發本行（PowerPoint“單擊下列物件時”） |
| 計時修飾 | `repeat_count`/`repeat_duration`、`auto_reverse`、`rewind`、`accelerate`、`decelerate`、`bounce_end` 與 `restart` |
| 播放完成 | `after_effect`（變暗/隱藏）和 `.m4a`/`.mp3`/`.wav` `sound` 路徑 |

執行 `python3 skills/ppt-master/scripts/pptx_animations.py --describe
<canonical_effect>` 可查看该效果实际接受的完整参数。速度由 `duration` 控制，
平滑開始/結束由 `accelerate`/`decelerate` 控制。

`trigger_shape` 只能寫在物件組上，並指向同一頁另一個分組 id。它只讓當前動畫行
變為互動觸發，其他行仍遵循頁面 Start 模式；錄製旁白不接受這種互動動畫。

當使用者要求 AI 調整具體物件時，使用 [`customize-animations`](../../skills/ppt-master/workflows/stages/customize-animations.md) 階段。完整 sidecar schema 與目標校驗規則仍由[動畫執行規範](../../skills/ppt-master/references/animations.md)維護。

## 校驗與相容性

PPT Master 會嚴格校驗動畫設定：未知效果或 Start 模式、非法計時、缺失頁面/分組引用，以及嘗試給結構物件加動畫都會直接失敗，不會靜默改成另一種行為。匯出還會在替換現有產物前回讀候選 PPTX。

| 邊界 | 對使用者的影響 |
|---|---|
| 動畫目標 | 元素動畫作用於邏輯內容組，而不是每一個 SVG 原子 |
| 靜態結構 | 背景、Master/Layout 內容、placeholder 與頁面框架保持靜態 |
| 輸出路線 | 動畫存在於從 `svg_output/` 生成的原生 PPTX；`svg_final/` 只是靜態預覽 |
| 現有 PPTX 路線 | Template Fill 與 Native Enhance 保留源物件動畫，不把它翻譯成生成路線的動畫模型 |
| 播放相容性 | Microsoft PowerPoint 桌面版是主要驗證目標；Keynote、WPS、LibreOffice 與較舊 Office 可能重新對映或忽略個別效果 |

完整 CLI 說明見 [`svg-pipeline.md`](../../skills/ppt-master/scripts/docs/svg-pipeline.md)。精確效果定義、sidecar 要求、錨點回退邏輯與 OOXML 回讀規則見[動畫執行規範](../../skills/ppt-master/references/animations.md)。
