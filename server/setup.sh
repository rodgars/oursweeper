#!/bin/bash

# Function to install pyenv
install_pyenv() {
    curl https://pyenv.run | bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
}

# Check if pyenv is installed, if not, install it
if ! command -v pyenv &> /dev/null
then
    echo "pyenv could not be found. Installing pyenv..."
    install_pyenv
else
    echo "pyenv is already installed."
fi

# Read the Python version from .python-version file
PYTHON_VERSION=$(cat .python-version)

# Install the specified Python version using pyenv
if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"
then
    echo "Installing Python $PYTHON_VERSION..."
    pyenv install $PYTHON_VERSION
else
    echo "Python $PYTHON_VERSION is already installed."
fi

# Set the local Python version
pyenv local $PYTHON_VERSION

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip and install pip-tools
echo "Upgrading pip and installing pip-tools..."
pip install --upgrade pip
pip install pip-tools

# Install the libraries from requirements.txt and requirements-dev.txt
echo "Installing dependencies from requirements.txt and requirements-dev.txt..."
pip install -r requirements.txt
pip install -r requirements_dev.txt

echo "Setup complete. Virtual environment is ready."
