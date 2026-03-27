import os
import sys
import subprocess
import venv
from pathlib import Path

def run_command(command, cwd=None):
    print(f"Executing: {' '.join(command)}")
    try:
        subprocess.check_call(command, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False
    return True

def setup():
    print("=== Endpoint Asset Classification Engine Bootstrap ===")
    root_dir = Path(__file__).parent.parent.absolute()
    venv_dir = root_dir / "venv"
    pip_exe = str(venv_dir / "Scripts" / "pip.exe") if os.name == "nt" else str(venv_dir / "bin" / "pip")
    python_exe = str(venv_dir / "Scripts" / "python.exe") if os.name == "nt" else str(venv_dir / "bin" / "python")

    # 1. Create venv
    if not venv_dir.exists():
        print(f"Creating virtual environment in {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("Virtual environment already exists.")

    # 2. Upgrade pip
    print("Upgrading pip...")
    run_command([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    # 3. Install requirements
    req_file = root_dir / "requirements.txt"
    if req_file.exists():
        print("Installing dependencies from requirements.txt...")
        run_command([pip_exe, "install", "-r", str(req_file)])
    else:
        print("requirements.txt not found.")

    print("\n=== Setup Completed! ===")
    if os.name == "nt":
        print(f"To activate the environment, run: .\\venv\\Scripts\\activate")
    else:
        print(f"To activate the environment, run: source venv/bin/activate")
    print("Then run the engine with: python main.py")

if __name__ == "__main__":
    setup()
