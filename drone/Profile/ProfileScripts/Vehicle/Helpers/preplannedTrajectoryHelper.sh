#!/bin/bash
#
# This script will start the preplanned trajectory sample application
#

if [ -z ${MISSION} ]; then
    echo "\$MISSION must be specified for preplanned trajectory"
    exit 1
fi

cd $PROFILE_DIR"/vehicle_control/aerpawlib/examples"
$AERPAW_PYTHON -u -m aerpawlib \
    --vehicle $VEHICLE_TYPE \
    --script preplanned_trajectory \
    --conn :14550 \
    --file $MISSION\
    --output $RESULTS_DIR/$LOG_PREFIX\_vehicleOut.txt


