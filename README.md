# Morserino-32 Firmware Updater

This program is a stand-alone console utility application for updating the [Morserino-32](https://github.com//oe1wkl/Morserino-32) using a USB port on macOS or Windows (x64).

The [Morserino-32](https://github.com//oe1wkl/Morserino-32) is a multi-functional Morse code training and radio keyer electronics kit developed by Willi Kraml, OE1WKL.


## Instructions for normal use

Please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual).

The release files for this firmware update utility program are available to download [here](https://github.com/joewittmer/Morserino-32-Firmware-Updater/releases).


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

macOS steps to build update_m32:

- Clone this repository
- Download and install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
- Create the virtual envionment
  ```
  conda env create
  ```
- Activate the virtual environment
  ```
  conda activate update-m32
  ```
- Create distribution
  ```
  sh distribute.sh
  ```

Windows steps to build update_m32.exe:

- Clone this repository
- Download and install [Miniconda3](https://docs.conda.io/en/latest/miniconda.html)
- Open the Anaconda Prompt: Start -> Anaconda3 (64-Bit) -> Anaconda Prompt (Miniconda3)
- Create the virtual envionment
  ```
  conda env create
  ```
- Activate the virtual environment
  ```
  conda activate update-m32
  ```
- Create distribution
  ```
  distribute.bat
  ```



## Acknowledgements

Special thanks to [Matthias Jordan](https://github.com/matthiasjordan/Morserino-32) for his assistance with the esptool Python scripts. His original post to the Morserino-32 groups.io list can be viewed [here](https://morserino.groups.io/g/main/message/1044?p=,,,20,0,0,0::relevance,,Matthias,20,2,0,72596503).
