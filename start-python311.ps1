Write-Host "========================================" -ForegroundColor Yellow
Write-Host "   一口口麻辣串記帳系統" -ForegroundColor Red
Write-Host "   Python 3.11 版本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "正在檢查 Python 3.11 環境..." -ForegroundColor Green
py -3.11 --version

Write-Host ""
Write-Host "正在執行資料庫遷移..." -ForegroundColor Green
py -3.11 manage.py makemigrations
py -3.11 manage.py migrate

Write-Host ""
Write-Host "正在啟動開發伺服器..." -ForegroundColor Green
Write-Host "網站將在 http://localhost:8000 啟動" -ForegroundColor Cyan
Write-Host "管理後台: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止伺服器" -ForegroundColor Yellow
Write-Host ""

py -3.11 manage.py runserver 0.0.0.0:8000

Write-Host ""
Write-Host "伺服器已停止" -ForegroundColor Red
Read-Host "按 Enter 鍵退出"


