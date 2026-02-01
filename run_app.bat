@echo off
echo Starting Universal Appointment Notifier...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)
python main.py
echo.
echo Process finished. Check logs/activity.log for details.
pause