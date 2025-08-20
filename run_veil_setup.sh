#!/bin/bash

# Run Veil setup script with force and silent options
# This will install all necessary dependencies for Veil

echo "=========================================="
echo "       Veil Framework Setup Script"
echo "=========================================="
echo ""
echo "This script will install Veil with all dependencies."
echo "Options used:"
echo "  --force  : Force reinstall of all dependencies"
echo "  --silent : Automate the installation (minimize prompts)"
echo ""
echo "You will be prompted for your sudo password."
echo ""
echo "Starting installation..."
echo ""

# Run the setup
sudo /usr/share/veil/config/setup.sh --force --silent

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "   Installation completed successfully!"
    echo "=========================================="
    echo ""
    echo "You can now run 'veil' to start using the framework."
else
    echo ""
    echo "=========================================="
    echo "   Installation encountered an error."
    echo "=========================================="
    echo ""
    echo "Please check the output above for error messages."
fi
