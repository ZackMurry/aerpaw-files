#!/bin/bash
cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S txcalGRC -dm \
       bash -c "stdbuf -oL -eL ./startcalibrationTXGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_calibrationtxgrc_log.txt"
