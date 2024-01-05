#!/bin/bash
#
# This script will start an srsLTE EPC process
#

mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun srs_spgw_sgi
ip link set dev srs_spgw_sgi mtu 1500
ifconfig srs_spgw_sgi 172.16.0.1/24

srsepc
