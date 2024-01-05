#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
screen -S radio -dm \
       bash -c "stdbuf -oL -eL ./startOFDMRX.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_log.txt"

screen -S tsFile -dm \
       bash -c "tail -f /root/Results/out.txt \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_ts_out.txt"
