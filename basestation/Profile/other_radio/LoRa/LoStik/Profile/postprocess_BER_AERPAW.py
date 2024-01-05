#!/usr/bin/env python
# coding: utf-8

import serial
import time
import io
import argparse
import configparser
from serial.threaded import LineReader, ReaderThread
import json
import sys
import numpy as np

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


total_sent = len(input_list)
total_received = len(output_list)
length = total_sent

if total_sent != total_received:
    print('CRC Header is used, no BER Calculation is viable!')
    sys.exit()
else:
    pass
 

def strToBinary(s): 
    bin_conv = [] 
  
    for c in s: 
          
        # convert each char to 
        # ASCII value 
        ascii_val = ord(c) 
          
        # Convert ASCII value to binary 
        binary_val = bin(ascii_val) 
        bin_conv.append(binary_val[2:]) 
          
    return (' '.join(bin_conv))

def solve( A,  B): 
   
    if len(A) != len(B):
        print("Different lengths of sequences, no BER calculation viable!")
        sys.exit()
              
           
    count = 0 
  
    # since, the numbers are less than 2^31 
    # run the loop from '0' to '31' only 
    for i in range(len(A)): 
  
        if A[i]!=B[i]:
            count=count+1
           
       
  
    return count, len(A)

BERS_list = []
for i in range(length):
    tra = input_list[i]
    rec = output_list[i]
    
    tra_bin = strToBinary(tra)
    rec_bin = strToBinary(rec)
    
    BERS_list.append(solve(tra_bin, rec_bin))
    
err_bits = 0
tot_bits = 0
                     
for ber in BERS_list:
    err_bits += ber[0]
    tot_bits += ber[1]
                     
print('BER Calculations for transmitter {} and receiver {}'.format(input_file.split('.txt')[0].split('input_')[-1], output_file.split('.txt')[0].split('output_')[-1]))            

if err_bits == 0:
    BER_log10 = '-inf'
else:
    BER_log10 = np.log10(err_bits/tot_bits)
    
print('Average BER: ', str(err_bits/tot_bits))
                    
    






