#!/bin/bash
#
# This script will start the hide rover sample application
#

if [ -z ${MISSION} ]; then
    echo "\$MISSION must be specified for hide rover"
    exit 1
fi

if [ -z ${HIDE_GEOFENCE} ]; then
    echo "\$HIDE_GEOFENCE must be specified for hide rover"
    exit 1
fi

cd $PROFILE_DIR"/vehicle_control/aerpawlib/examples"
$AERPAW_PYTHON -u -m aerpawlib \
    --vehicle $VEHICLE_TYPE \
    --script hide_rover \
    --conn :14550 \
    --file $MISSION\
    --hide-fence $HIDE_GEOFENCE \
    --output $RESULTS_DIR/$LOG_PREFIX\_vehicleOut.txt \
    --skip-rtl
