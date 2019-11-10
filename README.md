# Grill Probe Extender

Web server that runs on a Raspberry Pi Zero W and connects to an iGrill so that
temperatures can be monitored when your phone is not within Bluetooth range.

##Installation notes for headless Raspberry Pi Zero W

Obtain a copy of Rasbian Stretch Lite. Don't extract it.

https://www.raspberrypi.org/downloads/raspbian/

Write the image to an SD card with Etcher.

Configure the Pi to connect to a wireless network by adding a wpa_supplicant.conf to boot partition.

Configure the Pi to start ssh by adding empty ssh.txt to boot partion.

Connect to the Pi with ssh. It should advertise itself with Avahi as rasberrypi.local.

default user: pi

default pass: rasberry

Optionally install git (takes a long time).

sudo apt install git

Install pip.

sudo apt install -y pip-python

Clone the repo with git.

Install required Python packages.
sudo apt install -y libglib2.0-dev
sudo pip install -r requirements.txt

Configure service

sudo systemctl link /home/pi/igrill/grillserver.service
sudo systemctl start grillserver.service
sudo systemctl enable grillserver.service





