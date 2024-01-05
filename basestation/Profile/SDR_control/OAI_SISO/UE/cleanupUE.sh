#!/bin/bash
pkill srsue
pkill python3
sleep 15
ip link delete tun0
ip link delete tun
ip link delete tun_srsue

