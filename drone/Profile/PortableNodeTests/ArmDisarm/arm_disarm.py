#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage: python arm_disarm.py --connect <*connection string>
This script connects to the drone, arms it, waits for a few (10) seconds, and
then disarms the vehicle.
"""

from __future__ import print_function

import time
import argparse

from dronekit import connect, VehicleMode

# option parsing to get connection string
parser = argparse.ArgumentParser(
        description="Tests arming and disarming the vehicle")
parser.add_argument("--connect", help="Vehicle connection target string")
args = parser.parse_args()

# acquire connection string
conn_string = args.connect

# if no string specified, use dronekit's SITL package for testing
if not conn_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    conn_string = sitl.connection_string()

# connect to vehicle
print("Connecting to vehicle on: ", conn_string)
vehicle = connect(conn_string, wait_ready=True)
print("Succesfully connected to vehicle")

# attempt to arm and set the vehicle's mode
vehicle.armed = True
while not vehicle.armed:
    time.sleep(1)
print("Vehicle armed")

vehicle.mode = VehicleMode("STABILIZE")

print(vehicle.gps_0)
print(vehicle.battery)

# wait a few seconds
time.sleep(10)

# disarm and close
vehicle.armed = False
while vehicle.armed:
    time.sleep(1)
print("Vehicle disarmed")

print("Done!")

vehicle.close()
