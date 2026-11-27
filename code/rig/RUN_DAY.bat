@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - day run (2026-11-10) =====
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
start "D1 two-asset sign map (CPU, 24 workers)" cmd /k jobs\D1_two_asset_sweep.bat
start "D2 plateau n=5 (CPU, 12 workers, 4 h)" cmd /k jobs\D2_plateau_n5.bat
echo.
echo Two job windows launched (36 CPU workers in all, no GPU). Each prints ===== DONE ===== and drops its result in RESULTS_TO_SEND.
echo Nothing waits for anything else. STOP_ALL.bat stops every job.
pause
