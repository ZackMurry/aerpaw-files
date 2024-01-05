#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

interface_name="eth-XM-EVM" 
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

sed -i "s/^gtp_s1c_bind_addr=.*/gtp_s1c_bind_addr=$ip_address/" startSRSRAN-5G-SISO-GNB.sh

# for the gNB
screen -S radioENB -dm \
       bash -c "stdbuf -oL -eL ./startSRSRAN-5G-SISO-GNB.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_enb_log.txt"
