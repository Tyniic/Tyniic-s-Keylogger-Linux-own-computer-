# ⌨️ Tyniic's Keylogger (Linux/Ubuntu)

En enkel guide för att installera och köra en keylogger som en bakgrundstjänst på **Ubuntu 24.04**. 

> [!IMPORTANT]
> **Varning:** Detta verktyg är endast avsett för utbildningssyfte och personligt bruk på din egen dator. Logga aldrig någon annan utan deras uttryckliga tillstånd.

---

## Installation

Börja med att uppdatera systemet och installera nödvändiga bibliotek:

```
sudo apt update
sudo apt install python3-evdev
```
---
Förberedelse
-
Plasera scriptet i /home/user där du lägger in det i din hem katalog

>Nu gör vi plats där loggen ska placeras (ändra user till din profil)

```
sudo mkdir -p /var/log/logger_service
sudo chown user:user /var/log/logger_service
sudo chmod 755 /var/log/logger_service
```
---
Nu gör vi systemtjänsten som ska gå i bakgrunden som drar igång scriptet och har igång det även vid omstart
```
sudo nano /etc/systemd/system/logger.service
```
```
[Unit]
Description=Key Logger Service
After=network.target

[Service]
User=NAMN
ExecStart=/usr/bin/python3 /home/NAMN/logger.py
Restart=always

[Install]
WantedBy=multi-user.target
```
---
Starta tjänsten så den är igång
```
sudo systemctl daemon-reload
sudo systemctl start logger.service
sudo systemctl enable logger.service
```
Efter det kollar vi status
```
sudo systemctl status logger.service
```
Dax för att kolla loggen 
```
tail -f /var/log/logger_service/my_history.txt
```



