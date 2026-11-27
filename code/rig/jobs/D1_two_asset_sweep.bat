@echo off
cd /d "%~dp0..\hank_port"
set PYTHONUTF8=1
set PY=..\.venv\Scripts\python.exe
echo D1: two-asset sign map - 300 random two-asset economies, 24 workers. Prints one line per finished economy (first lines after 15-30 min).
%PY% sweep_two_asset.py --draws 300 --workers 24
%PY% summarize_two_asset.py
%PY% ..\jobs\zipit.py results_two_asset ..\RESULTS_TO_SEND\D1_two_asset_sweep
echo.
echo ===== D1 DONE - send RESULTS_TO_SEND\D1_two_asset_sweep.zip =====
