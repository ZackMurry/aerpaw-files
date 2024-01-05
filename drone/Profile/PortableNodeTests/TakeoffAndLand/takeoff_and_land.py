#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage: python takeoff_and_land.py --connect <*connection_string>
This script connects to the drone and waits until armed. When armed it will takeoff
to 3m altitude, wait for 5 seconds, and then land.
"""

from __future__ import print_function

import time
from dronekit import connect, VehicleMode

# Desired altitude (in meters) to takeoff to
TARGET_ALTITUDE = 3
# Portion of TARGET_ALTITUDE at which we will break from takeoff loop
ALTITUDE_REACH_THRESHOLD = 0.95
# Seconds to stay at altitude
LOITER_TIME = 5

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

# Wait for pilot before proceeding
print('Waiting for safety pilot to arm...')

# Wait until safety pilot arms drone
while not vehicle.armed:
    time.sleep(1)

vehicle.mode = VehicleMode("GUIDED")
# Takeoff to short altitude
print("Taking off!")
vehicle.simple_takeoff(TARGET_ALTITUDE)  # Take off to target altitude

while True:
     # Break just below target altitude.
    if vehicle.location.global_relative_frame.alt >= TARGET_ALTITUDE * ALTITUDE_REACH_THRESHOLD:
        break
    time.sleep(0.5)

# Stay at altitude for 5 seconds
time.sleep(LOITER_TIME)

# Land
vehicle.mode = VehicleMode("LAND")

# Stay connected to vehicle until landed and disarmed
while vehicle.armed:
    time.sleep(1)

# Set mode to STABILIZE upon landing so it is armable
vehicle.mode = VehicleMode("STABILIZE")

print("Done!")

# Close vehicle object before exiting script
vehicle.close()
