# datacollector

This repository contins the various programs that are deployed to our Raspberry
Pi for the SuperMileage cars. Various data from sensors, such as RPM, speed,
engine temperature, and battery capacity, are retrieved from an Arduino and
sent to and Android device.

**`src/adb.py`** is responsible for collection the sensor from the Arduinos and
relaying that to the Android device over a socket connection established by
`adb forward`.

**`src/gpio-shutdown.py`** simply allows an easy way of safely shutting down
the Raspberry Pi by pressing a button connected via GPIO.

**`arduino/`** contains the Arduino sketch that is run by the Arduino to
collect the data from sensors.

systemd services are included that will automatically start the requisite
services when the Pi is turned on.


## Requirements

- Python v3.0 or higher
- Debian based distribution (really, something  apt-based)
  - systemd


## Install

Clone this repository and run `install.sh`:
```sh
git clone https://github.com/MSOE-Supermileage/datacollector.git
cd datacollector
./install.sh
```


## Usage

Once the systemd service file has been enabled (`systemctl enable
datacollector.service`), the program should automatically startup on boot. If
there are problems with systemd that need troubleshooting [here are some
commands](https://wiki.archlinux.org/index.php/Systemd#Using_units) to help.


## License

This work is published under the Eclipse Public License 1.0, see LICENSE for
more details.

