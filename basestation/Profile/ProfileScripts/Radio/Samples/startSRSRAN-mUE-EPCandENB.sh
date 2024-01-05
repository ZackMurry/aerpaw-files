#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the EPC + ENB
screen -S radioEPC -dm \
       bash -c "stdbuf -oL -eL ./startEPC.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_epc_log.txt"

screen -S radioENB -dm \
       bash -c "stdbuf -oL -eL ./startENB.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_enb_log.txt"
