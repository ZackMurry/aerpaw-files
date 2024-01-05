#!/bin/bash
#
# This script will start the rover search sample application
#

C_VM_ADDR="192.168.32.25"
SAFETY_CHECKER_PORT=14580

cd $PROFILE_DIR"/vehicle_control/RoverSearch"
$AERPAW_PYTHON -u -m aerpawlib \
    --vehicle $VEHICLE_TYPE \
    --script rover_search \
    --conn :14550 \
    --safety_checker_ip $C_VM_ADDR \
    --safety_checker_port $SAFETY_CHECKER_PORT
#    --fake_radio True \
#    --vehicle_config $AERPAW_REPO/"AHN/E-VM/Profile_software/vehicle_control/RoverSearch/Geofences/safety_checker_config_copter.yaml"




