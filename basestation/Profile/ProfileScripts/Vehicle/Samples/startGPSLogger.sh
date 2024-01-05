#!/bin/bash

# use vehicle type generic to skip the arming requirement
export VEHICLE_TYPE="${VEHICLE_TYPE:-generic}"

# GPS Logger sample application (this does not move the vehicle)

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL ./gpsLoggerHelper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"	    
