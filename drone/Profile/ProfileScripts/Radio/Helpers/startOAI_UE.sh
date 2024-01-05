#!/bin/bash
#
# This script will start an srsLTE UE process
#    when OAI ENB is used on the other end
#
# needs to be called with LAUNCH_MODE=EMULATION or  LAUNCH_MODE=TESTBED

# For emulation:
#CHEM_IP_ADDR=192.168.151.192
CHEM_IP_ADDR=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_pl="-p 5301"
port_args_pl="-p $(( 5300 + $node_num))"
CHEM_DIR=/root/AERPAW-Dev/DCS/Emulation/emul_wireless_channel/CHEM/


# For testbed
tx_gain=70
rx_gain=40
#2.6 GHz
#earfcn=3350 
#3.5 GHz
earfcn=6700


mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue
ip link set dev tun_srsue mtu 1500

if [ $LAUNCH_MODE == "TESTBED" ]
then
   bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rf.dl_earfcn=$earfcn" 
elif [ $LAUNCH_MODE == "EMULATION" ]
then
  # there is no IQ Emulation for OAI, so we start the packet level emulation
	cd $CHEM_DIR
    python3 zmq_tun.py -c -i "${CHEM_IP_ADDR}" ${port_args_pl} -t 172.16.0.2 -n tun_srsue &
fi
