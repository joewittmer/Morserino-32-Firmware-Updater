__version__ = '0.0.6'

import sys
import esptool
from contextlib import redirect_stdout
import io
import os
import time

# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resourcePath(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def getUpdateCommand(port, rate, path):
    otadata = resourcePath('bin/boot_app0.bin')
    bootloader = resourcePath('bin/bootloader_qio_80m.bin')
    app = path
    partitionTable = resourcePath('bin/morse_3_v3.0.ino.partitions.bin')

    return [
        '--chip', 'esp32',
        '--port', port,
        '--baud', rate,
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '80m',
        '0xe000', otadata,
        '0x1000', bootloader,
        '0x10000', app,
        '0x8000', partitionTable ]

def updateMorserino(port, rate, path):
    f = io.StringIO()
    with redirect_stdout(f):
        command = getUpdateCommand(port, rate, path)
        esptool.main(command)
    s = f.getvalue().rstrip()
    writeConfirmation = 'Hash of data verified.'
    return s.count(writeConfirmation) == 4, s
    
def getEraseCommand(port, rate):
    return [
        '--chip', 'esp32',
        '--port', port,
        '--baud', rate,
        '--before', 'default_reset',
        '--after', 'hard_reset',
        'erase_flash' ]

def eraseMorserino(port, rate):
    f = io.StringIO()
    with redirect_stdout(f):
        command = getEraseCommand(port, rate)
        esptool.main(command)
    s = f.getvalue().rstrip()
    writeConfirmation = 'Chip erase completed successfully'
    return s.count(writeConfirmation) == 1, s

def showGeneralError(app):
    print('Error...')
    print('Please try again with the following command line options: ')
    print('  ' + app + ' {serial_port} {rate} {file_path} erase')
    print('Where: {rate} is 115200, 460800, or 921600')
    print('       erase is optional; clears entire flash memory')
    print()

def showRateError(rate):
    print('Error...')
    print('Unable to use rate ' + rate)
    print('Please use 115200, 460800, or 921600')
    print()

def showPathError(path):
    print('Error...')
    print('Unable to open file path: ' + path)
    print()

def showUnexpectedError():
    print('Error...')
    print('An unexpected error occured. Please ask for assistance.')
    print()

def showAttemptingToUpdate(port, rate, path):
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    print('Attempting to update firmware')
    print('  Port: ' + port)
    print('  Rate: ' + rate)
    print('  Firmware: ' + filename + ' (' + str(filesize) + ' bytes)')
    print('Please wait...')
    print()
    
def showAttemptingToEraseFlash(port, rate):
    filename = os.path.basename(path)
    print('Attempting to erase flash')
    print('  Port: ' + port)
    print('  Rate: ' + rate)
    print('Please wait...')
    print()
    
def showEraseSuccess():
    print('Chip was erased successfully')
    print()

def showEraseFailure(info):
    print(info)
    print()
    print('Error...')
    print('Chip erase failed. Please ask for assistance providing the console output.')
    print()

def showSuccess():
    print('Firmware was updated successfully')
    print()
    
def showFileSystemSetupWarning():
    print('Setting up SPIFFS file system')
    print('Please wait...')
    time.sleep(40)
    print()

def showFailure(info):
    print()
    print(info)
    print()
    print('Error...')
    print('Firmware update failed. Please ask for assistance providing the console output.')
    print()

def getRateExists(rate):
    rates = ['115200', '460800', '921600']
    return rate in rates

def getPathExists(path):
    return os.path.exists(path)

def showBanner(version):
    print()
    print('Welcome to Morserino-32 USB Firmware Updater v' + version)
    print()

def main(port, rate, path, eraseFlash):
    showBanner(__version__)
    if getRateExists(rate):
        if getPathExists(path):
            if eraseFlash:
                showAttemptingToEraseFlash(port, rate)
                try:
                    result, info = eraseMorserino(port, rate)
                    if result:
                        showEraseSuccess()
                        showAttemptingToUpdate(port, rate, path)
                        try:
                            result, info = updateMorserino(port, rate, path)
                            if result:
                                showFileSystemSetupWarning()
                                showSuccess()
                            else:
                                showFailure(info)
                        except:
                            showUnexpectedError()
                    else:
                        showEraseFailure(info);
                except:
                    showUnexpectedError()
            else:
                showAttemptingToUpdate(port, rate, path)
                try:
                    result, info = updateMorserino(port, rate, path)
                    if result:
                        showSuccess()
                    else:
                        showFailure(info)
                except:
                    showUnexpectedError()
        else:
            showPathError(path)
    else:
        showRateError()

if __name__ == '__main__':
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
               showGeneralError(app)
        else:
            eraseFlash = False
            main(port, rate, path, eraseFlash) 
    else:
        showGeneralError(app)
