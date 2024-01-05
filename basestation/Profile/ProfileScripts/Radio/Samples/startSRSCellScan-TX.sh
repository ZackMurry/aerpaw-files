#!/bin/bash

CELL_SEARCH_DIR="/root/Profiles/SDR_control/CellSearch"

TX_GAIN=70
RX_GAIN=40
EARFCN=6600
N_PRB=100
ACHEM_PORT=4702
#ACHEM_IP="192.168.151.192"
ACHEM_IP="$AP_EXPENV_CHEMVM_XE"
BAND=22

#cd $CELL_SEARCH_DIR
cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

if [ "$LAUNCH_MODE" == "TESTBED" ]; then
    screen -S radioEPC -dm \
       bash -c "stdbuf -oL -eL ./startEPC.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_epc_log.txt"

    screen -dmS radioENB \
       bash -c  "printf 't\n' | stdbuf -oL -eL srsenb --rf.tx_gain=$TX_GAIN --rf.rx_gain=$RX_GAIN --rf.dl_earfcn=$EARFCN --enb.n_prb=$N_PRB" 
elif [ "$LAUNCH_MODE" == "EMULATION" ]; then
    screen -dmS cellEmulatorTx \
       bash -c "printf 't\n' | stdbuf -oL -eL python3 -u ./cellSearchEmulatorTx.py \
       -b $BAND -p $ACHEM_PORT -t $TX_GAIN -i $ACHEM_IP | ts $TS_FORMAT | tee -a $RESULTS_DIR/$LOG_PREFIX\_cellsearch_emulation_tx.txt"
fi
