#!/bin/bash
#
# This script will start a ping to the specified destination
#

# Ping time interval (in seconds)
PING_PERIOD="${PING_PERIOD:-0.2}"  # seconds

# How many to send (unset $count to make it unlimited)
PING_COUNT=200

while ((1)) ; do 
  echo "Looking for connection..."
  ping $2 -c 1 -W 1 -I $1 >& /dev/null
  rv=$?;
  if (test $rv -eq 0); then
     echo "Got it"
     break;
  fi
  sleep 1;
done

if [ -z ${PING_COUNT} ]; then
    ping -i $PING_PERIOD $PING_DESTINATION
else
    ping -i $PING_PERIOD -c $PING_COUNT $2
fi
