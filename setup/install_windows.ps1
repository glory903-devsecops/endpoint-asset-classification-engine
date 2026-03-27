# Windows Setup Script for Endpoint Asset Classification Engine
# Requires Winget (Windows Package Manager)

Write-Host "Installing required software via Winget..." -ForegroundColor Cyan

# Install Python 3.12
Write-Host "Installing Python 3.12..."
winget install --id Python.Python.3.12 --source winget --silent --accept-package-agreements --accept-source-agreements

# Install Git
Write-Host "Installing Git..."
winget install --id Git.Git --source winget --silent --accept-package-agreements --accept-source-agreements

# Install GitHub CLI
Write-Host "Installing GitHub CLI..."
winget install --id GitHub.cli --source winget --silent --accept-package-agreements --accept-source-agreements

Write-Host "Installation completed. Please restart your terminal." -ForegroundColor Green
