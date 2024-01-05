#!/usr/bin/env python
# coding: utf-8

import serial.tools.list_ports
import serial
from serial.threaded import LineReader, ReaderThread
import time
from io import StringIO 
import sys
import json
import re

active_ports = [comport.device for comport in serial.tools.list_ports.comports()]

ser_list = [serial.Serial(active_port, baudrate=57600) for active_port in active_ports]

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
    
class PrintLines(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
#         self.send_cmd("sys set pindig GPIO11 0")
#         self.send_cmd('sys get ver')
#         self.send_cmd('radio get mod')
#         self.send_cmd('radio get freq')
#         self.send_cmd('radio get sf')
#         self.send_cmd('mac pause')
#         self.send_cmd('radio set pwr 10')
#         self.send_cmd("sys set pindig GPIO11 0")
#         self.frame_count = 0

    def handle_line(self, data):
        if data == "ok":
            return
        print("RECV: %s" % data)
        
    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")
        
    def send_cmd(self, cmd, delay=.5):
        print("SEND: %s" % cmd)
        self.write_line(cmd)
        time.sleep(delay)
        
#     def tx(self):
#         self.send_cmd("sys set pindig GPIO11 1")
#         txmsg = 'radio tx %x%x' % (int(time.time()), self.frame_count)
  
#         self.send_cmd(txmsg)
#         time.sleep(.3)
#         self.send_cmd("sys set pindig GPIO11 0")
#         self.frame_count = self.frame_count + 1

with Capturing() as printed_values:
    for ser in ser_list:
        with ReaderThread(ser, PrintLines) as protocol:
        
            protocol.send_cmd('sys get ver')
            print(ser)
# p holds the COM ports that has a LoStik attached to it, i.e., ['COM8','COM10']            
for i,v in enumerate(printed_values):
    if 'RN2903' in v:
        pattern = re.compile("port='(COM\d+)'")
        p = pattern.findall(printed_values[i+1])

with open('config_files/COM_ports.json', 'w') as f:
    json.dump(p, f)

    

    

