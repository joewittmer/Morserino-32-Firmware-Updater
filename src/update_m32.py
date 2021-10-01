__version__ = "0.0.7"

import argparse
import io
import os
import sys
import time
from contextlib import redirect_stdout

import esptool


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
    for s in text:
        print(s)
    print("")


def show_missing_required_args_error(app):
    msg = [
        "Error: Missing required command line arguements.",
        "",
        "For help, please run:",
        "",
        app + " --help",
        "",
    ]
    show(msg)


def show_baud_error(baud):
    msg = [
        "Error: Unable to use baud " + baud,
        "",
        "Please use 115200, 460800, or 921600.",
    ]
    show(msg)


def show_path_error(path):
    msg = [
        "Error: Unable to open file at " + path,
        "",
        "Please check file name and path.",
    ]
    show(msg)


def show_unexpected_error(ex):
    msg = [
        "Error: An unexpected error occured " + ex,
        "",
        "Please ask for assistance.",
    ]
    show(msg)


def show_attempting_to_update(device, baud, path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)

    msg = [
        "Attempting to update firmware",
        "  Device: " + device,
        "  Baud: " + baud,
        "  Firmware: " + filename + " (" + str(filesize) + " bytes)",
        "",
        "Please wait...",
    ]
    show(msg)


def show_attempting_to_erase_flash(device, baud):
    msg = [
        "Attempting to erase flash",
        "  Device: " + device,
        "  Baud: " + baud,
        "",
        "Please wait...",
    ]
    show(msg)


def show_erase_success():
    msg = ["Chip was erased successfully."]
    show(msg)


def show_erase_failure(info):
    msg = [
        "Error: " + info,
        "",
        "Chip erase failed. Please ask for assistance.",
    ]
    show(msg)


def show_success():
    msg = ["Firmware was updated successfully."]
    show(msg)


def show_file_system_setup_warning():
    msg = [
        "Setting up SPIFFS file system.",
        "",
        "Please wait...",
    ]
    show(msg)


def show_flash_failure(info):
    msg = [
        "Error: " + info,
        "",
        "Firmware update failed. Please ask for assistance.",
    ]
    show(msg)


def get_baud_exists(baud):
    bauds = ["115200", "460800", "921600"]
    return baud in bauds


def get_path_exists(path):
    return os.path.exists(path)


def show_banner(version):
    msg = ["", "Welcome to Morserino-32 USB Firmware Updater v" + version]
    show(msg)


def erase_flash(device, baud):
    show_attempting_to_erase_flash(device, baud)
    result = True
    try:
        result, info = erase_morserino(device, baud)
        if not result:
            show_erase_failure(info)
            result = False
    except Exception as ex:
        show_unexpected_error(ex)
        result = False
    return result


def update_firmware(device, baud, path):
    show_attempting_to_update(device, baud, path)
    result = True
    try:
        result, info = update_morserino(device, baud, path)
        if not result:
            show_flash_failure(info)
            result = False

    except Exception as ex:
        show_unexpected_error(ex)
        result = False
    return result


def create_args_parser(app_version):
    parser = argparse.ArgumentParser(add_help=False)

    help = parser.add_argument_group("Help arguments")
    help.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    help.add_argument(
        "-v",
        "--version",
        action="version",
        version=app_version,
        help="Show this program's version number and exit.",
    )

    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "-p", "--port", type=str, help="Specify the USB serial port device name."
    )
    required.add_argument(
        "-f",
        "--file",
        type=str,
        help="Specify the path to the firmware .bin file to upload.",
    )

    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "-b",
        "--baud",
        type=str,
        default="921600",
        help="Include to set baud rate when updating. Valid options are 115200, 460800, or 921600. Default is 921600.",
    )
    optional.add_argument(
        "-e",
        "--erase",
        action="store_true",
        default=False,
        help="Include to erase the memory before updating.",
    )
    return parser


def parse_args(parser):
    args = parser.parse_args()
    arg_pairs = args._get_kwargs()
    result = not any(x is None for _, x in arg_pairs)
    return (result, args)


def main(device, baud, path, eraseFlash):

    carryOn = True

    if not get_baud_exists(baud):
        show_baud_error(baud)
        carryOn = False

    if not get_path_exists(path):
        show_path_error(path)
        carryOn = False

    if carryOn and eraseFlash:
        carryOn = erase_flash(device, baud)

    if carryOn:
        carryOn = update_firmware(device, baud, path)

    if carryOn:
        if eraseFlash:
            show_file_system_setup_warning()
            time.sleep(40)
        show_success()


if __name__ == "__main__":
    show_banner(__version__)
    app = sys.argv[0]
    parser = create_args_parser(__version__)
    result, args = parse_args(parser)

    if not result:
        show_missing_required_args_error(app)
    else:
        main(args.port, args.baud, args.file, args.erase)
