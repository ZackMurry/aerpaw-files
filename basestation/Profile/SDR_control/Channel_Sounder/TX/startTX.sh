#!/bin/bash
# MODE is either IQ_EMULATION, or IQ_DIRECT, or TESTBED                                            
MODE=$1
GAIN=40
RATE=2M
FREQUENCY=3.5G
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
DIRECT_IP_ADDR='tcp://192.168.151.66:5001'
DIRECT_IP_ADDR='tcp://192.168.1.147:5001'
CHEM_IP_ADDR='tcp://192.168.151.192:5001'
IP_local='tcp://127.0.0.1:5001'

if [ $MODE == "TESTBED" ]
then
   mode='uhd'
   IP=NULL
elif [ $MODE == "IQ_EMULATION" ]
then
   mode='zmq'
   IP=CHEM_IP_ADDR
elif [ $MODE == "IQ_DIRECT" ]
then
   mode='zmq'
   IP=$DIRECT_IP_ADDR
else
  echo "Specify correct mode"
fi

screen -S sounderTX -dm bash -c "python3 sounder_TX.py -g $GAIN -r $RATE -f $FREQUENCY --arguments $ARGS  --mode $mode --ip $IP"
