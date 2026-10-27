@echo off
setlocal
cd /d "%~dp0"
title RON-SHO Browser 8-10 GPT - START
echo.
echo ====================================================
echo  RON-SHO BROWSER WORKBENCH - BUOC 1: MO 8-10 GPT
echo ====================================================
echo  1. Chon 8 hoac 10 tab ChatGPT.
echo  2. Chrome mo profile rieng.
echo  3. Anh DANG NHAP trong browser neu duoc hoi.
echo  4. Moi tab la mot chat, CHUA phai AI agent tu dong.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0LAUNCH_BROWSER.ps1"
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (echo [ERROR] Launcher dung ma loi %ERR%.) else (echo [OK] Chrome launch requested.)
echo Xem RUNBOOK_HUMAN.md
pause
exit /b %ERR%
