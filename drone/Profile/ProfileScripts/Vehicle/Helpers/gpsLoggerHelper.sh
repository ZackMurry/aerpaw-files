#!/bin/bash
#
# This script will start a basic GPS logging script
# 
# Depending on the vehicle type, arming may or may not be required (use
# "generic" to avoid arming)
#

VEHICLE_TYPE="generic"      # this should always be run as a 'generic' vehicle
                            # (doesn't need to be armed, can't be told to move)

SAMPLE_RATE=1               # log sampling rate in Hz

cd $PROFILE_DIR"/vehicle_control/GPSLogger"
$AERPAW_PYTHON -u -m aerpawlib \
    --vehicle $VEHICLE_TYPE \
    --script gps_logger \
    --conn :14550 \
    --samplerate $SAMPLE_RATE \
    --output $RESULTS_DIR/$LOG_PREFIX\_vehicleOut.txt
