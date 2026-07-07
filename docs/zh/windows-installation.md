# Windows 安裝指南

本指南將手把手教你在 Windows 上安裝 PPT Master。按順序操作，10 分鐘內即可跑通第一份 PPT。

---

## Step 1 — 安裝 Python（必須）

Python 是唯一的硬性要求。

1. 前往 **[python.org/downloads](https://www.python.org/downloads/)**，下載最新的 **Python 3.10+** 安裝包。

2. **⚠️ 關鍵步驟：安裝時務必勾選 "Add python.exe to PATH"** — 這是 Windows 上最常見的安裝失誤，不勾的話後面每一步都會出問題。

   ![Python 安裝器 — 勾選 Add to PATH](../assets/windows-python-path.png)

3. 安裝完成後，開啟 **PowerShell**（在開始選單搜尋「PowerShell」）並驗證：

   ```powershell
   python --version
   ```

   應該看到 `Python 3.12.x` 之類的輸出。如果提示「未找到」或彈出 Microsoft Store，見下方[常見問題](#python-未找到或彈出-microsoft-store)。

> **💡 提示**：Anaconda / Miniconda 安裝的 Python 也可以用，只要 `python --version` 顯示 3.10+ 即可。

---

## Step 2 — 下載專案

**方式 A — 下載 ZIP**（最簡單）：

1. 開啟 [GitHub](https://github.com/hugohe3/ppt-master)（或 [AtomGit 映象](https://atomgit.com/hugohe3/ppt-master)，國內更快）
2. 點選綠色 **Code** 按鈕 → **Download ZIP**
3. 解壓到 `C:\Users\你的用户名\ppt-master`

**方式 B — Git Clone**（需要 [Git](https://git-scm.com/downloads)）：

```powershell
# GitHub
git clone https://github.com/hugohe3/ppt-master.git
# AtomGit（国内更快）
git clone https://atomgit.com/hugohe3/ppt-master.git
cd ppt-master
```

---

## Step 3 — 安裝依賴

```powershell
cd C:\Users\你的用户名\ppt-master   # ← 替换为你的实际路径
pip install -r requirements.txt
```

> 如果 `pip` 無法識別，用 `python -m pip install -r requirements.txt`。

等待安裝完成，最後看到 `Successfully installed ...` 就行。

---

## Step 4 — 驗證安裝

```powershell
python -c "import pptx; import fitz; print('All core dependencies OK')"
```

✅ 輸出 `All core dependencies OK` → 核心環境沒問題。

❌ 報錯 → 見下方[常見問題](#常見問題)。

---

## Step 5 — 跑一個最小示例

開啟你的 AI 編輯器（Cursor、VS Code + Copilot 等），開啟 `ppt-master` 目錄，在聊天面板輸入：

```
请创建一个 3 页测试 PPT，封面 + 内容页 + 封底，主题"Hello World"
```

`exports/` 下出現 `.pptx` 且能在 PowerPoint 中開啟 → **搞定了。**

---

## Step 6 — 可選增強（大多數使用者可以跳過）

裝好 Python 和 `requirements.txt` 後，生成 PPT 的全部功能已經就緒。下面是**邊緣場景的備用方案和增強項**——只有遇到對應的具體場景才需要裝。

| 增強項 | 只在以下情況才裝 | 安裝方式 | 驗證 |
|--------|-----------------|---------|------|
| **CairoSVG** — 更高質量 PNG 後備圖 | 你希望在不原生支援 SVG 的 Office 版本下獲得更清晰的 PNG 後備圖。`svglib`（已預設安裝）足夠大多數場景。 | 安裝 [GTK3 Runtime](https://github.com/nickvdp/gtk3/releases) 後 `pip install cairosvg` | `python -c "import cairosvg"` |
| **Pandoc** — 舊格式檔案 | 你需要轉 `.doc`、`.odt`、`.rtf`、`.tex`、`.rst`、`.org`、`.typ`。`.docx`/`.html`/`.epub`/`.ipynb` 已由 Python 原生處理。 | [pandoc.org](https://pandoc.org/installing.html) 下載 `.msi` 安裝 | `pandoc --version` |

---

## 常見問題

### `python` 未找到或彈出 Microsoft Store

**原因：** Python 沒有加入系統 PATH。

**方法 1** — 重新執行 Python 安裝程式，選擇 **Modify**，確保勾選 **"Add Python to environment variables"**。

**方法 2** — 手動新增 PATH：
1. 先在 PowerShell 中執行 `where python`，記下輸出的路徑（如 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\python.exe`）
2. 開始選單搜尋「環境變數」
3. 找到 `Path` → **編輯** → 新增上面路徑的**目錄部分**及其 `Scripts` 子目錄：
   ```
   C:\Users\你的使用者名稱\AppData\Local\Programs\Python\Python312
   C:\Users\你的使用者名稱\AppData\Local\Programs\Python\Python312\Scripts
   ```
4. 確定，**重啟 PowerShell**

**方法 3** — 試試 `python3` 或 `py` 命令。

### 命令裡的 `python3` 報錯（exit 49 / 彈 Microsoft Store）

python.org 安裝包只裝了 `python.exe`，沒有 `python3.exe`。**把命令裡的 `python3` 換成 `python` 即可**（AI 通常也會自動改用 `python` 繼續）。

### `pip install` 報許可權錯誤

```powershell
pip install --user -r requirements.txt
```

或以管理員身份執行 PowerShell。

### `pip install` 網路問題

```powershell
# 清华镜像（国内推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 代理
pip install -r requirements.txt --proxy http://your-proxy:port
```

### `ModuleNotFoundError`

`pip` 裝到了另一個 Python 環境。用 `python -m pip install -r requirements.txt` 確保對應同一個。

### `import fitz` 失敗

1. 升級 pip：`python -m pip install --upgrade pip`
2. 預編譯包：`pip install PyMuPDF --only-binary :all:`
3. 仍失敗 → 安裝 [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### PowerShell「指令碼執行被停用」

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 還是搞不定？

- 📖 [常見問題 (FAQ)](./faq.md)
- 🐛 [GitHub Issues](https://github.com/hugohe3/ppt-master/issues) — 附上 Python 版本、Windows 版本和完整報錯
- 💬 [GitHub Discussions](https://github.com/hugohe3/ppt-master/discussions)
