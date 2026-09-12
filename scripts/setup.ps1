$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "Environment setup complete."
Write-Host "Activate with: .\.venv\Scripts\Activate.ps1"
