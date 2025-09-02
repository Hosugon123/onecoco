Write-Host "🔥 一口口麻辣串記帳系統" -ForegroundColor Red
Write-Host "======================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "🚀 正在啟動 Docker 環境..." -ForegroundColor Green
docker-compose up --build

Write-Host ""
Write-Host "✅ 系統已啟動！" -ForegroundColor Green
Write-Host "🌐 網站地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🎯 管理後台: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意鍵關閉..." -ForegroundColor Yellow
Read-Host


