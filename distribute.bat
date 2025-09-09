@echo off
setlocal enableextensions enabledelayedexpansion

echo Running flake8 lint...
where flake8 >nul 2>&1
if %errorlevel%==0 (
	flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics || exit /b 1
	flake8 src --count --max-complexity=10 --max-line-length=127 --statistics || exit /b 1
) else (
	echo flake8 not found; skipping lint. 1>&2
)

echo Building executable with PyInstaller...
pyinstaller --clean -y --onefile ^
    --collect-all esptool ^
	--add-data "src\m32\*.bin;m32" ^
	--add-data "src\m32pocket\*.bin;m32pocket" ^
	src\update_m32.py || exit /b 1

endlocal