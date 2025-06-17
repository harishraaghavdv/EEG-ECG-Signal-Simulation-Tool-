@echo off
echo 🚀 Starting EEG/ECG Generator Frontend...
echo ================================================

cd frontend

echo 📦 Installing dependencies...
call npm install

echo 🌐 Starting React development server...
echo    Frontend will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ================================================

call npm start

pause 