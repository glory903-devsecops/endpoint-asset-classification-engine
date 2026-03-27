#!/bin/bash
# macOS Setup Script for Endpoint Asset Classification Engine
# Requires Homebrew (brew)

echo "Installing required software via Homebrew..."

# Install Homebrew if not already installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew not found. Please install Homebrew from https://brew.sh/"
    exit 1
fi

# Install Python 3.12
echo "Installing Python 3.12..."
brew install python@3.12

# Install Git
echo "Installing Git..."
brew install git

# Install GitHub CLI
echo "Installing GitHub CLI..."
brew install gh

echo "Installation completed. Please restart your terminal."
