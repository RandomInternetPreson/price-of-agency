@echo off
cd /d "%~dp0..\hank_port"
set PYTHONUTF8=1
set PY=..\.venv\Scripts\python.exe
echo W1: sign-stability sweep (400 fast draws, 20 workers, ~3 h). Warnings about overflow/invalid are expected.
%PY% sweep_signs.py --fast --draws 400 --workers 20
%PY% summarize_sweep.py
%PY% ..\jobs\zipit.py results_sweep_fast ..\RESULTS_TO_SEND\W1_sweep
echo.
echo ===== W1 DONE - send RESULTS_TO_SEND\W1_sweep.zip =====
