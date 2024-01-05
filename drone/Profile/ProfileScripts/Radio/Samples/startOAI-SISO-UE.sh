#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
screen -S radio -dm \
       bash -c "stdbuf -oL -eL ./startOAI_UE.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_log.txt"
