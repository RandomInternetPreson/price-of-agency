@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set PY=.venv\Scripts\python.exe
echo N2: certified ceiling on the plateau edge in the reference world, n=6 (8 workers, 6 h). Silent until done.
%PY% plateau_edge_bnb.py 6 0.5 1e-3 21600 --workers 8 --incumbent 0.334841
copy /Y results_exact\plateau_edge_bnb_n6_s0.5.txt RESULTS_TO_SEND\N2_plateau_n6.txt >nul
echo.
echo ===== N2 DONE - send RESULTS_TO_SEND\N2_plateau_n6.txt =====
