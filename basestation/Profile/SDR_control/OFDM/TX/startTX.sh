#!/bin/bash
# MODE is either IQ_EMULATION, or IQ_DIRECT, or TESTBED                                            
MODE=$1
#To select a specific device
#ARGS="serial=31E74A9"

if [ $MODE == "TESTBED" ]
then
   mode='uhd'
   python3 tx_ofdm.py --source uhd $2 $3 $4 $5 $6 $7 | ts '[%Y-%m-%d %H:%M:%.S]' > tx_ofdm.log
elif [ $MODE == "EMULATION" ]
then
   mode='zmq'
   python3 tx_ofdm.py --source zmq $2 $3 $4 $5 $6 $7 | ts '[%Y-%m-%d %H:%M:%.S]' > tx_ofdm.log
else
  echo "Specify correct mode"
fi
