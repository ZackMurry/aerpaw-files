#!/bin/bash

screen -S IQ -dm \
       bash -c "stdbuf -oL -eL python3 -u \
       /root/Profiles/SDR_control/LTE_IQ/get_IQ.py \
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_IQ_log.txt"
