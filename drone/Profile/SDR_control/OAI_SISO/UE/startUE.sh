#!/bin/bash

# MODE is either IQ_EMULATION, or PL_EMULATION, or TESTBED                                            
MODE=$1
ENB_IP_ADDR=192.168.151.65
CHEM_IP_ADDR=192.168.151.192
PORT_ARGS="tx_port=tcp://*:5001,rx_port=tcp://${ENB_IP_ADDR}:5101"
PORT_ARGS_IQ="tx_port=tcp://*:5102,rx_port=tcp://${CHEM_IP_ADDR}:5002"
ZMQ_ARGS="--rf.device_name=zmq --rf.device_args=\"${PORT_ARGS},id=ue,base_srate=23.04e6\""
ZMQ_ARGS_IQ="--rf.device_name=zmq --rf.device_args=\"${PORT_ARGS_IQ},id=ue,base_srate=23.04e6\""
TX_GAIN=70
RX_GAIN=40
EARFCN=2900


mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue 

if [ $MODE == "TESTBED" ]
then
  srsue --rf.tx_gain=$TX_GAIN --rf.rx_gain=$RX_GAIN --rf.dl_earfcn=$EARFCN | ts '[%Y-%m-%d %H:%M:%.S]' > srsUE.log &
elif [ $MODE == "IQ_EMULATION" ]
then
   srsue ${ZMQ_ARGS_IQ}  &
elif [ $MODE == "IQ_DIRECT" ]
then
   srsue ${ZMQ_ARGS}  &
elif [ $MODE == "PL_EMULATION" ]
then
  #ifconfig tun 172.16.0.2/24
  python3 zmq_tun.py -c -i "${CHEM_IP_ADDR}" -p 5002 -t 172.16.0.2 -n tun &
  #echo "Starting in Packet Level Mode"
elif [ $MODE == "PL_DIRECT" ]
then
  #ifconfig tun 172.16.0.2/24
  python3 zmq_tun.py -c -i "${ENB_IP_ADDR}" -p 5002 -t 172.16.0.2 -n tun &
  #echo "Starting in Packet Level Mode"
else
  echo "Specify correct mode"
fi
