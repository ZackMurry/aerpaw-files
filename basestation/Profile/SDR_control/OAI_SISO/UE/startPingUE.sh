#!/bin/bash                                                                                          
sleep 3
ping -i 0.2 -c 2000 172.16.0.1 |  ts '[%Y-%m-%d %H:%M:%.S]' | tee pingResultsUE.txt

