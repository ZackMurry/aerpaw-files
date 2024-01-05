This is the AERPAW profile for the LoStik hardware from Ronoth.

The code was initially written and maintained by Ender Ozturk (eozturk2@ncsu.edu) - please contact him for any questions regarding this code.

The relevant wiki page is here:
https://sites.google.com/a/ncsu.edu/aerpaw-wiki/user-wiki-start/lora-experiments



CONFIG FILES:

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

SH FILES:

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


STEPS FOR AN EXPERIMENT

1. Arrange config.conf files for each TX and RX that will take place in the experiment
2. Arrange traffic.conf files for each TX that will take place in the experiment
3. Make sure that .conf files are in ./config_files/ folder. 
4. If the device in a container should receive, run rx.sh
5. If the device in a container should receive, run tx.sh
6. Once the experiment is over, collect the output files in ./output_files/ folder. 
7. Optional postprocessing.sh file allows experimenter to calculate BER and PDR given the input (transmitted) packets and output (received) packets. 