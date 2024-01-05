#! /usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import sys
sys.path.insert(0, '..')

import logging
import serial
import serial.threaded
import threading
import re
import os
import time
import csv
from collections import OrderedDict
#import pandas as pd
from tabulate import tabulate
from datetime import datetime

try:
    import queue
except ImportError:
    import Queue as queue


class ATException(Exception):
    pass

import argparse
parser = argparse.ArgumentParser(description="Usage: sudo python at_rm500q.py -a \"Broadband\" -p /dev/ttyUSB2")
parser.add_argument("-a", "--apn", help="apn to be loaded", default="aerpaw1")
parser.add_argument("-p", "--usbpath", help="Specify USB port, else /dev/ttyUSB2 or USB3 (if ttyUSB2 fails) will be used, if otherwise specify",default="/dev/ttyUSB2")
args = parser.parse_args()
config = vars(args)

class ATProtocol(serial.threaded.LineReader):

    TERMINATOR = b'\r\n'

    def __init__(self):
        super(ATProtocol, self).__init__()
        self.alive = True
        self.responses = queue.Queue()
        self.events = queue.Queue()
        self._event_thread = threading.Thread(target=self._run_event)
        self._event_thread.daemon = True
        self._event_thread.name = 'at-event'
        self._event_thread.start()
        self.lock = threading.Lock()
        self.previousline = []

    def stop(self):
        #Stop the event processing thread, abort pending commands, if any.
        self.alive = False
        self.events.put(None)
        self.responses.put('<exit>')

    def _run_event(self):
        #Process events in a separate thread so that input thread is not blocked.
        while self.alive:
            try:
                self.handle_event(self.events.get())
            except:
                logging.exception('_run_event')

    def handle_line(self, line):
        #Handle input from serial port, check for events.
        if line.startswith('+'):
            self.events.put(line)
        else:
            self.responses.put(line)

    def handle_event(self, event):
        #Spontaneous message received.
        print('event received:', event)

    def command(self, command, response='OK', timeout=5):
        #Set an AT command and wait for the response.
        with self.lock:  # ensure that just one thread is sending commands at once
            self.write_line(command)
            lines = []
            while True:
                try:
                    line = self.responses.get(timeout=timeout)
                    #~ print("%s -> %r" % (command, line))
                    if line == response:
                        return lines
                    else:
                        lines.append(line)
                except queue.Empty:
                    raise ATException('AT command timeout ({!r})'.format(command))

# test Main
if __name__ == '__main__':

    # Define Main defs
    class RM500Q(ATProtocol):

        def __init__(self):
            super(RM500Q, self).__init__()
            self.event_responses = queue.Queue()
            self._awaiting_response_for = None

        def handle_event(self, event):
            #Handle events and command responses starting with '+..'
            if event:
                rev = event
                self.event_responses.put(rev)
            else:
                logging.warning('unhandled event: {!r}'.format(event))

        def command_with_event_response(self, command, outresponse='OK', timeout=2):
            #Send a command that responds with '+...'  then 'OK'
            with self.lock:  # ensure that just one thread is sending commands at once
                self._awaiting_response_for = command
                self.transport.write(b'{}\r\n'.format(command.encode(self.ENCODING, self.UNICODE_HANDLING)))
                Real_response = []
                while True:
                    try:
                        response = self.event_responses.get(timeout=timeout)
                        Real_response.append(response)
                    except:
                        return Real_response
            self._awaiting_response_for = None
            return Real_response

        def sleep_countdown(self, timer_count):
            while timer_count:
                mins, secs = divmod(timer_count, 60) ; timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end='\r') ; sys.stdout.flush()
                time.sleep(1) ; timer_count -= 1

    #Start MAIN
    continue_execution = False
    #print(args.usbpath)
    try:
        ser = serial.serial_for_url(args.usbpath, baudrate=115200, timeout=1, stopbits=1, rtscts=1)
    except:
        continue_execution = True
        pass

    if continue_execution:
        try:
            continue_execution = False
            ser = serial.serial_for_url('/dev/ttyUSB2', baudrate=115200, timeout=1, stopbits=1, rtscts=1)
        except:
            continue_execution = True
            pass

    if continue_execution:
        try:
            ser = serial.serial_for_url('/dev/ttyUSB3', baudrate=115200, timeout=1, stopbits=1, rtscts=1)
        except:
            print("USB serial AT port not found: Quiting!!!!")
            quit()

    ser.reset_input_buffer() ; ser.reset_output_buffer()
    rows, columns = os.popen('stty size', 'r').read().split()
    #print(rows) ; print(columns)

    connected_string  = "========CONNECTED" ; spaces = '='.join([''] * (int(columns) - len(connected_string) - 10)) ; empty_print = spaces ; print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), connected_string, empty_print, end="\n")


    #start serial USB thread
    with serial.threaded.ReaderThread(ser, RM500Q) as Quectel_module:

        # System Info
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end = " ")
        print(' '.join(Quectel_module.command("ATI")), end=" ")
        print("IMEI:", Quectel_module.command("AT+GSN")[1], end=" ")
        print("IMSI:",Quectel_module.command("AT+CIMI")[1])


        #Initialize the Modem

        # Step1 Set right APN
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Set Provided or default APN:", args.apn)
        Var_PDP_Type = "IPV4V6" ; Var_APN = args.apn
        APN_string = "AT+CGDCONT=1,\"%s\",\"%s\"" % (Var_PDP_Type, Var_APN)
        Quectel_module.command_with_event_response(APN_string)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Also set all bands")
        # Step2 Set all bands
        Quectel_module.command_with_event_response("AT+QNWPREFCFG= \"lte_band\",1:2:3:4:5:7:8:12:13:14:18:19:20:25:26:28:29:30:32:34:38:39:40:41:42:43:46:48:66:71")
        Quectel_module.command_with_event_response("AT+QNWPREFCFG= \"nsa_nr5g_band\",1:2:3:5:7:8:12:20:25:28:38:40:41:48:66:71:77:78:79")
        Quectel_module.command_with_event_response("AT+QNWPREFCFG= \"nr5g_band\",1:2:3:5:7:8:12:20:25:28:38:40:41:48:66:71:77:78:79")
        Quectel_module.command_with_event_response("AT+QNWPREFCFG= \"mode_pref\",AUTO")
        Quectel_module.command_with_event_response("AT+QNWPREFCFG=\"ue_usage_setting\",1")
        Quectel_module.command_with_event_response("AT+QNWPREFCFG=\"nr5g_disable_mode\",0")
        Quectel_module.command_with_event_response("AT+QNWCFG=\"csi_ctrl\",1,1")

        #Set USBnet status
        Quectel_module.command_with_event_response("AT+QCFG=\"usbnet\",2")

        # Operator status
        Var_current_operator_status_and_mode = Quectel_module.command_with_event_response("AT+COPS?")

        # Try register if no operator/ no registration
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Operator selected:", re.search(r"(?<=\+COPS\:...).*", Var_current_operator_status_and_mode[0]).group(0))
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Quectel modem not registered to network, trying now..")
            #Either not in auto mode or NW not found
            #Set COPS =0 & CREG=1
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Set Auto selection mode to YES and Registration status to 1 and wait ~5 mins")
            Quectel_module.command_with_event_response("AT+COPS=0")
            Quectel_module.command_with_event_response("AT+CREG=1") ; Quectel_module.sleep_countdown(300)

        #Verify after reregister
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Operator selected:", re.search(r"(?<=\+COPS\:...).*", Var_current_operator_status_and_mode[0]).group(0))
        except:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Network registration Failure: Try again later or with different parameters")
            quit()

        ################################
        #If Registartion succesful
        #MT in Auto mode and nw found
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Network already selected, Re-registration not required") ; Selection_and_registration_status = 2

        #Post self registration check
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Enter logging state")

        ################################
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "BASIC Params")
        #Line1 Basic params
        Var_CREG = Quectel_module.command_with_event_response("AT+CREG?")[0] #; Quectel_module.sleep_countdown(2)
        Var_CSQ = Quectel_module.command_with_event_response("AT+CSQ")[0] #; Quectel_module.sleep_countdown(2)
        Var_QNWINFO = Quectel_module.command_with_event_response("AT+QNWINFO") #; Quectel_module.sleep_countdown(2)
        Var_QSPN = Quectel_module.command_with_event_response("AT+QSPN") ; #Quectel_module.sleep_countdown(2)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ", re.search(r"(?<=\+).*", Var_CREG).group(0), end=" ") ; print(re.search(r"(?<=\+).*", Var_CSQ).group(0), end=" ")
        print((re.search(r"(?<=\+).*", Var_QSPN[0]).group(0)))
        print('\n')
        print("Started Logging now")
