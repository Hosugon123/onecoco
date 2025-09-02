@echo off
echo 🔥 一口口麻辣串記帳系統
echo ======================================
echo.

echo 🚀 正在啟動 Docker 環境...
docker-compose up --build

echo.
echo ✅ 系統已啟動！
echo 🌐 網站地址: http://localhost:8000
echo 🎯 管理後台: http://localhost:8000/admin
echo.
echo 按任意鍵關閉...
pause >nul


