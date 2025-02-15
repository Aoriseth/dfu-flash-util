**Archived, see [codeberg](https://codeberg.org/Aoriseth/dfu-flash-util)**

# dfu-flash-util
Python interface for quickly flashing bin files to STM32 devices, without requiring keyboard input

## How to run
use `sudo python /ui/interface.py` to run the program.

## How to flash
* Put your device into bootloader mode
* Click `Scan for devices`
* Check if it correctly recognizes the flash memory of the STM controller
* Click `Select bin file`
* Click `Flash device firmware`
* Wait until the flashing process finishes
