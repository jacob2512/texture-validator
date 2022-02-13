@echo off
 
goto :DOES_PYTHON_EXIST
 
:DOES_PYTHON_EXIST
echo Checking for Python...
python --version 2>NUL
if errorlevel 1 goto :PYTHON_DOES_NOT_EXIST
goto :DOES_GIT_EXIST
 
:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system. Please install Python 3+ from https://www.python.org/downloads/windows/
goto :EOF
 
:DOES_GIT_EXIST
echo Checking for Git...
git --version 2>NUL
if errorlevel 1 goto :GIT_DOES_NOT_EXIST
goto :REQUIREMENTS_MET
 
:GIT_DOES_NOT_EXIST
echo Git is not installed on your system. Please install Git 2+ from https://git-scm.com/download/win
goto :EOF
 
:REQUIREMENTS_MET
echo Pre-requisites already installed.
python -m ensurepip --upgrade
python -m pip install virtualenv
virtualenv txpt_env
call txpt_env/Scripts/activate.bat
python -m pip install -r requirements.txt
python texture_prep_tool.pyw
call txpt_env/Scripts/deactivate.bat
goto :EOF