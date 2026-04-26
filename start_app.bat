@echo off
cd /d "C:\Users\badal\OneDrive\Dokumen\vs code projects\smart-it-service-desk"
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Starting IT Service Desk...
echo.
python backend\app.py
pause