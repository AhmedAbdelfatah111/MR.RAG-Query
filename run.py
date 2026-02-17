
import subprocess
import time
import os
import sys

def run_services():
    # Start Backend
    print("Starting Backend...")
    backend_env = os.environ.copy()
    backend_env["PYTHONIOENCODING"] = "utf-8"
    backend = subprocess.Popen(
        [sys.executable, "-m", "app.server"],
        env=backend_env
    )
    
    # Wait for backend to start
    time.sleep(5)
    
    # Start Frontend
    print("Starting Frontend...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "ui.app"],
        env=os.environ.copy()
    )
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("Stopping services...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    run_services()
