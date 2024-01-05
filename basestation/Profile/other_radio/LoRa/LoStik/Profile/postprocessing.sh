#!/bin/bash

# THIS FILE ASSUMES THAT INPUT AND OUTPUT FILES EXISTS IN THE CURRENT FOLDER

# Postprocessing (BER and PDR calculation) PARAMETERS
input_file = input.txt
output_file = output.txt


python3 postprocess_PDR_AERPAW.py $input_file $output_file

python3 postprocess_BER_AERPAW.py $input_file $output_file