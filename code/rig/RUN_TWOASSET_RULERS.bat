@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - two-asset host on three rulers (2026-11-10 evening) =====
echo Folder: %CD%
if not exist ".venv\Scripts\python.exe" (
  echo Building the Python environment in %CD%\.venv  (one time for this folder; a few minutes, pip reuses its download cache)
  py -3.12 -m venv .venv
  if errorlevel 1 ( echo FAILED: Python 3.12 not found. & pause & exit /b 1 )
  ".venv\Scripts\python.exe" -m pip install --upgrade pip
  ".venv\Scripts\python.exe" -m pip install numpy scipy numba matplotlib sequence-jacobian
  ".venv\Scripts\python.exe" -m pip install torch --index-url https://download.pytorch.org/whl/cu128
)
".venv\Scripts\python.exe" jobs\check_env.py
if errorlevel 1 ( echo FAILED: environment check. Paste this window to Claude. & pause & exit /b 1 )
if not exist RESULTS_TO_SEND mkdir RESULTS_TO_SEND
start "T1 two-asset host on three rulers (CPU, 14 workers)" cmd /k jobs\T1_two_asset_rulers.bat
echo.
echo One job window launched (14 CPU workers, no GPU). It prints ===== T1 DONE ===== and drops T1_two_asset_rulers.zip in RESULTS_TO_SEND.
echo The R1 job already running in the other folder is not touched. If this one is interrupted, run this file again: finished economies are kept.
pause
