#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import asyncio
import yaml
import csv
import datetime
import time
import math


from argparse import ArgumentParser
from time import sleep
from typing import List
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal


#from aerpawlib.runner import StateMachine
#from aerpawlib.vehicle import Vehicle, Drone
#from aerpawlib.runner import state, background
#from aerpawlib.util import Coordinate, VectorNED

ALTITUDE_REACH_THRESHOLD = 0.95
WAYPOINT_LIMIT = 1


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def distanceToWaypoint(coordinates):
    """
    Returns distance between vehicle and specified coordinates
    """
    distance = get_distance_metres(vehicle.location.global_frame, coordinates)
    return distance




params_file = open("speed_test_params.yaml", "r")
params = yaml.load(params_file)

location_index = 0
lats = params["lats"]
longs = params["longs"]
targetAltitude = params["altitude"]

# Construct a list of coordinates based on the yaml params
#coords: List[Coordinate] = [0] * len(lats)
#for i in range(len(lats)):
#    coords[i] = Coordinate(lats[i], longs[i], altitude)

parser = ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
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

home = vehicle.home_location

locationA = LocationGlobal(lats[0], longs[0], home.alt+targetAltitude);
locationB = LocationGlobal(lats[1], longs[1], home.alt+targetAltitude);
locations = [locationA, locationB]

# Takeoff to target altitude
print("Taking off!")
vehicle.simple_takeoff(targetAltitude)

# Wait to get to altitude
while True:
    # Break just below target altitude.
    if vehicle.location.global_relative_frame.alt >= targetAltitude * ALTITUDE_REACH_THRESHOLD:
        break
    time.sleep(3)


currentLocation=vehicle.location.global_relative_frame
iteration = 0


while (True):  # A <---> B loop

    while (True): # Reading a valid speed loop
        speed_str = input("Input speed in m/s or type exit to rtl: ")
        try:
            speed = float(speed_str)
            # negative speed check
            if speed < 0:
                print("Speed must be greater than 0 m/s! Try again.")
                # too high speed check
            elif speed > 44.7:
                print("Speed cannot be greater than 44.7 m/s (100mph)! Try again.")
            else:
                break             # Input speed was valid
        except:   # float conversion failed
            if speed_str in ["exit", "rtl"]:
                speed = 0
                break

    if (speed == 0):
        break  # go home
    targetLocation=locations[iteration % 2]
    iteration+=1
    vehicle.simple_goto(targetLocation, groundspeed=speed)

    while (distanceToWaypoint(targetLocation) > WAYPOINT_LIMIT):
        vel = str(round(vehicle.groundspeed,2))
        print("Current speed: "+vel+ " m/s")
        time.sleep(1)

# done, we're going home
vehicle.mode = VehicleMode("RTL")

vehicle.close()
print("done!")
