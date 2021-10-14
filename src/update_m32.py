__version__ = "0.0.8-preview.4"

import argparse
import os
import sys

from morserino import Morserino
from soc_info import SocInfo


def show(text):
    text.append("")
    for s in text:
        print(s)


def show_error(app, error):

    s = str(error)

    msg = [
        "  Error: " + str(s),
        "",
        "For help, please run:",
        "",
        app + " --help",
        "",
    ]

    show(msg)


def show_banner(version):
    msg = ["", "Welcome to Morserino-32 USB Firmware Updater v" + version]
    show(msg)


def show_updating(starting_update, path, port, baud):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    msg = [
        starting_update,
        "  Port: " + port,
        "  Baud: " + baud,
        "  Firmware: " + filename + " (" + str(filesize) + " bytes)",
    ]
    show(msg)


def show_md5(md5):
    print("  MD5 Checksum: " + md5)


def show_verification_passed():
    msg = [
        "  Verification: Passed",
    ]
    show(msg)


def show_connected(socInfo: SocInfo):
    msg = [
        "  SOC: " + socInfo.soc,
        "  Features: " + socInfo.features,
        "  Crystal: " + socInfo.crystal,
        "  MAC: " + socInfo.mac,
        "  Flash size: " + socInfo.flash_size,
    ]
    show(msg)


def show_completion(percentage):
    msg = "\r  Complete: %3s %%" % (str(percentage))

    sys.stdout.write(msg)

    if percentage == 100:
        sys.stdout.write(os.linesep)
        sys.stdout.write(os.linesep)


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
        "-p", "--port", type=str, help="Specify the USB serial port name."
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
        help="Include to erase all content and settings to factory defaults.",
    )
    optional.add_argument(
        "-md5",
        "--md5",
        type=str,
        help="Include to verify firmware with the provided md5 checksum instead of known release file checksums.",
    )
    optional.add_argument(
        "-no-md5",
        "--no-md5",
        action="store_true",
        default=False,
        help="Include to skip md5 checksum verification of firmware file before updating.",
    )
    return parser


def main(app, port, baud, path, eraseFlash):

    starting_update = "Starting update"
    verifying_firmware = "Verifying firmware"
    connecting = "Connecting"
    erasing_flash = "Erasing flash"
    updating_firmware = "Updating firmware"
    setting_up_file_system = [
        "The Morserino-32 is now setting up the SPIFF file system.",
        "",
        "Please wait to disconnect the USB cable until the Morserino-32 reboots (about 60 seconds).",
    ]
    firmware_update_success = "Firmware was updated successfully."

    try:
        morserino = Morserino(port, baud, path)

        show_updating(starting_update, path, port, baud)

        if args.md5 is not None:
            morserino.update_md5_checksum_table_with_single_checksum(args.md5)

        if args.no_md5 is False:
            print(verifying_firmware)
            morserino.check_firmware_against_known_md5_checksums(
                path, show_md5, show_verification_passed
            )

        print(connecting)
        morserino.get_info(show_connected)

        if eraseFlash:
            print(erasing_flash)
            morserino.erase(show_completion)

        print(updating_firmware)
        morserino.update(show_completion)

        print(firmware_update_success)
        print()

        if eraseFlash:
            show(setting_up_file_system)

    except Exception as ex:
        show_error(app, ex)


if __name__ == "__main__":
    show_banner(__version__)
    app = sys.argv[0]
    parser = create_args_parser(__version__)
    args = parser.parse_args()

    if args.port is None or args.baud is None:
        show_error(app, "Missing required command line arguements.")
    else:
        main(app, args.port, args.baud, args.file, args.erase)
