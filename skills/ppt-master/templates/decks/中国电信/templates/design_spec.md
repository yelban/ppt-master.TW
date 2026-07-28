---
deck_id: 中國電信
kind: deck
category: brand
summary: 中國電信政企數字化方案、轉型規劃與內部評審，用於說明方案並對齊決策和下一步；採用剋制的紅灰品牌視覺。
keywords: [中國電信, 政企, 數字化, 企業彙報]
primary_color: "#C00000"
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

# 中國電信 — Design Specification

## I. Template Overview

| Application context | Definition |
| --- | --- |
| Recurring presentation family | 政企數字化方案、轉型規劃、內部評審和客戶彙報 |
| Intended audiences and outcomes | 面向政企客戶決策者、專案幹係人與內部評審者；幫助受眾理解背景與方案、形成判斷，並明確下一步 |
| Delivery and reading assumptions | 以會議講解為主，同時需要會後流轉和複核；頁面應保留關鍵結論與必要證據，不依賴口頭說明才能辨認主題 |
| Representative narrative/page roles | 當前原型覆蓋封面、目錄、章節、開放內容和結束語；具體選頁、重複、順序與內容處理由當前專案的 Strategist 根據材料決定 |

- 視覺基調為白底、通訊紅結構條、銀灰內容承載區與少量城市線稿，強調權威、清晰和剋制。
- 結構上分為兩個可複用 Master 家族：China Telecom Brand 服務封面、章節與收尾，China Telecom Content 服務目錄與正文；它們按視覺體系分工，不是按單個 Layout 拆分出的重複 Master。

## II. Color Scheme

| Role | Color | Application |
| --- | --- | --- |
| Telecom red | #C00000 | 頁首膠囊、編號、分隔線和關鍵強調 |
| Silver gray | #D9D9D9 | 頁首結構帶 |
| Panel gray | #F8FAFC | 內容承載區與品牌卡片 |
| Graphite | #111827 | 標題和關鍵文字 |
| Muted gray | #6B7280 | 輔助說明與頁尾 |
| White | #FFFFFF | Master 背景與反白文字 |

## III. Typography

| Role | Font stack | Application |
| --- | --- | --- |
| Chinese title and body | `"Microsoft JhengHei", "PingFang TC", Arial, sans-serif` | 標題、正文、目錄項與中文品牌說明 |
| Latin label and folio | `Arial, "Microsoft JhengHei", sans-serif` | 英文標識、日期與頁碼 |

字型棧僅使用常見系統字型；Windows 優先Microsoft JhengHei，macOS 可回退蘋方，不依賴額外字型安裝。

## IV. Signature Design Elements

- 內容頁和目錄頁使用“紅色膠囊 + 銀灰長帶”的頁首結構，右側保留橫向品牌圖形。
- 封面、章節頁和結束頁複用紅色口號、城市線稿與底部紅色飄帶，但控制在獨立品牌卡片中。
- China Telecom Brand Master 統一承載白底、頂部紅線、底部品牌飄帶與英文標識；China Telecom Content Master 統一承載紅灰頁首、橫向品牌標識和頁尾分隔線。
- 內容承載區採用淺灰圓角面板；實際內容由邊界完整的 `object` slot（PowerPoint 內容佔位區域）承載，不顯示提示性虛線。
- 標題與通用內容保持左對齊；只在品牌圖形內部使用居中構圖。

## V. Page Roster

| File | Master | Layout key | PowerPoint picker name | Visual character | Reusable slots |
| --- | --- | --- | --- | --- | --- |
| `01_cover.svg` | China Telecom Brand | cover | Cover | 左側標題簇、右側品牌卡片、底部飄帶 | 標題、副標題、單位、日期 |
| `02_toc.svg` | China Telecom Content | agenda | Agenda | 左側品牌說明卡、右側四行編號目錄 | 頁面標題、四個目錄項、頁碼 |
| `03_chapter.svg` | China Telecom Brand | section | Section Header | 左側章節資訊、右側品牌卡片、底部飄帶 | 章節號、章節標題、章節副標題 |
| `04_content.svg` | China Telecom Content | content | Title and Content | 紅灰頁首與大面積淺灰開放內容區 | 欄目標、頁面標題、內容物件、來源、頁碼 |
| `05_ending.svg` | China Telecom Brand | closing | Closing | 左側結束語、右側品牌卡片、底部飄帶 | 結束標題、副標題、聯絡資訊、頁碼 |

## VI. Assets

| File | Intended usage |
| --- | --- |
| logo.png | 封面、章節頁和結束頁品牌標識 |
| header_brand.png | 目錄頁和內容頁橫向頁首標識 |
| footer_ribbon.png | 封面、章節頁和結束頁底部品牌飄帶 |
| slogan_red.png | 右側品牌卡片口號 |
| skyline_bg.png | 右側品牌卡片城市線稿 |
| top_emblem.png | 保留的備用橫向品牌資產 |
