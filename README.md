# Morserino-32 Firmware Updater
macOS and Windows console utility application for updating the Morserino-32 via virtual serial port.

Steps to use:
  1. Download the latest Morserino [firmware](https://github.com/oe1wkl/Morserino-32/tree/master/Software/binary)
  2. Download the latest [console utility](https://github.com/joewittmer/Morserino-32-Firmware-Updater/blob/master/release)
  3. Extract the console utility zip file to a temporary location
  4. Run update_m32 {port} {baud_rate} {file_path}

  macOS example:
  ./update_m32 /dev/tty.SLAB_USBtoUART 115200 morse_3_v2.4.ino.wifi_lora_32.bin

  Windows example:
  update_m32.exe COM5 115200 morse_3_v2.4.ino.wifi_lora_32.bin