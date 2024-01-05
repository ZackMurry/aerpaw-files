#!/bin/bash
./cleanupUE.sh
sleep 5
./startUE.sh $1
sleep 5
if [ $2 == "PING" ]
  then
  ./startPingUE.sh
elif [ $2 == "IPERF" ]
  then
  ./startIperfUE.sh
fi
