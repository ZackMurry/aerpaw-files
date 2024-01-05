#!/bin/bash
# Example : sudo ./Quectel_mbim_start_att.sh


echo "Try to connect Quectel to ATT network"
Out_Quectel_Modem_number_ATT_sim=$(sudo mmcli -L | pcregrep -o1 -i 'ModemManager\d\/Modem\/(\d+).\[Quectel')
if [ -z ${Out_Quectel_Modem_number_ATT_sim+x} ]; then echo "Quectel Modem not found cannot find index"; else echo "Quectel Modem found, Index = '$Out_Quectel_Modem_number_ATT_sim'"; fi
bash -c "sudo mmcli -m $Out_Quectel_Modem_number_ATT_sim --simple-connect=\"apn=Broadband\""

sleep 15
Out_Quectel_Modem_Interface=$(sudo mmcli -m $Out_Quectel_Modem_number_ATT_sim | pcregrep -o1 -i '\,\s(.+?)(?=\s\(net\))')
if [[ -z "${Out_Quectel_Modem_Interface// }" ]]; then echo "1" ; Out_Quectel_Modem_Interface=$(sudo mmcli -m $Out_Quectel_Modem_number_ATT_sim | pcregrep -o1 -i '\:\s(.+?)(?=\s\(net\))') ; fi
echo $Out_Quectel_Modem_Interface
echo "Wait until dhcp client assigns IP"
bash -c "sudo udhcpc -i $Out_Quectel_Modem_Interface"
inet_set_ip=$(ifconfig $Out_Quectel_Modem_Interface | grep -P 'inet\s')
set=0
until [ $set -gt 1 ]
do
	if [ -z ${inet_set_ip+x} ]; then echo "No address assigned by DHCP service yet"; else set=2; fi
	sleep 2
	inet_set_ip=$(ifconfig $Out_Quectel_Modem_Interface | grep -P 'inet\s')
done
sleep 50

Assigned_IP_address=$(ifconfig $Out_Quectel_Modem_Interface | pcregrep -o1 -i 'inet\s(\d+\.\d+\.\d+\.\d+)')
echo "IP address assigned by DHCP"
echo $Out_Quectel_Modem_Interface $Assigned_IP_address
echo "Changing Interface name"
sleep 10
bash -c "sudo ifconfig $Out_Quectel_Modem_Interface down"
#bash -c "sudo ip link delete $Out_Quectel_Modem_Interface name wwanQ"
bash -c "sudo ip link set $Out_Quectel_Modem_Interface name wwanQ"
bash -c "sudo ifconfig wwanQ up"
echo "Interface name changed to wwanQ on purpose from" $Out_Quectel_Modem_Interface
#bash -c "sudo udhcpc -i wwanQ"
