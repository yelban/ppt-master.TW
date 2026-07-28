---
deck_id: 中汽研
kind: deck
category: brand
summary: 中汽研認證展示、評測彙報與技術交流，用於建立可信理解並推進評審或合作；採用專業的深藍工程視覺。
keywords: [中汽研, 認證, 評測, 技術交流]
primary_color: "#004098"
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: fidelity
native_structure_mode: structured
page_count: 5
---

# 中汽研 — Design Specification

## I. Template Overview

| Application context | Definition |
| --- | --- |
| Recurring presentation family | 產品認證展示、評測彙報、技術推廣和業務來訪 |
| Intended audiences and outcomes | 面向客戶、技術評審者、合作伙伴與來訪團隊；幫助受眾理解認證或評測能力、信任證據，並推進評審、交流或合作下一步 |
| Delivery and reading assumptions | 以現場講解和技術交流為主，同時允許會後獨立閱讀；頁面需保留關鍵結論、證據標籤與必要上下文 |
| Representative narrative/page roles | 當前原型覆蓋封面、目錄、章節、開放內容和結束語；具體選頁、重複、順序與內容處理由當前專案的 Strategist 根據材料決定 |

- 視覺以中汽研深藍、白底內容頁、方形章節編號和簡潔網格為識別核心，強調專業、可信和工程秩序。
- 結構上分為兩個可複用 Master 家族：CATARC Dark 服務封面、章節與收尾，CATARC Light 服務目錄與正文；它們按深淺視覺體系分工，不是按單個 Layout 拆分出的重複 Master。

## II. Color Scheme

| Role | Color | Application |
| --- | --- | --- |
| CATARC blue | #004098 | 深色頁面背景、章節編號塊、結構線 |
| Deep blue | #003B82 | 封面背景 |
| Panel gray | #F8FAFC | 內容承載區 |
| Border gray | #E0E0E0 | 分隔線和麵板邊界 |
| Primary text | #333333 | 內容頁標題和正文 |
| White | #FFFFFF | 深色頁面文字與 Master 背景 |

## III. Typography

| Role | Font stack | Application |
| --- | --- | --- |
| Chinese title and body | `"Microsoft JhengHei", "PingFang TC", Arial, sans-serif` | 標題、正文、目錄項與聯絡資訊 |
| Latin label and folio | `Arial, "Microsoft JhengHei", sans-serif` | 英文機構名、編號、頁碼與短標籤 |

字型棧僅使用常見系統字型；Windows 優先Microsoft JhengHei，macOS 可回退蘋方，不依賴額外字型安裝。

## IV. Signature Design Elements

- 白底內容頁使用“藍色方形章節號 + 左對齊標題 + 右上角 Logo”的穩定頁首。
- 封面、章節頁和結束頁保留深藍底、低透明度圓形與細網格，但刪除無內容價值的複雜漸變和動態圖片依賴。
- CATARC Dark Master 統一承載深藍背景和上下結構線；章節頁與結束頁各自保留原稿中的圓形幾何，封面不繼承圓形。CATARC Light Master 統一承載白底、章節號方塊、頁首 Logo、分隔線和底部藍線。
- 目錄頁延續數字與雙豎線的行式導航，並保留右側獨立 `object` slot。
- 通用內容 carrier 從 slot bounds 左上角開始；封面、章節頁、結束頁以及小型章節號屬於短焦點內容，允許在完整 bounds 內居中。

## V. Page Roster

| File | Master | Layout key | PowerPoint picker name | Visual character | Reusable slots |
| --- | --- | --- | --- | --- | --- |
| `01_cover.svg` | CATARC Dark | cover | Cover | 深藍背景、居中大型 Logo 與標題簇 | 標題、副標題、單位、英文單位 |
| `02_toc.svg` | CATARC Light | agenda | Agenda | 數字雙豎線目錄、右側資料面板 | 頁面標題、五個目錄項、資料物件、頁碼 |
| `03_chapter.svg` | CATARC Dark | section | Section Header | 深藍章節頁、居中章節號和標題 | 章節號、章節標題、章節副標題 |
| `04_content.svg` | CATARC Light | content | Title and Content | 方形章節號頁首與開放內容面板 | 章節號、頁面標題、內容物件、頁碼 |
| `05_ending.svg` | CATARC Dark | closing | Closing | 深藍網格背景、居中 Logo 與結束語 | 結束標題、英文副標題、聯絡資訊、頁尾 |

## VI. Assets

| File | Intended usage |
| --- | --- |
| 大型 logo.png | 封面和結束頁主標識 |
| 右上角 logo.png | 目錄頁和內容頁頁首標識 |
