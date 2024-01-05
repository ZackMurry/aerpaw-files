#!/bin/bash
GAIN_RX=30
FREQUENCY=3.32G

if [ $LAUNCH_MODE == "TESTBED" ]
then
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
elif [ $LAUNCH_MODE == "EMULATION" ]
then
#ARGS='type=zmq'
ARGS=NULL
else
  echo "Specify correct mode"
fi

cd $PROFILE_DIR"/SDR_control/Channel_Sounderv3"
python3 CSRX_noGUI.py --freq $FREQUENCY --gainrx $GAIN_RX --args $ARGS
