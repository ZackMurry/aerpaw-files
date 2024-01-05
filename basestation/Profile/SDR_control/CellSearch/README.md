# Cell Search

There are 2 version for cell search. SRSLTE changed it's name(libraries and code itself) to SRSRAN. Therefore, 2 version of cell search code available on this folder. Instructions are same for both of them.

## Instructions for Build

Before starting anything you should check for which SRS(SRSLTE/SRSRAN) is installed on your system.  

```
cd srslte-version
```

After changing directory, you can build the code as shown below.

```
mkdir build && cd build
cmake ../
make -j${nproc}
```
or
```
./start_cellsearch.sh -m BUILD
```

## USAGE

There is 2 mode in the cell search. These are;

* TESTBED 
* EMULATION-TX
* EMULATION-RX

After choosing which mode you are going to use, you can start the cell search shown as below;
```
./start_cellsearch.sh -m <MODE> -b <BAND> -s <EARFCN_START> -e <EARFCN_END> -g <RX_GAIN>
```
Example
```
./start_cellsearch.sh -m TESTBED -s 5230 -e 5231 -b 13 -g 40
```

After executing the command, output folder is going to be created. The log files are going to be created under the output folder with {year-month-day-hour:minute}.txt format.

For emulation,
```
./start_cellsearch.sh -m <MODE> -b <BAND> -s  -c <CONFIG_FILE> -t <TX_POWER> -p <CHEM_PORT> -r <RX_PORT> -c <CHEM_IP_ADDRESS>
```
Example
```
./start_cellsearch.sh EMULATION-TX -b 2 -t 70 -p 4700 -c
```
Note: Earfcn_start and Earfcn_end is ignored at emulation.