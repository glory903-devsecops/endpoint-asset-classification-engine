#!/bin/bash
# Linux Setup Script for Endpoint Asset Classification Engine
# Requires apt (Debian/Ubuntu) or dnf (CentOS/Fedora)

echo "Installing required software via package manager..."

# Check for apt (Debian/Ubuntu)
if command -v apt-get &> /dev/null
then
    echo "Updating system..."
    sudo apt-get update
    
    # Install Python 3
    echo "Installing Python 3..."
    sudo apt-get install -y python3 python3-pip
    
    # Install Git
    echo "Installing Git..."
    sudo apt-get install -y git
    
    # Install GitHub CLI
    echo "Installing GitHub CLI..."
    # Add GitHub official repository and install gh
    (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
    && sudo mkdir -p -m 755 /etc/apt/keyrings \
    && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && sudo apt update \
    && sudo apt install gh -y
    
# Check for dnf (Fedora/CentOS)
elif command -v dnf &> /dev/null
then
    echo "Installing Python 3, Git, and GitHub CLI..."
    sudo dnf install -y python3 git gh
else
    echo "Unsupported package manager. Please install Python 3, Git, and GitHub CLI manually."
    exit 1
fi

echo "Installation completed. Please restart your terminal."
