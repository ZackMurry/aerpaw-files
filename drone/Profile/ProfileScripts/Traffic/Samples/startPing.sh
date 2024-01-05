#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Traffic/Helpers"
screen -S traffic -dm \
       bash -c "stdbuf -oL -eL ./pingHelper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_traffic_log.txt"
