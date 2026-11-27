@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set CUDA_VISIBLE_DEVICES=1
set PY=.venv\Scripts\python.exe
echo W3: town under stress (GPU 1, ~10-20 min).
%PY% town_stress_T13.py --seasons 20000 --shard 0 --nshards 1
%PY% summarize_town_stress.py
%PY% jobs\zipit.py results_town RESULTS_TO_SEND\W3_town
echo.
echo ===== W3 DONE - send RESULTS_TO_SEND\W3_town.zip =====
