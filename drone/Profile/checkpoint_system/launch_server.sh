#!/bin/bash

screen -S checkpoint_server -dm -X python3 server.py

sleep 5

curl 'http://127.0.0.1:12434/reset' -X POST