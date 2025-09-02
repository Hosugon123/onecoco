@echo off
chcp 65001 >nul
echo ========================================
echo   一口口麻辣串記帳系統
echo ========================================
echo.

echo 正在檢查 Python 環境...
python --version

echo.
echo 正在啟動開發伺服器...
echo 網站將在 http://localhost:8000 啟動
echo 管理後台: http://localhost:8000/admin
echo.
echo 按 Ctrl+C 停止伺服器
echo.

python manage.py runserver 0.0.0.0:8000

echo.
echo 伺服器已停止
pause


