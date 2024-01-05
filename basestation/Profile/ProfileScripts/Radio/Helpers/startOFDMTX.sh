#!/bin/bash

RATE=1000000
FREQUENCY=3.5G
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
GAIN=40
#For MOD:
#2 -> BPSK
#4 -> QPSK
#16 -> 16QAM
MOD=4
#Duration is measured in seconds
duration=60
#OWN_IP_ADDR='tcp://192.168.152.66:5102'
#OWN_IP_ADDR='tcp://*:5102'
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
OWN_IP_ADDR="tcp://*:$(( 5100 + $node_num))"


if [ $LAUNCH_MODE == "TESTBED" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/TX"
   if [ $MOD == 2 ]
   then
      python3 tx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN --duration $duration
   elif [ $MOD == 4 ]
   then
      python3 tx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN --duration $duration
   elif [ $MOD == 16 ]
   then
      python3 tx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN --duration $duration
   fi
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/TX"
   if [ $MOD == 2 ]
   then
      python3 tx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN  --duration $duration
   elif [ $MOD == 4 ]
   then
      python3 tx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN  --duration $duration
   elif [ $MOD == 16 ]
   then
      python3 tx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --tx-gain $GAIN  --duration $duration
   fi
else
  echo "Specify correct mode"
fi
