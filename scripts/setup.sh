#!/bin/bash
set -e

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
else
    OS=$(uname -s)
fi

# Run appropriate installation script
if [[ "$OS" == "Ubuntu"* ]]; then
    bash scripts/ubuntu_install.sh
else
    echo "Unsupported operating system: $OS"
    echo "Currently only Ubuntu is supported"
    exit 1
fi