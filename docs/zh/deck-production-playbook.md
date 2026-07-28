# 實戰產出手冊（給 AI agent 照著執行）

本檔記錄用 Generate PPTX 路由實際做完一份簡報後，值得在下一份重複使用的操作規則。寫法是**規範式**的：直接寫「該怎麼做」，不描述專案現況。路由順序、閘門與指令的權威仍在 [`skills/ppt-master/SKILL.md`](../../skills/ppt-master/SKILL.md) 與 [`generate-pptx.md`](../../skills/ppt-master/workflows/generate-pptx.md)，本檔不重複，只補這些檔案不會告訴你、但每次都會踩到的東西。

fork 專屬功能清單見 [`tw-fork-guide.md`](tw-fork-guide.md)；上游同步見 [`upstream-sync-runbook.md`](upstream-sync-runbook.md)。

---

## 1. 執行環境

| 事項 | 做法 |
|---|---|
| Python 依賴 | 系統 `python3`（homebrew）沒有 mammoth／PyMuPDF／flask，用 repo 內建 venv：每個指令前加 `export PATH="$PWD/.venv/bin:$PATH"` |
| 工作目錄 | **一律從 repo 根目錄執行**，見 §5 的假故障 |
| 綁埠的服務 | `confirm_ui/server.py` 與 `svg_editor/server.py` 綁 `127.0.0.1:5050`，沙箱會擋（`Operation not permitted`）。這兩支要停用沙箱執行 |
| 目視驗收 | 用 `rsvg-convert`（已安裝）。`cairosvg` 在本機缺 libcairo，不要用 |

---

## 2. 中文字寬：先算，不要先寫

品質檢查器會用 SVG→PPTX 的共用估算，比對每段文字與其所屬 `data-pptx-bounds`。**中文字的估算寬度約為 `font-size × 1.09`**，不是 `font-size × 1.0`。差這 9% 會讓長行整批爆掉。

先用這張表反推每行最多幾個中文字，再寫文案：

```
每行最大字數 ≈ 容器寬度 ÷ (font-size × 1.09)
```

| 字級 | 全幅 1184px | 半欄 576px | 三分之一欄 376px |
|---:|---:|---:|---:|
| 32 | 33 | 16 | 10 |
| 24 | 45 | 22 | 14 |
| 20 | 54 | 26 | 17 |
| 18 | 60 | 29 | 19 |
| 16 | 67 | 33 | 21 |

夾雜英數會再吃寬度（拉丁字母與數字約 `font-size × 0.55`，但空格與標點會讓實際值浮動），估算時對含英數的行再留 10% 餘裕。

**先算再寫的理由**：不先算就寫，18 頁裡會有一半在最終閘門才報錯，而且修法只有「重寫文案」或「改版面」兩種，兩種都比事前算貴。

---

## 3. 版面的三條硬規則

這三條在第一頁閘門就會被抓到，屬於方法級——第一頁怎麼寫，後面 17 頁就會照抄：

1. **一段散文只能有一個 `<text>`**。換行用直接子 `<tspan>`，重複 parent 的 `x`，配正的 `dy`。用兄弟 `<text>` 排視覺行會被判定為段落被拆散。語意上獨立的列點則本來就該各自一個 `<text>`，那個提醒可以忽略。
2. **根層的靜態框架要標角色**。直接掛在根 `<svg>` 底下的背景圖、全幅色塊、規則線，要有穩定 `id` 加 `data-pptx-role="background"` 或 `"decoration"`，否則會報「ungrouped top-level element」。不要為了消警告而多包一層 `<g>`。
3. **模組的 `data-pptx-bounds` 不得互相重疊**。多欄版面調整欄寬時，欄位的 bounds 與分隔線位置要一起改；只改文字 `x` 而忘了改 bounds，檢查器會在另一欄報溢位。

---

## 4. 閘門過關不等於版面對

`svg_quality_checker.py` 驗的是語法、資源可解析、文字對 bounds。它**不驗**下列每一項，而這些正是簡報看起來不專業的主因：

- 背景圖的圖形壓到文字
- 圖片超出畫布被切掉（`x + width > 1280`）
- 引線／標註沒有指到圖中真正的主體
- 疊在圖上的文字落在圖的忙碌區而非留白區

所以**每一頁含圖的頁面，匯出前一定要逐頁看**：

```bash
rsvg-convert -w 1280 -h 720 "svg_final/<頁名>.svg" -o /tmp/check.png
```

然後真的開啟 PNG 檢視。這一步不能用「checker 過了」代替。

---

## 5. 一個會浪費半小時的假故障

檢查器解析 SVG 內 `href="../images/xxx.png"` 時是**相對於當前工作目錄**，不是相對於 SVG 檔案位置。如果 shell 之前 `cd` 進了 `svg_output/`，所有圖片都會報：

```
invalid image source: external image '../images/x.png' is empty, corrupt, or does not match its .png extension
```

檔案其實完全正常。回到 repo 根目錄重跑即可。看到這個錯誤時，先確認 `pwd`，不要去檢查圖檔。

---

## 6. 產圖：後端與提示詞

### 6.1 後端選擇

| 後端 | 適用 | 限制 |
|---|---|---|
| `openai` + `gpt-image-2` | **需要構圖精確控制時的預設選擇** | 需 `OPENAI_API_KEY`；尺寸須為 16 的倍數、長短邊比 ≤ 3:1 |
| `codex` | 只需要氛圍圖、不在意構圖落點時 | **不服從構圖分區指令**；長寬比只支援 `1:1` / `16:9` / `9:16` / `4:3` / `2.35:1`；`--image_size` 被忽略、由 Codex 自行決定像素 |

規劃 §VIII 的 `aspect_ratio` 前，先確認要用的後端支援該比例。用 `codex` 時寫了 `2:3` 會直接失敗。

### 6.2 切換到 gpt-image-2 的指令

```bash
OPENAI_QUALITY=high IMAGE_BACKEND=openai \
python3 skills/ppt-master/scripts/image_gen.py \
  --manifest projects/<專案>/images/image_prompts.json \
  --output   projects/<專案>/images \
  --backend openai --model gpt-image-2 --concurrency 3
```

走 manifest 而不是單張正列式呼叫：狀態會寫回 manifest，提示詞留下稽核紀錄，重跑時只會處理狀態為 `Pending` / `Failed` 的條目。

`image_size` 對應的實際解析度（`aspect_ratio` × `image_size` 決定）：

| | 1:1 | 16:9 | 9:16 |
|---|---|---|---|
| 2K | 2048×2048 | 2048×1152 | 1152×2048 |
| 4K | 2880×2880 | 3840×2160 | 2160×3840 |

`OPENAI_QUALITY` 不設時由 `image_size` 推導；要保證高品質就顯式設 `high`。

### 6.3 提示詞要寫成硬性分區，不是描述性建議

模型會照做的是**帶百分比的分區與明確禁區**，不是「主體在左側、右邊留白」這種描述。有效的寫法：

> COMPOSITION IS A HARD CONSTRAINT: every drawn mark must sit inside the lower-right quadrant only, that is the right 45 percent of the width and the bottom 45 percent of the height. The left 55 percent and the top 55 percent must be completely empty pure white with absolutely no marks, no faint lines, no specks.

同時要寫死的還有：

- **邊界留白**：「必須完整落在畫面內，距右緣至少 8% 留白，任何線條不得觸碰或穿出畫布邊界」——否則圖形會貼邊被切。
- **禁止元素**：不想要外框就寫「draw absolutely no frames, no borders, no panel rectangles, no outer box」。上一版沒寫，模型自作主張加了三個外框，擺上版面後右邊被畫布切掉。
- **色彩配額**：「exactly one small crimson red square, no larger than 1.5 percent of the canvas area」——用面積百分比而不是「少量」。

`page_role` 也要選對：只有 `hero_page`（SVG 疊在圖上）才可以在提示詞裡寫「留某區給 SVG 疊字」；`local`（圖是版面中的一塊區域）寫這種話沒有意義。

---

## 7. 來源轉檔的已知損失

DOCX 轉 Markdown 時，**表格的儲存格網底不會保留**。甘特圖之類「用底色表示區間」的表格轉出來會是一張空表。

處理方式：只畫文字內容明載日期的區間，其餘改用並列標籤呈現，並在 `design_spec.md §IX` 的 `Visualization` 寫明為什麼不畫。**不要從章節順序推估起訖月份**——那是憑空生成事實。

---

## 8. 講稿

`notes/total.md` 的正文會被語音轉檔逐字朗讀。正文裡**不能有**時長標記、階段標籤、條列符號或任何中繼資料。

配速預算寫在 `design_spec.md §X`，不要寫進 `notes/`。數字與符號在講稿裡要寫成口語形式（「百分之十」而不是「10%」、「二點二公斤」而不是「2.2 kg」）。

---

## 9. 建議的執行順序

在既有 Step 1–7 之上，插入兩個本檔新增的檢查點：

1. Step 4 寫 §IX 前 → 先用 §2 的表反推每個容器的行長上限，文案照上限寫
2. Step 6 每頁畫完 → 照 §3 的三條規則自檢
3. 最終閘門通過後、`finalize_svg.py` 之前 → **照 §4 逐頁 render 成 PNG 目視**
4. 目視發現問題 → 修 SVG → 重跑最終閘門 → 再 finalize → 再匯出
