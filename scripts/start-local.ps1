param(
  [string]$EnvFile = ".env.local"
)

$ErrorActionPreference = "Stop"

function Load-EnvFile {
  param([string]$Path)
  if (!(Test-Path $Path)) {
    throw "Env file not found: $Path"
  }
  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#")) {
      $parts = $line.Split("=", 2)
      if ($parts.Count -eq 2) {
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
      }
    }
  }
}

function Start-ServiceWindow {
  param(
    [string]$Name,
    [string]$WorkDir,
    [string]$Command
  )
  Start-Process powershell -ArgumentList "-NoExit", "-Command", $Command -WorkingDirectory $WorkDir
  Write-Host "Started $Name"
}

Load-EnvFile $EnvFile

$root = (Resolve-Path ".").Path

Start-ServiceWindow -Name "Pets Service" -WorkDir "$root\services\pets" -Command "python -m pip install -r requirements.txt; python -m uvicorn app.main:app --host 0.0.0.0 --port $env:PETS_SERVICE_PORT --reload"
Start-ServiceWindow -Name "Gateway" -WorkDir "$root\gateway" -Command "python -m pip install -r requirements.txt; python -m uvicorn app.main:app --host 0.0.0.0 --port $env:GATEWAY_PORT --reload"
Start-ServiceWindow -Name "Frontend" -WorkDir "$root\frontend" -Command "npm install; npm run dev -- --host 0.0.0.0 --port 5173"

Write-Host ""
Write-Host "Local stack launch requested."
Write-Host "Frontend: http://localhost:5173"
Write-Host "Gateway:  http://localhost:$env:GATEWAY_PORT/docs"
