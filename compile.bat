@echo off

set PYTHON=python
set VENV_NAME=venv
%PYTHON% -m venv %VENV_NAME%
call %VENV_NAME%\Scripts\activate

echo "Installing dependencies..."
pip install nuitka
pip install pygame

echo "Compiling ..."
nuitka --standalone --include-data-dir=./assets=assets main.py

echo "Tidying up ..."
powershell Compress-Archive -Path "main.dist" -DestinationPath "main.dist.zip"

echo "Done, deactivating..."
deactivate