#!/bin/bash

# Define the virtual environment directory
VENV_DIR=".venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Attempting to run setup.sh..."
    if [ -f "./setup.sh" ]; then
        chmod +x ./setup.sh
        ./setup.sh
        if [ $? -ne 0 ]; then
             echo "Setup failed. Exiting."
             exit 1
        fi
    else
        echo "Error: setup.sh not found. Please set up the environment manually."
        exit 1
    fi
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Run the application
# Assuming the package is run as a module from the root directory
python3 -m clasp.main "$@"
