# Morserino-32 Firmware Updater


This program is a stand-alone console utility application for updating the [Morserino-32](https://github.com//oe1wkl/Morserino-32) and the new **Morserino-32 Pocket (M32Pocket)** device using a USB port on macOS or Windows (x64).

The [Morserino-32](https://github.com//oe1wkl/Morserino-32) is a multi-functional Morse code training and radio keyer electronics kit developed by Willi Kraml, OE1WKL.

**New Device Support: Morserino-32 Pocket (M32Pocket)**

> **Note:** Support for the M32Pocket device is new! Please see below for details and watch for updates as more information becomes available.

The M32Pocket is a new variant of the Morserino-32 family. This firmware updater now supports both the original Morserino-32 and the M32Pocket. If you have an M32Pocket, please select it using the `-d M32Pocket` option as described below.

<!-- TODO: Add more details about the M32Pocket hardware, features, and differences from the original Morserino-32. -->


## Instructions for normal use

Please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual).

The release files for this firmware update utility program are available to download [here](https://github.com/joewittmer/Morserino-32-Firmware-Updater/releases).

## Command-line options (summary)


This updater exposes a small set of command-line options. **New in this release is support for selecting the M32Pocket device.**

- `-d`, `--device`: Select the target device type. Valid values are `M32` (original Morserino-32) or `M32Pocket` (Morserino-32 Pocket).

<!-- TODO: Add more information about device selection, compatibility, and troubleshooting for M32Pocket. -->

Example usage (macOS, show help):

```
./update_m32 -help
```
Example usage (macOS, target M32):

```
./update_m32 -d M32 -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin
```

Example usage (macOS, target M32Pocket / ESP32-S3):

```
./update_m32 -d M32Pocket -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin -d M32Pocket
```

<!-- TODO: Add more usage examples for Windows, troubleshooting, and common issues for M32Pocket. -->


## Instructions for full factory erase


To fully erase the Morserino-32 or M32Pocket, please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual), adding an optional erase parameter. 

<!-- TODO: Add specific notes about erasing the M32Pocket if any differences exist. -->

macOS example:

```
./update_m32 -d M32 -p /dev/tty.usbserial-0001 -f m32_v4.1.ino.wifi_lora_32_V2.bin -e
```

Windows example:

```
update_m32.exe -d M32 -p COM5 -f m32_v4.1.ino.wifi_lora_32_V2.bin -e
```



## For developers

<!-- TODO: Add developer notes for M32Pocket support, build/test instructions, and contributing guidelines. -->

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
- Create the virtual environment (macOS Apple Silicon)
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
