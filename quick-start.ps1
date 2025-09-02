Write-Host "🔥 一口口麻辣串記帳系統 - 快速啟動" -ForegroundColor Red
Write-Host "===========================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 正在檢查 Python 環境..." -ForegroundColor Cyan
python --version

Write-Host ""
Write-Host "🚀 正在啟動開發伺服器..." -ForegroundColor Green

# 直接使用系統 Python 運行
python manage.py runserver 0.0.0.0:8000

Write-Host ""
Write-Host "✅ 伺服器已啟動！" -ForegroundColor Green
Write-Host "🌐 網站地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🎯 管理後台: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意鍵關閉..." -ForegroundColor Yellow
Read-Host


