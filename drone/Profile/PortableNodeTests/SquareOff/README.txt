This script connects to the drone and waits until armed. When armed it will takeoff to 3m altitude, then navigate a 10x10 meter square. At each corner of the square, the drone will wait for 5 seconds.

Executing software on drone SITL:
1) Start OEO-VM and start QGroundControl.
2) Start VE-VM and start SITL. (cd /ardupilot/ArduCopter; sim_vehicle.py)
***Note: If not done before the SITL outputs must be set to OEO-VM and E-VM IPs.
   Run: cd scripts; ./startSitl oeo-vm-ip e-vm-ip 1)
   The outputs will be saved and from now on SITL can be started using sim_vehicle.py***
3) Start E-VM and navigate to dronekit directory. (cd dronekit)
4) Run profile on E-VM: python square_off.py --connect :14550
5) View movement of drone on QGroundControl (OEO-VM)
