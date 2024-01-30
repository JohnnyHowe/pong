@echo off

@REM This section here creates a little wee virtual environment. It's not required, but makes the builds more consistent
set PYTHON=python
set VENV_NAME=venv
%PYTHON% -m venv %VENV_NAME%
call %VENV_NAME%\Scripts\activate

@REM Install required packages (can't use the ones installed on your computer because it's in a virtual environment)
echo "Installing dependencies..."
pip install nuitka
pip install pygame

echo "Compiling ..."
nuitka --standalone --include-data-dir=./assets=assets main.py

@REM Deactivating the virtual environment
echo "Done, deactivating..."
deactivate