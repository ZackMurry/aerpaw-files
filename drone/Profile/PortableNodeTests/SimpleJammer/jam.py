#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: keith
# GNU Radio version: v3.8.2.0-80-g40c04cae

from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from time import perf_counter



class jam(gr.top_block):

    def __init__(self, args='', duration=0, freq=2.635e9, gain=0, rate=2e6):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.args = args
        self.duration = duration
        self.freq = freq
        self.gain = gain
        self.rate = rate

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 1, 8675309, 8192)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.uhd_usrp_sink_0, 0))


    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.uhd_usrp_sink_0.set_samp_rate(self.rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--args", dest="args", type=str, default='',
        help="Set args [default=%(default)r]")
    parser.add_argument(
        "-d", "--duration", dest="duration", type=intx, default=0,
        help="Set duration [default=%(default)r]")
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="2.635G",
        help="Set freq [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain", dest="gain", type=eng_float, default="0.0",
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "-r", "--rate", dest="rate", type=eng_float, default="2.0M",
        help="Set rate [default=%(default)r]")
    return parser


def main(top_block_cls=jam, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(args=options.args, duration=options.duration, freq=options.freq, gain=options.gain, rate=options.rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    print("Jamming...")
    start = 0
    
    if options.duration > 0:
        start = perf_counter()
        elapsed = False
        while not elapsed:
            stop = perf_counter()
            #print("elapsed:", stop - start)
            if (stop - start) > options.duration:
                elapsed = True
        print("Stopping Jamming...")
        tb.stop()
        tb.wait()
    if options.duration == 0:    
        try:
            input('Press Enter to quit: ')
        except EOFError:
            pass
        print("Stopping Jamming...")
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
