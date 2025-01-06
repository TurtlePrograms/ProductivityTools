@echo off
%~dp0\.venv\Scripts\python.exe "%~dp0\main.py" %*
if %errorlevel% neq 0 (
	call "%~dp0install/installer.bat"
)
