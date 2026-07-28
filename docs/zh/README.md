# 檔案索引

[English](../README.md) | [中文](./README.md)

---

使用者檔案集中在 `docs/` 目錄：英檔案案為規範源，本目錄（`docs/zh/`）是同步中文譯本。AI 自身消費的工作流與技術參考位於 [`skills/ppt-master/`](../../skills/ppt-master/SKILL.md)。

## 快速上手

| 檔案 | 說明 |
|---|---|
| [快速入門](./getting-started.md) | 三步做出第一份 deck，外加模板、即時預覽、動畫、旁白、聲音復刻的用法 |
| [Windows 安裝指南](./windows-installation.md) | Windows 使用者手把手安裝教程 |
| [常見問題](./faq.md) | 模型選擇、費用、排版問題排查、自定義模板——基於真實使用者反饋持續更新 |

## 能力專題

| 檔案 | 說明 |
|---|---|
| [音訊旁白](./audio-narration.md) | 從演講者備註到逐頁旁白：服務商、聲音復刻、時序、PPTX 嵌入 |
| [轉場與動畫](./animations.md) | 頁間轉場與頁內元素動畫的預設行為和自定義方式 |
| [模板使用指南](./templates-guide.md) | 品牌 / 版式 / 成品模板的建立與套用 |

## 架構與原理

| 檔案 | 說明 |
|---|---|
| [技術路線](./technical-design.md) | 架構、設計哲學、為什麼選 SVG → DrawingML |
| [PowerPoint–SVG 能力對映](./powerpoint-svg-mapping.md) | PowerPoint 構造與管線之間逐項能力對映 |
| [模板體系架構](./templates-architecture.md) | 品牌 / 版式 / 成品模板體系的設計 |

## 專案方向

| 檔案 | 說明 |
|---|---|
| [什麼是 PPT？](./what-is-ppt.md) | 演示媒介、使用者任務、傳遞場景、原生物件模型、模板與質量層次 |
| [為什麼選 PPT Master](./why-ppt-master.md) | 為什麼選它、以及它不適合的場景 |
| [專案定位與能力邊界](./project-positioning.md) | 長期定位、產品承諾、能力邊界與准入判據 |
| [路線圖](./roadmap.md) | 已交付能力、當前優先順序與明確推遲的方向 |

## 貢獻者規則

| 檔案 | 說明 |
|---|---|
| [風格規則](../rules/README.md)（英文） | 面向提示詞參考檔案與 Python 指令碼的貢獻者風格規則 |

## 本 fork 專屬

上游沒有的檔案，僅有繁中版。

| 檔案 | 說明 |
|---|---|
| [實戰產出手冊](./deck-production-playbook.md) | 實際做完一份簡報後沉澱的操作規則：中文字寬估算、版面硬規則、目視驗收、產圖後端與提示詞寫法 |
| [.TW Fork 擴充與維護指南](./tw-fork-guide.md) | 本 fork 相對上游的所有新增功能與差異，同時是上游同步的檢查清單 |
| [上游同步 Runbook](./upstream-sync-runbook.md) | 上游有新版本時的逐步執行手冊 |
