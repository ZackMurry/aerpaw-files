#!/bin/bash

# This script saves the current mission from the autopilot
# (SITL in development mode) as a mission plan file
# It only saves the waypoints (even if a geofence or rally points are 
# present in the autopilot
#
# It takes an optional argument as the output .plan file
#    - by default it saves it in ./PreplannedTrajectory/Missions/default.plan
#

AERPAW_REPO=${AERPAW_REPO:-/root/AERPAW-Dev}
SAVE_MISSION_DIR=$AERPAW_REPO"/OEO/vehicle_oeo"
SAVE_MISSION_SCRIPT=$SAVE_MISSION_DIR"/savePlan.py"

DEFAULT_MISSION=$AERPAW_REPO"/AHN/E-VM/Profile_software/vehicle_control/PreplannedTrajectory/Missions/default.plan"

MISSION_PLAN=${1:-$DEFAULT_MISSION}

cd $SAVE_MISSION_DIR
bash -c "python3 $SAVE_MISSION_SCRIPT --connect :14550 --output $MISSION_PLAN"

