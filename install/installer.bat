@REM This is a script to check if everything is set up correctly and install the required packages, meant to run after the main script fails to run.

cd %~dp0..

@REM Check if Python is installed globally
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python is not installed on this system. Please install Python and try again.
    EXIT /B 1
)

@REM Python Environment
IF NOT EXIST ".venv\Scripts\python.exe" (
    ECHO Python environment does not exist, installing...

    ECHO Creating a virtual environment
    python -m venv .venv

    ECHO Install the required packages
    .venv\Scripts\pip install -r requirements.txt

    ECHO Installation complete!
)