#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing pip..."

    # Download the get-pip.py script
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    # Run get-pip.py to install pip for python3 with --user flag
    python3 get-pip.py --user

    # Clean up by removing the get-pip.py script
    rm get-pip.py
fi

# Ensure pip is available
if ! command -v pip &> /dev/null
then
    echo "pip installation failed. Please check your environment."
    exit 1
fi

# Install the required dependencies from requirements.txt
pip install --user -r requirements.txt