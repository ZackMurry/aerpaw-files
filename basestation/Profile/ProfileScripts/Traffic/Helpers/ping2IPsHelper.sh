#!/bin/bash
#
# This script will start pings to two destinations 
#

# Ping time interval (in seconds)
PING_PERIOD="${PING_PERIOD:-0.2}"  # seconds

# How many to send (unset $count to make it unlimited)
# PING_COUNT=2000

# Destination IP address
PING_DESTINATION="${PING_DESTINATION:-172.16.0.2}"
PING_DESTINATION2="${PING_DESTINATION2:-172.16.0.3}"


while ((1)) ; do 
  echo "Looking for connection..."
  ping  -c 1 -W 1 $PING_DESTINATION >& /dev/null
  rv=$?;
  if (test $rv -eq 0); then
     echo "Got it"
     break;
  fi
  sleep 1;
done

while ((1)) ; do 
  echo "Looking for connection..."
  ping  -c 1 -W 1 $PING_DESTINATION2 >& /dev/null
  rv=$?;
  if (test $rv -eq 0); then
     echo "Got it"
     break;
  fi
  sleep 1;
done


if [ -z ${PING_COUNT} ]; then
    ping -i $PING_PERIOD $PING_DESTINATION &
    ping -i $PING_PERIOD $PING_DESTINATION2
else
    ping -i $PING_PERIOD -c $PING_COUNT $PING_DESTINATION &
    ping -i $PING_PERIOD -c $PING_COUNT $PING_DESTINATION2
fi
