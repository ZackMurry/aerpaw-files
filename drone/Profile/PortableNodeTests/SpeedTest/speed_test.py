import asyncio
from argparse import ArgumentParser
import yaml
import csv
from time import sleep
from typing import List
import datetime

from aerpawlib.runner import StateMachine
from aerpawlib.vehicle import Vehicle, Drone
from aerpawlib.runner import state, background
from aerpawlib.util import Coordinate, VectorNED


class SpeedTest(StateMachine):
    _cur_line: int
    _csv_writer: object
    _sampling_delay: float
    _sampling: bool

    def initialize_args(self, extra_args: List[str]):
        # use an extra argument parser to read in custom script arguments
        default_file = (
            f"GPS_DATA_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
        )

        parser = ArgumentParser()
        parser.add_argument(
            "--skipoutput", help="don't dump gps data to a file", action="store_false"
        )
        parser.add_argument(
            "--output", help="log output file", required=False, default=default_file
        )
        parser.add_argument(
            "--samplerate", help="log sampling rate (Hz)", required=False, default=1
        )
        parser.add_argument(
            "--params",
            help="path to speed test parameters file",
            required=False,
            default="speed_test_params.yaml",
            dest="params_filename",
        )

        args = parser.parse_args(args=extra_args)
        self._sampling = args.skipoutput
        self._sampling_delay = 1 / args.samplerate
        self.params_filename = args.params_filename

        if self._sampling:
            self._log_file = open(args.output, "w+")
            self._cur_line = sum(1 for _ in self._log_file) + 1
            self._csv_writer = csv.writer(self._log_file)
        
        params_file = open(self.params_filename, "r")
        params = yaml.load(params_file)

        self.location_index = 0
        self.waypoints = params["waypoints"]
        self.altitude = params["altitude"]

        # Construct a list of coordinates based on the yaml params
        self.coords: List[Coordinate] = [0] * len(self.waypoints)
        for i in range(len(self.waypoints)):
            self.coords[i] = Coordinate(self.waypoints[i][0], self.waypoints[i][1], self.altitude)


    @state(name="init_test", first=True)
    async def init_test(self, vehicle: Drone):
        input("Press enter to start the speed test")
        print("Moving to first location")
        await vehicle.goto_coordinates(self.coords[self.location_index])

        return "start_test"

    @state(name="start_test")
    async def start_test(self, vehicle: Drone):
        print("Changing heading")
        # face the next location
        last_location = self.coords[self.location_index]
        self.location_index = (self.location_index + 1) % len(self.waypoints)
        new_heading = last_location.bearing(self.coords[self.location_index])
        # Rovers cannot set heading, so only do for a drone
        if isinstance(vehicle, Drone):
            await vehicle.set_heading(new_heading)
        while True:
            speed_str = input("Input speed in m/s or type exit to exit: ")
            try:
                speed = float(speed_str)
                # negative speed check
                if speed <= 0:
                    print("Speed must be greater than 0 m/s! Try again.")
                # too high speed check
                elif speed > 44.7:
                    print("Speed cannot be greater than 44.7 m/s (100mph)! Try again.")
                # Input speed was valid
                else:
                    break
            # float conversion failed
            except:
                if speed_str in ["exit", "rtl"]:
                    return "rtl"
                print("Could not convert input to a float! Try again.")

        # update location index to go to the next set of lats and longs

        await vehicle.set_groundspeed(speed)
        print("Starting speed test")
        await vehicle.goto_coordinates(self.coords[self.location_index])
        return "start_test"

    @state(name="rtl")
    async def rtl(self, vehicle: Vehicle):
        # return to the take off location and stop the script
        home_coords = Coordinate(
            vehicle.home_coords.lat, vehicle.home_coords.lon, vehicle.position.alt
        )
        await vehicle.goto_coordinates(home_coords)
        if isinstance(vehicle, Drone):
            await vehicle.land()
        print("done!")

    @background
    async def periodic_dump(self, vehicle: Vehicle):
        await asyncio.sleep(self._sampling_delay)
        if not self._sampling:
            return
        self._dump_to_csv(vehicle, self._cur_line, self._csv_writer)
        self._cur_line += 1

    def cleanup(self):
        if self._sampling:
            self._log_file.close()

    def _dump_to_csv(self, vehicle: Vehicle, line_num: int, writer):
        """
        This function will continually log stats about the vehicle to a file specified by command line args
        """
        pos = vehicle.position
        lat, lon, alt = pos.lat, pos.lon, pos.alt
        volt = vehicle.battery.voltage
        blevel = vehicle.battery.level
        timestamp = datetime.datetime.now()
        gps = vehicle.gps
        fix, num_sat = gps.fix_type, gps.satellites_visible
        if fix < 2:
            lat, lon, alt = -999, -999, -999
        writer.writerow(
            [line_num, lon, lat, alt, volt, blevel, timestamp, fix, num_sat]
        )
