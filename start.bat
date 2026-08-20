@echo off
setlocal

:: Get the directory where this script is located (project root)
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: Detect python executable
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
) else (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=py"
    ) else (
        echo ERROR: Python is not installed or not added to PATH.
        exit /b 1
    )
)

:: Execute start.py passing along any arguments
"%PYTHON_CMD%" "%PROJECT_ROOT%\start.py" %*
