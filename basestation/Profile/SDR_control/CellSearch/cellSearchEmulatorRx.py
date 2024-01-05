#!/usr/bin/python3

import argparse
import logging
import time
import sys
import json
import pickle
from threading import Lock, Thread, Event
import numpy as np
from socket import *
from datetime import datetime
from signal import signal,  SIGINT
import os 

bandFile = open('ltebands.json')
bands = json.load(bandFile)

CHN_UPD_PORT = 4700
CHN_INFO_PORT = 4701
LTE_BAND_DEFAULT = 2
MAX_PACKET_SIZE = 1024
threadActive = True


##### logging init ####
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('fakeCellSearchRx')

# Sample Output
# Aug 27 11:00:39 Found CELL MHz, 3500.0,  EARFCN, 6600, PHYID, 1, PRB, 50,  ports, 1, PSS power dBm, -9.0,  PSR, 3.9, 2021-08-27 11:00:39:172

def signal_handler(signal, frame):
    global threadActive
    threadActive = False
    print('Handling Ctrl+C')

def readConfiguration(fName):
    try:
        with open(fName) as json_data_file:
            configList = json.load(json_data_file)
        return configList
    except IOError as e:
        logger.error('Error reading ' + fName)
        logger.error(e)
        return
    except ValueError as e:
        logger.error('Error parsing ' + fName)
        logger.error(e)
        return
    except Exception as e:
        logger.error('Unexpected error parsing ' + fName + ':' + str(sys.exc_info()[0]))
        logger.error(e)
        return


def getFreqInfoFromBand(band:int):
    freq = 0 # in MHz
    for b in bands:
        if band == b["Band"]:
            freq = b["FDL_Low"]
    assert freq != 0, "Band value is wrong"

    return freq

def printResult(freq, rxPower):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Found CELL MHz, %.1f,  EARFCN, 6600, PHYID, 1, PRB, 50,  ports, 1, PSS power dB, %.1f,  PSR, 7.0, %s" % (
        freq,
        rxPower,
        current_time
    ))

def receiveCellInfo(bindPort, freq, rxgain):
    global threadActive

    try:
        rxInfoSocket = socket(AF_INET, SOCK_DGRAM)
        rxInfoSocket.bind(('0.0.0.0', bindPort))
        rxInfoSocket.settimeout(1);  # 1 second - used for clean exit on Ctrl+C
    except Exception as err:
        print('Failed to create cell info socket. Error Code : ', err)
        sys.exit()

    while(threadActive):
        try:
            (payload, clientAddress) = rxInfoSocket.recvfrom(MAX_PACKET_SIZE)
            rData = pickle.loads(payload)
            
            if rData["frequency"] != freq:
                pass
            
            if isinstance(rData["emulatedPower"],list):
                numberOfNodes = len(rData["emulatedPower"])
                for i in range(numberOfNodes): 
                    for j in range(numberOfNodes):
                        if (i != j):
                            if rData["emulatedPower"][i][j] != float("-inf") and threadActive: 
                                printResult(freq, rxgain + rData["emulatedPower"][i][j])
                                time.sleep(1)
                                
            elif isinstance(rData["emulatedPower"], np.ndarray):
                for rxPower in rData["emulatedPower"]:
                    if rxPower != float("-inf") and threadActive: 
                        printResult(freq, rxgain + rxPower)
                        time.sleep(1)

        except Exception as error:
            pass


def main():
    global threadActive

    signal(SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='Emulated Cell Search RX')

    parser.add_argument('-b','--band',help='LTE Band', type=int, default=LTE_BAND_DEFAULT)
    parser.add_argument('-r','--rxport',help='Cell Info Rx Port', type=int, default=CHN_INFO_PORT)
    parser.add_argument('-g','--gain',help='Rx Gain', type=int, default=CHN_INFO_PORT)

    args = parser.parse_args()

    freq = getFreqInfoFromBand(args.band)

    ## Thread Start
    threadChnInfo = Thread(target = receiveCellInfo, args = (args.rxport, freq, args.gain, ))
    threadChnInfo.start()

    print("Emulated Cell Search RX Listening on Port", str(args.rxport))

    try:
      # This try-except block is for avoiding from SIGPIPE error
      # ref. https://docs.python.org/3/library/signal.html#note-on-sigpipe
      while threadActive:
        time.sleep(1)
      sys.stdout.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE


if __name__ == "__main__":
    main()
    