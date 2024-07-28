@echo off

:: Change directory to WCtoSS
cd /d ".\WCtoSS"

:: Activate the virtual environment
call "venv\Scripts\activate"

:: Run WCtoSS.py
python WCtoSS.py

:: Pause the batch file so it remains open
pause
