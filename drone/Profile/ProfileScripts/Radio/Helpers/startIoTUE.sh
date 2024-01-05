#!/bin/bash
#
# This script will start an srsLTE UE process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

# For emulation:
#chem_ip_addr=192.168.151.192
#chem_ip_addr=$AP_EXPENV_CHEMVM_XE
#node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5101,rx_port=tcp://${chem_ip_addr}:5001"
#port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"

# For testbed
rx_gain=40
freq=915e6

#Not needed for IoT
#mkdir /dev/net
#mknod /dev/net/tun c 10 200
#ip tuntap add mode tun tun_srsue 
#ip link set dev tun_srsue mtu 1500

if [ $LAUNCH_MODE == "TESTBED" ]
then
   bash -c "printf 't\n' | /root/npdsch_ue -g $rx_gain -f $freq -r 0x1234 -s" 
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   bash -c "printf 't\n' | /root/npdsch_ue -g $rx_gain -f $freq -r 0x1234 -s"  
fi
