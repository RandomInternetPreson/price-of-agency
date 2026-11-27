@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set PY=.venv\Scripts\python.exe
echo N3: tighter ceiling for n=4 (8 workers, 6 h). Silent until done.
%PY% plateau_edge_bnb.py 4 0.5 2e-4 21600 --workers 8 --incumbent 0.310536
copy /Y results_exact\plateau_edge_bnb_n4_s0.5.txt RESULTS_TO_SEND\N3_plateau_n4.txt >nul
echo.
echo ===== N3 DONE - send RESULTS_TO_SEND\N3_plateau_n4.txt =====
