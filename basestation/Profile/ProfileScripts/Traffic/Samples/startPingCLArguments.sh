#!/bin/bash
#
# This script will start a ping test to the specified destination
#

DESTINATION_IP=${1-172.16.0.1}

while ((1)) ; do 
  echo "Looking for connection..."
  ping  -c 1 -W 1 $DESTINATION_IP >& /dev/null
  rv=$?;
  if (test $rv -eq 0); then
     echo "Got it"
     break;
  fi
  sleep 1;
done

# ping interval (in seconds)
PING_INTERVAL=0.2

screen -S ping -dm \
       bash -c "stdbuf -oL -eL ping $DESTINATION_IP -i $PING_INTERVAL\
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_ping_log.txt"
