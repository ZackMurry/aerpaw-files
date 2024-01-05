#!/bin/bash
CONFIG_DIR=/opt/open5gs/build/configs/

cd $CONFIG_DIR

interface_name="eth-XM-EVM" 
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

yq eval ".upf.gtpu[0].addr = \"$ip_address\"" -i open5gs_nr_core.yaml
yq eval ".amf.ngap[0].addr = \"$ip_address\"" -i open5gs_nr_core.yaml

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the core network
screen -S open5gsCore -dm \
       bash -c "stdbuf -oL -eL ./startOpen5GS.sh $CONFIG_DIR/5g_open5gs_core.yaml \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_epc_log.txt"
