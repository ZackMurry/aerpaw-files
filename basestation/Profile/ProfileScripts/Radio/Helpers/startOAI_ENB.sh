#!/bin/bash
#
# This script will start an OAI ENB process 
#
# needs to be called with LAUNCH_MODE=EMULATION or LAUNCH_MODE=TESTBED

EXEC_PATH=/opt/openairinterface5g/cmake_targets/lte_build_oai/build/lte-softmodem
#CONFIG_PATH=/opt/openairinterface5g/ci-scripts/conf_files/enb.band7.tm1.100PRB.usrpb210.conf
CONFIG_PATH=/root/Profiles/ProfileScripts/Radio/Helpers/enb.band7.tm1.100PRB.usrpb210.conf

# For emulation:
chem_ip_addr=192.168.151.192

# For testbed:
# Modify .conf file in the CONFIG_PATH to change parameters

if [ $LAUNCH_MODE == "TESTBED" ]; then
    $EXEC_PATH -O $CONFIG_PATH

elif [ $LAUNCH_MODE == "EMULATION" ]; then
    :	#  We don't currently have an IQ emulation for OAI, so nothing is here,
	#  and the emulation will be setup for packet level emulation
	#  the startOAI_EPC.sh will set this up
fi
