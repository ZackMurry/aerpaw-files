#!/usr/bin/env python3
import time
import sys
import serial
import argparse 
import json

from serial.threaded import LineReader, ReaderThread

parser = argparse.ArgumentParser(description='LoRa Radio mode receiver.')
parser.add_argument('window', help = "the amount of time that reception is open")
args = parser.parse_args()

with open('config_files/COM_Ports.json') as f:
    COM_Ports = json.load(f)




class PrintLines(LineReader):
           
    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.snr_indicator = False
        self.snr_ = - 128
        self.rssi_indicator = False
        self.rssi_ = -128
        self.current_packet_ = ''
        self.frame_counter = 0
        self.output_dict = {}
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.send_cmd('radio rx 0')
        self.send_cmd("sys set pindig GPIO10 0")

    def ascii_to_string(self, asc):
        L = [int(asc[i:i+2],16) for i in range(0,len(asc),2)]
        return ''.join(chr(i) for i in L)
    
    def handle_line(self, data):
        if data == "ok" or data == 'busy':
            return
        
        elif data == "radio_err":
            self.send_cmd('radio rx 0')
            return
        
        elif data[:2] == 'RN':
            return 
        elif data[:10] == '4294967245':
            return
            
            
        elif (self.rssi_indicator==False) and (self.snr_indicator == False):
            data = self.ascii_to_string(data.strip('radio_rx  '))
#             print(data)
            with open('output_files/output.txt','a+') as f:
                f.write(data)
                f.write('\n')

            self.current_packet_ = data


            self.rssi_indicator = True
            self.send_cmd("radio get rssi", delay=.1)

        elif (self.rssi_indicator == True) and (self.snr_indicator == False):
#             print('RSSI: ', data)

            self.rssi_ = data
            self.snr_indicator = True
            self.send_cmd("radio get snr", delay=.1)

        elif (self.rssi_indicator == True) and (self.snr_indicator == True):

#             print('SNR: ',data)
            self.snr_ = data

            self.snr_indicator = False
            self.rssi_indicator = False

            temp_dict = dict({self.frame_counter : [self.current_packet_, self.rssi_, self.snr_]})
            print(f'Frame Counter: {self.frame_counter}, RSSI: {self.rssi_}, SNR: {self.snr_}')
            with open('output_files/output_rssi_snr.json', 'a+') as fp:
                json.dump(temp_dict, fp)
            with open('output_files/output_bulk_file.txt', 'a+') as f:
                f.write(self.current_packet_)
            
            self.frame_counter += 1
            self.current_packet_ = ''
            self.rssi_ = -128
            self.snr_ = -128
            

        time.sleep(.1)

        self.send_cmd('radio rx 0')


    
    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

        
    def send_cmd(self, cmd, delay=.5):
        self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
        time.sleep(delay)


global window, exp_begin, ser

window = float(args.window)*60
exp_begin = time.time()

ser = serial.Serial(COM_ports[0], baudrate=57600)
with ReaderThread(ser, PrintLines) as protocol:
    if window == 0:
        while(1):
            pass
    else:
        while(1):
            if time.time()-exp_begin > window:
                exit()
            pass
