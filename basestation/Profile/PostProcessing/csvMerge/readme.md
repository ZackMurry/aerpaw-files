# How to use log2csv

First of all, you need to have required packages to run the log2csv.py.
To install these packages,

```
pip install argparse pandas
```

## Usage
After installing the required packages, the log2csv can be executes as shown below,
```
python log2csv.py [logFileName].txt -m MODE -o OutputFileName.csv

Arguments:
-m or --mode argument for choosing which kind of log file is going to be parsed. Options are:
ue, enb, epc, ping, iperfServer, iperfClient, cellSearch, vehicleLog, vehicleOut
-o or --output argument for output file name

Sample usage

python log2csv.py 2021-11-22_11:10:47_radio_log.txt -m ue -o testUe.csv
```