import os
import sys

import esptool

from custom_exception import CustomException
from erase_firmware_message_parser import EraseFirmwareMessageParser
from generate_md5checksum import generate_md5checksum
from get_resource_path import get_resource_path
from soc_info import SocInfo
from soc_info_message_parser import SocInfoMessageParser
from stdout_parser import StdoutParser
from update_firmware_message_parser import UpdateFirmwareMessageParser


class Morserino(object):
    def __init__(self, port, baud, path):
        self.__validate_baud(baud)
        self.__validate_path(path)
        self.md5_checksum_table = self.__get_md5_checksum_table()
        self.update_command = self.__get_update_command(port, baud, path)
        self.erase_command = self.__get_erase_command(port, baud)
        self.info_command = self.__get_info_command(port, baud)

    def __get_update_command(self, port, baud, path):
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
            baud,
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

    def __get_erase_command(self, port, baud):
        return [
            "--chip",
            "esp32",
            "--port",
            port,
            "--baud",
            baud,
            "--before",
            "default_reset",
            "--after",
            "hard_reset",
            "erase_flash",
        ]

    def __get_info_command(self, port, baud):
        return [
            "--chip",
            "esp32",
            "--port",
            port,
            "--baud",
            baud,
            "flash_id",
        ]

    def __get_md5_checksum_table(self):
        return [
            "6eff362633be2b6a54071259ac0448ad",
            "23459824764033918dbba536e4f35ea5",
            "40e1b020227f8b1702586d3aa9c80ef6",
            "1a600a8da0cfbd29fe5f05fb9b6bcdd1",
            "0131a5a4b3025a10ad5854f38c7305ed",
            "fab777612ae7ecfa71e24f55b4292e58",
            "bd8cab3a4e08b5359294cc809f154a54",
            "0b95ee9ee4f3f6ab06f2c821b6cd65aa",
            "382284ca46b24c4a21999b9a8ac3ac07",
            "fcdab68b51c3296d75a6584cce026fe1",
            "5f7b4f57eb92675d6b10bc399f4ea360",
            "10550ca5451c31f3e43a952e63d40fac",
            "714a46bfc069f086e61db4883a6feb4a",
            "7984199a0022c877513221464ffb5100",
        ]

    def __validate_baud(self, baud):
        bauds = ["115200", "460800", "921600"]
        if baud not in bauds:
            raise CustomException(
                "Invalid baud rate.%s%sPlease use a baud rate: 115200, 460800, or 921600."
                % (os.linesep, os.linesep)
            )

    def __validate_path(self, path):
        if not os.path.exists(path):
            raise CustomException(
                "Unable to open file at %s%s%sPlease check firmware file location."
                % (path, os.linesep, os.linesep)
            )

    def __validate_md5_checksum(self, path, show_md5, show_verification_passed):
        md5 = generate_md5checksum(path)
        md5 = str(md5)
        show_md5(md5)
        if md5 not in self.md5_checksum_table:
            raise CustomException(
                "Verification of firmware failed.%s%sPlease check for file corruption."
                % (os.linesep, os.linesep)
            )
        else:
            show_verification_passed()

        return md5

    def update_md5_checksum_table_with_single_checksum(self, checksum):
        self.md5_checksum_table = [checksum]

    def check_firmware_against_known_md5_checksums(
        self, path, show_md5, show_verification_passed
    ):
        return self.__validate_md5_checksum(path, show_md5, show_verification_passed)

    def get_info(self, callback=lambda: SocInfo()):
        socInfo = SocInfo()
        socInfoMessageParser = SocInfoMessageParser(socInfo)
        save_stdout = sys.stdout
        sys.stdout = StdoutParser(socInfoMessageParser.parse)

        try:
            esptool.main(self.info_command)

        except Exception as ex:
            raise ex
        finally:
            sys.stdout = save_stdout

        if socInfoMessageParser.result:
            callback(socInfo)
        else:
            raise CustomException(
                "Error connecting to morserino.%s%s Please check the port is correct."
                % (os.linesep, os.linesep)
            )

    def erase(self, callback):
        stdout = sys.stdout
        eraseFirmwareParser = EraseFirmwareMessageParser(callback, stdout)
        process_stdout = StdoutParser(eraseFirmwareParser.parse)

        try:
            sys.stdout = process_stdout
            esptool.main(self.erase_command)

        except Exception as ex:
            raise ex

        finally:
            sys.stdout = stdout

        if not eraseFirmwareParser.result:
            raise CustomException(
                "Error erasing morserino.%s%sPlease ask for assistance"
                % (os.linesep, os.linesep)
            )

    def update(self, callback):
        stdout = sys.stdout
        updateFirmwareParser = UpdateFirmwareMessageParser(callback, sys.stdout)
        process_stdout = StdoutParser(updateFirmwareParser.parse)

        try:
            sys.stdout = process_stdout
            esptool.main(self.update_command)

        except Exception as ex:
            raise ex

        finally:
            sys.stdout = stdout

        if not updateFirmwareParser.result:
            raise CustomException(
                "Error updating morserino.%s%sPlease ask for assistance"
                % (os.linesep, os.linesep)
            )
