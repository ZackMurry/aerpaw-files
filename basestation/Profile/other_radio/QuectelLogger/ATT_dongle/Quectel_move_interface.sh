#!/bin/bash
# Example : sudo ./Quectel_move_interface.sh



IPprefix_by_netmask() {
    #function returns prefix for given netmask in arg1
    bits=0
    for octet in $(echo $1| sed 's/\./ /g'); do
         binbits=$(echo "obase=2; ibase=10; ${octet}"| bc | sed 's/0//g')
         let bits+=${#binbits}
    done
    #echo "/${bits}"
}

CONTAINER=E-VM-X0104-M1
HOST_DEV=wwanQ
GUEST_DEV=test

/sbin/ifconfig | grep -Po '(?<=\binet )[^/]+/\w+|(?<=\binet6 )[^/]+/\w+'
Assigned_address=$(sudo /sbin/ifconfig wwanQ | grep -w inet |awk '{print $2}')
Assigned_subnet=$(sudo /sbin/ifconfig wwanQ | grep -w inet |awk '{print $4}')
echo $Assigned_address
echo $Assigned_subnet
IPprefix_by_netmask ${Assigned_subnet}
Mask="/${bits}"
echo $Mask
#Assigned_address="10.169.254.32"
#Mask="/26"

echo "Get docker PID and move interface into the docker netns"
PID=$(sudo docker inspect -f '{{.State.Pid}}' $CONTAINER)

sudo ln -s /proc/$PID/ns/net /var/run/netns/$PID

sudo ip link set $HOST_DEV netns $PID name $GUEST_DEV

echo "Bring up the interface on the container and assign address"
echo ${Assigned_address}${Mask}
sudo ip netns exec $PID ip addr add $Assigned_address$Mask dev $GUEST_DEV

sudo ip netns exec $PID ip link set $GUEST_DEV up

#Routes

sudo rm /var/run/netns/$PID
