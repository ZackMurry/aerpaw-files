#!/bin/bash

# MODEs are BUILD, TESTBED, EMULATION-TX or EMULATION-RX

POSITIONAL=()

BAND=2
TXPOWER=70
RXGAIN=40
PORT=4702
RXPORT=4701
ACHEM_IP="127.0.0.1"

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -m|--mode)
      MODE="$2"
      shift 
      shift 
      ;;
    -b|--band)
      BAND="$2"
      shift 
      shift 
      ;;
    -s|--earfcnstart)
      S="$2"
      shift 
      shift 
      ;;
    -e|--earfcnend)
      E="$2"
      shift 
      shift 
      ;;
    -t|--txpower)
      TXPOWER="$2"
      shift 
      shift 
      ;;
    -p|--port)
      PORT="$2"
      shift 
      shift 
      ;;
    -r|--rxport)
      RXPORT="$2"
      shift 
      shift 
      ;;
    -a|--achemip)
      ACHEM_IP="$2"
      shift 
      shift 
      ;;
    -g|--gainrx)
      RXGAIN="$2"
      shift 
      shift 
      ;;
    *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ -n $1 ]]; then
    echo "There is no option as $1"
fi

OUTPUT_DIR=/root/Results
DNAME=$(date +"%Y-%m-%d-%H:%M")
OUTPUT_FILE="/root/Results/$DNAME"
CHEMDIR="/root/AERPAW-Dev/DCS/Emulation/emul_wireless_channel/CHEM/achem.py"

if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir $OUTPUT_DIR
fi

if [ "$MODE" == "BUILD" ]; then
  cd srsran-version
  if [ ! -d "build" ]; then
    mkdir build
  fi
  cd build
  cmake ../
  make -j$(nproc)
  cp cell_search ../../
elif [ "$MODE" == "TESTBED" ]; then
 ./cell_search -s $S -e $E -b $BAND -g $RXGAIN | ts '[%Y-%m-%d %H:%M:%.S]' | tee -a $OUTPUT_FILE-testbed.txt
elif [ "$MODE" == "EMULATION-TX" ]; then 
 python3 -u ./cellSearchEmulatorTx.py -b $BAND -p $PORT -t $TXPOWER -i $ACHEM_IP | ts '[%Y-%m-%d %H:%M:%.S]' | tee -a $OUTPUT_FILE-emulation-tx.txt
elif [ "$MODE" == "EMULATION-RX" ]; then
 python3 -u ./cellSearchEmulatorRx.py -b $BAND -r $RXPORT | ts '[%Y-%m-%d %H:%M:%.S]' | tee -a $OUTPUT_FILE-emulation-rx.txt
fi
