@echo off
cd /d "%~dp0..\hank_port"
set PYTHONUTF8=1
set PY=..\.venv\Scripts\python.exe
echo T1: the 300 two-asset economies again, keeping every program's bandwidth, so each can be read on three rulers. 14 workers. One line per finished economy (first lines after 20-40 min).
%PY% sweep_two_asset.py --draws 300 --workers 14 --out results_two_asset_rulers
%PY% summarize_two_asset_rulers.py
%PY% ..\jobs\zipit.py results_two_asset_rulers ..\RESULTS_TO_SEND\T1_two_asset_rulers
echo.
echo ===== T1 DONE - send RESULTS_TO_SEND\T1_two_asset_rulers.zip =====
