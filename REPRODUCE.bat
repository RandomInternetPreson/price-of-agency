@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
echo ===== The Price of Agency - reproduce =====
echo Re-runs the book's computations and checks each number against the page that prints it.
echo.
set "PY=python"
where py >nul 2>nul
if not errorlevel 1 set "PY=py -3"
if exist ".venv_reproduce\Scripts\python.exe" goto run
echo Building a small Python environment in .venv_reproduce - one time, a minute or two.
%PY% -m venv .venv_reproduce
if errorlevel 1 goto nopython
".venv_reproduce\Scripts\python.exe" -m pip install --upgrade pip
".venv_reproduce\Scripts\python.exe" -m pip install numpy scipy matplotlib
if errorlevel 1 goto nopackages
:run
".venv_reproduce\Scripts\python.exe" reproduce.py %*
set RC=%errorlevel%
echo.
if "%RC%"=="0" echo ===== DONE: every number matched. The report is REPRODUCE_REPORT.md =====
if not "%RC%"=="0" echo ===== SOME NUMBERS DID NOT MATCH. See REPRODUCE_REPORT.md =====
pause
exit /b %RC%
:nopython
echo FAILED: Python 3 was not found. Install it from python.org, or run:  winget install Python.Python.3.12
echo Then start this file again.
pause
exit /b 1
:nopackages
echo FAILED: numpy, scipy and matplotlib could not be installed. Check the network connection and start this file again.
pause
exit /b 1
