pyinstaller --clean -y --onefile \
		--add-data "src/m32/*.bin:m32/" \
		--add-data "src/m32pocket/*.bin:m32pocket/" \
	src/update_m32.py