#!/bin/bash

#create the folder for output files if doesn't exist already
mkdir -p output_files

# TRANSMISSION MODE PARAMETERS
config_file = config.conf
traffic_file = traffic.conf
period= 15
duration = 15


# Detects and stores the active port number that has the LoStik
python3 preprocessing_AERPAW.py

# Configure the LoRa dongle with parameters given in config.conf, e.g., frequency band, spread factor etc.
python3 configure_AERPAW.py $config_file

# Initiate the transmission. Transmits packets defined in $traffic_file. Each packet is transmitted with a period of $period in seconds. Total duration of the experiment is $duration in minutes.

screen -S TX -dm bash -c "python3 transmitter_AERPAW.py $traffic_file $period $duration"
