#!/bin/bash
pkill srsue
pkill python3
pkill iperf3
sleep 15
ip link delete tun0
ip link delete tun
ip link delete tun_srsue

