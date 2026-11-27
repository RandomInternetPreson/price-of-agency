@echo off
cd /d "%~dp0"
echo Stopping every python process started from this rig folder...
powershell -NoProfile -ExecutionPolicy Bypass -File jobs\stop_all.ps1
pause
