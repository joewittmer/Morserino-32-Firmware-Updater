# Morserino-32 Firmware Updater

This program is a stand-alone console utility application for updating the [Morserino-32](http://www.morserino.info/morserino-32.html) using a USB port on macOS or Windows (x64).

The [Morserino-32](http://www.morserino.info/morserino-32.html) is a multi-functional Morse code training and radio keyer electronics kit developed by Willi Kraml, OE1WKL.


# Instructions for normal use

Full step by step instructions can be found in Appendix 4 of the [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual).


# Instructions for full factory erase

To fully erase the Morserino-32 follow the Appendix 4 [Morserino-32 Manual](https://github.com/oe1wkl/Morserino-32/tree/master/Documentation/User%20Manual) instructions adding an optional erase parameter to the end. 

macOS example:

```
./update_m32 /dev/tty.SLAB_USBtoUART 115200 morse_3_v2.4.ino.wifi_lora_32.bin erase
```

Windows example:

```
update_m32.exe COM5 115200 morse_3_v2.4.ino.wifi_lora_32.bin
```


# Acknowledgements

Special thanks to [Matthias Jordan](https://github.com/matthiasjordan/Morserino-32) for his assistance with the esptool Python scripts. His original post to the group can be viewed [here](https://morserino.groups.io/g/main/message/1044?p=,,,20,0,0,0::relevance,,Matthias,20,2,0,72596503).
