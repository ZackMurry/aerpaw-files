#!/bin/bash

# Example:sudo ./start_UE_Quectel.sh Broadband 2
export AERPAW_REPO=${AERPAW_REPO:-/root/AERPAW-Dev}
export PROFILE_DIR=$AERPAW_REPO"/AHN/E-VM/Profile_software"
cd $PROFILE_DIR"/other_radio/QuectelLogger/Radio/helpers"

export RESULTS_DIR="${RESULTS_DIR:-/root/Results}"
export TS_FORMAT="${TS_FORMAT:-'[%Y-%m-%d %H:%M:%.S]'}"

Ports=$(ls /dev/ttyUSB* | pcregrep -o1 -i 'USB(\d+)')
#echo $Ports
AT_Port=$(ls /dev/ttyUSB* | pcregrep -o1 -i 'USB(\d+)' | sort -nr | head -n1)
echo "Ctrl-Z or Ctrl-C to stop"
Time_New=$(date +"%Y_%m_%d_%H_%M_%S")
mkdir $RESULTS_DIR"/logs/"
mkdir $RESULTS_DIR"/logs/$Time_New"
mkdir $RESULTS_DIR"/logs/$Time_New/Init_log1"
mkdir $RESULTS_DIR"/logs/$Time_New/log1"
mkdir $RESULTS_DIR"/logs/$Time_New/csv_kpi"
touch $RESULTS_DIR"/logs/$Time_New/csv_kpi/Basic_and_Other_Params.csv"
touch $RESULTS_DIR"/logs/$Time_New/csv_kpi/Neighbourcell_Params_inter_.csv"
touch $RESULTS_DIR"/logs/$Time_New/csv_kpi/Neighbourcell_Params_intra_.csv"
touch $RESULTS_DIR"/logs/$Time_New/csv_kpi/Serving_cell_Params_ENDC.csv"
touch $RESULTS_DIR"/logs/$Time_New/csv_kpi/Serving_cell_Params_LTE_only.csv"

#Initialize
log_file=$RESULTS_DIR"/logs/$Time_New/Init_log1/Quectel_log_$(date +"%Y_%m_%d_%H\:%M\:%S").log"
apn_to_be_used="Broadband"
path_to_use="/dev/ttyUSB$AT_Port"

bash -c "stdbuf -oL -eL \
	python init_at_rm500q.py -a $apn_to_be_used -p $path_to_use \
	| tee -a $log_file"
#Logging

while true
	do
		echo "Ctrl-Z or Ctrl-C to stop"
		log_file=$RESULTS_DIR"/logs/$Time_New/log1/Quectel_log_$(date +"%Y_%m_%d_%H\:%M\:%S").log"
		bash -c "stdbuf -oL -eL \
			python no_pandas_at_rm500q.py -p $path_to_use -t $Time_New\
			| tee -a $log_file"
	done
