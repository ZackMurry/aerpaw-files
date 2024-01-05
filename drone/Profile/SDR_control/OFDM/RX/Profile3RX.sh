#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
screen -S radio -dm \
       bash -c "./startRX.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_log.txt"
