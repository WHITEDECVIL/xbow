#!/bin/bash

# XBOW Installation and Setup Script

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  XBOW - AI Penetration Testing Framework                   ║"
echo "║  Installation Script                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[*] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "[+] Found Python $python_version"

# Extract major and minor version
major=$(echo $python_version | cut -d. -f1)
minor=$(echo $python_version | cut -d. -f2)

if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 9 ]]; then
    echo "[-] Python 3.9+ required"
    exit 1
fi

# Check system dependencies
echo "[*] Checking system dependencies..."

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "[-] pip3 not found, installing..."
    sudo apt-get install -y python3-pip
fi

# Check for git
if ! command -v git &> /dev/null; then
    echo "[!] git not found, installing..."
    sudo apt-get install -y git
fi

# Optional: Check for nmap
if ! command -v nmap &> /dev/null; then
    echo "[!] nmap not found, installing..."
    sudo apt-get install -y nmap
fi

# Optional: Check for dnsutils
if ! command -v dig &> /dev/null; then
    echo "[!] dnsutils not found, installing..."
    sudo apt-get install -y dnsutils
fi

# Create virtual environment
echo ""
echo "[*] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[+] Virtual environment created"
else
    echo "[+] Virtual environment already exists"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "[*] Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Install XBOW
echo "[*] Installing XBOW..."
python3 -m pip install -e .

# Create directories
echo "[*] Creating directories..."
mkdir -p results
mkdir -p logs
mkdir -p models

# Download additional resources
echo "[*] Downloading additional resources..."
# Download popular wordlists if needed
if [ ! -f "config/common.txt" ]; then
    echo "[*] Note: You can add wordlists to config/ directory"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ Installation Complete                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "To get started:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. View help: xbow --help"
echo "  3. Run scan: xbow scan --target example.com --scan-type web"
echo ""
echo "For detailed documentation, see: docs/GETTING_STARTED.md"
echo ""
