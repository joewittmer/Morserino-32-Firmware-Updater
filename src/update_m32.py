import sys
import esptool
from contextlib import redirect_stdout
import io
import os

def update_morserino(port, rate, path):
	f = io.StringIO()
	command = ['--port', port, '--baud', rate, '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '0x10000', path]
	with redirect_stdout(f):
		esptool.main(command)
	s = f.getvalue().rstrip()
	suffix = "Hard resetting via RTS pin..."
	return s.endswith(suffix)

def main(port, rate, path):
    if update_morserino(port, rate, path):
        print("Firmware was updated successfully")
    else:
        print("Firmware update failed")
        
if __name__ == "__main__":
    if (len(sys.argv) > 3):
        port = sys.argv[1]
        rate = sys.argv[2]
        path = sys.argv[3]
        pathExists = os.path.exists(path)
        if (pathExists):
            filename = os.path.basename(path)
            print()
            print("Attempting to update Morserino-32")
            print("  Port: " + port)
            print("  Rate: " + rate)
            print("  Firmware: " + filename)
            print("Please wait...")
            main(port, rate, path)
        else:
            print()
            print("Error opening path: " + path);
    else:
        print()
        print(sys.argv[0] + "error...")
        print("Please try again with the following command line options: ")
        print("  " + sys.argv[0] + " {serial_port}" + " {rate}" + " {file_path}")