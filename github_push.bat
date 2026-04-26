@echo off
echo ========================================
echo Preparing Git Push for GitHub
echo ========================================
echo.

echo Step 1: Creating .gitignore...
echo __pycache__/ > .gitignore
echo venv/ >> .gitignore
echo .env >> .gitignore
echo .env.local >> .gitignore
echo *.pyc >> .gitignore
echo .DS_Store >> .gitignore
echo Thumbs.db >> .gitignore
echo instance/ >> .gitignore

echo.
echo Step 2: Creating .env.example...
echo SECRET_KEY=your-secret-key-here > .env.example
echo DB_USER=postgres >> .env.example
echo DB_PASSWORD=your_password_here >> .env.example
echo DB_HOST=localhost >> .env.example
echo DB_PORT=5432 >> .env.example
echo DB_NAME=service_desk >> .env.example

echo.
echo Step 3: Removing .env from git if exists...
git rm --cached .env 2>nul

echo.
echo Step 4: Initializing git...
git init

echo.
echo Step 5: Adding files...
git add .

echo.
echo Step 6: Committing...
git commit -m "Initial commit: IT Service Desk with SLA Analytics"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create repository on GitHub
echo 2. Run: git remote add origin https://github.com/Anwesha-mishra-9090/it-service-desk-sla-analytics.git
echo 3. Run: git push -u origin main
echo.
pause