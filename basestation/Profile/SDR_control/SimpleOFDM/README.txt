Here is the GNURadio graph for a simple OFDM transmitter/receiver. 
The current form operates using 1 antenna (TX/RX port) on each USRP at 2.62GHz.

To operate the flowgraph, open GNURadio with root.
Attach appropriate antennas on the TX/RX port of the devices you wish to communicate.
Open the flowgraph in the instance of GNURadio running as root.
Click the "play" button to start the flowgraph. Another terminal window should open.
On each device enter the following command:
"sudo ifconfig tap2 192.168.200.X" -> where 'X' is the device number you are using. ie 1, 2, 3 etc.
No 2 systems should use the same number for 'X'.
On any of the devices, you should be able to run the following command:
"ping 192.168.200.X" -> where 'X' is the device number you wish to ping. Must be an IP different from the one setup on this device.
You should see ping results regarding the time taken for the packet. The best results have occured when using the X300 with the B210.
