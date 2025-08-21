@echo off
title MP4 to WebP Converter

cd /d "%~dp0"

echo ========================================
echo MP4 to WebP Converter
echo ========================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found!
    start https://www.python.org/downloads/
    pause
    exit /b
)
echo Python OK!

REM Check packages
echo.
echo [2/4] Checking packages...
python -c "import flask, cv2, PIL, psutil" 2>nul
if errorlevel 1 (
    echo Installing missing packages...
    python -m pip install Flask opencv-python Pillow psutil --user --quiet 2>nul
    echo Packages installed!
) else (
    echo All packages are already installed!
)

REM Create folders
echo.
echo [3/4] Setting up folders...
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist templates mkdir templates

REM Check HTML
if not exist templates\index.html (
    echo WARNING: templates\index.html missing!
    start templates
    pause
)

REM Start server and browser in correct order
echo.
echo [4/4] Starting server...
echo ========================================
echo Starting Flask server...
echo Browser will open after server starts
echo ========================================
echo.

REM Start server first, then open browser after delay
start /b timeout /t 3 >nul && start http://localhost:5000
python app.py

echo.
echo Server stopped.
pause