
Directory for useful (!) Experimenter scripts.

checkPlan.sh [mission.plan] [vehicle_config.yaml]

Checks a preplanned trajectory mission plan for compliance with altitude, as well as geofence breaches. Will tell for each leg if a violation will occur (or not) when flying the mission. By default is checks the default.plan mission here:
$AERPAW_REPO/AHN/E-VM/Profile_software/vehicle_control/PreplannedTrajectory/Missions/default.plan




savePlan.sh [mission.plan]

Pulls a mission from the autopilot and saves it into a file. By default, to the same default.plan mission as checkPlan.sh.