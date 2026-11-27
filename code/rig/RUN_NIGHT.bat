@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - night run =====
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
start "N1 sweep part two (CPU, ~6 h)" cmd /k jobs\N1_sweep_more.bat
start "N2 plateau n=6 (CPU, 6 h)" cmd /k jobs\N2_plateau_n6.bat
start "N3 plateau n=4 long (CPU, 6 h)" cmd /k jobs\N3_plateau_n4_long.bat
start "N4 town 2 (GPU 1, ~10 min)" cmd /k jobs\N4_town2.bat
echo.
echo Four job windows launched (36 CPU workers in all, one GPU). Each prints ===== DONE ===== and drops its result in RESULTS_TO_SEND.
echo Nothing waits for anything else. STOP_ALL.bat stops every job.
pause
