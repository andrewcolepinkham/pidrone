# pidrone

# This is a repository

#
# Current Sensor Drivers include: BMP180 (Temperature, Pressure, Altitude)

# PiDrone

PiDrone is a Python repository created by @andrewpinkham for research at Colorado College. We use this driver code to control sensor modules via a Raspberry Pi 4 model B

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the bme280 and gps modules.

```bash
pip install bme280
pip install gps
```

The Raspberry Pi will also need to install the python-smbus, i2c-tools, python, python-smbus, gpsd, and gpsd-clients modules.

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
sudo apt-get install python
sudo apt-get install python-smbus
sudo apt-get install gpsd gpsd-clients
```

## Usage

To Inspect GPS data flow:

```bash
sudo systemctl start gpsd.socket
sudo cgps -s
```

To run the main data collection file:

```bash
cd main
python main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[ColoradoCollege](https://coloradocollege.edu/)
