@echo off
cd /d "%~dp0..\hank_port"
set PYTHONUTF8=1
set PY=..\.venv\Scripts\python.exe
echo R1: the 800 economies of the sign map again, this time keeping every program's reading on all three rulers. 20 workers. A line every 10 economies.
%PY% sweep_signs.py --draws 800 --workers 20 --fast --out results_sweep_rulers
%PY% sweep_signs.py --draws 800 --workers 20 --fast --out results_sweep_rulers --retry-failed
%PY% summarize_rulers.py
%PY% ..\jobs\zipit.py results_sweep_rulers ..\RESULTS_TO_SEND\R1_rulers_sweep
echo.
echo ===== R1 DONE - send RESULTS_TO_SEND\R1_rulers_sweep.zip =====
