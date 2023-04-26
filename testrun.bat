@echo off
set "VIRTUAL_ENV_DIR=D:\TEN\TEN-env"

call "%VIRTUAL_ENV_DIR%\Scripts\activate.bat"
python "%VIRTUAL_ENV_DIR%\..\TESTING.py"

pause
