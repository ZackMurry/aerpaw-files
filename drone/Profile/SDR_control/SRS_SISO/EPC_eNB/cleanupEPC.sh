#!/bin/bash

pkill srsepc
pkill srsenb
pkill python3
pkill iperf3
sleep 5
ip link delete tun0
ip link delete srs_spgw_sgi
ip link delete tun
