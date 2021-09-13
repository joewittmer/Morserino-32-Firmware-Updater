__version__ = "0.0.6"

import sys
import esptool
from contextlib import redirect_stdout
import io
import os
import time


# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def get_resource_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    base = getattr(sys, "_MEIPASS", dir)
    return os.path.join(base, relative_path)


def get_update_command(port, rate, path):
    otadata = get_resource_path("bin/boot_app0.bin")
    bootloader = get_resource_path("bin/bootloader_qio_80m.bin")
    app = path
    partitionTable = get_resource_path("bin/morse_3_v3.0.ino.partitions.bin")

    return [
        "--chip",
        "esp32",
        "--port",
        port,
        "--baud",
        rate,
        "--before",
        "default_reset",
        "--after",
        "hard_reset",
        "write_flash",
        "-z",
        "--flash_mode",
        "dio",
        "--flash_freq",
        "80m",
        "0xe000",
        otadata,
        "0x1000",
        bootloader,
        "0x10000",
        app,
        "0x8000",
        partitionTable,
    ]


def update_morserino(port, rate, path):
    f = io.StringIO()
    with redirect_stdout(f):
        command = get_update_command(port, rate, path)
        esptool.main(command)
    s = f.getvalue().rstrip()
    writeConfirmation = "Hash of data verified."
    return s.count(writeConfirmation) == 4, s


def get_erase_command(port, rate):
    return [
        "--chip",
        "esp32",
        "--port",
        port,
        "--baud",
        rate,
        "--before",
        "default_reset",
        "--after",
        "hard_reset",
        "erase_flash",
    ]


def erase_morserino(port, rate):
    f = io.StringIO()
    with redirect_stdout(f):
        command = get_erase_command(port, rate)
        esptool.main(command)
    s = f.getvalue().rstrip()
    writeConfirmation = "Chip erase completed successfully"
    return s.count(writeConfirmation) == 1, s


def show(text):
    [print(i) for i in text]
    print("")


def show_general_error(app):
    filename = os.path.basename(app)
    msg = [
        " Error...",
        "",
        " Please try again with the following command line options: ",
        "  " + filename + " {serial_port} {rate} {file_path} erase",
        "",
        " Where: {rate} is 115200, 460800, or 921600",
        "         erase is optional; clears entire flash memory",
    ]
    show(msg)


def show_rate_error(rate):
    msg = [
        "Error...",
        "Unable to use rate " + rate,
        "Please use 115200, 460800, or 921600",
    ]
    show(msg)


def show_path_error(path):
    msg = ["Error...", "Unable to open file path: " + path]
    show(msg)


def show_unexpected_error(ex):
    msg = [
        ex,
        "Error...",
        "An unexpected error occured. Please ask for assistance.",
    ]
    show(msg)


def show_attempting_to_update(port, rate, path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)

    msg = [
        "Attempting to update firmware",
        "  Port: " + port,
        "  Rate: " + rate,
        "  Firmware: " + filename + " (" + str(filesize) + " bytes)",
        "Please wait...",
    ]
    show(msg)


def show_attempting_to_erase_flash(port, rate):
    msg = [
        "Attempting to erase flash",
        "  Port: " + port,
        "  Rate: " + rate,
        "Please wait...",
    ]
    show(msg)


def show_erase_success():
    msg = ["Chip was erased successfully"]
    show(msg)


def show_erase_failure(info):
    msg = [
        info,
        "Error...",
        "Chip erase failed. Please ask for assistance.",
    ]
    show(msg)


def show_success():
    msg = ["Firmware was updated successfully", ""]
    show(msg)


def show_file_system_setup_warning():
    msg = ["Setting up SPIFFS file system", "Please wait...", ""]
    show(msg)


def show_failure(info):
    msg = [
        info,
        "Error...",
        "Firmware update failed. Please ask for assistance.",
    ]
    show(msg)


def get_rate_exists(rate):
    rates = ["115200", "460800", "921600"]
    return rate in rates


def get_path_exists(path):
    return os.path.exists(path)


def show_banner(version):
    msg = ["", "Welcome to Morserino-32 USB Firmware Updater v" + version]
    show(msg)


def main(port, rate, path, eraseFlash):
    show_banner(__version__)
    if get_rate_exists(rate):
        if get_path_exists(path):
            if eraseFlash:
                show_attempting_to_erase_flash(port, rate)
                try:
                    result, info = erase_morserino(port, rate)
                    if result:
                        show_erase_success()
                        show_attempting_to_update(port, rate, path)
                        try:
                            result, info = update_morserino(port, rate, path)
                            if result:
                                show_file_system_setup_warning()
                                time.sleep(40)
                                show_success()
                            else:
                                show_failure(info)
                        except Exception as ex:
                            show_unexpected_error(ex)
                    else:
                        show_erase_failure(info)
                except Exception as ex:
                    show_unexpected_error(ex)
            else:
                show_attempting_to_update(port, rate, path)
                try:
                    result, info = update_morserino(port, rate, path)
                    if result:
                        show_success()
                    else:
                        show_failure(info)
                except Exception as ex:
                    show_unexpected_error(ex)
        else:
            show_path_error(path)
    else:
        show_rate_error()


if __name__ == "__main__":
    app = sys.argv[0]
    if len(sys.argv) > 3:
        port = sys.argv[1]
        rate = sys.argv[2]
        path = sys.argv[3]
        if len(sys.argv) > 4:
            if sys.argv[4].lower() == "erase":
                eraseFlash = True
                main(port, rate, path, eraseFlash)
            else:
                show_general_error(app)
        else:
            eraseFlash = False
            main(port, rate, path, eraseFlash)
    else:
        show_general_error(app)
