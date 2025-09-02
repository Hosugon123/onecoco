@echo off
echo 🔥 一口口麻辣串記帳系統 - 快速啟動
echo ============================================
echo.

echo 📋 正在檢查 Python 環境...
python --version

echo.
echo 🚀 正在啟動開發伺服器...

REM 直接使用系統 Python 運行
python manage.py runserver 0.0.0.0:8000

echo.
echo ✅ 伺服器已啟動！
echo 🌐 網站地址: http://localhost:8000
echo 🎯 管理後台: http://localhost:8000/admin
echo.
echo 按任意鍵關閉...
pause >nul


