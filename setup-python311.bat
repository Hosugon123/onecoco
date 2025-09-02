@echo off
echo 🔥 一口口麻辣串記帳系統 - Python 環境設定
echo ====================================================
echo.

echo 📋 正在檢查 Python 環境...
python --version

echo.
echo 🚀 正在建立 Python 3.11 虛擬環境...

REM 嘗試使用 py launcher 建立 Python 3.11 環境
py -3.11 -m venv venv311

if %errorlevel% neq 0 (
    echo ❌ 無法建立 Python 3.11 環境
    echo.
    echo 💡 請先安裝 Python 3.11：
    echo 1. 下載：https://www.python.org/downloads/release/python-3119/
    echo 2. 安裝時勾選 "Add Python to PATH"
    echo 3. 重新執行此腳本
    pause
    exit /b 1
)

echo ✅ Python 3.11 虛擬環境建立成功！

echo.
echo 🔧 正在安裝依賴套件...
call venv311\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🎯 正在執行資料庫遷移...
python manage.py makemigrations
python manage.py migrate

echo.
echo 👤 正在建立超級使用者...
echo 請輸入管理員帳號資訊：
python manage.py createsuperuser

echo.
echo 🚀 啟動開發伺服器...
python manage.py runserver

echo.
echo ✅ 設定完成！
pause


