#!/bin/bash

CELL_SEARCH_DIR="/root/Profiles/SDR_control/CellSearch"

RX_GAIN=40
BAND=22
EARFCN_START=6600
EARFCN_END=6601
RX_PORT=4701

cd $CELL_SEARCH_DIR


if [ "$LAUNCH_MODE" == "TESTBED" ]; then
    screen -dmS cellSearch bash -c "printf 't\n' | stdbuf -oL -eL ./cell_search -s $EARFCN_START -e $EARFCN_END -b $BAND -g $RX_GAIN | ts $TS_FORMAT | tee -a $RESULTS_DIR/$LOG_PREFIX\_cellsearch_testbed.txt" 
elif [ "$LAUNCH_MODE" == "EMULATION" ]; then
    screen -dmS cellSearchEmulatorRx bash -c "printf 't\n' | stdbuf -oL -eL  python3 -u ./cellSearchEmulatorRx.py -b $BAND -r $RX_PORT -g $RX_GAIN \
      | ts $TS_FORMAT | tee -a $RESULTS_DIR/$LOG_PREFIX\_cellsearch_emulation_rx.txt"
fi
