#!/bin/bash
./cleanupUE.sh
sleep 5
./startUE.sh $1
sleep 5
./startPingUE.sh
