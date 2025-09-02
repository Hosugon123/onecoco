@echo off
chcp 65001 >nul
echo ========================================
echo   一口口麻辣串記帳系統
echo   Python 3.11 版本
echo ========================================
echo.

echo 正在檢查 Python 3.11 環境...
py -3.11 --version

echo.
echo 正在執行資料庫遷移...
py -3.11 manage.py makemigrations
py -3.11 manage.py migrate

echo.
echo 正在啟動開發伺服器...
echo 網站將在 http://localhost:8000 啟動
echo 管理後台: http://localhost:8000/admin
echo.
echo 按 Ctrl+C 停止伺服器
echo.

py -3.11 manage.py runserver 0.0.0.0:8000

echo.
echo 伺服器已停止
pause


