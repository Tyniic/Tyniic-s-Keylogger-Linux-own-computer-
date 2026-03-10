# Tyniic-s-Keylogger-Linux-own-computer-
A guide how to install a keylogger on linux ubuntu 24.04
sudo apt update
sudo apt install python3-evdev
Put the logger file in /home/user
wherever you see user in this guide you need to change it to your username.
Now you need your keyboard event, mine was event.2 so i put in in the python file but you NEED to change it to wahtever you got.
find what event you have with cat /proc/bus/input/devices and look for keyboard.

sudo nano /etc/systemd/system/logger.service
Here you put : 
´´´
[Unit]
Description=Keyboard Logger
After=network.target

[Service]

Type=simple
ExecStart=/usr/bin/python3 /home/student/logger.py
Restart=always
# Logs get in /home/user/my_history.txt
WorkingDirectory=/home/user

[Install]
WantedBy=multi-user.target
´´´
sudo systemctl start logger.service
sudo systemctl enable logger.service
sudo systemctl status logger.service
For checking if the service is online

Then go to /home/user/my_history.txt
