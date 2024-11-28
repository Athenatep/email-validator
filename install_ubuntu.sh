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

# Qt6 dependencies
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

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install project in development mode
echo "Installing project dependencies..."
pip install -e .

# Create required directories
echo "Creating required directories..."
mkdir -p logs
mkdir -p reports/visualizations
mkdir -p data

echo "Installation completed successfully!"
echo
echo "To start the GUI application:"
echo "  source venv/bin/activate"
echo "  python -m src.main"
echo
echo "To start the REST API:"
echo "  source venv/bin/activate"
echo "  python -m uvicorn src.api.main:app --reload"