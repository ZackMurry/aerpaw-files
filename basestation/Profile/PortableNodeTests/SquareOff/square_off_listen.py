#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage: python square_off_listen.py --connect <*connection_string>
This script connects to the rover and waits until armed. It issues go to waypoint commands
so that the rover will travel in a square. The rover will wait at each corner for 5 seconds.
"""

from __future__ import print_function

import math
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Size of square in meters
SQUARE_SIZE = 10
# Flag used to determine if rover has reached waypoint
reached_waypoint = False

def get_location_metres(original_location, dNorth, dEast, altitude):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobalRelative(newlat, newlon, altitude)


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

# MISSION_ITEM_REACHED message listener
# When message is received, set reached_waypoint to True
@vehicle.on_message('MISSION_ITEM_REACHED')
def listener(self, name, message):
    global reached_waypoint
    reached_waypoint = True

print('Succesfully connected to vehicle')

# Wait for pilot before proceeding
print('Waiting for safety pilot to arm...')

# Wait until safety pilot arms drone
while not vehicle.armed:
    time.sleep(1)

vehicle.mode = VehicleMode("GUIDED")

# Go 10 meters north
currentLocation=vehicle.location.global_relative_frame
targetLocation=get_location_metres(currentLocation, SQUARE_SIZE, 0, currentLocation.alt)
vehicle.simple_goto(targetLocation)
while not reached_waypoint:
    time.sleep(1)
time.sleep(5)

# Go 10 meters west
reached_waypoint = False
currentLocation=vehicle.location.global_relative_frame
targetLocation=get_location_metres(currentLocation, 0, -SQUARE_SIZE, currentLocation.alt)
vehicle.simple_goto(targetLocation)
while not reached_waypoint:
    time.sleep(1)
time.sleep(5)

# Go 10 meters north
reached_waypoint = False
currentLocation=vehicle.location.global_relative_frame
targetLocation=get_location_metres(currentLocation, -SQUARE_SIZE, 0, currentLocation.alt)
vehicle.simple_goto(targetLocation)
while not reached_waypoint:
    time.sleep(1)
time.sleep(5)

# Go 10 meters north
reached_waypoint = False
currentLocation=vehicle.location.global_relative_frame
targetLocation=get_location_metres(currentLocation, 0, SQUARE_SIZE, currentLocation.alt)
vehicle.simple_goto(targetLocation)
while not reached_waypoint:
    time.sleep(1)
time.sleep(5)

vehicle.armed = False

print("Done!")

# Close vehicle object before exiting script
vehicle.close()
