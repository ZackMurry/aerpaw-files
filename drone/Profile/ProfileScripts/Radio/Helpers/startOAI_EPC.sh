#!/bin/bash
#
# This script will start an srsLTE EPC process when running the OAI ENB
#
# needs to be called with LAUNCH_MODE=EMULATION or  LAUNCH_MODE=TESTBED

# For emulation:
#CHEM_IP_ADDR=192.168.151.192
CHEM_IP_ADDR=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_pl="-p 5302"
port_args_pl="-p $(( 5300 + $node_num))"

CHEM_DIR=/root/AERPAW-Dev/DCS/Emulation/emul_wireless_channel/CHEM/

mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun srs_spgw_sgi
ip link set dev srs_spgw_sgi mtu 1500
ifconfig srs_spgw_sgi 172.16.0.1/24

if [ $LAUNCH_MODE == "TESTBED" ]; then
	srsepc
elif [ $LAUNCH_MODE == "EMULATION" ]; then
	# We setup the packet level emulation for OAI
	cd $CHEM_DIR
    python3 zmq_tun.py -c -i "${CHEM_IP_ADDR}" ${port_args_pl} -t 172.16.0.1 -n srs_spgw_sgi &
fi




