#!/bin/bash
cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S txGRC -dm \
       bash -c "stdbuf -oL -eL ./startchannelsounderTXGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_channelsoundertxgrc_log.txt"
