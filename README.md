# ⌨️ Tyniic's Keylogger (Linux/Ubuntu)

En enkel guide för att installera och köra en keylogger som en bakgrundstjänst på **Ubuntu 24.04**. 

> [!IMPORTANT]
> **Varning:** Detta verktyg är endast avsett för utbildningssyfte och personligt bruk på din egen dator. Logga aldrig någon annan utan deras uttryckliga tillstånd.

---

## 🛠 Installation

Börja med att uppdatera systemet och installera nödvändiga bibliotek:

```bash
sudo apt update
sudo apt install python3-evdev
