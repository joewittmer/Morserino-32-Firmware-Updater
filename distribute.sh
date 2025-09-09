#!/usr/bin/env bash
set -euo pipefail

echo "Running flake8 lint..."
if command -v flake8 >/dev/null 2>&1; then
  flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
  flake8 src --count --max-complexity=10 --max-line-length=127 --statistics
else
  echo "flake8 not found; skipping lint." >&2
fi

echo "Building executable with PyInstaller..."
pyinstaller --clean -y --onefile \
	--collect-all esptool \
	--add-data "src/m32/*.bin:m32/" \
	--add-data "src/m32pocket/*.bin:m32pocket/" \
	src/update_m32.py