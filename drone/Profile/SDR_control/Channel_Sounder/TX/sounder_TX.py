#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Sounder TX
# Author: oozdemi
# GNU Radio version: v3.8.3.1-16-g9d94c8a6

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from AERPAW_Sink import AERPAW_Sink  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class sounder_TX(gr.top_block):

    def __init__(self, arguments='', freq=3.5e9, gain=0, rate=2e6, mode='uhd', ip= 'tcp://127.0.0.1:5001'):
        gr.top_block.__init__(self, "Sounder TX")

        ##################################################
        # Variables
        ##################################################
#        self.samp_rate = samp_rate = 2e6

        ##################################################
        # Parameters
        ##################################################
        self.arguments = arguments
        self.freq = freq
        self.gain = gain
        self.rate = rate
        self.mode = mode
        self.ip = ip

        ##################################################
        # Blocks
        ##################################################
        self.digital_glfsr_source_x_0 = digital.glfsr_source_f(12, True, 0, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.99)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.AERPAW_Sink_0_0 = AERPAW_Sink(
            args=arguments,
            center_freq=freq,
            samp_rate=rate,
            source=mode,
            tx_gain=gain,
            zmq_tx_address=ip,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.AERPAW_Sink_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.blocks_float_to_complex_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.AERPAW_Sink_0_0.set_samp_rate(self.samp_rate)

def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--arguments", dest="arguments", type=str, default='',
        help="Set args [default=%(default)r]")
    parser.add_argument(
        "-f", "--freq", dest="freq", type=eng_float, default="3.5G",
        help="Set freq [default=%(default)r]")
    parser.add_argument(
        "-g", "--gain", dest="gain", type=eng_float, default="0.0",
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "-r", "--rate", dest="rate", type=eng_float, default="2.0M",
        help="Set rate [default=%(default)r]")
    parser.add_argument(
        "--mode", dest="mode", type=str, default='uhd',
        help="Set sink [default=%(default)r]")
    parser.add_argument(
        "--ip", dest="ip", type=str, default='tcp://127.0.0.1:5001',
        help="Set zmq ip:port [default=%(default)r]")

    return parser





def main(top_block_cls=sounder_TX, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(arguments=options.arguments, freq=options.freq, gain=options.gain, rate=options.rate, mode=options.mode, ip=options.ip)
    
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
