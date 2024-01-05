#!/usr/bin/python3
import argparse
import sys
import pandas as pd
from datetime import datetime


def parseArgs():

    parser = argparse.ArgumentParser(description='Generate CSV from log file.')
    parser.add_argument('logfile', type=str,
                        help='Log file for CSV')
    parser.add_argument('-m','--mode', choices=['ue','enb','epc','ping','iperfClient','iperfServer','cellSearch','vehicleLog','vehicleOut','gnuradioOctave','gnuradioOfdm'], 
                        help='Mode for parsing')
    parser.add_argument('-o','--output', type=str, default=sys.stdout,
                        help='output file for csv, default is ')
    
    return parser.parse_args()

class LogParser:
    def __init__(self, logFile, outputFname):
        self.outputFname = outputFname
        with open(logFile) as f:
            self.raw = f.readlines()
        self.data = {}
    
    def parse_cellSearch(self):
        self.data = {
            "time":[],
            "Freq": [],
            "EARFCN":[],
            "PHYID": [],
            "PRB":[],
            "Ports":[],
            "PSS":[],
            "PSR":[]
        }
        try:
            for l in self.raw[1:]:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = (" ".join(l.split("]")[1:])).split(",")
 
                self.data["time"].append(ts)
                self.data["Freq"].append(dt[dt.index(" Found CELL MHz")+1])
                self.data["EARFCN"].append(dt[dt.index("  EARFCN")+1])
                self.data["PHYID"].append(dt[dt.index(" PHYID")+1])
                self.data["PRB"].append(dt[dt.index(" PRB")+1])
                self.data["Ports"].append(dt[dt.index("  ports")+1])
                self.data["PSS"].append(dt[dt.index(" PSS power dB")+1])
                self.data["PSR"].append(dt[dt.index("  PSR")+1])

        except Exception as e:
            print("Error parsing cell search log file: ", e)

    def parse_ue(self):
        self.data = {
            "time":[],
            "cc": [],
            "pci":[],
            "rsrp": [],
            "pl":[],
            "cfo":[],
            "mcsDl":[],
            "snr":[],
            "turbo":[],
            "brateDl":[],
            "blerDl":[],
            "ta_us":[],
            "mcsUl":[],
            "buff":[],
            "brateUl":[],
            "blerUl":[]
        }
        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1], "%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[1][:-1].split(" ")
                
                dt = [i for i in dt if '' != i]
                if len(dt) == 15 and dt[0] != "cc" and dt[0] != "Current":
                    self.data["time"].append(ts)
                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+1]].append(j)

        except Exception as e:
            print("Error parsing UE log file: ", e)

    def parse_enb(self):
        self.data = {
            "time":[],
            "rnti":[],
            "cqi":[],
            "ri":[],
            "mcsDl":[],
            "brateDl":[],
            "okDl":[],
            "nokDl":[],
            "(%)Dl":[],
            "snr":[],
            "phr":[],
            "mcsUl":[],
            "brateUl":[],
            "okUl":[],
            "nokUl":[],
            "(%)Ul":[],
            "bsr":[]
        }
        ## Multi User case??
        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[1][:-1].split(" ")
                
                dt = [i for i in dt if '' != i]
                if len(dt) == 16 and dt[0] != "rnti":
                    self.data["time"].append(ts)
                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+1]].append(j)

        except Exception as e:
            print("Error parsing ENB log file: ", e)

    def parse_epc(self):
        # There are too much diverse data. Therefore, I parsed it without any filtering
        self.data = {
            "time":[],
            "log":[]
        }
        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[1].replace("\n","")
                if dt and not dt.isspace():
                    self.data["time"].append(ts)
                    self.data["log"].append(dt)
                
        except Exception as e:
            print("Error parsing EPC log file: ", e)

    def parse_ping(self):
        self.data = {
            "time":[],
            "size(byte)":[],
            "destination":[],
            "icmp_seq":[],
            "ttl":[],
            "pingtime":[]
        }

        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[1].replace("\n","")
                
                if "icmp_seq" in dt:
                    dt = dt.split(" ")[1:-1]
                    dt.remove("bytes");dt.remove("from")
                    dt = [i for i in dt if '' != i]
                    self.data["time"].append(ts)
                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+1]].append(j.split("=")[-1])
                        if index == len(dt) - 1:
                            self.data[list(self.data.keys())[index+1]][-1] += l[-3:-1].strip()
                             
                        
        except Exception as e:
            print("Error parsing Ping log file: ", e)

    def parse_iperfServer(self):
        self.data = {
            "time":[],
            "ID":[],
            "Interval(sec)":[],
            "Transfer(MBytes)":[],
            "Bandwidth(MBits/sec)":[]
        }
        try:
            for l in self.raw:
                if "- - - - - - - -" in l:
                    break
                
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[-1].replace("\n","").split(" ")
                if "sec" in dt or "MBytes" in dt:
                    dt = [i for i in dt if '' != i]
                    self.data["ID"].append(l.split("]")[1].split("[")[1].strip())
                    self.data["time"].append(ts)
                    
                    dt.remove("sec") if "sec" in dt else None
                    dt.remove("MBytes") if "MBytes" in dt else None
                    dt.remove("MBytes") if "MBytes" in dt else None
                    dt.remove("Mbits/sec") if "Mbits/sec" in dt else None
                    dt.remove("Kbits/sec") if "Kbits/sec" in dt else None
                    dt.remove("KBytes") if "KBytes" in dt else None
                    dt.remove("KBytes") if "KBytes" in dt else None

                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+2]].append(j)
        except Exception as e:
            print("Error parsing iperf log file: ", e)

    def parse_iperfClient(self):
        self.data = {
            "time":[],
            "ID":[],
            "Interval(sec)":[],
            "Transfer(MBytes)":[],
            "Bandwidth(MBits/sec)":[],
            "Retr":[],
            "Cwnd(KBytes)":[]
        }
        try:
            for l in self.raw:

                if "- - - - - - - -" in l:
                    break

                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[-1].replace("\n","").split(" ")
                
                if "sec" in dt or "MBytes" in dt or "KBytes" in dt :
                    dt = [i for i in dt if '' != i]
                    self.data["ID"].append(l.split("]")[1].split("[")[1].strip())
                    self.data["time"].append(ts)
                    
                    dt.remove("sec") if "sec" in dt else None
                    dt.remove("MBytes") if "MBytes" in dt else None
                    dt.remove("MBytes") if "MBytes" in dt else None
                    dt.remove("Mbits/sec") if "Mbits/sec" in dt else None
                    dt.remove("Kbits/sec") if "Kbits/sec" in dt else None
                    dt.remove("KBytes") if "KBytes" in dt else None
                    dt.remove("KBytes") if "KBytes" in dt else None

                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+2]].append(j)
        except Exception as e:
            print("Error parsing iperf log file: ", e)

    def parse_vehicleLog(self):
        self.data = {
            "time":[],
            "log":[]
        }
        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[1].replace("\n","")
                if dt and not dt.isspace():
                    self.data["time"].append(ts)
                    self.data["log"].append(dt)

        except Exception as e:
            print("Error parsing Vehicle log file: ", e)

    def parse_vehicleOut(self):
        self.data = {
            "num":[],
            "Longitude":[],
            "Latitude":[],
            "Altitude":[],
            "Volt":[],
            "Battery Level": [],
            "time":[],
            "Fix":[],
            "Number of Satellite":[]
        }
        try:
            for l in self.raw:
                dt = l.replace("\n","").split(",")

                t_ind = 5
                if len(dt) >= 8:
                    t_ind = 6
                for index, j in enumerate(dt):
                    if t_ind == 5:
                        self.data[list(self.data.keys())[index]].append(datetime.strptime(j, "%Y-%m-%d %H:%M:%S.%f"))
                    else:
                        self.data[list(self.data.keys())[index]].append(j)

        except Exception as e:
            print("Error parsing Vehicle Out log file: ", e)

    def parse_gnuradioOctave(self):
        self.data = {
            "time":[],
            "Measurement No":[],
            "Power in dB":[]
        }
        try:
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[-1].replace("\n","").split(" ")

                if "measurement" in dt:
                    dt = [i for i in dt if '' != i]
                    self.data["time"].append(ts)

                    dt.remove("ans") if "ans" in dt else None
                    dt.remove("=") if "=" in dt else None
                    dt.remove("measurement") if "measurement" in dt else None
                    dt.remove("no:") if "no:" in dt else None
                    dt.remove("Power") if "Power" in dt else None
                    dt.remove("in") if "in" in dt else None
                    dt.remove("dB:") if "dB:" in dt else None

                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+1]].append(j)
        except Exception as e:
            print("Error parsing Gnuradio Octave log file: ", e)

    def parse_gnuradioOfdm(self):
        self.data = {
            "time":[],
            "Offset":[],
            "Source":[],
            "Key":[],
            "Value":[]
        }
        try:
            parseInd = 0
            for l in self.raw:
                ts = datetime.strptime(l.split("]")[0].split("[")[1],"%Y-%m-%d %H:%M:%S.%f")
                dt = l.split("]")[-1].replace("\n","")
                if "Tag Debug: Rx Bytes with SNR" in dt or "Input Stream:" in dt:
                    if parseInd != 2:
                        parseInd += 1
                        continue
                
                if parseInd == 2:
                    dt = dt.split(" ")
                    dt = [i for i in dt if '' != i]
                    self.data["time"].append(ts)
                
                    dt.remove("Offset:") if "Offset:" in dt else None
                    dt.remove("Source:") if "Source:" in dt else None
                    dt.remove("Key:") if "Key:" in dt else None
                    dt.remove("Value:") if "Value:" in dt else None

                    for index, j in enumerate(dt):
                        self.data[list(self.data.keys())[index+1]].append(j)
                    parseInd = 0
        except Exception as e:
            print("Error parsing Gnuradio OFDM log file: ", e)
 
    def exportCsv(self):
        try:
            csvDf = pd.DataFrame.from_dict(self.data)
            csvFName = self.outputFname if ".csv" in self.outputFname else self.outputFname + ".csv"
            csvDf.to_csv(csvFName, index=False)
        except Exception as e:
            print("Error generating CSV: ",e)




def main():
    args = parseArgs()
    
    parser =  LogParser(args.logfile, args.output)
    getattr(parser, "parse_"+args.mode)()
    parser.exportCsv()


if __name__ == '__main__':
    main()
