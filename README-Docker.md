# 🐳 Docker 快速啟動指南

## 🚀 一鍵啟動

### Windows 用戶
```bash
# 方法 1：雙擊執行
start.bat

# 方法 2：PowerShell 執行
.\start.ps1

# 方法 3：手動執行
docker-compose up --build
```

### macOS/Linux 用戶
```bash
docker-compose up --build
```

## 📋 系統需求

- Docker Desktop (Windows/macOS)
- Docker Compose
- 至少 4GB RAM

## 🔧 安裝 Docker

### Windows
1. 下載 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. 安裝並重啟電腦
3. 啟動 Docker Desktop

### macOS
1. 下載 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. 安裝並啟動

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

## 🌐 訪問網站

- **主網站**: http://localhost:8000
- **管理後台**: http://localhost:8000/admin
- **API 文檔**: http://localhost:8000/api/

## 🛠️ 常用命令

```bash
# 啟動服務
docker-compose up

# 背景啟動
docker-compose up -d

# 停止服務
docker-compose down

# 重新建置
docker-compose up --build

# 查看日誌
docker-compose logs

# 進入容器
docker-compose exec web bash
```

## 🔍 故障排除

### 端口被占用
```bash
# 檢查端口使用情況
netstat -an | findstr :8000

# 修改 docker-compose.yml 中的端口映射
ports:
  - "8001:8000"  # 改為 8001
```

### 權限問題
```bash
# Windows: 以管理員身份運行 PowerShell
# Linux/macOS: 使用 sudo
sudo docker-compose up
```

## 📁 專案結構

```
onecoco/
├── Dockerfile              # Docker 映像檔配置
├── docker-compose.yml      # Docker Compose 配置
├── start.bat              # Windows 啟動腳本
├── start.ps1              # PowerShell 啟動腳本
├── requirements.txt        # Python 依賴
└── onecoco/               # Django 專案
```

## 🎯 優勢

✅ **環境隔離**：不會影響系統 Python 環境  
✅ **版本穩定**：使用 Python 3.11 + Django 4.2.7  
✅ **一鍵啟動**：無需手動安裝依賴  
✅ **跨平台**：Windows/macOS/Linux 都能運行  
✅ **資料庫整合**：PostgreSQL 資料庫自動配置  

---

**🔥 現在您只需要雙擊 start.bat 就能啟動網站了！**


