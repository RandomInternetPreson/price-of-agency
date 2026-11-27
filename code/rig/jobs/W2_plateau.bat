@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set PY=.venv\Scripts\python.exe
echo W2: certified plateau edge, n=4 (6 workers, up to 1 h). Prints nothing until done.
%PY% plateau_edge_bnb.py 4 0.5 1e-3 3600 --workers 6 --incumbent 0.310536
copy /Y results_exact\plateau_edge_bnb_n4_s0.5.txt RESULTS_TO_SEND\W2_plateau_n4.txt >nul
echo.
echo ===== W2 DONE - send RESULTS_TO_SEND\W2_plateau_n4.txt (or paste the certified line above) =====
