#!/bin/bash
export AERPAW_REPO=${AERPAW_REPO:-/root/AERPAW-Dev}
export AERPAW_PYTHON=${AERPAW_PYTHON:-python3}
#export LAUNCH_MODE=${LAUNCH_MODE:-'EMULATION'}
#export EXP_NUMBER=${EXP_NUMBER:-1}

#export RESULTS_DIR="${RESULTS_DIR:-/root/Results}"
#export TS_FORMAT="${TS_FORMAT:-'[%Y-%m-%d %H:%M:%.S]'}"
export LOG_PREFIX="$(date +%Y-%m-%d_%H:%M:%S)"

export PROFILE_DIR=$AERPAW_REPO"/AHN/E-VM/Profile_software"
cd $PROFILE_DIR"/other_radio/QuectelLogger"

/bin/kill -9 $(pgrep -f Quectel_log) > /dev/null 2> /dev/null
/bin/kill -9 $(pgrep -f start_UE_Quectel) > /dev/null 2> /dev/null

#screen -S Quectel_radio -dm bash -c "./Radio/samples/start_UE_Quectel_ATT.sh"
#screen -S Quectel_radio -dm bash -c "./Radio/samples/start_UE_Quectel_AERPAW.sh"
bash -c "./Radio/samples/start_UE_Quectel_ATT.sh"
