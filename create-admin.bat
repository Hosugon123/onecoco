@echo off
chcp 65001 >nul
echo ========================================
echo   建立超級管理員帳號
echo ========================================
echo.

echo 正在建立超級管理員帳號...
echo 請按照提示輸入帳號資訊：
echo.

py -3.11 manage.py createsuperuser

echo.
echo 如果建立成功，您就可以使用新帳號登入管理後台了！
echo 管理後台地址: http://localhost:8000/admin/
echo.
pause


