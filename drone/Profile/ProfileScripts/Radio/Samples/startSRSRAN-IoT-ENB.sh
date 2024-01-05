#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the EPC + ENB
screen -S radioENB -dm \
       bash -c "stdbuf -oL -eL ./startIoTENB.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_enb_log.txt"
