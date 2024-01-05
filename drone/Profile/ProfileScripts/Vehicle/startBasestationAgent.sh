#!/bin/bash
#
# This script will start the basestation agent
#

pushd /root/flypaw/basestation/basestationAgent

rm screenlog.0

screen -L -S basestationAgent -dm \
       bash -c "python3.10 /root/flypaw/basestation/basestationAgent/basestationAgent.py"

