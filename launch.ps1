# launch_chimera.ps1
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Starting Project Chimera Engine        " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Verify Ollama is running, launch if dormant
$ollamaProcess = Get-Process -Name "ollama_app" -ErrorAction SilentlyContinue
if (-not $ollamaProcess) {
    Write-Host "[1/3] Launching Ollama Server..." -ForegroundColor Yellow
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/3] Ollama Server is active." -ForegroundColor Green
}

# 2. Navigate to Project Directory
$projectDir = "f:\GitHub\projects\Chimera"
Set-Location -Path $projectDir
Write-Host "[2/3] Set workspace context to: $projectDir" -ForegroundColor Green

# 3. Locate Python Interpreter (System or Virtual Environment)
$pythonPath = "C:\Users\oscar\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    # Fallback to system PATH python
    $pythonPath = "python"
}

Write-Host "[3/3] Initializing Chimera Gateway..." -ForegroundColor Green
Write-Host "Press Ctrl+C in this terminal window to stop the bot.`n" -ForegroundColor DarkGray

# Execute Chimera Core
& $pythonPath "f:\GitHub\projects\Chimera\chimera_core.py"