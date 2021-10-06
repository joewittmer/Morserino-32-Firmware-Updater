__version__ = "0.0.8-preview.3"

import argparse
import io
import os
import sys
import threading
import time

import esptool


class SocInfo(object):
    soc = ""
    features = ""
    mac = ""
    crystal = ""

    def __init__(self):
        self.stdout = sys.stdout
        self.show_me = True

    def parse(self, s):

        if "Chip is " in s:
            self.soc = s.split("Chip is ")[1]

        elif "Features: " in s:
            self.features = s.split("Features: ")[1].split("MHz")[0] + "MHz"

        elif "Crystal is " in s:
            self.crystal = s.split("Crystal is ")[1]

        elif "MAC: " in s:
            self.mac = s.split("MAC: ")[1].upper()
            self.show()

    def show(self):
        if self.show_me:
            self.show_me = False
            msg = [
                "Connected",
                "  SOC: " + self.soc,
                "  Features: " + self.features,
                "  Crystal: " + self.crystal,
                "  MAC: " + self.mac,
                "",
            ]
            for m in msg:
                self.stdout.write(m)
                self.stdout.write(os.linesep)
                self.stdout.flush()


def percentage(part, whole):
    percentage = 100 * float(part) / float(whole)
    return str(int(percentage)) + " %"


def show_progress(t, file=sys.stdout, hault=lambda: False):
    start = time.time()
    end = time.time()

    while end - start < t:
        if hault():
            break
        p = percentage(end - start, t)
        m = "\r  Complete: %s" % (p)
        file.write(m)
        time.sleep(0.5)
        end = time.time()

    m = "\r  Complete: 100 %"
    file.write(m)
    file.write(os.linesep)
    file.write(os.linesep)


class StdoutFilter(object):
    def __init__(self, socInfo: SocInfo):
        self.stdout = sys.stdout
        self.io_str = io.StringIO()
        self.socInfo = socInfo
        self.read_flash_size = False
        self.flash_erase_complete = False
        self.read_percentage_complete = False

    def write(self, message):
        s = str(message)

        self.socInfo.parse(s)

        t = threading.Thread(
            target=show_progress,
            args=(20, self.stdout, lambda: self.flash_erase_complete),
        )

        if "Erasing flash" in s:
            self.show("Erasing flash")
            t.start()

        elif "Chip erase completed successfully" in s:
            self.flash_erase_complete = True
            time.sleep(1)

        if "Writing at 0x00010000" in s:
            self.show("Writing to flash")
            self.read_percentage_complete = True

        if self.read_percentage_complete:
            if "%" in s:
                p = s.split("(")[1].split(")")[0]
                self.stdout.write("\r  Complete: " + p)

                if p == "100 %":
                    self.read_percentage_complete = False
                    self.show()
                    self.show()

        self.io_str.write(message)

    def flush(self):
        pass

    def show(self, msg=""):
        self.stdout.write(msg)
        self.stdout.write(os.linesep)


socInfo = SocInfo()
stdoutFilter = StdoutFilter(socInfo)


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
    sys.stdout = stdoutFilter
    command = get_update_command(port, rate, path)

    try:
        esptool.main(command)
    except Exception as ex:
        raise ex
    finally:
        sys.stdout = stdoutFilter.stdout

    s = stdoutFilter.io_str.getvalue().rstrip()
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
    sys.stdout = stdoutFilter
    command = get_erase_command(port, rate)

    try:
        esptool.main(command)
    except Exception as ex:
        raise ex
    finally:
        sys.stdout = stdoutFilter.stdout

    s = stdoutFilter.io_str.getvalue().rstrip()
    writeConfirmation = "Chip erase completed successfully"
    return s.count(writeConfirmation) == 1, s


def show(text):
    text.append("")
    for s in text:
        print(s)


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
        "Error: An unexpected error occured " + str(ex),
        "",
        "Please ask for assistance.",
    ]
    show(msg)


def show_updating(port, baud, path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    msg = [
        "Starting update",
        "  Port: " + port,
        "  Baud: " + baud,
        "  Firmware: " + filename + " (" + str(filesize) + " bytes)",
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


def show_setting_up_file_system():

    print("Setting up SPIFFS file system")
    show_progress(40)


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


def erase_flash(port, baud):
    result = True
    try:
        result, info = erase_morserino(port, baud)
        if not result:
            show_erase_failure(info)
            result = False
    except Exception as ex:
        show_unexpected_error(ex)
        result = False
    return result


def update_firmware(port, baud, path):
    result = True
    try:
        result, info = update_morserino(port, baud, path)
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
    return parser


def parse_args(parser):
    args = parser.parse_args()
    arg_pairs = args._get_kwargs()
    result = not any(x is None for _, x in arg_pairs)
    return (result, args)


def main(port, baud, path, eraseFlash):

    carryOn = True

    if not get_baud_exists(baud):
        show_baud_error(baud)
        carryOn = False

    if not get_path_exists(path):
        show_path_error(path)
        carryOn = False

    if carryOn:
        show_updating(port, baud, path)

    if carryOn and eraseFlash:
        carryOn = erase_flash(port, baud)

    if carryOn:
        carryOn = update_firmware(port, baud, path)

    if carryOn:
        if eraseFlash:
            show_setting_up_file_system()
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
