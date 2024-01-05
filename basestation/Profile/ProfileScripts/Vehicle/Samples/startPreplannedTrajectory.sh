#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-drone}" # out of rover, drone, generic

# Preplanned trajectory sample application

# mission should be the aboslute path to a mission .plan file to run
export MISSION=$PROFILE_DIR"/vehicle_control/PreplannedTrajectory/Missions/default.plan"

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL ./preplannedTrajectoryHelper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"	    
