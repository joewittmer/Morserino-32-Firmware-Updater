import os
import sys

import esptool

from custom_exception import CustomException
from erase_firmware_message_parser import EraseFirmwareMessageParser
from get_resource_path import get_resource_path
from image_info_validation_parser import ImageInfoValidationParser
from soc_info import SocInfo
from soc_info_message_parser import SocInfoMessageParser
from stdout_parser import StdoutParser
from update_firmware_message_parser import UpdateFirmwareMessageParser


class Morserino(object):
    def __init__(self, port, baud, path, model="M32", flash_mode=None, flash_freq=None):

        model_key = (model or "M32").lower()
        if "pocket" in model_key or "s3" in model_key:
            self.model = "M32Pocket"
            self.chip = "esp32s3"
        else:
            self.model = "M32"
            self.chip = "esp32"

    self.update_command = self.__get_update_command(port, baud, path, flash_mode, flash_freq)
        self.erase_command = self.__get_erase_command(port, baud)
        self.info_command = self.__get_info_command(port, baud)
        self.image_info_command = self.__get_image_info_command(port, baud, path)

    def __get_update_command(self, port, baud, path, flash_mode_override=None, flash_freq_override=None):
        if self.model == "M32":
            res_folder = "m32"
            otadata = get_resource_path(res_folder + "/boot_app0.bin")
            bootloader = get_resource_path(res_folder + "/bootloader_qio_80m.bin")
            partitionTable = get_resource_path(res_folder + "/morse_3_v3.0.ino.partitions.bin")
        else:
            res_folder = "m32pocket"
            otadata = get_resource_path(res_folder + "/boot_app0.bin")
            bootloader = get_resource_path(res_folder + "/bootloader.bin")
            partitionTable = get_resource_path(res_folder + "/partitions.bin")

        app = path
        if self.model == "M32":
            otadata_offset = "0xe000"
            bootloader_offset = "0x1000"
            app_offset = "0x10000"
            partition_offset = "0x8000"
            flash_mode = "dio"
            flash_freq = "80m"
        else:
            otadata_offset = "0xe000"
            bootloader_offset = "0x0"
            app_offset = "0x10000"
            partition_offset = "0x8000"
            flash_mode = "qio"
            flash_freq = "80m"

        # Override with user-supplied values if provided
        if flash_mode_override:
            flash_mode = flash_mode_override
        if flash_freq_override:
            flash_freq = flash_freq_override

        return [
            "--chip",
            self.chip,
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
            flash_mode,
            "--flash_freq",
            flash_freq,
            otadata_offset,
            otadata,
            bootloader_offset,
            bootloader,
            app_offset,
            app,
            partition_offset,
            partitionTable,
        ]

    def __get_erase_command(self, port, baud):
        return [
            "--chip",
            self.chip,
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
            self.chip,
            "--port",
            port,
            "--baud",
            baud,
            "flash_id",
        ]

    def __get_image_info_command(self, port, baud, path):
        return [
            "--chip",
            self.chip,
            "--port",
            port,
            "--baud",
            baud,
            "image_info",
            path,
        ]

    def validate_baud(self, baud, callback):
        bauds = ["115200", "460800", "921600"]
        if baud not in bauds:
            raise CustomException(
                "Invalid baud rate.%s%sPlease use a baud rate: 115200, 460800, or 921600."
                % (os.linesep, os.linesep)
            )
        callback()

    def validate_firmware(self, path, callback):

        if not os.path.exists(path):
            raise CustomException(
                "Unable to open the file at %s%s%sPlease check the firmware file location and try again."
                % (path, os.linesep, os.linesep)
            )

        imageInfoValidationParser = ImageInfoValidationParser()
        save_stdout = sys.stdout
        sys.stdout = StdoutParser(imageInfoValidationParser.parse)

        try:
            esptool.main(self.image_info_command)

        except Exception as ex:
            raise ex
        finally:
            sys.stdout = save_stdout

        if imageInfoValidationParser.result:
            callback()
        else:
            raise CustomException(
                "Unable to verify the firmware file at %s%s%sPlease download the firmware file again and retry."
                % (path, os.linesep, os.linesep)
            )

    def update_md5_checksum_table_with_single_checksum(self, checksum):
        self.md5_checksum_table.append(str(checksum))

    def check_firmware_against_known_md5_checksums(
        self, path, show_md5, show_verification_passed
    ):
        return self.__validate_md5_checksum(path, show_md5, show_verification_passed)

    def get_info(self, callback=lambda: SocInfo()):
        def bad_port_exception():
            raise CustomException(
                "Error connecting to morserino.%s%sPlease check the port is correct."
                % (os.linesep, os.linesep)
            )

        socInfo = SocInfo()
        socInfoMessageParser = SocInfoMessageParser(socInfo)
        save_stdout = sys.stdout
        sys.stdout = StdoutParser(socInfoMessageParser.parse)

        try:
            esptool.main(self.info_command)

        except Exception:
            raise bad_port_exception()
        finally:
            sys.stdout = save_stdout

        if socInfoMessageParser.result:
            callback(socInfo)
        else:
            raise bad_port_exception()

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
