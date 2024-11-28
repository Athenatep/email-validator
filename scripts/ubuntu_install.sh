#!/bin/bash
set -e

echo "Installing Email Validator on Ubuntu..."

# Function to check command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system package if not present
ensure_package() {
    if ! dpkg -l "$1" >/dev/null 2>&1; then
        echo "Installing $1..."
        sudo apt-get install -y "$1"
    fi
}

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install Python if not present
if ! command_exists python3; then
    echo "Installing Python..."
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Install required system dependencies
echo "Installing system dependencies..."
PACKAGES=(
    python3-dev
    build-essential
    libssl-dev
    libffi-dev
    libxml2-dev
    libxslt1-dev
    zlib1g-dev
    libjpeg-dev
    libpng-dev
    libfreetype6-dev
)

# Qt6 dependencies - updated list
PACKAGES+=(
    qt6-base-dev
    qt6-base-private-dev
    libqt6gui6
    libqt6widgets6
    libqt6core6
    libqt6dbus6
    libgl1-mesa-glx
    libegl1-mesa
    libxcb-cursor0
    libxcb-icccm4
    libxcb-image0
    libxcb-keysyms1
    libxcb-randr0
    libxcb-render-util0
    libxcb-shape0
    libxcb-xinerama0
    libxcb-xkb1
    libxkbcommon-x11-0
    '^libxcb.*-dev'
    libx11-xcb-dev
    libglu1-mesa-dev
    libxrender-dev
    libxi-dev
    libxkbcommon-dev
    libxkbcommon-x11-dev
)

for pkg in "${PACKAGES[@]}"; do
    ensure_package "$pkg"
done

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Clean pip cache
echo "Cleaning pip cache..."
pip cache purge

# Install PyQt6 and qt-material separately first
echo "Installing PyQt6 and qt-material..."
pip install PyQt6==6.5.2 qt-material==2.14

# Install other base requirements
echo "Installing other Python dependencies..."
pip install numpy==1.26.4
pip install pandas==2.1.3
pip install matplotlib==3.8.2
pip install seaborn==0.13.0
pip install -r requirements-base.txt

# Create required directories
echo "Creating required directories..."
mkdir -p logs
mkdir -p reports/visualizations
mkdir -p data

# Set correct permissions
echo "Setting permissions..."
chmod +x scripts/*.sh

echo "Installation completed successfully!"
echo
echo "To start the GUI application:"
echo "  source venv/bin/activate && python src/main.py"
echo
echo "To start the REST API:"
echo "  source venv/bin/activate && python -m uvicorn src.api.main:app --reload"
echo