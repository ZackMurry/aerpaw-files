#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-drone}" # out of rover, drone, generic

# Rover search sample application

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL ./roverSearchHelper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"	    
