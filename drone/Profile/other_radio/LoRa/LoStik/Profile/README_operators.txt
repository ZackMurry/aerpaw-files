This is the AERPAW profile for the LoStik hardware from Ronoth.

The code was initially written and maintained by Ender Ozturk (eozturk2@ncsu.edu) - please contact him for any questions regarding this code.

The relevant wiki page is here:
https://sites.google.com/a/ncsu.edu/aerpaw-wiki/user-wiki-start/lora-experiments



CONFIG FILES:

COM_ports.json
Json file that is created by preprocessing.py. preprocessing.py checks the active COM ports attached, and stores the port indexes of those which are LoRa LoStiks, i.e., checks if the "sys get ver" returns "RN2903 ...". Returned port indexes are stored in COM_ports.json file. 

Config.conf
Config file that is used to configure a specific device. These are the physical layer parameters such that frequency band, bandwidth, spreading factor. See the device manual for detailed information. configure_AERPAW.py file uses this file to configure a certain device connected to a COM port.

traffic.conf
Configures the traffic that is transmitted by a transmitter. User may:
	- Add transmitter ID at the beginning of the packet
	- Add packet index number at the end of the packet
	- Add time_stamp following transmitter ID (if used)
	- Use custom packets, these packets are transmitted in order, once all are transmitted, turns back to first packet until the total tranmission time is over.
	- Choose a file to transmit dividing the file in packets of certain length.
	- Turn on or off all these options above
User defines packet period in terms of seconds and total duration in minutes using this file. 

custom_file.txt
traffic.conf has an option [custom_packets] to use this file. if the status under [custom_packets] = file, then the information in custom_file.txt is transmitted. 

PY FILES:

preprocessing_AERPAW.py:
Checks all active ports and creates COM_ports.json that includes COM port indexes, e.g., ['COM3','COM5']

configure_AERPAW.py:
Configures devices as defined in the relevant config file given as a parameter

receiver_AERPAW.py:
Puts a device in continuous reception mode, logs the received packets, RSSI and SNR of the packets together with the packets in a json file, and a bulk file that stacks all the packets.

transmitter_AERPAW.py:
Transmits as defined in the relevant traffic config file

postprocess_PDR_AERPAW.py
Comparing the transmitted and received packets, calculates and prints the packet delivery ratio. Takes input and output text files as parameters

postprocess_BER_AERPAW.py
Compating the transmitted and received bits, calculates and prints the bit error rate. Takes input and output text files as parameters

tx.sh
runs the preprocessing file to capture active COM ports
runs the configuration file to configure the device, takes in the config.conf file as parameter
runs the transmit file to initiate transmission from the device. Takes traffic.conf file, packet transmission period in sec and experiment duration in min.


rx.sh
runs the preprocessing file to capture active COM ports
runs the configuration file to configure the device, takes in the config.conf file as parameter
runs the receive file to open reception window. Takes the duration of receptin window as parameter. If given 0, reception window stays open.

postprocessing.sh
runs postprocessing BER and PDR files. Takes in input and output text files to calculate bit error rate and packet delivery ratio.
