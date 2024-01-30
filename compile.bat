@echo off

set PYTHON=python
set VENV_NAME=venv
%PYTHON% -m venv %VENV_NAME%
call %VENV_NAME%\Scripts\activate

echo "Installing dependencies..."
pip install pygame
pip install nuitka

echo "Compiling ..."
nuitka --standalone --include-data-dir=./assets=assets main.py

echo "Done, deactivating..."
deactivate