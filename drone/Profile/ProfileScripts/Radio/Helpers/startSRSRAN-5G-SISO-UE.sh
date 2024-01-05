#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

#chem_ip_addr=192.168.151.192
chem_ip_addr=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5102,rx_port=tcp://${chem_ip_addr}:5002"
# port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"
# zmq_args_iq="--rf.device_name=zmq --rf.device_args=\"${port_args_iq},id=enb,base_srate=23.04e6\""

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue
ip link set dev tun_srsue mtu 1500

# For testbed:
tx_gain=70
rx_gain=40

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rat.eutra.nof_carriers=0 --rat.nr.bands=3 --rat.nr.nof_carriers=1 --nas.apn=internet  --rrc.release=15 --rf.srate=11.52e6"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rat.eutra.nof_carriers=0 --rat.nr.bands=3 --rat.nr.nof_carriers=1 --nas.apn=internet  --rrc.release=15 --rf.srate=11.52e6"
fi
