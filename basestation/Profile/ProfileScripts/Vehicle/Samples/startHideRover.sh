#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-rover}" # out of rover, drone, generic

# Hide rover sample application

# mission should be the aboslute path to a mission .plan file to run
export MISSION=$PROFILE_DIR"/vehicle_control/RoverSearch/MidpinesRoverSetup.plan"
export HIDE_GEOFENCE=$PROFILE_DIR"/vehicle_control/RoverSearch/AFAR_Rover.kml"

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL ./hideRoverHelper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"
