#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

#chem_ip_addr=192.168.151.192
chem_ip_addr=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#port_args_iq="tx_port=tcp://*:5102,rx_port=tcp://${chem_ip_addr}:5002"
port_args_iq="tx_port=tcp://*:$(( 5100 + $node_num)),rx_port=tcp://${chem_ip_addr}:$(( 5000 + $node_num))"
zmq_args_iq="--rf.device_name=zmq --rf.device_args=\"${port_args_iq},id=enb,base_srate=23.04e6\""
CONFIG_PATH=/root/Profiles/ProfileScripts/Radio/Helpers/Handover/rrHO2.conf

interface_name="eth-XM-EVM"
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

# For testbed:
tx_gain=70
rx_gain=40
earfcn=6700
n_prb=25
mme_addr=192.168.103.1
gtp_s1c_bind_addr=$ip_address

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rf.dl_earfcn=$earfcn --enb.n_prb=$n_prb --enb_files.rr_config=$CONFIG_PATH --enb.mme_addr=$mme_addr --enb.gtp_bind_addr=$gtp_s1c_bind_addr --enb.s1c_bind_addr=$gtp_s1c_bind_addr --enb.enb_id=0x19C"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | srsenb --rf.srate=11.52e6 --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rf.dl_earfcn=$earfcn --enb.n_prb=$n_prb --enb_files.rr_config=$CONFIG_PATH --enb.mme_addr=$mme_addr --enb.gtp_bind_addr=$gtp_s1c_bind_addr --enb.s1c_bind_addr=$gtp_s1c_bind_addr --enb.enb_id=0x19C"
fi
