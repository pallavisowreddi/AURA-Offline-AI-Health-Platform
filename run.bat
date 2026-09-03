@echo off
title AURA - Offline Health Chatbot Setup
color 0B
cls

echo =====================================================================
echo    AURA HEALTH CHATBOT - OFFLINE ML PREDICTIVE ANALYTICS SYSTEM
echo =====================================================================
echo.
echo  This batch script will automatically:
echo  1. Create a local Python 3.13 virtual environment
echo  2. Install required packages (Flask, scikit-learn, numpy, pandas, Pillow)
echo  3. Train offline symptom and skin condition predictive models
echo  4. Start the Flask application
echo  5. Open the chatbot in your web browser
echo.
echo =====================================================================
echo.

:: Check if Python Launcher (py) is installed
py --version >nul 2>&1
if errorlevel 1 (
    :: Fallback to default python command if py launcher is missing
    python --version >nul 2>&1
    if errorlevel 1 (
        color 0C
        echo ERROR: Python is not installed or not added to your system PATH.
        echo Please install Python 3.13 and check "Add Python to PATH".
        echo.
        pause
        exit /b 1
    )
)

:: Validate and create virtual environment using Python 3.13
if exist ".venv" (
    echo Checking virtual environment Python version...
    .venv\Scripts\python.exe -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 13) else 1)" >nul 2>&1
    if errorlevel 1 (
        echo [1/5] Virtual environment is not Python 3.13. Recreating...
        rd /s /q .venv
        py -3.13 -m venv .venv
        if errorlevel 1 (
            :: Fallback to standard python if py launcher failed
            python -m venv .venv
        )
    ) else (
        echo [1/5] Virtual environment Python 3.13 already exists.
    )
) else (
    echo [1/5] Creating Python 3.13 virtual environment...
    py -3.13 -m venv .venv
    if errorlevel 1 (
        :: Fallback
        python -m venv .venv
    )
)

:: Activate Virtual Environment
echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install Requirements
echo [3/5] Installing dependencies (this may take a moment)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    color 0C
    echo ERROR: Dependency installation failed.
    pause
    exit /b 1
)

:: Run training script
echo.
echo [4/5] Training local machine learning models...
python train_models.py
if errorlevel 1 (
    color 0C
    echo ERROR: Model training failed.
    pause
    exit /b 1
)

:: Start Flask server and open browser
echo.
echo [5/5] Launching AURA Web Application...
echo.
echo -------------------------------------------------------------
echo  Success! Starting local server...
echo  If the page does not open automatically, go to:
echo  http://127.0.0.1:5000/
echo -------------------------------------------------------------
echo.

timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000/

:: Start the Flask app
python app.py

pause
