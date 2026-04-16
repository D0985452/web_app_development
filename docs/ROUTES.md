# 讀書筆記本 - 路由與頁面設計 (Routes)

這份文件基於 PRD、架構文件以及資料庫設計產出，涵蓋了系統中所有 URL 路徑的規劃、操作與模板對應關係。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁與搜尋** | GET | `/` | `index.html` | 顯示所有最新文章與搜尋框 |
| **首頁與搜尋** | GET | `/search` | `index.html` | 根據 query `?q=` 顯示搜尋結果 |
| **會員驗證** | GET, POST | `/auth/register` | `register.html` | 會員註冊表單與處理邏輯 |
| **會員驗證** | GET, POST | `/auth/login` | `login.html` | 會員登入表單與處理邏輯 |
| **會員驗證** | POST | `/auth/logout` | — | 登出並清除 Session，重導向至首頁 |
| **心得操作** | GET, POST | `/review/create` | `review_form.html` | 新增心得表單與儲存動作 |
| **心得操作** | GET | `/review/<int:id>` | `review_detail.html` | 顯示特定 ID 的心得詳細頁面 |
| **心得操作** | GET, POST | `/review/<int:id>/edit` | `review_form.html` | 顯示/覆寫特定心得的編輯狀態 |
| **心得操作** | POST | `/review/<int:id>/delete` | — | 刪除特定文章，限作者與管理員 |
| **後台管理** | GET | `/admin/reviews` | `admin.html` | [管理員專屬] 列出全站心得供管理審核 |

## 2. 每個路由的詳細說明

### Blueprint: `main_bp` (前台首頁)
- **`GET /`**
  - **處理邏輯**：調用 `Review.get_all()` 撈取所有最新心得。
  - **輸出**：渲染 `index.html`，傳入 `reviews` 清單。
- **`GET /search`**
  - **輸入**：URL Query `q` (e.g. `?q=哈利波特`)
  - **處理邏輯**：調用 `Review.search_by_title(q)` 查詢資料表。
  - **輸出**：渲染 `index.html`，傳入過濾後的 `reviews` 與 `query` 以便顯示搜尋結果字串。

### Blueprint: `auth_bp` (會員認證)
- **`GET /auth/register`**
  - **輸出**：渲染 `register.html`。
- **`POST /auth/register`**
  - **輸入**：表單欄位 `username`, `password`
  - **處理邏輯**：檢查帳號是否重複，若無則密碼雜湊後調用 `User.create()`，完成後自動幫用戶設定 session (登入狀態)。
  - **輸出**：重導向至 `/`，驗證失敗重導至 `/auth/register` 並顯示錯誤。(Flash message)
- **`GET /auth/login`**
  - **輸出**：渲染 `login.html`。
- **`POST /auth/login`**
  - **輸入**：表單欄位 `username`, `password`
  - **處理邏輯**：`User.get_by_username()` 校對密碼，成功則將 `user_id` 與 `is_admin` 寫入 Session。
  - **輸出**：重導向至 `/`。密碼錯誤顯示 Flash message。
- **`POST /auth/logout`**
  - **處理邏輯**：清除 Session 暫存。
  - **輸出**：重導向至 `/`。

### Blueprint: `review_bp` (讀書心得管理)
- **`GET /review/create`**
  - **權限**：需登入
  - **輸出**：渲染 `review_form.html`。
- **`POST /review/create`**
  - **權限**：需登入
  - **輸入**：表單 `title`, `author`, `content`, `rating`
  - **處理邏輯**：驗證非空與 rating 範圍，調用 `Review.create()`。
  - **輸出**：重導向至 `/review/<新id>`。
- **`GET /review/<int:id>`**
  - **處理邏輯**：`Review.get_by_id(id)` 取出單篇詳細內容與所有者。
  - **輸出**：若找不到目標回傳 `404`。找到則渲染 `review_detail.html`。
- **`GET /review/<int:id>/edit`**
  - **權限**：需登入，且 session `user_id` 與該篇作者相符。
  - **處理邏輯**：撈出舊資料帶入至表單。
  - **輸出**：渲染 `review_form.html`。
- **`POST /review/<int:id>/edit`**
  - **權限**：同上。
  - **輸入**：表單更新值。
  - **處理邏輯**：`Review.update()` 儲存，成功後 Flash 提示。
  - **輸出**：重導向回詳情頁。
- **`POST /review/<int:id>/delete`**
  - **權限**：需為原作者或具備 `is_admin` 許可權。
  - **處理邏輯**：判斷後執行 `Review.delete()`。
  - **輸出**：回到 `/` 首頁。

### Blueprint: `admin_bp` (系統後台)
- **`GET /admin/reviews`**
  - **權限**：需登入且 `is_admin == 1`
  - **處理邏輯**：`Review.get_all()` 列出全部，可能包含隱藏細節或管理員快捷操作按鈕。
  - **輸出**：渲染 `admin.html`。
  
## 3. Jinja2 模板清單

所有的基礎模板都會繼承自 `base.html`，以保持外觀框架一致：

1. `base.html`: 大框架 (含 Header 導覽列與 Footer)，處理全域 Flash 錯誤訊息與樣式載入。
2. `index.html`: 首頁，展示文章清單。若帶有搜尋情境，動態更改提示文字。
3. `login.html`: 登入授權表單頁面。
4. `register.html`: 新帳號註冊表單。
5. `review_detail.html`: 單篇文章全版面展示。
6. `review_form.html`: 共用的編輯表單，利用變數判斷當下是「新增」或「編輯舊文」。
7. `admin.html`: 管理員專屬的列表型面板，方便檢視與處理違規。

*(路由骨架程式碼詳見 `app/routes/` 內的檔案)*
