@echo off
chcp 65001 >nul
title JARVIS Assistant v2.0.0

echo.
echo    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
echo    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
echo    ██║███████║██████╔╝██║   ██║██║███████╗
echo    ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
echo    ██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║
echo    ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝ ╚═╝╚══════╝
echo        AI Assistant v2.0.0
echo        Ready to serve, sir!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

REM Check if jarvis.py exists
if not exist "jarvis.py" (
    echo ❌ jarvis.py not found!
    echo Please run install.py first
    pause
    exit /b 1
)

REM Check for command line arguments
set MODE=normal
set PROFILE=
set DEBUG=

:parse_args
if "%1"=="" goto :run_jarvis
if "%1"=="--mode" (
    set MODE=%2
    shift
    shift
    goto :parse_args
)
if "%1"=="--profile" (
    set PROFILE=%2
    shift
    shift
    goto :parse_args
)
if "%1"=="--debug" (
    set DEBUG=--debug
    shift
    goto :parse_args
)
if "%1"=="--help" (
    echo.
    echo Usage: start_j.bat [options]
    echo.
    echo Options:
    echo   --mode ^<mode^>    Start mode ^(normal, text, silent^)
    echo   --profile ^<name^> Use specific profile
    echo   --debug          Enable debug mode
    echo   --help           Show this help
    echo.
    pause
    exit /b 0
)
shift
goto :parse_args

:run_jarvis
echo Starting JARVIS in %MODE% mode...
if defined PROFILE echo Using profile: %PROFILE%
if defined DEBUG echo Debug mode enabled
echo.

REM Create necessary directories
mkdir data 2>nul
mkdir logs 2>nul
mkdir memory 2>nul
mkdir voice_profile 2>nul

REM Start JARVIS
python jarvis.py --mode=%MODE% %PROFILE% %DEBUG%

if errorlevel 1 (
    echo.
    echo ❌ JARVIS encountered an error
    echo Check logs\jarvis.log for details
)

echo.
pause