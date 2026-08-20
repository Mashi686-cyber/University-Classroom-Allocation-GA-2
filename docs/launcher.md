# UniClass GA Cross-Platform Launcher

The UniClass GA launcher provides a single, unified entry point to automatically configure dependencies and start both the FastAPI backend and Next.js frontend across all operating systems.

## 1. Supported Platforms

The launcher detects the OS and automatically adjusts paths, shell usage, and commands.

- **Linux / macOS:** `./start.sh`
- **Windows Command Prompt:** `start.bat`
- **Windows PowerShell:** `.\start.ps1`
- **Direct Python Execution:** `python start.py`

## 2. First-Time Setup

For a brand new environment without any configurations, you can execute the setup mode:

```bash
python start.py --setup
```

**This command automatically:**
1. Verifies Python 3 and Node.js are installed.
2. Creates a Python virtual environment (`.venv`) if one does not exist.
3. Installs all required backend pip dependencies from `web/backend/requirements.txt`.
4. Installs all required frontend npm packages via `web/frontend/package.json`.

## 3. Starting the Application

Once setup is complete (or if the dependencies already exist), simply run:

```bash
python start.py
```
*(or use your platform's wrapper script)*

**The launcher will:**
1. Check if ports `8000` (backend) and `3000` (frontend) are free.
2. Start the FastAPI backend inside the virtual environment.
3. Start the Next.js frontend using `npm run dev`.
4. Poll the backend health API (`/api/health`) until the server is fully ready.
5. Automatically open `http://localhost:3000` in your default web browser.
6. Manage both processes. Pressing `Ctrl+C` once will cleanly terminate both servers.

## 4. System Check

If you are experiencing issues or want to verify the environment manually, use the check flag:

```bash
python start.py --check
```

This will run a diagnostic and output a simple PASS/FAIL report concerning Python, Node.js, the virtual environment, the required directories, and dataset availability.

## 5. Command-Line Options

The Python launcher `start.py` accepts several arguments for customization:

| Flag | Description |
|---|---|
| `--help` | Displays help information. |
| `--setup` | Runs the initial environment setup. |
| `--check` | Checks system readiness and reports status. |
| `--no-browser` | Prevents the browser from opening automatically. |
| `--backend-only` | Starts only the FastAPI backend server. |
| `--frontend-only` | Starts only the Next.js frontend server. |
| `--port-backend <port>`| Specifies a custom backend port (default: 8000). |
| `--port-frontend <port>`| Specifies a custom frontend port (default: 3000). |

## 6. Architecture & Implementation

To comply with the requirement of avoiding bash-specific logic, the core launcher `start.py` is written entirely in Python.
The scripts `start.sh`, `start.bat`, and `start.ps1` are extremely lightweight wrappers whose sole responsibility is to locate the Python executable and forward execution to `start.py`.

The launcher heavily uses the `subprocess` module to manage child processes and the `signal` module to intercept interrupts for clean shutdowns across platforms.
