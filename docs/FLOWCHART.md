# 讀書筆記本 - 流程圖文件 (Flowchart)

這份文件基於 [產品需求文件 (PRD)](PRD.md) 與 [系統架構設計 (Architecture)](ARCHITECTURE.md) 所產出，主要透過視覺化的圖表來展示「讀書筆記本」系統中的使用者操作路徑，以及在系統背後資料是如何流動的。

## 1. 使用者流程圖 (User Flow)

此流程圖涵蓋了從訪客進入網站開始，一直到他們登入、撰寫心得，甚至是管理員進行後台操作的主要路徑。

```mermaid
flowchart LR
    A([訪客進入網站]) --> B[首頁 - 心得列表與搜尋]
    
    B --> C{是否已登入？}
    
    C -->|否| D[閱讀他人心得 / 搜尋特定書籍]
    D --> F[進入登入 / 註冊頁面]
    F -->|登入成功| E[個人操作畫面]
    
    C -->|是| E
    
    E --> G{要執行什麼操作？}
    G -->|撰寫| H[填寫「新增讀書心得」表單]
    G -->|管理| I[編輯或刪除自己過去發布的筆記]
    G -->|登出| K[清除登入狀態回首頁]
    
    E -. 如果具備管理員身分 .-> J[進入後台管理：刪除違規內容]
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖具體描述了使用者在「新增一篇讀書心得」時，系統背後的資料處理過程。角色涵蓋了使用者端到後端模型及資料庫。

```mermaid
sequenceDiagram
    actor User as 使用者 (已登入)
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>(/review/create)
    participant Model as Review Model<br>(Python 物件)
    participant DB as SQLite<br>(database.db)

    User->>Browser: 填寫書名、心得、評分並送出表單
    Browser->>Route: POST /review/create (帶表單資料 payload)
    
    rect rgb(240, 240, 240)
        Note over Route: 系統後端處理與防護
        Route->>Route: 確認 Session (是否已登入)
        Route->>Route: 驗證表單欄位是否為空、評分是否合法
    end
    
    Route->>Model: 初始化 Review 模型物件並綁定使用者 ID
    Model->>DB: 執行 INSERT INTO ... 寫入資料庫
    DB-->>Model: 寫入成功確認
    Model-->>Route: 回傳處理完成訊號
    
    Route-->>Browser: HTTP 302 Redirect (重導向至心得明細頁或首頁)
    Browser->>User: 渲染最新頁面，顯示新增成功
```

## 3. 功能清單對照表 (Routing Table)

這是一張對應功能、網址與 HTTP 方法的對照表，有助於後續串接路由與實作。

| 功能項目 | URL 路徑 | HTTP 方法 | 說明與職責 |
| --- | --- | --- | --- |
| **首頁 / 心得列表** | `/` | GET | 從資料庫撈取最新的讀書心得，並提供介面搜尋框。 |
| **搜尋書籍** | `/search` | GET | 接收 URL query (如 `?q=書名`)，進行關鍵字查詢過濾並渲染結果。 |
| **檢視單篇心得** | `/review/<id>` | GET | 根據心得的 ID 顯示特定書籍詳細筆記與評分。 |
| **註冊帳號** | `/auth/register` | GET, POST | `GET`: 顯示註冊表單。<br>`POST`: 接收資料，建立新用戶並存入 DB。 |
| **登入帳號** | `/auth/login` | GET, POST | `GET`: 顯示登入表單。<br>`POST`: 驗證密碼，若正確則寫入 Session。 |
| **登出帳號** | `/auth/logout` | POST / GET | 清除當前 Session 並重導向回首頁。 |
| **新增讀書心得** | `/review/create` | GET, POST | `GET`: 顯示填寫表單。<br>`POST`: 接收書名、心得、評分並寫入 DB。需登入。 |
| **編輯心得** | `/review/<id>/edit` | GET, POST | `GET`: 帶入舊有資料到表單中。<br>`POST`: 更新資料庫。需確認為原作者。 |
| **刪除心得** | `/review/<id>/delete`| POST | 執行刪除動作。需確認為原作者或管理員。 |
| **管理員後台** | `/admin/reviews` | GET | 列出全部使用者的心得，供管理員檢視。需管理員權限。 |
