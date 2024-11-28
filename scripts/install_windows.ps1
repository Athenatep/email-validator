# Windows PowerShell installation script
param(
    [string]$InstallPath = "C:\Program Files\Email Validator",
    [switch]$Development
)

# Stop on any error
$ErrorActionPreference = "Stop"

# Create installation directory
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null

# Function to check command existence
function Test-Command($Command) {
    try { Get-Command $Command -ErrorAction Stop | Out-Null; return $true }
    catch { return $false }
}

# Check Python installation
if (-not (Test-Command python)) {
    Write-Error "Python is not installed or not in PATH"
    exit 1
}

# Check Python version
$pythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ([version]$pythonVersion -lt [version]"3.9") {
    Write-Error "Python 3.9 or higher is required"
    exit 1
}

# Create and activate virtual environment
Write-Host "Creating virtual environment..."
python -m venv "$InstallPath\venv"
& "$InstallPath\venv\Scripts\Activate.ps1"

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

if ($Development) {
    # Check Node.js installation
    if (-not (Test-Command node)) {
        Write-Error "Node.js is not installed or not in PATH"
        exit 1
    }
    
    # Install npm dependencies
    Write-Host "Installing Node.js dependencies..."
    npm install
}

# Create required directories
Write-Host "Creating required directories..."
New-Item -ItemType Directory -Force -Path "$InstallPath\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallPath\reports" | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallPath\data" | Out-Null

# Create startup scripts
$guiScript = @"
@echo off
call "$InstallPath\venv\Scripts\activate.bat"
python -m src.main
"@

$apiScript = @"
@echo off
call "$InstallPath\venv\Scripts\activate.bat"
python -m uvicorn src.api.main:app --reload
"@

Set-Content -Path "$InstallPath\start_gui.bat" -Value $guiScript
Set-Content -Path "$InstallPath\start_api.bat" -Value $apiScript

Write-Host "Installation completed successfully!"
Write-Host
Write-Host "To start the GUI application:"
Write-Host "  $InstallPath\start_gui.bat"
Write-Host
Write-Host "To start the REST API:"
Write-Host "  $InstallPath\start_api.bat"