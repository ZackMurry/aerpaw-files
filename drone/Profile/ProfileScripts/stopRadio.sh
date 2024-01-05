#!/bin/bash
#
# This script will stop the radio application


# Profile 1
# SRS_LTE SISO - please select either the UE or the EPC+ENB

# for the UE
screen -S radio -X quit

# for EPC and ENB:
screen -S radioENB -X quit
screen -S radioEPC -X quit
screen -S txGRC -X quit
screen -S channelsounderrxGRC -X quit
screen -S channelsounderrxOCTAVE -X quit
