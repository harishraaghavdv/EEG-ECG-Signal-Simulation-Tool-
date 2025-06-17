#!/usr/bin/env python3
"""
Setup script for the EEG/ECG Generator Application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🧠❤️  Synthetic EEG & ECG Generator Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed")
    print("   Please install Node.js from: https://nodejs.org/")
    return False

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Determine the pip command based on OS
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("📦 Installing Node.js dependencies...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "backend/static/plots",
        "backend/static/csv",
        "backend/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")

def create_startup_scripts():
    """Create startup scripts"""
    print("📝 Creating startup scripts...")
    
    # Windows batch file for backend
    backend_bat = """@echo off
echo 🚀 Starting EEG/ECG Generator Backend...
echo ================================================

call venv\\Scripts\\activate
cd backend
python app.py

pause
"""
    
    Path("start_backend.bat").write_text(backend_bat)
    print("   ✅ start_backend.bat")
    
    # Unix shell script for backend
    backend_sh = """#!/bin/bash
echo "🚀 Starting EEG/ECG Generator Backend..."
echo "================================================"

source venv/bin/activate
cd backend
python app.py
"""
    
    backend_script = Path("start_backend.sh")
    backend_script.write_text(backend_sh)
    backend_script.chmod(0o755)
    print("   ✅ start_backend.sh")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("1. Start the backend server:")
    if platform.system() == "Windows":
        print("   start_backend.bat")
    else:
        print("   ./start_backend.sh")
    print()
    print("2. Start the frontend (in a new terminal):")
    if platform.system() == "Windows":
        print("   start_frontend.bat")
    else:
        print("   ./start_frontend.sh")
    print()
    print("3. Open your browser and go to:")
    print("   http://localhost:3000")
    print()
    print("Backend API will be available at:")
    print("   http://localhost:5000")
    print()
    print("Happy generating! 🧠❤️")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        sys.exit(1)
    
    print()
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    if not install_node_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 