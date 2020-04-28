import sys
import esptool
from contextlib import redirect_stdout
import io
import os

def update_morserino(port, path):
	f = io.StringIO()
	command = ['--port', port, '--baud', '921600', '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '0x10000', path]
	with redirect_stdout(f):
		esptool.main(command)
	s = f.getvalue().rstrip()
	suffix = "Hard resetting via RTS pin..."
	return s.endswith(suffix)

def main(port, path):
    if update_morserino(port, path):
        print("Firmware was updated successfully")
    else:
        print("Firmware update failed")
        
if __name__ == "__main__":
    if (len(sys.argv) > 2):
        port = sys.argv[1]
        path = sys.argv[2]
        pathExists = os.path.exists(path)
        if (pathExists):
            filename = os.path.basename(path)
            print()
            print("Attempting to update Morserino-32")
            print("  Port: " + port)
            print("  Firmware: " + filename)
            print("Please wait...")
            main(port, path)
        else:
            print()
            print("Error opening path: " + path);
    else:
        print()
        print(sys.argv[0] + "error...")
        print("Please try again with the following command line options: ")
        print("  " + sys.argv[0] + " {serial_port} " + "{file_path}")