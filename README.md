
INSTRUCTIONS FOR INSTALLING THE MODULE

1. OS SETUP 
* Using Rasperry Pi Imager flash an Ubuntu Image for Rasperry on the SD Card
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

4.  Set up the Zebra printers on the CUPS configuration
  - Go to http://localhost:631/admin
  - Add the Zebra Printer. CUPS will recognize the Zebra printer for you
  - On the model, choose ZPL model
  - On the label size, choose 2.25x1.25"

5. Copy the /etc/labeler.conf file in /etc/supervisor/conf.d/ folder
6.  Reboot, to test that everything is working 