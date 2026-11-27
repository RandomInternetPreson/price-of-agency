@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set PY=.venv\Scripts\python.exe
echo D2: certified ceiling on the plateau edge with five futures (12 workers, 4 h). Silent until done.
%PY% plateau_edge_bnb.py 5 0.5 5e-4 14400 --workers 12 --incumbent 0.357101
copy /Y results_exact\plateau_edge_bnb_n5_s0.5.txt RESULTS_TO_SEND\D2_plateau_n5.txt >nul
echo.
echo ===== D2 DONE - send RESULTS_TO_SEND\D2_plateau_n5.txt =====
