#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage: python land.py --connect <*connection_string>
This script connects to the drone and immediately changes mode to LAND.
"""

from __future__ import print_function

import math
import time
import sys
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

# Set up option parsing to get connection string and mission plan file
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string.")
args = parser.parse_args()

# aquire connection_string
connection_string = args.connect

# Exit if no connection string specified
if not connection_string:
    sys.exit('Please specify connection string')

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

print('Succesfully connected to vehicle')

vehicle.mode = VehicleMode("LAND")

# Stay connected to vehicle until landed and disarmed
while vehicle.armed:
    time.sleep(1)

print("Done!")

# Close vehicle object before exiting script
vehicle.close()
