# Morserino-32 Firmware Updater

This program is a stand-alone console utility application for updating the [Morserino-32](https://github.com//oe1wkl/Morserino-32) using a USB port on macOS or Windows (x64).

The [Morserino-32](https://github.com//oe1wkl/Morserino-32) is a multi-functional Morse code training and radio keyer electronics kit developed by Willi Kraml, OE1WKL.


## Instructions for normal use

Please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual).

The release files for this firmware update utility program are available to download [here](https://github.com/joewittmer/Morserino-32-Firmware-Updater/releases).

## Command-line options (summary)

This updater exposes a small set of command-line options. Of particular note is the new device selector:

- -d, --device: Select the target device type. Valid values are `M32` or `M32Pocket`. Default is `M32`.

- M32 -> uses the ESP32 chip string for esptool (`--chip esp32`).
- M32Pocket -> uses the ESP32-S3 chip string for esptool (`--chip esp32s3`).

Example (macOS, default device M32):

```
./update_m32 -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin
```

Example (macOS, target M32Pocket / ESP32-S3):

```
./update_m32 -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin -d M32Pocket
```


## Instructions for full factory erase

To fully erase the Morserino-32, please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual) adding an optional erase parameter. 

macOS example:

```
./update_m32 -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin -e
```

Windows example:

```
update_m32.exe -p COM5 -f m32_v4.1.ino.wifi_lora_32_V2.bin -e
```


## For developers

### macOS (Intel) steps to build:

- Clone this repository
- Install [Homebrew](https://brew.sh)
- Install Miniforge3
  ```commandline
  brew install miniforge
  ```
- Create the virtual environment (macOS Intel)
  ```commandline
  conda env create --file environment.yml
  ```
- Create the virtual envionment (macOS Apple Silicone)
  ```commandline
   CONDA_SUBDIR=osx-64 conda env create --file environment.yml

- Activate the virtual environment
  ```commandline
  conda activate update-m32
  ```
- Create distribution
  ```commandline
  sh distribute.sh
  ```

### Windows steps to build:

- Clone this repository
- Download and install [Miniforge3](https://github.com/conda-forge/miniforge)
- Open the Miniforge Prompt: Start -> Miniforge Prompt
- Create the virtual environment
  ```commandline
  conda env create
  ```
- Activate the virtual environment
  ```commandline
  conda activate update-m32
  ```
- Create distribution
  ```commandline
  distribute.bat
  ```

## Acknowledgements

Special thanks to [Matthias Jordan](https://github.com/matthiasjordan/Morserino-32) for his assistance with the esptool Python scripts. His original post to the Morserino-32 groups.io list can be viewed [here](https://morserino.groups.io/g/main/message/1044?p=,,,20,0,0,0::relevance,,Matthias,20,2,0,72596503).
