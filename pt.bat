@echo off
%~dp0\.venv\Scripts\python.exe "%~dp0\main.py" %*

@REM Check if the virtual environment is installed and fix it if it's not
if %errorlevel% neq 0 (
	call "%~dp0install/installer.bat"
)
