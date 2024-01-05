##!/usr/bin/env python3

import serial
import time
import io
import argparse
import configparser
import json

parser = argparse.ArgumentParser(description='Configure LoStik device')
# parser.add_argument('port', help="Site ID of LoStik")
parser.add_argument('config', help="Configuration File")
parser.add_argument('--debug', '-d', help="Print debug output", action='store_const', const=True, default=False)

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config_files/'+args.config)


with open('config_files/COM_Ports.json') as f:
    COM_Ports = json.load(f)
    
ser = serial.Serial(COM_Ports[0], baudrate=57600, timeout=10)


def send_cmd(cmd):
    if args.debug:
        print(cmd)
    ser.write(("%s\r\n"% cmd).encode("UTF-8"))
    time.sleep(.5)

def get_var(cmd):
    send_cmd(cmd)
    var = ser.readline().strip().decode("UTF8")
    if args.debug:
        print(var)
    return var

def set_confirm(cmd):
    res = get_var(cmd)
    if args.debug:
        print(res)
    
    if res != "ok":
        raise Exception("Error in command: %s\r\n Response: %s" % (cmd, res))

max_ch = 72
sku = "RN2903"

send_cmd('sys get ver')
verinfo = ser.readline().decode("UTF-8")
if not verinfo:
    print("Timeout connecting to device")
    exit()

if("RN2483" in verinfo):
    sku = "RN2483"
    max_ch = 16
elif "RN2903" in verinfo:
    sku = "RN2903"
else:
    raise Exception("Invalid SKU")


mode = config.get('mode', 'mode')

print(verinfo.strip())
print('Configuring   %s   in   %s   mode' % (COM_Ports[0],mode))

if mode == 'lora':
    print('Configuring lora')
    set_confirm('radio set freq %s' % config.get('lora', 'frequency'))
    print('frequency (freq): %s ' % config.get('lora','frequency'))
    
    set_confirm('radio set pwr %s' % config.get('lora', 'output_power'))
    print('output power (pwr): %s' % config.get('lora', 'output_power'))
    
    set_confirm('radio set crc %s' % config.get('lora', 'CRC_header'))
    print('CRC header (crc): %s' % config.get('lora', 'CRC_header'))
    
    set_confirm('radio set wdt %s' % config.get('lora', 'watchdog_timer'))
    print('Watchdog Timer (wdt): %s' % config.get('lora', 'watchdog_timer'))
    
    set_confirm('radio set sync %s' % config.get('lora', 'sync_word'))
    print('sync word (sync): %s' % config.get('lora', 'sync_word'))
    
    
    set_confirm('radio set sf %s' % config.get('lora', 'spreading_factor'))
    print('spreading factor (sf): %s' % config.get('lora', 'spreading_factor'))
    
    set_confirm('radio set iqi %s' % config.get('lora', 'IQ_inversion'))
    print('IQ Inversion (iqi): %s' % config.get('lora', 'IQ_inversion'))
    
    set_confirm('radio set cr %s' % config.get('lora', 'coding_rate'))
    print('coding rate (cr): %s' % config.get('lora', 'coding_rate'))
    
    set_confirm('radio set bw %s' % config.get('lora', 'bandwidth'))
    print('bandwidth (bw): %s' % config.get('lora', 'bandwidth'))
    
    
    
elif mode == 'fsk':
    print('Configuring fsk')
    
    set_confirm('radio set freq %s' % config.get('fsk', 'frequency'))
    print('frequency (freq): %s ' % config.get('fsk','frequency'))
    
    set_confirm('radio set pwr %s' % config.get('fsk', 'output_power'))
    print('output power (pwr): %s' % config.get('fsk', 'output_power'))
        
    set_confirm('radio set crc %s' % config.get('fsk', 'CRC_header'))
    print('CRC header (crc): %s' % config.get('fsk', 'CRC_header'))
    
    set_confirm('radio set wdt %s' % config.get('fsk', 'watchdog_timer'))
    print('Watchdog Timer (wdt): %s' % config.get('fsk', 'watchdog_timer'))
    
    set_confirm('radio set sync %s' % config.get('fsk', 'sync_word'))
    print('sync word (sync): %s' % config.get('fsk', 'sync_word'))
    
    
    set_confirm('radio set bt %s' % config.get('fsk', 'GFSK_shaping_factor'))
    print('GFSK Shaping Factor (bt): %s' % config.get('fsk', 'GFSK_shaping_factor'))
    
    set_confirm('radio set afcbw %s' % config.get('fsk', 'automatic_freq_corr_bandwidth'))
    print('Automatic Frequency Correction Bandwidth (afcbw): %s' % config.get('fsk', 'automatic_freq_corr_bandwidth'))
    
    set_confirm('radio set bitrate %s' % config.get('fsk', 'bitrate'))
    print('Bitrate (bitrate): %s' % config.get('fsk', 'bitrate'))
    
    set_confirm('radio set fdev %s' % config.get('fsk', 'freq_deviation'))
    print('Frequency Deviation (fdev): %s' % config.get('fsk', 'freq_deviation'))
    
    set_confirm('radio set prlen %s' % config.get('fsk', 'preamble_length'))
    print('Preamble Length (prlen): %s' % config.get('fsk', 'preamble_length'))
    
else:
    raise Exception('Invalid mode %s' % mode)


