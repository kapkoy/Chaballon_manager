@echo off
setlocal

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and rerun this script.
    exit /b 1
)

REM Set up virtual environment
echo Setting up virtual environment...
python -m venv _files\venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    exit /b 1
)
echo Virtual environment created successfully.

REM Activate virtual environment
echo Activating virtual environment...
call _files\venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r _files\requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    exit /b 1
)
echo Dependencies installed successfully.

REM Deactivate virtual environment
echo Deactivating virtual environment...
deactivate

echo Installation complete.
pause
pause
exit /b 0