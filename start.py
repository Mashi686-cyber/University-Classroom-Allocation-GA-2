import os
import sys
import time
import argparse
import subprocess
import signal
import socket
import urllib.request
import urllib.error
import webbrowser
import platform
import venv
from pathlib import Path

# --- Constants & Paths ---
PROJECT_ROOT = Path(__file__).parent.absolute()
IS_WINDOWS = platform.system().lower() == "windows"
VENV_DIR = PROJECT_ROOT / ".venv"

if IS_WINDOWS:
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
    VENV_UVICORN = VENV_DIR / "Scripts" / "uvicorn.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"
    VENV_UVICORN = VENV_DIR / "bin" / "uvicorn"

BACKEND_DIR = PROJECT_ROOT / "web" / "backend"
FRONTEND_DIR = PROJECT_ROOT / "web" / "frontend"
BACKEND_REQ = BACKEND_DIR / "requirements.txt"
FRONTEND_PKG = FRONTEND_DIR / "package.json"
NODE_MODULES = FRONTEND_DIR / "node_modules"

processes = []

# --- UI Helpers ---
def print_header(title):
    print("=" * 45)
    print(f"  {title}".center(45))
    print("=" * 45)

def print_step(title):
    print(f"\n{title}")

def check_mark(text):
    print(f"[✓] {text}")

def error_mark(text):
    print(f"[✗] {text}")

# --- Environment Detection ---
def check_command(cmd_list):
    for cmd in cmd_list:
        if shutil_which(cmd):
            return cmd
    return None

def shutil_which(cmd):
    import shutil
    return shutil.which(cmd)

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

def wait_for_health(url, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=1) as response:
                if response.getcode() == 200:
                    return True
        except (urllib.error.URLError, socket.timeout, ConnectionResetError):
            pass
        time.sleep(1)
    return False

# --- Setup Routine ---
def setup_environment():
    print_header("UniClass GA - Setup")
    print_step("[1/5] Checking environment...")
    
    python_cmd = check_command(["python3", "python", "py"])
    if not python_cmd:
        error_mark("Python is not installed or not in PATH.")
        sys.exit(1)
    check_mark(f"Python ({python_cmd})")

    node_cmd = check_command(["node"])
    if not node_cmd:
        error_mark("Node.js is not installed. Please install Node.js 20 LTS or newer.")
        sys.exit(1)
    check_mark("Node.js")

    npm_cmd = check_command(["npm", "npm.cmd"] if IS_WINDOWS else ["npm"])
    if not npm_cmd:
        error_mark("npm is not installed.")
        sys.exit(1)
    check_mark("npm")

    print_step("[2/5] Checking virtual environment...")
    if not VENV_DIR.exists() or not VENV_PYTHON.exists():
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
        check_mark(f"Created .venv")
    else:
        check_mark(".venv exists")

    print_step("[3/5] Installing backend dependencies...")
    subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(BACKEND_REQ)], check=True)
    check_mark("Backend dependencies installed")

    print_step("[4/5] Installing frontend dependencies...")
    subprocess.run([npm_cmd, "install"], cwd=str(FRONTEND_DIR), shell=IS_WINDOWS, check=True)
    check_mark("Frontend dependencies installed")
    
    print_step("[5/5] Setup Complete!")
    print("\nYou can now run 'python start.py' to launch the application.")

# --- Check Routine ---
def run_checks():
    print_header("UniClass GA - System Check")
    all_pass = True
    
    def report(name, condition, error_msg):
        nonlocal all_pass
        if condition:
            check_mark(name)
        else:
            error_mark(name)
            print(f"    -> {error_msg}")
            all_pass = False

    python_cmd = check_command(["python3", "python", "py"])
    report("Python", bool(python_cmd), "Python is not installed.")
    
    node_cmd = check_command(["node"])
    report("Node.js", bool(node_cmd), "Node.js is not installed.")
    
    report("Virtual Environment", VENV_DIR.exists() and VENV_PYTHON.exists(), f"Virtual environment missing at {VENV_DIR}")
    report("Backend Requirements", BACKEND_REQ.exists(), "Backend requirements.txt missing.")
    report("Frontend Package.json", FRONTEND_PKG.exists(), "Frontend package.json missing.")
    report("Frontend node_modules", NODE_MODULES.exists(), "Frontend node_modules missing. Run setup.")
    
    dataset_dir = PROJECT_ROOT / "data" / "generated" / "small"
    report("Small Dataset", (dataset_dir / "courses.csv").exists(), "Datasets are missing. Run validation/generation scripts.")
    
    if all_pass:
        print("\nSTATUS: PASS")
    else:
        print("\nSTATUS: FAIL")
        sys.exit(1)

# --- Process Management ---
def shutdown_handler(signum, frame):
    print("\nShutting down services...")
    for p in processes:
        if p.poll() is None:
            if IS_WINDOWS:
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
                try:
                    p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    p.kill()
    sys.exit(0)

# --- Main Launcher ---
def main():
    parser = argparse.ArgumentParser(description="UniClass-GA Cross-Platform Launcher")
    parser.add_argument("--setup", action="store_true", help="Run initial environment setup")
    parser.add_argument("--check", action="store_true", help="Check system readiness")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    parser.add_argument("--backend-only", action="store_true", help="Only start the backend server")
    parser.add_argument("--frontend-only", action="store_true", help="Only start the frontend server")
    parser.add_argument("--port-backend", type=int, default=8000, help="Backend port (default 8000)")
    parser.add_argument("--port-frontend", type=int, default=3000, help="Frontend port (default 3000)")
    
    args = parser.parse_args()

    if args.setup:
        setup_environment()
        return

    if args.check:
        run_checks()
        return

    print_header("UniClass GA")

    if not VENV_DIR.exists():
        print("Virtual environment not found. Please run: python start.py --setup")
        sys.exit(1)

    if not args.backend_only and not NODE_MODULES.exists():
        print("Frontend node_modules not found. Please run: python start.py --setup")
        sys.exit(1)

    signal.signal(signal.SIGINT, shutdown_handler)
    if not IS_WINDOWS:
        signal.signal(signal.SIGTERM, shutdown_handler)

    print_step("[1/3] Checking ports...")
    
    if not args.frontend_only:
        if not check_port(args.port_backend):
            error_mark(f"Backend port {args.port_backend} is already in use.")
            sys.exit(1)
        check_mark(f"Port {args.port_backend} is free")
        
    if not args.backend_only:
        if not check_port(args.port_frontend):
            error_mark(f"Frontend port {args.port_frontend} is already in use.")
            sys.exit(1)
        check_mark(f"Port {args.port_frontend} is free")

    print_step("[2/3] Starting services...")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    if not args.frontend_only:
        uvicorn_cmd = str(VENV_UVICORN) if VENV_UVICORN.exists() else f"{str(VENV_PYTHON)} -m uvicorn"
        backend_cmd = [str(VENV_UVICORN), "app.main:app", "--host", "127.0.0.1", "--port", str(args.port_backend)]
        if not VENV_UVICORN.exists():
            backend_cmd = [str(VENV_PYTHON), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(args.port_backend)]
            
        b_process = subprocess.Popen(backend_cmd, cwd=str(BACKEND_DIR), env=env)
        processes.append(b_process)
        check_mark(f"Backend  -> http://localhost:{args.port_backend}")

    if not args.backend_only:
        npm_cmd = check_command(["npm.cmd"] if IS_WINDOWS else ["npm"])
        f_process = subprocess.Popen([npm_cmd, "run", "dev", "--", "-p", str(args.port_frontend)], cwd=str(FRONTEND_DIR), env=env, shell=IS_WINDOWS)
        processes.append(f_process)
        check_mark(f"Frontend -> http://localhost:{args.port_frontend}")

    print_step("[3/3] Waiting for health checks...")
    
    if not args.frontend_only:
        health_url = f"http://127.0.0.1:{args.port_backend}/api/health"
        if wait_for_health(health_url):
            check_mark("Backend is healthy")
        else:
            error_mark("Backend failed to start properly.")
            shutdown_handler(None, None)
            
    print_header("UniClass GA is ready!")
    print(f"Open:\nhttp://localhost:{args.port_frontend}")
    print("\nPress Ctrl+C to stop all services.")
    print("=" * 45)

    if not args.no_browser and not args.backend_only:
        webbrowser.open(f"http://localhost:{args.port_frontend}")

    try:
        while True:
            time.sleep(1)
            for p in processes:
                if p.poll() is not None:
                    print(f"\nProcess terminated unexpectedly with code {p.returncode}")
                    shutdown_handler(None, None)
    except KeyboardInterrupt:
        shutdown_handler(None, None)

if __name__ == "__main__":
    main()
