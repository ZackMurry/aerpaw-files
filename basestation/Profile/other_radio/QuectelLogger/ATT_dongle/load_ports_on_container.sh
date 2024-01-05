#!/bin/bash
Ports=$(ls /dev/ttyUSB* | pcregrep -o1 -i 'USB(\d+)')
for i in $Ports
	do sudo docker exec E-VM-X0104-M1 mknod /dev/ttyUSB$i c 188 $i
done
