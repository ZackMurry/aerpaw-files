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
O5GS_DIR=/opt/open5gs/build/tests/app/

#!/bin/sh

SYSTEM=`uname`;

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200

if [ "$SYSTEM" = "Linux" ]; then
    if ! grep "ogstun" /proc/net/dev > /dev/null; then
        ip tuntap add name ogstun mode tun
    fi
    ip addr del 172.16.0.1/16 dev ogstun 2> /dev/null
    ip addr add 172.16.0.1/16 dev ogstun
    ip link set ogstun up
fi

mongodb_path="/opt/open5gsdb/"

if [ -d "$mongodb_path" ]; then
        screen -S mongodb -dm  bash -c "mongod --dbpath $mongodb_path"
else
        mkdir -p $mongodb_path
        screen -S mongodb -dm  bash -c "mongod --dbpath $mongodb_path"
fi

sleep 1

cd $O5GS_DIR
./app -c $1




