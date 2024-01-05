#!/bin/bash
#
# This script will start an iperf client to the specified destination
#
#Example: ./startIperfClient_UL.sh <Source IP> <Destination IP> <port def 5201>
#
log_file="Iperf_client_UL_log_$(date +"%Y_%m_%d_%H\:%M\:%S").log"
# Checking the connection via ping to server until it gets it
while ((1)) ; do 
  echo "Looking for connection..."
  ping $2 -c 1 -W 1 -I $1 >& /dev/null
  rv=$?;
  if (test $rv -eq 0); then
     echo "Got it"
     break;
  fi
  sleep 1;
done

# total transmit time (in seconds)
#IPERF_DURATION="${IPERF_DURATION:-300}" # seconds
IPERF_DURATION=300

# Destination IP address
#DESTINATION_IP="${DESTINATION_IP:-'172.16.0.1'}"


# add -u to use UDP instead of the default TCP 
# add -R to use reverse direction (from server to client)

#iperf3 -c $DESTINATION_IP -t $IPERF_DURATION



bash -c "stdbuf -oL -eL iperf3 -c $2 -t $IPERF_DURATION -B $1 -p $3\
	| ts | tee log/$log_file"
