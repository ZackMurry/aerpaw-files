#! /usr/bin/env python
# encoding: utf-8

from __future__ import print_function


from datetime import datetime
def current_milli_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


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
print(current_milli_time())
from pandas.lite import  DataFrame as df
print(current_milli_time())
from tabulate import tabulate

try:
    import queue
except ImportError:
    import Queue as queue


class ATException(Exception):
    pass

import argparse
parser = argparse.ArgumentParser(description="Usage: sudo python at_rm500q.py -p /dev/ttyUSB2")
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
        #self.events.put(line)
        if line.startswith('+'):
            self.events.put(line)
        elif line.startswith('OK'):
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

    def current_milli_time():
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

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
                        if response == outresponse:
                            return Real_response
                        else:
                            Real_response.append(response)
                    except queue.Empty:
                        raise ATException('AT command timeout ({!r})'.format(command))
            self._awaiting_response_for = None
            return Real_response

        def sleep_countdown(self, timer_count):
            while timer_count:
                mins, secs = divmod(timer_count, 60) ; timer = '{:02d}:{:02d}'.format(mins, secs)
                #print(timer, end='\r') ; sys.stdout.flush()
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
    connected_string  = "========" ; spaces = '='.join([''] * (int(columns) - len(connected_string) - 10)) ; empty_print = spaces ; print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), connected_string, empty_print, end="\n")

    with serial.threaded.ReaderThread(ser, RM500Q) as Quectel_module:
            #Intial check
            #Var_current_operator_status_and_mode = Quectel_module.command_with_event_response("AT+COPS?")
            #try:
            #    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Operator selected:", re.search(r"(?<=\+COPS\:...).*", Var_current_operator_status_and_mode[0]).group(0))
            #except:
            #    print("No operator registered ,refer logs, Quitting!!!")
            #    quit()

            ###################################
            #Serving cell Parameters

            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Serving cell Params", "\n")
            #Line2 Serving cell Params
            Line2_Part_LTE = ["servingcell","state","LTE","is_tdd","MCC","MNC","cellID","PCID","earfcn","freq_band","UL_bw","DL_bw","TAC","RSRP","RSRQ","RSSI","SINR","CQI","tx_power","srxlev"]
            Line2_Part1 = ["servingcell", "State"]
            Line2_Part2 = ["LTE", "is_TDD", "MCC","MNC","cellID","PCID","earfcn","freq_band","UL_bw","DL_bw","TAC","RSRP","RSRQ","RSSI","SINR","CQI", "tx_power", "srxlev"]
            Line2_Part3 = ["NR5G-NSA","MCC","MNC","PCID","RSRP","SINR","RSRQ","ARFCN","band","NR_DL_bw","scs"]
            
            Var_Serving_cell_string = Quectel_module.command_with_event_response("AT+QENG=\"servingcell\"")
            lst_Var_Serving_cell_string = Var_Serving_cell_string
            if (len(lst_Var_Serving_cell_string) == 1):
                #LTE mode
                Dict_Serving_cell_Line_LTE = OrderedDict(zip(Line2_Part_LTE, lst_Var_Serving_cell_string[0].split(",")))
                Dict_Serving_cell_Line_LTE_print = df.from_dict(Dict_Serving_cell_Line_LTE, orient='index').transpose()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_Serving_cell_Line_LTE_print,headers='keys', tablefmt='psql'), "\n")
            else:
                #ENDC mode
                Dict_Serving_cell_Line1 = OrderedDict(zip(Line2_Part1, lst_Var_Serving_cell_string[0].split(",")))
                Dict_Serving_cell_Line2 = OrderedDict(zip(Line2_Part2, lst_Var_Serving_cell_string[1].split(",")))
                Dict_Serving_cell_Line3 = OrderedDict(zip(Line2_Part3, lst_Var_Serving_cell_string[2].split(",")))

                Dict_Serving_cell_Line1_print = df.from_dict(Dict_Serving_cell_Line1, orient='index').transpose()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_Serving_cell_Line1_print,headers='keys', tablefmt='psql'), "\n")
                Dict_Serving_cell_Line2_print = df.from_dict(Dict_Serving_cell_Line2, orient='index').transpose()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_Serving_cell_Line2_print,headers='keys', tablefmt='psql'), "\n")
                Dict_Serving_cell_Line3_print = df.from_dict(Dict_Serving_cell_Line3, orient='index').transpose()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_Serving_cell_Line3_print,headers='keys', tablefmt='psql'), "\n")

            #Write to CSV Serving cell params
            Header_Servingcell_LTE = ["timestamp","servingcell","state","LTE","is_tdd","MCC","MNC","cellID","PCID","earfcn","freq_band","UL_bw","DL_bw","TAC","RSRP","RSRQ","RSSI","SINR","CQI","tx_power","srxlev"]
            Header_Servingcell_ENDC_Part1 = ["timestamp","servingcell", "State"]
            Header_Servingcell_ENDC_Part2 = ["LTE", "is_TDD", "LTE_MCC","LTE_MNC","LTE_cellID","LTE_PCID","LTE_earfcn","LTE_freq_band","LTE_UL_bw","LTE_DL_bw","LTE_TAC","LTE_RSRP","LTE_RSRQ","LTE_RSSI","LTE_SINR","LTE_CQI", "LTE_tx_power", "LTE_srxlev"]
            Header_Servingcell_ENDC_Part3 = ["NR5G-NSA","nr_MCC","nr_MNC","nr_PCID","nr_RSRP","nr_SINR","nr_RSRQ","nr_ARFCN","nr_band","NR_DL_bw","nr_scs"]
            Header_Servingcell_ENDC = Header_Servingcell_ENDC_Part1 + Header_Servingcell_ENDC_Part2 + Header_Servingcell_ENDC_Part3

            if (len(lst_Var_Serving_cell_string) == 1):
                Servingcell_LTE_params_Write = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")] ; Servingcell_LTE_params_Write = Servingcell_LTE_params_Write + Dict_Serving_cell_Line_LTE.values()
                Servingcell_LTE_Params_OrderedDict = OrderedDict(zip(Header_Servingcell_LTE, Servingcell_LTE_params_Write))
                with open('/root/Results/logs/csv_kpi/Serving_cell_Params_LTE_only.csv', 'a') as file_serving_lte:
                    writer = csv.DictWriter(file_serving_lte, fieldnames=Servingcell_LTE_Params_OrderedDict.keys(), delimiter=',')
                    writer.writerow(Servingcell_LTE_Params_OrderedDict)
                    file_serving_lte.close()
            else:
                Servingcell_ENDC_params_Write = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")] ; Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + Dict_Serving_cell_Line1.values()
                Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + Dict_Serving_cell_Line2.values() ; Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + Dict_Serving_cell_Line3.values()
                Servingcell_ENDC_Params_OrderedDict = OrderedDict(zip(Header_Servingcell_ENDC, Servingcell_ENDC_params_Write))
                with open('/root/Results/logs/csv_kpi/Serving_cell_Params_ENDC.csv', 'a') as file_serving_endc:
                    writer = csv.DictWriter(file_serving_endc, fieldnames=Servingcell_ENDC_Params_OrderedDict.keys(), delimiter=',')
                    writer.writerow(Servingcell_ENDC_Params_OrderedDict)
                    file_serving_endc.close()

            #################################

            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Neighbour cell Params", "\n")
            #Line3 Neighbour cell Params
            Line3_Part1 = ["neighbourcell intra","LTE","earfcn","PCID","RSRQ","RSRP","RSSI","SINR","srxlev","cell_resel_priority","s_non_intra_search","thresh_serving_lo","s_intra_search"]
            Line3_Part2 = ["neighbourcell inter","LTE","earfcn","PCID","RSRQ","RSRP","RSSI","SINR","srxlev","cell_resel_priority","threshX_low","threshX_high"]
            Var_Neighbour_cell_string = Quectel_module.command_with_event_response("AT+QENG=\"neighbourcell\"")
            lst_Var_Neighbour_cell_string = Var_Neighbour_cell_string
            for i in range (len(lst_Var_Neighbour_cell_string)):
                #print(lst_Var_Neighbour_cell_string[i]) ; 
                Dict_Neighbour_cell_Line = []
                if((re.search(r"(?<=intra).*",lst_Var_Neighbour_cell_string[i]))):
                    Dict_Neighbour_cell_Line = OrderedDict(zip(Line3_Part1, lst_Var_Neighbour_cell_string[i].split(",")))
                if((re.search(r"(?<=inter).*",lst_Var_Neighbour_cell_string[i]))):
                    Dict_Neighbour_cell_Line = OrderedDict(zip(Line3_Part2, lst_Var_Neighbour_cell_string[i].split(",")))
                Dict_Neighbour_cell_Line_print = df.from_dict(Dict_Neighbour_cell_Line, orient='index').transpose()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_Neighbour_cell_Line_print,headers='keys', tablefmt='psql'), "\n")

            #Write to CSV neighbour cell params
            Header_Neighbourcell_intra = ["timestamp","neighbourcell intra","LTE","earfcn","PCID","RSRQ","RSRP","RSSI","SINR","srxlev","cell_resel_priority","s_non_intra_search","thresh_serving_lo","s_intra_search"]
            Header_Neighbourcell_inter = ["timestamp","neighbourcell inter","LTE","earfcn","PCID","RSRQ","RSRP","RSSI","SINR","srxlev","cell_resel_priority","threshX_low","threshX_high"]
            for i in range (len(lst_Var_Neighbour_cell_string)):
                #print(lst_Var_Neighbour_cell_string[i]) ;
                Dict_Neighbour_cell_Line = []
                if((re.search(r"(?<=intra).*",lst_Var_Neighbour_cell_string[i]))):
                    Neighbour_cell_intra_params_Write = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")] ; Neighbour_cell_intra_params_Write_params_Write = Neighbour_cell_intra_params_Write + lst_Var_Neighbour_cell_string[i].split(",")
                    Dict_Neighbour_cell_Line = OrderedDict(zip(Header_Neighbourcell_intra, Neighbour_cell_intra_params_Write_params_Write))
                    with open('/root/Results/logs/csv_kpi/Neighbourcell_Params_intra_.csv', 'a') as file_neighbour_intra:
                        writer = csv.DictWriter(file_neighbour_intra, fieldnames=Dict_Neighbour_cell_Line.keys(), delimiter=',')
                        writer.writerow(Dict_Neighbour_cell_Line)
                        file_neighbour_intra.close()
                if((re.search(r"(?<=inter).*",lst_Var_Neighbour_cell_string[i]))):
                    Neighbour_cell_inter_params_Write = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")] ; Neighbour_cell_inter_params_Write_params_Write = Neighbour_cell_inter_params_Write + lst_Var_Neighbour_cell_string[i].split(",")
                    Dict_Neighbour_cell_Line = OrderedDict(zip(Header_Neighbourcell_inter, Neighbour_cell_inter_params_Write_params_Write))
                    with open('/root/Results/logs/csv_kpi/Neighbourcell_Params_inter_.csv', 'a') as file_neighbour_inter:
                        writer = csv.DictWriter(file_neighbour_inter, fieldnames=Dict_Neighbour_cell_Line.keys(), delimiter=',')
                        writer.writerow(Dict_Neighbour_cell_Line)
                        file_neighbour_inter.close()

            ##############################################
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Other Parameters", "\n")
            Line4_Part1 = ["+QENDC: endc_avl","plmn_info_list_r15_avl","endc_rstr","5G_basic"]
            Line4_Part2 = ["+QNWCFG: lte_csi","lte_mcs","lte_ri","lte_cqi","lte_pmi"]
            Line4_Part3 = ["+QNWCFG: nr5g_csi","nr_mcs","nr_ri","nr_cqi","nr_pmi"]
            Line4_Part4 = ["+QNWINFO: AcT","oper","band","channel"]

            Dict_ENDC_Line = OrderedDict(zip(Line4_Part1, Quectel_module.command_with_event_response("AT+QENDC")[0].split(",")))
            Dict_ENDC_print = df.from_dict(Dict_ENDC_Line, orient='index').transpose()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_ENDC_print,headers='keys', tablefmt='psql'), "\n")

            Dict_QNWCFG_LTE_CSI_Line = OrderedDict(zip(Line4_Part2, Quectel_module.command_with_event_response("AT+QNWCFG=\"lte_csi\"")[0].split(",")))
            Dict_QNWCFG_LTE_CSI_print = df.from_dict(Dict_QNWCFG_LTE_CSI_Line, orient='index').transpose()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_QNWCFG_LTE_CSI_print,headers='keys', tablefmt='psql'), "\n")

            Dict_QNWCFG_NR_Line = OrderedDict(zip(Line4_Part3, Quectel_module.command_with_event_response("AT+QNWCFG=\"nr5g_csi\"")[0].split(",")))
            Dict_QNWCFG_NR_print = df.from_dict(Dict_QNWCFG_NR_Line, orient='index').transpose()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_QNWCFG_NR_print,headers='keys', tablefmt='psql'), "\n")

            Var_QNWINFO = Quectel_module.command_with_event_response("AT+QNWINFO")
            Dict_QNWINFO_Line = OrderedDict(zip(Line4_Part4, Var_QNWINFO[0].split(",")))
            Dict_QNWINFO_print = df.from_dict(Dict_QNWINFO_Line, orient='index').transpose()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tabulate(Dict_QNWINFO_print,headers='keys', tablefmt='psql'), "\n")


            #Write to CSV basic & other params
            Basic_Param_and_Other_params_Write = [datetime.now().strftime("%Y/%m/%d %H:%M:%S")]
            Basic_Param_and_Other_params_Write = Basic_Param_and_Other_params_Write + Dict_ENDC_Line.values() ; Basic_Param_and_Other_params_Write = Basic_Param_and_Other_params_Write + Dict_QNWCFG_LTE_CSI_Line.values()
            Basic_Param_and_Other_params_Write = Basic_Param_and_Other_params_Write + Dict_QNWCFG_NR_Line.values() ; Basic_Param_and_Other_params_Write = Basic_Param_and_Other_params_Write + Dict_QNWINFO_Line.values()

            Header_Basic_and_other_params = ["timestamp","+QENDC: endc_avl","plmn_info_list_r15_avl","endc_rstr","5G_basic","+QNWCFG: lte_csi","lte_mcs","lte_ri","lte_cqi","lte_pmi","+QNWCFG: nr5g_csi","nr_mcs","nr_ri","nr_cqi","nr_pmi","+QNWINFO: AcT","oper","band","channel"]
            Basic_and_other_Params_OrderedDict = OrderedDict(zip(Header_Basic_and_other_params, Basic_Param_and_Other_params_Write))
            with open('/root/Results/logs/csv_kpi/Basic_and_Other_Params.csv', 'a') as file_basic:
                writer = csv.DictWriter(file_basic, fieldnames=Basic_and_other_Params_OrderedDict.keys(), delimiter=',')
                writer.writerow(Basic_and_other_Params_OrderedDict)
                file_basic.close()

            #######################################################

    disconnected_string  = "=====";spaces = '='.join([''] * (int(columns) - len(disconnected_string) - 7))
    empty_print = spaces ; print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "\n", disconnected_string, empty_print)
