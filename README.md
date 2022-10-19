
# CSF LABELER  

## INSTRUCTIONS FOR INSTALLING THE MODULE

1. OS SETUP 
* Using Rasperry Pi Imager flash an Ubuntu Image for Rasperry 64-bit on the SD Card
* Install the Ubuntu OS by inserting the SD card on the Rasperry and follow the instructions
* Set the username to be `cobuild`
* Make sure to select LOGIN AUTOMATICALLY option when setting the OS user
* Setup the Wifi access on the Rasperry Pi
* Turn off Bluetooth
* In the Power Settings, set the screen to never turn off
* On the Software Updates, disable the updates entirely, this prevents the UPDATE YOUR SYSTEM dialog that blocks the screen whe you have updates to install

2. Clone the repo from `https://github.com/cobuildlab/csf-labeler.git` into `/home/cobuild`
3. Run the `setup.sh` for:
  - Install OS dependencies
  - Install Python3 dependencies
  - Install Kivy
  - Create USB permissions
  - Set the SupervisorCTL to start the app automatically

4.  Set up the Zebra printers on the CUPS configuration
  - Go to http://localhost:631/admin
  - Add the Zebra Printer. CUPS will recognize the Zebra printer for you
  - On the model, choose ZPL model
  - On the label size, choose 2.25x1.25"

5. Reboot, to test that everything is working

## HOW TOs

1. Installing a new Scanner Device:
- Add a new entry in the variable BARCODE_CONFIG in the `config.py` file. This is python code, so make sure is a valid entry
- Use the `src` property, leave the `device` as it is in the others

example:

```python

    ,{
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2208CM221A4N1061-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    }
```

## TROUBLESHOOTING

- Screen in NO SIGNAL: There are cases where the power adapter with clicker doesn't provide enough energy to turn 
the screen to be detected

- Network Disable: This probably means that you are missing the Wifi connection 