#!/bin/bash
CONFIG_DIR=/opt/open5gs/build/configs/

cd $CONFIG_DIR

interface_name="eth-XM-EVM" 
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

yq eval ".mme.s1ap[0].addr = \"$ip_address\"" -i ho_core.yaml
yq eval ".sgwu.gtpu[0].addr = \"$ip_address\"" -i ho_core.yaml

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the core network
screen -S open5gs -dm \
       bash -c "stdbuf -oL -eL ./startOpen5GS.sh $CONFIG_DIR/ho_core.yaml \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_epc_log.txt"
