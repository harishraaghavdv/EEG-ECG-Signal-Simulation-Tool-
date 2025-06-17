#!/usr/bin/env python3
"""
Startup script for the EEG/ECG Generator Backend
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'neurokit2', 'mne', 'numpy', 
        'pandas', 'matplotlib', 'scipy', 'scikit-learn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "backend/static/plots",
        "backend/static/csv",
        "backend/data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    print("🚀 Starting EEG/ECG Generator Backend...")
    print("=" * 50)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies are installed")
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        sys.exit(1)
    
    os.chdir(backend_dir)
    
    # Start the Flask server
    print("\n🌐 Starting Flask server...")
    print("   Server will be available at: http://localhost:5000")
    print("   API documentation: http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

 