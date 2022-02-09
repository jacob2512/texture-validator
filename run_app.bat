@echo off

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system. Please install Python 3+ from https://www.python.org/downloads/windows/

:PYTHON_DOES_EXIST
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo %ver% detected...
python -m ensurepip --upgrade
python -m pip install virtualenv
virtualenv txpt_env
call txpt_env/Scripts/activate.bat
python -m pip install -r requirements.txt
python texture_prep_tool.pyw
call txpt_env/Scripts/deactivate.bat
goto :EOF