@echo off
title File Diagnostic Tool

echo ========================================
echo File Diagnostic Tool
echo ========================================
echo.

echo [DEBUG] Current directory:
cd
echo.

echo [DEBUG] Current directory contents:
dir /a
echo.

echo [DEBUG] Looking for app.py specifically:
dir app.py
echo.

echo [DEBUG] Looking for files with 'app' in name:
dir *app*
echo.

echo [DEBUG] Checking if app.py exists (Method 1):
if exist app.py (
    echo SUCCESS: app.py found with 'if exist'
) else (
    echo ERROR: app.py NOT found with 'if exist'
)

echo.
echo [DEBUG] Checking if app.py exists (Method 2):
if exist "app.py" (
    echo SUCCESS: app.py found with quoted 'if exist'
) else (
    echo ERROR: app.py NOT found with quoted 'if exist'
)

echo.
echo [DEBUG] Checking file attributes:
if exist app.py (
    echo File attributes for app.py:
    attrib app.py
    echo File size and date:
    for %%F in (app.py) do echo Size: %%~zF bytes, Date: %%~tF
) else (
    echo Cannot check attributes - file not found
)

echo.
echo [DEBUG] Checking for hidden or system files:
dir /a:h app.py 2>nul
if not errorlevel 1 echo app.py is HIDDEN
dir /a:s app.py 2>nul
if not errorlevel 1 echo app.py is SYSTEM file

echo.
echo [DEBUG] Checking current working directory vs batch file location:
echo Batch file location: %~dp0
echo Current working directory: %cd%

echo.
echo [DEBUG] Files in batch file directory:
dir "%~dp0"

echo.
echo [DEBUG] Looking for app.py in batch file directory:
if exist "%~dp0app.py" (
    echo SUCCESS: app.py found in batch file directory
) else (
    echo ERROR: app.py NOT found in batch file directory
)

echo.
echo ========================================
echo Analysis complete. Please check the results above.
echo ========================================
echo.
pause