# 上游同步 Runbook（給 AI agent 照著執行）

本檔是上游 [`hugohe3/ppt-master`](https://github.com/hugohe3/ppt-master) 有新版本時的**逐步執行手冊**，寫給 Claude Code 等 AI agent 直接照做。設計原則：每一步都有可驗證的完成判準，衝突有機械分流規則，該停下問人的時機明確列出。

fork 差異的完整清單（哪些檔案是本 fork 的功能）見 [`tw-fork-guide.md`](tw-fork-guide.md)；繁化管線內部機制見 [`tools/README.md`](../../tools/README.md)。本檔只管「怎麼安全地同步」。

## 第 0 步：前置檢查

```bash
git status --short          # 必須乾淨（untracked 的本機檔如 .mcp.json 可忽略）
git branch --show-current   # 必須在 main
git remote -v               # 需有 upstream；沒有就加：
# git remote add upstream https://github.com/hugohe3/ppt-master.git
```

工作區不乾淨就先停下，請使用者決定先 commit 還是 stash。接著開同步分支，**不直接在 main 上解衝突**：

```bash
git fetch upstream
git log --oneline main..upstream/main   # 先看上游改了什麼、多大量
git checkout -b sync/upstream-$(date +%Y%m%d)
```

若 `main..upstream/main` 顯示上游有**大規模檔案搬移或架構重構**（如 `scripts/` 目錄結構改變、`image_gen.py` 分派機制重寫），停下向使用者回報範圍，不要自行硬解。

## 第 1 步：合併

```bash
git merge upstream/main
```

沒有衝突就直接跳到第 3 步。有衝突時進第 2 步。

## 第 2 步：衝突分流（核心規則）

先列出衝突檔案：

```bash
git diff --name-only --diff-filter=U
```

分流前先把「fork 到底改過哪些檔」問出確定答案——別靠猜，也別只靠內容比對（繁化管線會套覆蓋表與保護規則，單純用 OpenCC 轉換去比會誤判）：

```bash
git log --oneline $(git merge-base HEAD upstream/main)..main            # fork 自有 commit
git log --format="COMMIT %h %s" --name-only $(git merge-base HEAD upstream/main)..main
```

其中「全 repo 繁化」那個 commit 動到的檔案屬繁化差異；**其餘 commit 動到的檔案才是 fork 功能檔**。兩份清單交叉比對衝突檔，即可把絕大多數衝突歸進分類 A。

每個衝突檔按下表分流，**判斷依據是上述 commit 清單，並與 [`tw-fork-guide.md`](tw-fork-guide.md)「這個 fork 加了什麼」表格對照**：

| 分類 | 判斷 | 解法 |
|------|------|------|
| **A. 純繁化差異檔** | 不在 fork 功能清單中；衝突內容只是「上游簡體新版 vs 本地繁體舊版」 | 一律取上游版：`git checkout --theirs <檔> && git add <檔>`。繁化交給第 3 步的管線重跑，不要手工繁化、不要心疼本地版本 |
| **B. fork 功能檔** | 在 fork 功能清單中（如 `tools/`、`html_deck.py`、`backend_codex.py`、CLI 接線處） | 人工合併：保留 fork 功能，套上游的其他改動。改完 `git add`。上游若把該檔重寫得面目全非，較省力的做法是先取上游版（`--theirs`），再用 `git show <fork commit> -- <檔>` 逐一把 fork 的新增套回新結構 |
| **C. 受保護的簡體來源** | `README_CN.md`、UI 的 `MESSAGES.zh` 區塊 | 一律取上游版（`--theirs`）。繁體產物（`README_TW.md`、`MESSAGES.zhtw`）由管線衍生，若它們也衝突同樣取任一版即可，反正會被管線覆寫 |

分類 B 中，若上游改動與 fork 功能**在同一段程式碼交錯、無法直觀合併**（例如上游重寫了 `BACKEND_REGISTRY` 結構、或重構了 `cli.py` 引數解析），停下向使用者回報衝突內容，不要猜。

全部解完後：

```bash
git merge --continue
```

## 第 3 步：重跑繁化管線

```bash
python3 tools/tw_localize.py
python3 tools/tw_localize.py --check
```

`--check` 必須輸出 `PASS: 殘留 0 檔` 才算通過。若有殘留：

- 殘留是**上游新增的簡中詞彙**且 OpenCC 沒轉到 → 把修正加進 `tools/tw_localize_overrides.json` 後重跑（這是正規做法，不要直接改目標檔）
- 殘留原因不明 → 停下回報殘留清單

## 第 4 步：fork 功能回歸驗證

逐條執行，輸出須符合判準；任何一條失敗就修復（或停下回報），不得跳過：

| # | 指令 | 通過判準 |
|---|------|----------|
| 1 | `python3 skills/ppt-master/scripts/image_gen.py --list-backends` | 輸出含 `codex` 條目（EXPERIMENTAL 區） |
| 2 | `.venv/bin/python3 skills/ppt-master/scripts/svg_to_pptx.py --help` | 輸出含 `--html-deck` 與 `--embed-fonts`（此條需 venv，`python-pptx` 不在系統 Python） |
| 3 | `grep -c "zhtw" skills/ppt-master/scripts/confirm_ui/static/app.js` | 大於 0（雙中文字典仍在） |
| 3b | `grep -c 'v !== "zhtw"\|stored === "zhtw"\|nav.indexOf("zh-tw")\|zhtw: "正體中文"' skills/ppt-master/scripts/confirm_ui/static/app.js` | 等於 4（語系**切換接線**仍在——字典存在不代表選單能切，2026-07-28 那次僅檢查第 3 條而漏掉這個） |
| 3c | `node --check skills/ppt-master/scripts/confirm_ui/static/app.js && node --check skills/ppt-master/scripts/svg_editor/static/app.js` | 兩者皆無輸出、exit 0 |
| 4 | `grep -n "FONT_FACE_BLOCK" tools/tw_localize.py` | 有命中（webfont 注入機制仍在） |
| 5 | `python3 -m py_compile skills/ppt-master/scripts/image_gen.py skills/ppt-master/scripts/image_backends/backend_codex.py skills/ppt-master/scripts/svg_to_pptx.py` | 無輸出、exit 0 |

> 這張表與 `tw-fork-guide.md` 的 fork 功能清單對應。**日後 fork 新增功能時，兩處要一起加**：清單加一列、這裡加一條可機械驗證的回歸檢查。

另需人工目視（agent 做完回報給使用者）：

- 上游若動了 `MESSAGES.zh`（UI 新增字串）→ 檢查衍生的 `zhtw` 有無需要臺灣在地化修正的用語，有就加進覆蓋表重跑
- 上游若動了字型或 CDN 相關 → 確認 `FONT_FACE_BLOCK` 的 woff2 檔名對得上 jsDelivr 實際檔案（`-R.woff2` vs `-Regular.woff2` 曾出錯）

## 第 5 步：收尾

```bash
git status --short && git diff --stat main   # 檢視總量
git add -A && git commit -m "chore(sync): merge upstream <上游版本或短 hash>＋重跑繁化管線"
```

commit 後回報使用者：上游帶進哪些主要變更、衝突分流各分類幾個檔、驗證五條的實際輸出。**由使用者確認後才合回 main 與 push**，agent 不自行 push：

```bash
git checkout main && git merge sync/upstream-<日期> && git branch -d sync/upstream-<日期>
```

## 何時必須停下問人（彙總）

- 前置檢查：工作區不乾淨
- 第 0 步：上游有大規模結構重構
- 第 2 步：fork 功能檔與上游改動交錯、無法直觀合併
- 第 3 步：`--check` 殘留原因不明
- 第 4 步：回歸驗證修不好
- 第 5 步：合回 main 與 push 一律等使用者確認
