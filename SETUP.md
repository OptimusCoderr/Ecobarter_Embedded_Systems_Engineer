# Raspberry Pi Setup Guide

This guide will walk you through the initial setup of your Raspberry Pi, including updating the system and installing necessary packages.

## Step 1: Update the Package List

Before installing new packages, it’s essential to ensure that your system's package list is up-to-date.

Run the following command:

```bash
sudo apt update
```

## Step 2: Upgrade the Installed Packages
Upgrade all the installed packages to their latest versions by running:

```bash
sudo apt full-upgrade
```
Restart the system
## Step 3: Install Python3 and Pip
Install Python3 and pip using the following command:

```bash
sudo apt install python3-pip
```
## Step 4: Install Python Packages
To install necessary Python packages, run the following commands. These packages are required for your project and will be installed with the --break-system-packages flag.
Install ESC/POS for printing support:
```bash
pip3 install escpos --break-system-packages
```
Install Pygame for multimedia support:
```bash
pip3 install pygame --break-system-packages
```
Install Gunicorn for WSGI HTTP server:
```bash
pip install gunicorn --break-system-packages
```

Note: The --break-system-packages flag allows you to install packages that may conflict with system packages.

## Step 5: Grant USB Device Access
If your Linux user doesn't have access to the USB device (such as a printer), you need to create a udev rule to grant access.

Copy printer.py and printer.rules to the home directory of the pi if you do not want to create a new one

### 1. Create the udev rule:
Create a file named printer.rules in the home directory with the following contents
```bash
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5743", MODE="666"
```
This rule grants access to the printer with the specified idVendor and idProduct.

### 2. Copy the rule into the correct directory:

Use the following command to copy the printer.rules file to the /etc/udev/rules.d directory:
```bash
sudo cp printer.rules /etc/udev/rules.d
```

### 3. Reload udev rules:

To apply the changes, reload the udev rules and trigger the new configuration with the following command:
#### Create New sudo password
```bash
sudo passwd
```
Enter new password. Then enter as sudo with the password created by entering the command
```bash
su
```
Then reload the udev rules:
```bash
udevadm control --reload-rules && udevadm trigger
```
Exit super user by using the exit command
```bash
exit
```
Attempt to Run printer.py
After granting access, you can now attempt to run your Python script (printer.py)   
Note: make sure printer.py is in home directory.
## Step 6: Autostart the Application
To autostart the Ecobarter app via Chromium, you can set up an autostart file. Follow these steps:

Open a new terminal and navigate to the following directory:
 ```
/etc/XDG/XSESSION//LDXEpi/
 ```
Open the autostart file using the following command:
```
sudo nano autostart
```
After the line @xscreensaver -no-splash, copy and paste the script below:
```
@xset s noblank
@xset s off
@unclutter -idle 1 -root &
@gunicorn -b localhost:8000 -w 1 App:app &
@sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' '~/.config/chromium/Default/Preferences'
@sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' '~/.config/chromium/Default/Preferences'
@chromium-browser --kiosk --noerrdialogs --disable-infobars --autoplay-policy=no-user-gesture-required http://127.0.0.1:8000 & 
```
Save the file by pressing CTRL + S, then exit by pressing CTRL + X.

## 7 List of files abd folders to be included in the home directory
App.py, sound.py, ultra.py, ultrasonic.py, servo.py, printer.py, load2.py, metal.py hx711.py    
printer.rules
#### -Folders
templates,static


https://drive.google.com/drive/folders/1pgGNdR4mhVyt-DLBeFePlXtrcOD3daKc?usp=sharing

