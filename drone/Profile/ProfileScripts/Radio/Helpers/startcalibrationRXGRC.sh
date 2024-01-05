#!/bin/bash
GAIN_RX=30
FREQUENCY=3.5G
SAMP_RATE=10e6
SIZE=100
FILE="/root/Power"

if [ $LAUNCH_MODE == "TESTBED" ]
then
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
elif [ $LAUNCH_MODE == "EMULATION" ]
then
ARGS='type=zmq'
else
  echo "Specify correct mode"
fi

cd $PROFILE_DIR"/SDR_control/calibration"
python3 calibRX.py --freq $FREQUENCY --gainrx $GAIN_RX --args $ARGS --samp-rate $SAMP_RATE --N $SIZE --file $FILE
