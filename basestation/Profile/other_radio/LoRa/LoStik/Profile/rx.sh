#!/bin/bash

#create the folder for output files if doesn't exist already
mkdir -p output_files

#RECEIVE MODE PARAMETERS
config_file = config.conf
window = 0


# Detects and stores the active port number that has the LoStik
python3 preprocessing_AERPAW.py

# Configure the LoRa dongle with parameters given in config.conf, e.g., frequency band, spread factor etc.
python3 configure_AERPAW.py $config_file

# Initiate the receive mode for $window in min. (if $window == 0, receive window stays open)
screen -S RX -dm bash -c "python3 receiver_AERPAW.py $window"
