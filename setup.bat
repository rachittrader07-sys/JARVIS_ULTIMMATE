@echo off
echo ========================================
echo        JARVIS SETUP SCRIPT
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python found.
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install packages!
    pause
    exit /b 1
)

echo Packages installed successfully.
echo.

echo Creating necessary directories...
if not exist "voice_profile" mkdir voice_profile
if not exist "memory" mkdir memory
if not exist "logs" mkdir logs
echo Directories created.
echo.

echo Downloading Vosk model...
if not exist "vosk-model-small-en-in-0.4" (
    echo Downloading speech recognition model...
    powershell -Command "Invoke-WebRequest -Uri 'https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip' -OutFile 'vosk-model.zip'"
    if errorlevel 1 (
        echo Failed to download model!
    ) else (
        echo Extracting model...
        powershell -Command "Expand-Archive -Path 'vosk-model.zip' -DestinationPath '.' -Force"
        del vosk-model.zip
        echo Model extracted.
    )
)
echo.

echo Initializing configuration...
if not exist "config.yaml" (
    echo Creating default configuration...
    copy config.default.yaml config.yaml
)
echo.

echo Setup complete!
echo.
echo To run JARVIS, use: python jarvis.py
echo.
pause