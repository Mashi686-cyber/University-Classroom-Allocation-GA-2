#!/usr/bin/env bash

# Find the directory where this script is located (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect python executable
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python is not installed. Please install Python 3."
    exit 1
fi

# Execute start.py passing along any arguments
exec "$PYTHON_CMD" "$PROJECT_ROOT/start.py" "$@"
