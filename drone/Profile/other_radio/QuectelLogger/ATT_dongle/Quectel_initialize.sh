#!/bin/bash
# Example : sudo ./Quectel_initialize.sh

echo "Try to connect Quectel"
Out_Quectel_Modem_number_ATT_sim=$(sudo mmcli -L | pcregrep -o1 -i 'ModemManager\d\/Modem\/(\d+).\[Quectel')
if [ -z ${Out_Quectel_Modem_number_ATT_sim+x} ]; then echo "Quectel Modem not found cannot find index"; else echo "Quectel Modem found, Index = '$Out_Quectel_Modem_number_ATT_sim'"; fi

# Get port
AT_Port=$(ls /dev/ttyUSB* | pcregrep -o1 -i 'USB(\d+)' | sort -nr | head -n1)

set -e
# configure port, exit immediately, don't reset
device_at=/dev/ttyUSB${AT_Port}

echo "Initialize Quectel modem"
sudo screen -d -m -S new $device_at 115200
sudo screen -S new -X stuff 'AT+QCFG=\"usbnet\",2\r'
sudo screen -S new -X stuff 'AT+QPOWD\r'
