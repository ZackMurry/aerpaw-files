#!/bin/bash
#
# This script will start the basestation agent
#

pushd /root/flypaw/basestation/video

rm screenlog.0

screen -L -S videoModule -dm \
       bash -c "python3.10 /root/flypaw/basestation/video/videoModule.py"

