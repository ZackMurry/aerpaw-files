#!/bin/bash
#
# This script will start an srsLTE ENB process for MIMO
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

#chem_ip_addr=192.168.151.192
chem_ip_addr=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5102,rx_port=tcp://${chem_ip_addr}:5002"
port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"
zmq_args_iq="--rf.device_name=zmq --rf.device_args=\"${port_args_iq},id=enb,base_srate=23.04e6\""

# For testbed:
tx_gain=70
rx_gain=40
#earfcn=6700
dl_freq=3410e6
ul_freq=3320e6
imsi=00$((1010123456700 + $node_num))

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue
ip link set dev tun_srsue mtu 1500

#for MIMO configuration
nof_rx_ant=2

if [ $LAUNCH_MODE == "TESTBED" ]; then
   bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
   --rf.nof_antennas=$nof_rx_ant \
   --rat.eutra.dl_freq=$dl_freq --rat.eutra.ul_freq=$ul_freq  --usim.imsi=$imsi \
   --usim.algo=mil --usim.opc=63bfa50ee6523365ff14c1f45f88737d" 
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   bash -c "printf 't\n' | srsue --rf.device_args=\"num_channels=2\" --rf.srate=23.04e6 \ 
   --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
   --rf.nof_antennas=$nof_rx_ant \
   --rat.eutra.dl_freq=$dl_freq --rat.eutra.ul_freq=$ul_freq --usim.imsi=$imsi \
   --usim.algo=mil --usim.opc=63bfa50ee6523365ff14c1f45f88737d"
fi
