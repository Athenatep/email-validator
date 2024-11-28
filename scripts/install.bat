@echo off
echo Installing Email Validator...

:: Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    exit /b 1
)

:: Create virtual environment
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)

:: Upgrade pip
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    exit /b 1
)

:: Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    exit /b 1
)

:: Create required directories
mkdir logs 2>nul
mkdir reports 2>nul
mkdir reports\visualizations 2>nul

echo Installation completed successfully!
echo.
echo To start the GUI application:
echo   python src/main.py
echo.
echo To start the REST API:
echo   python -m uvicorn src.api.main:app --reload
echo.
pause