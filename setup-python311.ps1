Write-Host "🔥 一口口麻辣串記帳系統 - Python 環境設定" -ForegroundColor Red
Write-Host "===================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 正在檢查 Python 環境..." -ForegroundColor Cyan
python --version

Write-Host ""
Write-Host "🚀 正在建立 Python 3.11 虛擬環境..." -ForegroundColor Green

# 嘗試使用 py launcher 建立 Python 3.11 環境
try {
    py -3.11 -m venv venv311
    Write-Host "✅ Python 3.11 虛擬環境建立成功！" -ForegroundColor Green
} catch {
    Write-Host "❌ 無法建立 Python 3.11 環境" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 請先安裝 Python 3.11：" -ForegroundColor Yellow
    Write-Host "1. 下載：https://www.python.org/downloads/release/python-3119/" -ForegroundColor Cyan
    Write-Host "2. 安裝時勾選 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "3. 重新執行此腳本" -ForegroundColor Cyan
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host ""
Write-Host "🔧 正在安裝依賴套件..." -ForegroundColor Green
& ".\venv311\Scripts\Activate.ps1"
& ".\venv311\Scripts\python.exe" -m pip install --upgrade pip
& ".\venv311\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host ""
Write-Host "🎯 正在執行資料庫遷移..." -ForegroundColor Green
& ".\venv311\Scripts\python.exe" manage.py makemigrations
& ".\venv311\Scripts\python.exe" manage.py migrate

Write-Host ""
Write-Host "👤 正在建立超級使用者..." -ForegroundColor Green
Write-Host "請輸入管理員帳號資訊：" -ForegroundColor Yellow
& ".\venv311\Scripts\python.exe" manage.py createsuperuser

Write-Host ""
Write-Host "🚀 啟動開發伺服器..." -ForegroundColor Green
& ".\venv311\Scripts\python.exe" manage.py runserver

Write-Host ""
Write-Host "✅ 設定完成！" -ForegroundColor Green
Read-Host "按 Enter 鍵退出"


