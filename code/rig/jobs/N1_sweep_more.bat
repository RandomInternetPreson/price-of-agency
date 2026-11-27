@echo off
cd /d "%~dp0..\hank_port"
set PYTHONUTF8=1
set PY=..\.venv\Scripts\python.exe
echo N1: sweep, part two - reruns the 69 unsolved economies with the bounded solver and adds 400 new ones (20 workers, about 6 h). Overflow warnings are expected.
%PY% sweep_signs.py --fast --draws 800 --workers 20 --retry-failed
%PY% summarize_sweep.py
%PY% ..\jobs\zipit.py results_sweep_fast ..\RESULTS_TO_SEND\N1_sweep_800
echo.
echo ===== N1 DONE - send RESULTS_TO_SEND\N1_sweep_800.zip =====
