@echo off
cd /d "%~dp0.."
set PYTHONUTF8=1
set CUDA_VISIBLE_DEVICES=1
set PY=.venv\Scripts\python.exe
echo N4: fishers who consult yesterday, and a master who misdirects when it pays (GPU 1, about 10 min).
%PY% town_stress2.py --seasons 20000
%PY% summarize_town_stress2.py
%PY% jobs\zipit.py results_town2 RESULTS_TO_SEND\N4_town2
echo.
echo ===== N4 DONE - send RESULTS_TO_SEND\N4_town2.zip =====
