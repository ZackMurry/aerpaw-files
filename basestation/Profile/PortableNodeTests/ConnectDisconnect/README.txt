This script connects to the vehicle, prints a couple of variables, waits for 5s, and then disconnects. No arming!

Executing software on SITL:
1) Start OEO-VM and start QGroundControl.
2) Start VE-VM and start SITL. (cd /ardupilot/ArduCopter; sim_vehicle.py)
***Note: If not done before the SITL outputs must be set to OEO-VM and E-VM IPs.
   Run: cd scripts; ./startSitl oeo-vm-ip e-vm-ip 1)
   The outputs will be saved and from now on SITL can be started using sim_vehicle.py***
3) Start E-VM and navigate to dronekit directory. (cd dronekit)
4) Run profile on E-VM: python connectDisconnect.py --connect :14550
5) View movement of drone on QGroundControl (OEO-VM)
