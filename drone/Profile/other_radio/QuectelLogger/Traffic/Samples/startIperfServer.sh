#!/bin/bash
#
# This script will start an iperf server 
#
# Example -  ./startIperfServer.sh 10.195.114.31
# add -u to use UDP instead of the default TCP 
log_file="Iperf_server_log_$(date +"%Y_%m_%d_%H\:%M\:%S").log"
#iperf3 -s
bash -c "stdbuf -oL -eL iperf3 -s -B $1 | tee log/$log_file"
