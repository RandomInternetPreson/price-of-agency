@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - three-ruler run (2026-11-10 evening) =====
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
start "R1 three rulers across 800 economies (CPU, 20 workers)" cmd /k jobs\R1_rulers_sweep.bat
echo.
echo One job window launched (20 CPU workers, no GPU). It prints ===== R1 DONE ===== and drops R1_rulers_sweep.zip in RESULTS_TO_SEND.
echo If it is interrupted, run this file again: finished economies are kept. STOP_ALL.bat stops it.
pause
