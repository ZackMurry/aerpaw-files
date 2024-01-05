#!/usr/bin/python3

import argparse
import logging
import sys
import json
import pickle
from threading import Lock, Thread, Event
import numpy as np
from socket import *
import time
import os
from signal import signal,  SIGINT

bandFile = open('ltebands.json')
bands = json.load(bandFile)

CHN_UPD_IP = '127.0.0.1'
CHN_UPD_PORT = 4702
TX_POWER_DB = 70
LTE_BAND_DEFAULT = 2
MAX_PACKET_SIZE = 1024
threadActive = True

##### logging init ####
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cellSearchEmulatorTx')

def signal_handler(signal, frame):
    global threadActive
    threadActive = False
    print('Handling Ctrl+C')

def getFreqInfoFromBand(band:int):
    freq = 0 # in MHz
    for b in bands:
        if band == b["Band"]:
            freq = b["FDL_Low"]
    assert freq != 0, "Band value is wrong"

    return freq

def updateChannel(freq, ip, emPort, txPower):
    global threadActive

    try:
        txSocket = socket(AF_INET,SOCK_DGRAM)
    except Exception as error:
        #print('Cannot open channel update channel:',error)
        logger.error('Cannot open channel update channel:',error)
        return
    
    tData = {   
        "txPower": txPower,
        "frequency": freq
        }
    payload = pickle.dumps(tData)
    
    while(threadActive):
        try:
            txSocket.sendto(payload,(ip, emPort))
        except Exception as error:
            logger.error('Cannot transmit packet :',error)
        time.sleep(0.33)

    print("Finished")

def pathLoss(freq, distance):
    ## compute path loss as a function of distance (free space)
    plConst = -27.55
    pathloss = 20 * np.log(freq) + 20 * np.log(distance) + plConst
    return pathloss

#cellSearchEmulatorTx.py
def main():
    global threadActive

    signal(SIGINT, signal_handler)

    ## Arg Parse
    parser = argparse.ArgumentParser(description='Fake Cell Search TX')


    parser.add_argument('-b','--band',help='LTE Band', type=int, default=LTE_BAND_DEFAULT)
    parser.add_argument('-i','--ip',help='ACHEM Emulator Ip', type=str, default=CHN_UPD_IP)
    parser.add_argument('-p','--port',help='ACHEM Emulator Port', type=int, default=CHN_UPD_PORT)
    parser.add_argument('-t','--txpower',help='TX power in dB', type=int, default=TX_POWER_DB)

    args = parser.parse_args()

    freq = getFreqInfoFromBand(args.band)

    threadTx = Thread(target = updateChannel, args = (freq, args.ip, args.port, args.txpower, ))
    threadTx.start()

    try:
        # This try-except block is for avoiding from SIGPIPE error
        # ref. https://docs.python.org/3/library/signal.html#note-on-sigpipe
        print("Fake Cell Search TX started")
       
        while threadActive:
            time.sleep(1)
        print("Fake Cell Search TX finished")

        sys.stdout.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE

    


if __name__ == "__main__":
    main()