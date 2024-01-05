#!/bin/bash
log_file="Ping_log_$(date +"%Y_%m_%d_%H\:%M\:%S").log"
bash -c "stdbuf -oL -eL ./pingHelper2.sh $1 $2 \
       | ts | tee log/$log_file.txt"
