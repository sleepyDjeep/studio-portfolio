@echo off
rem Daily autonomous portfolio publish. Scheduled with:
rem   schtasks /Create /F /SC DAILY /ST 07:00 /TN "Studio Portfolio Daily Publish" ^
rem     /TR "D:\Projects\Studio_Portfolio\tools\run_daily.cmd"
setlocal
cd /d "%~dp0.."
if not exist data\logs mkdir data\logs
python tools\daily_publish.py >> data\logs\scheduler.log 2>&1
exit /b %errorlevel%
