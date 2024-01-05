#!/bin/bash
mkfifo /root/Power
mkfifo /root/Quality

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S rxGRC -dm \
       bash -c "stdbuf -oL -eL ./startchannelsounderRXGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_channelsounderrxgrc_log.txt"

screen -S power -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_power_log.txt"

screen -S quality -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_quality_log.txt"
