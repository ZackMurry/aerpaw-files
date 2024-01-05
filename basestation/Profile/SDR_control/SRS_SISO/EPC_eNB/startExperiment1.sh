#!/bin/bash

./cleanupEPC.sh
./startEPCandENB.sh $1 $2	
sleep 5
if [ $2 == "PING" ]
  then
  sleep 15
  ./startPingEPC.sh
elif [ $2 == "IPERF" ]
  then
  ./startIperfEPC.sh
fi
