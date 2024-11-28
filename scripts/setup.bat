@echo off
echo Installing Email Validator...

:: Check Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    exit /b 1
)

:: Install Visual C++ Build Tools
echo Installing Visual C++ Build Tools...
powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vs_buildtools.exe' -OutFile 'vs_buildtools.exe'}"
vs_buildtools.exe --quiet --wait --norestart --nocache ^
    --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" ^
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
    --add Microsoft.VisualStudio.Component.Windows10SDK
del vs_buildtools.exe

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

:: Install base requirements first
pip install -r requirements-base.txt
if errorlevel 1 (
    echo Failed to install base requirements
    exit /b 1
)

:: Install numerical/visualization packages
pip install numpy==1.26.4
pip install pandas==2.1.3
pip install matplotlib==3.8.2
pip install seaborn==0.13.0

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