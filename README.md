# Morserino-32 Firmware Updater

This program is a stand-alone console utility application for updating the [Morserino-32](http://www.morserino.info/morserino-32.html) using a USB port on macOS or Windows (x64).

The [Morserino-32](http://www.morserino.info/morserino-32.html) is a multi-functional Morse code training and radio keyer electronics kit developed by Willi Kraml, OE1WKL.


## Instructions for normal use

Please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual).


## Instructions for full factory erase

To fully erase the Morserino-32, please follow the step-by-step instructions provided in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual) adding an optional erase parameter. 

macOS example:

```
./update_m32 /dev/tty.SLAB_USBtoUART 921600 morse_3_v3.0.ino.wifi_lora_32_V2.bin erase
```

Windows example:

```
update_m32.exe COM5 921600 morse_3_v3.0.ino.wifi_lora_32_V2.bin erase
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
