#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: v3.8.5.0-6-g57bd109d

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time


class calibRX(gr.top_block):

    def __init__(self, N=100, args='', file='/root/Power', freq=3.5e9, gainrx=30, samp_rate=10e6):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.N = N
        self.args = args
        self.file = file
        self.freq = freq
        self.gainrx = gainrx
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gainrx, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_ff(N, 1/N, 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(N, 1/N, 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(N, 1/N, 4000, 1)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, N)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, N)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, N)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file, False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))


    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N
        self.blocks_keep_one_in_n_0.set_n(self.N)
        self.blocks_keep_one_in_n_0_0.set_n(self.N)
        self.blocks_keep_one_in_n_0_0_0.set_n(self.N)
        self.blocks_moving_average_xx_0.set_length_and_scale(self.N, 1/self.N)
        self.blocks_moving_average_xx_0_0.set_length_and_scale(self.N, 1/self.N)
        self.blocks_moving_average_xx_0_0_0.set_length_and_scale(self.N, 1/self.N)

    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file
        self.blocks_file_sink_0.open(self.file)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_gainrx(self):
        return self.gainrx

    def set_gainrx(self, gainrx):
        self.gainrx = gainrx
        self.uhd_usrp_source_0.set_gain(self.gainrx, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--N", dest="N", type=intx, default=100,
        help="Set N [default=%(default)r]")
    parser.add_argument(
        "--args", dest="args", type=str, default='',
        help="Set args [default=%(default)r]")
    parser.add_argument(
        "--file", dest="file", type=str, default='/root/Power',
        help="Set file [default=%(default)r]")
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default="3.5G",
        help="Set freq [default=%(default)r]")
    parser.add_argument(
        "--gainrx", dest="gainrx", type=eng_float, default="30.0",
        help="Set gainrx [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="10.0M",
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=calibRX, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(N=options.N, args=options.args, file=options.file, freq=options.freq, gainrx=options.gainrx, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
