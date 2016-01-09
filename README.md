# SuperMileage RPi
The Raspberry Pi script for the SuperMileage car. Sends things such as speed and RPM to the HUD.

### About
- This is the raspberry pi script
- This sends data to the android app via TCP over ADB

### Requirements
- Python v3.0 or higher
- Debian based ditribution (really, something  apt-based)
  - systemd

### Install

Clone this repository and run `install.sh`:
```sh
git clone https://github.com/MSOE-Supermileage/datacollector.git
cd datacollector
./install.sh
```

### Usage

Once the systemd service file has been enabled (`systemctl enable
datacollector.service`), the program should automatically startup on boot. If
there are problems with systemd that need troubleshooting [here are some
commands](https://wiki.archlinux.org/index.php/Systemd#Using_units) to help.

