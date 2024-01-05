#!/bin/bash
mkfifo /root/Power

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S rxcalGRC -dm \
       bash -c "stdbuf -oL -eL ./startcalibrationRXGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_calibrationrxgrc_log.txt"

screen -S powercal -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_calib_log.txt"
