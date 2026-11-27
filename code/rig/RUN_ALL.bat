@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - rig launcher =====
echo Folder: %CD%
if not exist ".venv\Scripts\python.exe" (
  echo Building the Python environment in %CD%\.venv  (one time; includes the torch download, 5-15 min)
  py -3.12 -m venv .venv
  if errorlevel 1 ( echo FAILED: Python 3.12 not found. Run:  winget install Python.Python.3.12   then start this file again. & pause & exit /b 1 )
  ".venv\Scripts\python.exe" -m pip install --upgrade pip
  ".venv\Scripts\python.exe" -m pip install numpy scipy numba matplotlib sequence-jacobian
  ".venv\Scripts\python.exe" -m pip install torch --index-url https://download.pytorch.org/whl/cu128
)
".venv\Scripts\python.exe" jobs\check_env.py
if errorlevel 1 ( echo FAILED: environment check. Paste this window to Claude. & pause & exit /b 1 )
if not exist RESULTS_TO_SEND mkdir RESULTS_TO_SEND
start "W1 sweep (CPU)" cmd /k jobs\W1_sweep.bat
start "W2 plateau (CPU)" cmd /k jobs\W2_plateau.bat
start "W3 town (GPU 1)" cmd /k jobs\W3_town.bat
start "W4 living town (GPU 2)" cmd /k jobs\W4_living.bat
echo.
echo Four job windows launched. Each prints ===== DONE ===== and drops its result in RESULTS_TO_SEND.
echo Send me each file in RESULTS_TO_SEND as it appears. STOP_ALL.bat stops every job.
pause
