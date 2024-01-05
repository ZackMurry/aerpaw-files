Linux Setup and Connection

    1. Connect Quectel Modem and AT&T dongle
    2. Download Quectel directory from AERPAW github repository (Quectel github repo link )
    3. Install all dependencies
    4. Initially Quectel module serial port will be controlled/taken lock by ModemManager service and we have to take control from ModemManager(mm)
    5. sudo vim /etc/udev/rules.d/70-snap.modem-manager.rules   &&    sudo vim /etc/udev/rules.d/77-mm-usb-device-blacklist.rules
    6. Add this line to the files above
       ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_DEVICE_IGNORE}="1"

ACTION!="add|change", GOTO="mm_tty_blacklist_end"
ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_DEVICE_IGNORE}="1"
ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_PORT_IGNORE}="0"
ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_PORT_IGNORE}="1"
ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_PORT_IGNORE}="2"
ATTRS{idVendor}=="2c7c" ATTRS{idProduct}=="0800", ENV{ID_MM_PORT_IGNORE}="3"
LABEL="mm_tty_blacklist_end"




       (This is done to make sure mm does not take lock on serial ports again and Network manager will handle it further, and therefore Quectel modem will be considered as a USB ethernet module for all future references as shown in the further steps)
    7. sudo udevadm control --reload (to set the above new rule)
       sudo udevadm trigger 
    8. sudo usermod -a -G dialout $USER 
    9. Restart computer and reconnect Quectel modem
    10. Check ifconfig and see 2 interfaces are created 1 for AT&T dongle and another for Quectel modem (See picture above)
    11. Quectel modem will be considered as a USB ethernet device and AT&T dongle will be the only Mobile broadband as shown in pictures above
    12. ping 8.8.8.8 from both interfaces and check if its working (enp0s20f0u5i4 and wwan0 might change)
          ping 8.8.8.8 -I enp0s20f0u5i4     Quectel Modules (or or 192.168.89.3 (Ericsson BS))  
          ping 8.8.8.8 -I wwan0                        AT&T Dongle
    13. Check List of modems and only AT&T dongle should show up
          aerpawops@SPN1:~$ sudo mmcli -L
          [sudo] password for aerpawops:
          /org/freedesktop/ModemManager1/Modem/0 [Sierra Wireless, Incorporated] AirCard 340U
    14. Check this command on terminal -picocom -b 115200 /dev/ttyUSB2. If everything is set right we should not see resource busy or no permission errors.     15. Exit Picocom Ctrl+a and then Ctrl+q
    16. Run executable---> ./start_UE_Quectel.sh
    17. sudo snap set system refresh.metered=hold


Example output:

aerpawops@SPN1:~/Downloads/Quectel_UE$ ./start_UE_Quectel.sh 
Ctrl-Z or Ctrl-C to stop
2022-10-21 17:13:11 ========CONNECTED =====================================================================================================================================================
 Quectel RM500Q-GL Revision: RM500QGLABR11A02M4G  IMEI: 863305040266776 IMSI: 310030007085430
2022-10-21 17:13:13  Operator selected: 0,"AT&T",7 : Network already selected, Re-registration not required
2022-10-21 17:13:15 Enter logging state
2022-10-21 17:13:15 BASIC Params
2022-10-21 17:13:23   CREG: 0,1 CSQ: 16,99 QSPN: "AT&T","AT&T","",0,"310410"


2022-10-21 17:13:23 Serving cell Params 

2022-10-21 17:13:25 +----+----------------------+----------+
|    | servingcell          | State    |
|----+----------------------+----------|
|  0 | +QENG: "servingcell" | "NOCONN" |
+----+----------------------+----------+ 

2022-10-21 17:13:25 +----+--------------+----------+-------+-------+----------+--------+----------+-------------+---------+---------+-------+--------+--------+--------+--------+-------+------------+----------+
|    | LTE          | is_TDD   |   MCC |   MNC | cellID   |   PCID |   earfcn |   freq_band |   UL_bw |   DL_bw | TAC   |   RSRP |   RSRQ |   RSSI |   SINR |   CQI |   tx_power | srxlev   |
|----+--------------+----------+-------+-------+----------+--------+----------+-------------+---------+---------+-------+--------+--------+--------+--------+-------+------------+----------|
|  0 | +QENG: "LTE" | "FDD"    |   310 |   410 | BA23A09  |    492 |      950 |           2 |       5 |       5 | 270B  |   -113 |    -12 |    -80 |     14 |     0 |        230 | -        |
+----+--------------+----------+-------+-------+----------+--------+----------+-------------+---------+---------+-------+--------+--------+--------+--------+-------+------------+----------+ 

2022-10-21 17:13:25 +----+------------------+-------+-------+--------+--------+--------+--------+
|    | NR5G-NSA         |   MCC |   MNC |   PCID |   RSRP |   SINR |   RSRQ |
|----+------------------+-------+-------+--------+--------+--------+--------|
|  0 | +QENG:"NR5G-NSA" |   310 |   410 |  65535 | -32768 | -32768 | -32768 |
+----+------------------+-------+-------+--------+--------+--------+--------+ 

2022-10-21 17:13:25 Neighbour cell Params 

2022-10-21 17:13:27 +----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------+
|    | neighbourcell intra          | LTE   |   earfcn |   PCID |   RSRQ |   RSRP |   RSSI |   SINR | srxlev   | cell_resel_priority   | s_non_intra_search   | thresh_serving_lo   | s_intra_search   |
|----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------|
|  0 | +QENG: "neighbourcell intra" | "LTE" |      950 |    492 |    -13 |   -110 |    -77 |      0 | -        | -                     | -                    | -                   | -                |
+----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------+ 

2022-10-21 17:13:27 +----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------+
|    | neighbourcell intra          | LTE   |   earfcn |   PCID |   RSRQ |   RSRP |   RSSI |   SINR | srxlev   | cell_resel_priority   | s_non_intra_search   | thresh_serving_lo   | s_intra_search   |
|----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------|
|  0 | +QENG: "neighbourcell intra" | "LTE" |      950 |    359 |    -20 |   -119 |    -88 |      0 | -        | -                     | -                    | -                   | -                |
+----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+----------------------+---------------------+------------------+ 

2022-10-21 17:13:27 +----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+
|    | neighbourcell inter          | LTE   |   earfcn |   PCID |   RSRQ |   RSRP |   RSSI |   SINR | srxlev   | cell_resel_priority   | threshX_low   | threshX_high   |
|----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------|
|  0 | +QENG: "neighbourcell inter" | "LTE" |     5330 |    325 |    -14 |   -110 |    -86 |      0 | -        | -                     | -             | -              |
+----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+ 

2022-10-21 17:13:27 +----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+
|    | neighbourcell inter          | LTE   |   earfcn |   PCID |   RSRQ |   RSRP |   RSSI |   SINR | srxlev   | cell_resel_priority   | threshX_low   | threshX_high   |
|----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------|
|  0 | +QENG: "neighbourcell inter" | "LTE" |    67086 |      4 |    -12 |   -115 |    -92 |      0 | -        | -                     | -             | -              |
+----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+ 

2022-10-21 17:13:27 +----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+
|    | neighbourcell inter          | LTE   |   earfcn |   PCID |   RSRQ |   RSRP |   RSSI |   SINR | srxlev   | cell_resel_priority   | threshX_low   | threshX_high   |
|----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------|
|  0 | +QENG: "neighbourcell inter" | "LTE" |    67086 |     40 |    -19 |   -122 |    -92 |      0 | -        | -                     | -             | -              |
+----+------------------------------+-------+----------+--------+--------+--------+--------+--------+----------+-----------------------+---------------+----------------+ 

2022-10-21 17:13:27 Other Parameters 

2022-10-21 17:13:29 +----+--------------------+--------------------------+-------------+------------+
|    | +QENDC: endc_avl   |   plmn_info_list_r15_avl |   endc_rstr |   5G_basic |
|----+--------------------+--------------------------+-------------+------------|
|  0 | +QENDC: 1          |                        1 |           1 |          0 |
+----+--------------------+--------------------------+-------------+------------+ 

2022-10-21 17:13:31 +----+--------------------+-----------+----------+-----------+-----------+
|    | +QNWCFG: lte_csi   |   lte_mcs |   lte_ri |   lte_cqi |   lte_pmi |
|----+--------------------+-----------+----------+-----------+-----------|
|  0 | +QNWCFG: "lte_csi" |         0 |        2 |        11 |        12 |
+----+--------------------+-----------+----------+-----------+-----------+ 

2022-10-21 17:13:33 +----+---------------------+----------+---------+----------+----------+
|    | +QNWCFG: nr5g_csi   |   nr_mcs |   nr_ri |   nr_cqi |   nr_pmi |
|----+---------------------+----------+---------+----------+----------|
|  0 | +QNWCFG: "nr5g_csi" |        0 |       0 |        0 |        0 |
+----+---------------------+----------+---------+----------+----------+ 

2022-10-21 17:13:33 +----+---------------------+----------+--------------+-----------+
|    | +QNWINFO: AcT       | oper     | band         |   channel |
|----+---------------------+----------+--------------+-----------|
|  0 | +QNWINFO: "FDD LTE" | "310410" | "LTE BAND 2" |       950 |
+----+---------------------+----------+--------------+-----------+ 

2022-10-21 17:13:33 
 =====DISCONNECTED ========================================================================================================================================================
Ctrl-Z or Ctrl-C to stop
