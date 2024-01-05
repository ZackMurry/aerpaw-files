#!/bin/bash

RATE=1000000
FREQUENCY=3.5G
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
GAIN=30
#For MOD:
#2 -> BPSK
#4 -> QPSK
#16 -> 16QAM
MOD=4
#Duration is measured in seconds
duration=60
#CHEM_IP_ADDR='tcp://192.168.152.192:5001'
#CHEM_IP_ADDR="tcp://$AP_EXPENV_CHEMVM_XE:5001"
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
CHEM_IP_ADDR="tcp://$AP_EXPENV_CHEMVM_XE:$(( 5000 + $node_num))"

if [ $LAUNCH_MODE == "TESTBED" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/RX"
   if [ $MOD == 2 ] ; then
      python3 rx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 4 ] ; then
      python3 rx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 16 ] ; then
      python3 rx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   fi
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/RX"
   if [ $MOD == 2 ] ; then
      python3 rx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 4 ] ; then
      python3 rx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 16 ] ; then
      python3 rx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   fi
else
  echo "Specify correct mode"
fi
