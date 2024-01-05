##!/usr/bin/env python3

import serial
import time
import io
import argparse
import configparser
from serial.threaded import LineReader, ReaderThread
import json


parser = argparse.ArgumentParser(description='Transmit packets reading the traffic file')
parser.add_argument('traffic', help="Traffic File")
parser.add_argument('period', help="Packet transmission period in sec")
parser.add_argument('duration',help="Total transmission duration in min")
parser.add_argument('--debug', '-d', help="Print debug output", action='store_const', const=True, default=False)

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config_files/'+args.traffic)

with open('config_files/COM_Ports.json') as f:
    COM_Ports = json.load(f)

class PrintLines(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.frame_count = 0

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
        
    def str_to_ascii(self, string):
        return int(''.join(hex(ord(c))[2:] for c in string), 16)
    
    def infinite_sequence(self, my_list):
        num = 0
        while True:
            yield my_list[num]
            num += 1
            if num%len(my_list)==0:
                num=0
    def file_sequence(self, my_list):
        num = 0
        while True:
            yield my_list[num]
            num +=1
            if num == len(my_list):
                yield '_-_END OF FILE_-_'
            if num > len(my_list):
                yield ''
                
                
    def tx(self, txmsg):
        self.send_cmd("sys set pindig GPIO11 1")
        txmsg = 'radio tx %x' % (txmsg)
        self.send_cmd(txmsg)
        self.send_cmd("sys set pindig GPIO11 0")

if config.get('transmitter_id', 'status') == 'on':
    transmitter_id = config.get('transmitter_id','id')
else:
    transmitter_id = ''

if config.get('packet_index', 'status') == 'on':
    packet_index = True
else:
    packet_index = False
    
if config.get('time_stamp', 'status') == 'on':
    time_stamp = True
else:
    time_stamp = False

custom_packets = False
custom_file = False
custom_file_name = ''
custom_file_content = []
    
if config.get('custom_packets', 'status') == 'on':
    custom_packets = True
elif config.get('custom_packets', 'status') == 'file':
    custom_file = True
    custom_file_name = config.get('custom_packets', 'file_name')
    custom_file_packet_length = int(config.get('custom_packets', 'file_packet_length'))
    with open('config_files/'+custom_file_name, 'r') as f:
        bulk_text = f.read()
        custom_file_content = [bulk_text[i:i+custom_file_packet_length] for i in range(0,len(bulk_text),custom_file_packet_length)]


    
packet_period = float(args.period)
total_duration = float(args.duration)
custom_content = [p[1] for p in config.items('packets')]



global params 
params = dict()
params['transmitter_id'] = transmitter_id
params['packet_index'] = packet_index
params['time_stamp'] = time_stamp
params['custom_packets'] = custom_packets
params['packet_period'] = packet_period
params['total_duration'] = total_duration
params['custom_content'] = custom_content
params['custom_file'] = custom_file
params['custom_file_content'] = custom_file_content



ser = serial.Serial(COM_Ports[0], baudrate=57600)
with ReaderThread(ser, PrintLines) as protocol:
    

    frame_count = 0
    gen = protocol.infinite_sequence(params['custom_content'])
    gen_file = protocol.file_sequence(params['custom_file_content'])
    exp_begin = time.time()
    
    while (time.time()-exp_begin < params['total_duration'] * 60 ):
        packet = ''
        underscore = ''
        
        if params['custom_file']:
            piece =next(gen_file)
            if piece == "_-_END OF FILE_-_":
                print('FILE TRANSMISSION COMPLETED')
                packet = piece
            else:
                packet += piece
        else:
            if params['transmitter_id'] != '':
                packet += params['transmitter_id']
                underscore = '_'
            if params['custom_packets']:
                packet +=underscore+next(gen)
                underscore='_'
            if params['time_stamp']:
                packet +=underscore+ str(int(time.time()))
                underscore='_'
            if params['packet_index']:
                packet +=underscore+ str(frame_count)

        if packet == '':
            packet = 'AERPAW'
        elif packet == '_-_END OF FILE_-_':
            break
            
            print(f'Frame Count: {frame_count}, Packet: {packet}')
        with open('output_files/input.txt', 'a+') as f:
            f.write(packet)
            f.write('\n')
        
        packet = protocol.str_to_ascii(packet)
        protocol.tx(packet)
        time.sleep(params['packet_period'])
        frame_count += 1

