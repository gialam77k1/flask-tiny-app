# Set PowerShell execution policy to run scripts
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue

# Find and use Python
$pythonCommand = "python"

# Remove and recreate virtual environment
Remove-Item -Recurse -Force .\venv -ErrorAction SilentlyContinue
Write-Host "Creating virtual environment..." -ForegroundColor Green
& $pythonCommand -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Upgrade pip and install libraries
Write-Host "Upgrading pip and installing libraries..." -ForegroundColor Green
& $pythonCommand -m pip install --upgrade pip
& $pythonCommand -m pip install -r requirements.txt

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Green
& $pythonCommand -m flask --app flaskr init-db

Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "Starting Flask application..." -ForegroundColor Cyan

# Start Flask application
& $pythonCommand -m flask --app flaskr run 

Write-Host "
Default login credentials:
Username: admin123
Password: 123456
" -ForegroundColor Cyan

# Open default web browser
Start-Process "http://localhost:5000"