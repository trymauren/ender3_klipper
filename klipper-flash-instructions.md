# Klipper Flashing Instructions for Robin Ender3 V3 SE

Assumes Klipper is installed on the host.

**On the RPi host**:
1. Navigate to the Klipper directory:
   ```bash
   cd ~/klipper/
   ```

2. Open the configuration menu:
   ```bash
   make menuconfig
   ```

3. Configure with the following settings:
   - **Note:** No "Extra low-level configuration" option
   - **Micro-controller Architecture:** STMicroelectronics STM32
   - **Processor model:** STM32F103
   - **Bootloader offset:** 28KiB bootloader
   - **Communication interface:** Serial (on USART1 PA10/PA9)

The Ender3 V3 SE used has an older motherboard and requires the above make settings.
Ignore other suggestions online. Note that other Ender3 printers at ROBIN may require
other settings, as they may have a different motherboard.

4. Clean the build directory:
   ```bash
   make clean
   ```

5. Build the firmware:
   ```bash
   make
   ```

6. The binary file will be located (at RPi host) at: `~/klipper/out/klipper.bin`

7. Copy the binary file from the Raspberry Pi to your computer:
   ```bash
   scp -r HOSTNAME:~/klipper/out/klipper.bin ~/Downloads/
   ```
*Where HOSTNAME should be replaced with whatever necessary in order to connect
to the host using ssh.*

8. Insert an SD card into your computer:
Not sure what the requirements of the card is.

9. Format the SD card to FAT32 with an allocation size of 4096 bytes:
   ```bash
   diskutil list
   diskutil unmountDisk /dev/diskX
   sudo newfs_msdos -F 32 -c 8 -v SDCARD /dev/diskX
   diskutil mountDisk /dev/diskX
   ```
   **Note:** These are instructions for MacOS. Instruction may not be valid
   for you computer.
   **Note:** Replace `/dev/diskX` with your actual SD card device identifier

10. Copy `klipper.bin` to the SD card

*The *.bin filename should be different from the previously used flash
filename to ensure the board recognizes it as a new firmware update.*

**LAST FLASH FILENAME:** `994.bin`

11. Flash the printer.
- Insert the SD-card in the printer.
- Turn the printer on.
- Turn the printer off after ~30 seconds (I think somewhere between 15-60s is ok).
- Remove SD-card and insert it in your computer to remove *.bin file.

12. The RPi host should now be able to connect to the printer using the USB-C port
on the ender printer. Klipper may need to be restarted for the printer to be
detected (either through web UI, KlipperScreen touchscreen or through ssh at host).

