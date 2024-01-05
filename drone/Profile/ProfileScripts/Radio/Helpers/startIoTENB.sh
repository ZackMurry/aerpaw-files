#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

#chem_ip_addr=192.168.151.192
#chem_ip_addr=$AP_EXPENV_CHEMVM_XE
#node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5102,rx_port=tcp://${chem_ip_addr}:5002"
#port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"
#zmq_args_iq="--rf.device_name=zmq --rf.device_args=\"${port_args_iq}\""

# For testbed:
tx_gain=70
freq=915e6

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | /root/npdsch_enodeb -g $tx_gain -f $freq" 
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | /root/npdsch_enodeb -g $tx_gain -f $freq"
fi
