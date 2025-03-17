#!/bin/bash
# This script automates the installation of Git, FFmpeg, Poppler, and sets up a Python virtual environment.

# Exit immediately if a command exits with a non-zero status.
set -e

# Update the package list and upgrade existing packages
echo "Updating packages..."
sudo apt update && sudo apt upgrade -y

# Install Git, FFmpeg, Python3, the Python virtual environment module, Pip, and Poppler utilities
echo "Installing Git, FFmpeg, Python packages, and Poppler..."
sudo apt install -y git ffmpeg python3 python3-venv python3-pip poppler-utils libpoppler-cpp-dev

# Verify the installations
echo "Verifying installations:"
echo "Git version: $(git --version)"
echo "FFmpeg version: $(ffmpeg -version | head -n 1)"
echo "Python version: $(python3 --version)"
echo "Pip version: $(pip3 --version)"
echo "Poppler version: $(pdftoppm -v | head -n 1)"

# Create a Python virtual environment in the current directory
VENV_DIR="myenv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating a Python virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created successfully."
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# Activate the virtual environment and install python-poppler
echo "Activating virtual environment and installing python-poppler..."
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install python-poppler pdf2image pillow

# Provide instructions to activate the virtual environment
echo "To activate your virtual environment, run:"
echo "source ${VENV_DIR}/bin/activate"

# Optionally, install additional Python packages
# Uncomment the following lines to install packages from a requirements.txt file:
# if [ -f "requirements.txt" ]; then
#     echo "Installing Python packages from requirements.txt..."
#     pip install -r requirements.txt
# fi

# Deactivate virtual environment
deactivate

echo "Setup complete."
