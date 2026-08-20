$ErrorActionPreference = "Stop"

# Get the directory where this script is located (project root)
$ProjectRoot = $PSScriptRoot

# Detect python executable
$PythonCmd = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
} else {
    Write-Host "ERROR: Python is not installed or not added to PATH." -ForegroundColor Red
    exit 1
}

# Execute start.py passing along any arguments
$ScriptPath = Join-Path $ProjectRoot "start.py"

# Need to invoke via & to pass arguments correctly
& $PythonCmd $ScriptPath $args
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
