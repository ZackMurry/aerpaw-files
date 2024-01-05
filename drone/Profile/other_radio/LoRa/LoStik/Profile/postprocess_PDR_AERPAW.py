#!/usr/bin/env python
# coding: utf-8

import serial
import time
import io
import argparse
import configparser
from serial.threaded import LineReader, ReaderThread
import json

parser = argparse.ArgumentParser(description='Transmit packets reading the traffic file')
parser.add_argument('input_file', help="Input File")
parser.add_argument('output_file', help="Output File")
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file


with open(input_file, "r") as file:
    input_list = file.readlines()    

with open(output_file, "r") as file:
    output_list = file.readlines()    


input_list = [f.strip('\n') for f in input_list]
output_list = [f.strip('\n') for f in output_list]

# print('# packets input list: ', str(len(input_list)))
# print('# packets output list: ', str(len(output_list)))

total_sent = len(input_list)
total_received = len(output_list)
# total_received = 0
# index = 0

# while index < len(output_list):
    
#     input_index = index
#     while input_index < len(input_list):
#         if output_list[index] == input_list[input_index]:
# #             print(total_received)
#             total_received +=1
#             index += 1
#             input_index += 1
# #             print(index)
#         else:
#             input_index += 1
print('PDR Calculations for transmitter {} and receiver {}'.format(input_file.split('.txt')[0].split('input_')[-1], output_file.split('.txt')[0].split('output_')[-1]))            
print('\n','total packets sent: ', str(total_sent), '\n')
print(' total packets received: ', str(total_received), '\n')
print('PDR: ', str(round(total_received/total_sent * 100,2))+' %')