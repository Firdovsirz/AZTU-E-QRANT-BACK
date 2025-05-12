#!/bin/bash

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing pip..."

    # Download the get-pip.py script and use it to install pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    # Run get-pip.py to install pip
    python3 get-pip.py

    # Remove the get-pip.py script after installation
    rm get-pip.py
fi

# Now that pip is installed, install the required dependencies
pip install -r requirements.txt