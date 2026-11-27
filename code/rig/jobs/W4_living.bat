@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set CUDA_VISIBLE_DEVICES=2
set PY=.venv\Scripts\python.exe
echo W4: living town with skill decay (GPU 2, ~10 min).
%PY% living_town_skill.py --runs 2000 --days 600
%PY% summarize_living_town_skill.py
%PY% jobs\zipit.py results_living RESULTS_TO_SEND\W4_living
echo.
echo ===== W4 DONE - send RESULTS_TO_SEND\W4_living.zip =====
