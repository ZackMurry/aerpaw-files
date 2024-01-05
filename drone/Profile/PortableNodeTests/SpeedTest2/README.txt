

This is an alternate speed test script. The goal of the script is to test how fast a drone can go between two points A and B. The latitudes and longitudes of the two points are specified in the speed_test_params.yaml

In short, the drone takes of at the specified altitude (also in speed_test_params.yaml), and goes to point A. Then it prompts for a speed (in m/s) and attempts to go to point B at the specified speed. Along the way, it prints its current ground speed. Once at B, it prompts for the speed to go to A, and so on. If the speed entered is exit, rtl, or zero, the drone enters RTL mode (i.e., returns to launch) and the script exits.


Usage: python speedTest2.py --connect <connection_string>

Example: python speedTest2.py --connect :14560

