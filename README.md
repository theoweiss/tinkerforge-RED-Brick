# openHAB TinkerForge - RED Brick Weather Station

## Description
This project is meant to be used on a TinkerForge RED Brick.

The project contains a set of configuration files for openHAB and the TinkerForgeBinding.
The script bin/weatherstation.py adapts and installs the configuration files.
To achieve this weatherstation.py connects to the brickd, enumerates the devices and searches for
the uids of an Ambient Light, a Humidity, a Barometer and a LCD20x4 Bricklet and adapts the 
items configuration accordingly.

## Installation
* login as user tf
* switch to root: sudo su -
* Install openHAB and the TinkerForge Binding if not yet done
    * echo 'deb http://repository-openhab.forge.cloudbees.com/release/1.6.1/apt-repo/ /' > /etc/apt/sources.list.d/openhab.list
    * apt-get update
    * apt-get install openhab-runtime openhab-addon-binding-tinkerforge
* clone this repo: git clone https://github.com/theoweiss/tinkerforge-RED-Brick.git
* execute weatherstation.py: ./tinkerforge-RED-Brick/bin/weatherstation.py
* start openHAB if not yet running (the startup will need some *minutes* be patient!)
    * /etc/init.d/openhab start
* if openHAB is already running the configuration will be automatically reloaded, you do not need to restart openHAB!

    