#!/bin/bash
#
# This script will start an srsLTE UE process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

# For emulation:
#chem_ip_addr=192.168.151.192
chem_ip_addr=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5101,rx_port=tcp://${chem_ip_addr}:5001"
port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"
zmq_args_iq="--rf.device_name=zmq --rf.device_args=\"${port_args_iq},id=ue,base_srate=23.04e6\""

# For testbed
tx_gain=70
rx_gain=40
earfcn=6700
imsi=00$((1010123456700 + $node_num))

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue 
ip link set dev tun_srsue mtu 1500

if [ $LAUNCH_MODE == "TESTBED" ]
then
   bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
   --rat.eutra.dl_earfcn=$earfcn --usim.imsi=$imsi --usim.algo=mil \
   --usim.opc=63bfa50ee6523365ff14c1f45f88737d" 
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   bash -c "printf 't\n' | srsue --rat.eutra.dl_earfcn=$earfcn --usim.imsi=$imsi --usim.algo=mil \
   --usim.opc=63bfa50ee6523365ff14c1f45f88737d --rf.srate=11.52e6"  
fi
