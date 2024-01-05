#!/bin/bash
# Example : sudo ./ATT_Dongle_start.sh

unset Out_ATT_Modem_number; unset Out_ATT_Modem_Interface ; unset inet_set_ip ; unset Assigned_IP_address

#Connect ATT Dongle
echo "Try to connect ATT dongle"
Out_ATT_Modem_number=$(sudo mmcli -L | pcregrep -o1 -i 'ModemManager\d\/Modem\/(\d+).\[Sierra.Wireless')
#if [ -z ${Out_ATT_Modem_number+x} ]; then echo "ATT Modem not found cannot find index"; else echo "ATT Modem found, Index = '$Out_ATT_Modem_number'"; fi
if [[ -z "${Out_ATT_Modem_number// }" ]]; then echo "ATT Modem not found cannot find index, debug at sudo mmcli -L"; exit ; else echo "ATT Modem found, Index = '$Out_ATT_Modem_number'"; fi
#echo "ATT Modem number $Out_ATT_Modem_number"
bash -c "sudo mmcli -m $Out_ATT_Modem_number --simple-connect=\"apn=Broadband\""

# Get interface info
sleep 10
Out_ATT_Modem_Interface=$(sudo mmcli -m $Out_ATT_Modem_number | pcregrep -o1 -i '\:\s(.+?)(?=\s\(net\))')
echo $Out_ATT_Modem_Interface

#DHCP
echo "Wait until dhcp client assigns IP"
bash -c "sudo udhcpc -i $Out_ATT_Modem_Interface"
inet_set_ip=$(ifconfig $Out_ATT_Modem_Interface | grep -P 'inet\s')
set=0
until [ $set -gt 1 ]
do
        if [ -z ${inet_set_ip+x} ]; then echo "No address assigned by DHCP service yet"; else set=2; fi
        sleep 2
        inet_set_ip=$(ifconfig $Out_ATT_Modem_Interface | grep -P 'inet\s')
done
sleep 30
Assigned_IP_address=$(ifconfig $Out_ATT_Modem_Interface | pcregrep -o1 -i 'inet\s(\d+\.\d+\.\d+\.\d+)')
echo "IP address assigned by DHCP"
echo $Out_ATT_Modem_Interface $Assigned_IP_address
