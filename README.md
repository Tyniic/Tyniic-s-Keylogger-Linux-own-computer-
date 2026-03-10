# Tyniic-s-Keylogger-Linux-own-computer-
A guide how to install a keylogger on linux ubuntu 24.04
sudo apt update
sudo apt install python3-evdev
Put the logger file in /home/user
wherever you see user in this guide you need to change it to your username.

sudo nano /etc/systemd/system/logger.service
Here you put : 
´´´
[Unit]
Description=Key Logger Service
After=network.target

[Service]
User=user
ExecStart=/usr/bin/python3 /home/user/logger.py
Restart=always

[Install]
WantedBy=multi-user.target

´´´
sudo systemctl start logger.service
sudo systemctl enable logger.service
sudo systemctl status logger.service
For checking if the service is online

Then go to //var/log/my_history.txt
