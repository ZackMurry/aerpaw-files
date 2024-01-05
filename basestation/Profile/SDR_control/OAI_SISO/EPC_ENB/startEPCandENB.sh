#!/bin/bash

# MODE is either IQ_EMULATION, or PL_EMULATION, or TESTBED
#MODE=IQ_EMULATION
MODE=$1
EXEC_PATH=/opt/openairinterface5g/cmake_targets/lte_build_oai/build/lte-softmodem
CONFIG_PATH=/opt/openairinterface5g/ci-scripts/conf_files/enb.band7.tm1.100PRB.usrpb210.conf

if [ $MODE == "TESTBED" ]
then
  mkdir /dev/net
  mknod /dev/net/tun c 10 200
  ip tuntap add mode tun srs_spgw_sgi
  ifconfig srs_spgw_sgi 172.16.0.1/24
screen -S EPC -dm bash -c "srsepc | ts '[%Y-%m-%d %H:%M:%.S]' | tee srsEPC.log"

screen -S eNB -dm bash -c "$EXEC_PATH -O $CONFIG_PATH |  ts '[%Y-%m-%d %H:%M:%sS]' | tee OAI_ENB.log"
#elif [ $MODE == "IQ_EMULATION" ]
#then
#  mkdir /dev/net
#  mknod /dev/net/tun c 10 200
#  ip tuntap add mode tun srs_spgw_sgi
#  ifconfig srs_spgw_sgi 172.16.0.1/24
#  srsepc &
#  ./$EXEC_PATH -O $CONFIG_PATH &
#elif [ $MODE == "IQ_DIRECT" ]
#then
#  mkdir /dev/net
#  mknod /dev/net/tun c 10 200
#  ip tuntap add mode tun srs_spgw_sgi
#  ifconfig srs_spgw_sgi 172.16.0.1/24
#  srsepc &
#  ./$EXEC_PATH -O ~/$CONFIG_PATH  &
elif [ $MODE == "PL_EMULATION" ]
then

  screen -S zmqtun -dm bash -c "python3 zmq_tun.py -c -i ${CHEM_IP_ADDR} -p 5001 -t 172.16.0.1 -n tun "
 sleep 60
 screen -S ping -dm bash -c "ping -w 60 192.168.200.2 | ts '[%Y-%m-%d %H:%M:%.S]' > ping.log"

elif [ $MODE == "PL_DIRECT" ]
then
  screen -S zmqtun -dm bach -c "python3 zmq_tun.py -s -p 5002 -t 172.16.0.1 -n tun"

else
  echo "No mode specified"


fi
