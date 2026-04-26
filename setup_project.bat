@echo off
echo ========================================
echo IT Service Desk - Project Setup
echo ========================================

cd "C:\Users\badal\OneDrive\Dokumen\vs code projects\smart-it-service-desk"

echo.
echo Step 1: Creating virtual environment...
python -m venv venv

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies...
pip install Flask Flask-SQLAlchemy Flask-CORS Flask-Migrate psycopg2-binary python-dotenv pandas

echo.
echo Step 5: Creating __init__.py files...
if not exist backend\__init__.py type nul > backend\__init__.py
if not exist backend\routes\__init__.py type nul > backend\routes\__init__.py
if not exist backend\services\__init__.py type nul > backend\services\__init__.py
if not exist backend\models\__init__.py type nul > backend\models\__init__.py
if not exist backend\utils\__init__.py type nul > backend\utils\__init__.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update .env file with your PostgreSQL credentials
echo 2. Create database 'service_desk' in pgAdmin4
echo 3. Run: python backend\app.py
echo.

pause