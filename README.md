# 一口口麻辣串 - 記帳和利潤結算系統

## 專案簡介
這是一個專為「一口口麻辣串」麻辣燙店設計的記帳和利潤結算系統，提供每日銷售額、成本記錄和利潤分析功能。

## 🚀 改用 Django 的優勢

### ⚡ **開發速度更快**
- **內建管理後台**：Django Admin 可以立即提供完整的 CRUD 介面，無需額外開發
- **ORM 更強大**：Django ORM 比 Mongoose 功能更豐富，查詢更直觀
- **內建表單處理**：自動驗證、錯誤處理，減少重複程式碼

### 🏗️ **架構更完整**
- **內建認證系統**：User 模型、權限管理、Session 處理
- **內建安全機制**：CSRF 保護、SQL 注入防護、XSS 防護
- **內建快取系統**：Redis 整合、資料庫查詢優化

### 📊 **資料分析更強**
- **Pandas 整合**：利潤分析、趨勢計算更簡單
- **Matplotlib/Plotly**：圖表生成更專業
- **NumPy**：數學計算效能更好

### 🔧 **部署更簡單**
- **Django + PostgreSQL**：在 Render 上部署更穩定
- **環境管理**：pip + requirements.txt 比 npm 更可靠
- **靜態檔案處理**：內建 collectstatic 指令

## 功能特色
- 🔐 使用者認證系統（創始人登入）
- 💰 每日銷售額記錄
- 📊 成本管理（食材、營運費用）
- 📈 利潤結算和趨勢分析
- 🏪 為未來多店管理預留擴展性
- 🎯 **Django Admin 完整管理後台**

## 技術架構
- **後端**: Python + Django 4.2
- **資料庫**: PostgreSQL
- **API**: Django REST Framework
- **認證**: JWT (djangorestframework-simplejwt)
- **部署**: Render.com / Heroku

## 快速開始

### 方法一：使用自動化腳本（推薦）
```bash
# 執行自動化設定腳本
python run.py
```

### 方法二：手動設定
```bash
# 1. 建立虛擬環境
python -m venv venv

# 2. 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 設定環境變數
# 編輯 .env 檔案，設定資料庫連線資訊

# 5. 執行資料庫遷移
python manage.py makemigrations
python manage.py migrate

# 6. 建立超級使用者
python manage.py createsuperuser

# 7. 啟動開發伺服器
python manage.py runserver
```

## 環境變數設定
在專案根目錄建立 `.env` 檔案：
```env
# 資料庫連線
DB_NAME=onecoco
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django 設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 店面設定
STORE_ID=main_store
```

## 預設帳號
系統會自動建立三個創始人帳號：
- **founder1** / founder123
- **founder2** / founder123  
- **founder3** / founder123

## 系統功能

### 🔐 使用者管理
- 創始人、加盟商、員工角色管理
- JWT 認證系統
- 權限控制

### 💰 銷售額管理
- 每日銷售額記錄
- 銷售類別分類（堂食、外帶、外送）
- 自動店面ID關聯

### 📊 成本管理
- 成本項目記錄（食材、營運、人工等）
- 供應商管理
- 發票號碼追蹤

### 📈 報表分析
- 日報、週報、月報、季報、年報
- 利潤率自動計算
- 趨勢分析

### 🎯 Django Admin 後台
- 完整的資料管理介面
- 權限控制
- 資料匯出功能

## 部署到 Render

### 1. 準備工作
```bash
# 提交到 GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Render 設定
1. 在 Render 上建立新的 Web Service
2. 連接 GitHub 專案
3. 設定環境變數（參考 render.yaml）
4. 部署

### 3. 環境變數
- `SECRET_KEY`: 自動生成
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: 從 Render PostgreSQL 取得
- `DEBUG`: False
- `ALLOWED_HOSTS`: 你的 Render 網域

## 專案結構
```
onecoco-malatang/
├── onecoco/              # Django 專案設定
│   ├── settings.py       # 專案設定
│   ├── urls.py          # 主要 URL 配置
│   └── wsgi.py          # WSGI 配置
├── accounts/             # 使用者管理應用
├── sales/                # 銷售額管理應用
├── costs/                # 成本管理應用
├── reports/              # 報表分析應用
├── manage.py             # Django 管理腳本
├── requirements.txt      # Python 依賴
├── run.py               # 自動化啟動腳本
├── render.yaml          # Render 部署配置
└── README.md            # 專案說明
```

## 開發建議

### 🎯 **優先使用 Django Admin**
- 大部分日常操作都可以在 Django Admin 中完成
- 無需額外開發前端介面
- 快速驗證資料模型

### 📊 **善用 Django ORM**
- 使用 `annotate()` 和 `aggregate()` 進行複雜查詢
- 建立適當的資料庫索引
- 使用 `select_related()` 和 `prefetch_related()` 優化查詢

### 🔒 **安全性考量**
- 使用 Django 內建的安全機制
- 實作適當的權限控制
- 定期更新依賴套件

## 未來擴展
- 多店管理系統
- 加盟商專用介面
- 行動應用程式
- 進階報表功能
- 庫存管理系統

## 技術支援
如有問題，請檢查：
1. Python 版本是否為 3.8+
2. 虛擬環境是否正確啟動
3. 資料庫連線是否正常
4. 環境變數是否正確設定

---

**🔥 一口口麻辣串 - 讓記帳變得更簡單！**