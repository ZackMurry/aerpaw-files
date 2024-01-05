#!/bin/bash

screen -S monitor -dm \
       bash -c "stdbuf -oL -eL python3 -u \
       /root/AERPAW-Dev/AHN/C-VM/RF_monitoring/monitor_NCSU_loop.py \
        2>&1 | ts $TS_FORMAT \
       | tee /root/Results/$LOG_PREFIX\_spectrum_monitoring_log.txt"
