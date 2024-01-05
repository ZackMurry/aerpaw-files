#!/bin/bash

screen -S iperf3 -dm bash -c "iperf3 -c 172.16.0.1 -t 300 -R  | ts '[%Y-%m-%d %H:%M:%.S]' > iperf3.log"
