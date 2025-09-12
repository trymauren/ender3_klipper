# ROBIN Ender3 with Klipper tech stack (or something like that)
See `ssh_guide.md` for instructions on connecting to the 3d-printer.

## Printer firmware and host software

### [Klipper](https://github.com/Klipper3d/klipper) ([Docs](https://www.klipper3d.org))
Firmware for controlling 3d-printers.

### [Moonraker](https://github.com/Arksine/moonraker) ([Docs](https://moonraker.readthedocs.io/en/latest/))
"Moonraker is a Python 3 based web server that exposes APIs with which client
applications may use to interact with the 3D printing firmware Klipper.
Communication between the Klippy host and Moonraker is done over a Unix Domain
Socket. Tornado is used to provide Moonraker's server functionality."

### [Mainsail](https://github.com/mainsail-crew/mainsail) ([Docs](https://docs.mainsail.xyz/setup/getting-started))
Makes Klipper more accessible by adding a lightweight, responsive web user
interface, centred around an intuitive and consistent design philosophy.

### [KlipperScreen](https://github.com/KlipperScreen/KlipperScreen) ([Docs](https://klipperscreen.github.io/KlipperScreen/))
"KlipperScreen is a touchscreen GUI that interfaces with Klipper via Moonraker.
It allows you to switch between multiple printers and access them from a
single location. Notably, it doesn't need to run on the same host as your
printer; you can install it on another device and configure the IP address to
connect to the printer."

### [kiauh](https://github.com/dw-0/kiauh?tab=readme-ov-file)
Provides a super nice software for installing all the software above. Follow
their instructions for installing both their software and all other software
required for running a Klipper based system on an RPi host.

## Hardware

#### Host (computer connected to the printer(s)):
- RPi 3b+ with 4gb ram. Could be any RPi (I think).

#### Printer:
- Ender3 V3 SE (note: old motherboard, see below for flash config)

#### Touchscreen
- Since the Ender3 screen cannot be used with the setup, a RPi 7" screen is used.

## Adjusting z-offset (has to be done after flashing/new setup)

Using the Mainsail console:
```bash
> G28 (will home all axes)
> PROBE_CALIBRATE (starts a calibration "wizard")
```
Adjust by pressing the +/- buttons according to the [paper test](https://www.klipper3d.org/Bed_Level.html#the-paper-test).
```bash
> ACCEPT
> SAVE_CONFIG
```
