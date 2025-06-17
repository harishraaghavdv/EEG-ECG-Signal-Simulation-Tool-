# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## One-Command Setup (Recommended)

```bash
# Run the automated setup script
python setup.py
```

This will:
- ✅ Check Python and Node.js versions
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Generate startup scripts

## Manual Setup

### 1. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Use Generated Scripts
```bash
# Terminal 1 - Backend
start_backend.bat          # Windows
./start_backend.sh         # macOS/Linux

# Terminal 2 - Frontend
start_frontend.bat         # Windows
./start_frontend.sh        # macOS/Linux
```

### Option 2: Manual Commands
```bash
# Terminal 1 - Backend
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## First Steps

1. Open http://localhost:3000 in your browser
2. Choose between EEG or ECG generation
3. Select a signal category (Normal/Abnormal)
4. Choose a specific signal type
5. Configure parameters and generate
6. Download the results!

## Troubleshooting

### Backend Issues
- Ensure virtual environment is activated
- Check if port 5000 is available
- Verify all Python dependencies are installed

### Frontend Issues
- Ensure Node.js is installed
- Check if port 3000 is available
- Clear npm cache: `npm cache clean --force`

### API Connection Issues
- Ensure both backend and frontend are running
- Check browser console for CORS errors
- Verify API endpoints are accessible

## Support

 