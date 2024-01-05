# Profile Scripts

## Environment Variables

### All
* `AERPAW_REPO`     - Location of AERPAW-Dev repository cloned onto system
                      filter
* `AERPAW_PYTHON`   - python executable used by scripts. Ideally `python3.8` on
                      ubuntu 18.xx
* `LAUNCH_MODE`     - "EMULATION" -- run in emulation, "TESTBED" -- run on
                      hardware

### Vehicle specific
* `MAV_UPSTREAM`    - Upstream mavlink connection to the C-VM's
* `VEHICLE_TYPE`    - Type of vehicle being used. Defaults to `drone`

### Emulation
* `EXP_NUMBER`      - Experiment number for ip addresses
