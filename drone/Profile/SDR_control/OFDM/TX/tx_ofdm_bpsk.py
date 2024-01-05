#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
# GNU Radio version: v3.8.2.0-80-g40c04cae

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from AERPAW_Sink import AERPAW_Sink  # grc-generated hier_block
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class tx_ofdm(gr.top_block):

    def __init__(self, args="", duration=60, freq=3.52e9, samp_rate=500000, source='zmq', tx_gain=40, zmq_tx_address='tcp://*:5001'):
        gr.top_block.__init__(self, "OFDM Tx")

        ##################################################
        # Parameters
        ##################################################
        self.args = args
        self.duration = duration
        self.freq = freq
        self.samp_rate = samp_rate
        self.source = source
        self.tx_gain = tx_gain
        self.zmq_tx_address = zmq_tx_address

        ##################################################
        # Variables
        ##################################################
        self.occupied_carriers = occupied_carriers = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.length_tag_key = length_tag_key = "packet_len"
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.rolloff = rolloff = 0
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.payload_mod = payload_mod = digital.constellation_bpsk()
        self.packet_len = packet_len = 96
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.hdr_format = hdr_format = digital.header_format_ofdm(occupied_carriers, 1, length_tag_key,)
        self.fft_len = fft_len = 64

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, length_tag_key)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len + fft_len//4, rolloff, length_tag_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), length_tag_key, True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key, True)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_mod.points(), 1)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 96, length_tag_key)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.05)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, samp_rate*duration)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'in.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.AERPAW_Sink_0 = AERPAW_Sink(
            args=args,
            center_freq=freq,
            samp_rate=samp_rate,
            source=source,
            tx_gain=tx_gain,
            zmq_tx_address=zmq_tx_address,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_head_0, 0), (self.AERPAW_Sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))


    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args
        self.AERPAW_Sink_0.set_args(self.args)

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration
        self.blocks_head_0.set_length(self.samp_rate*self.duration)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.AERPAW_Sink_0.set_center_freq(self.freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.AERPAW_Sink_0.set_samp_rate(self.samp_rate)
        self.blocks_head_0.set_length(self.samp_rate*self.duration)

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source
        self.AERPAW_Sink_0.set_source(self.source)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.AERPAW_Sink_0.set_tx_gain(self.tx_gain)

    def get_zmq_tx_address(self):
        return self.zmq_tx_address

    def set_zmq_tx_address(self, zmq_tx_address):
        self.zmq_tx_address = zmq_tx_address
        self.AERPAW_Sink_0.set_zmq_tx_address(self.zmq_tx_address)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_hdr_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len




def argument_parser():
    description = 'Example of an OFDM Transmitter'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--args", dest="args", type=str, default="",
        help="Set Arguments [default=%(default)r]")
    parser.add_argument(
        "--duration", dest="duration", type=intx, default=60,
        help="Set Duration [default=%(default)r]")
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default="3.52G",
        help="Set Center Frequency [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=intx, default=500000,
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "--source", dest="source", type=str, default='zmq',
        help="Set Source [default=%(default)r]")
    parser.add_argument(
        "--tx-gain", dest="tx_gain", type=eng_float, default="40.0",
        help="Set TX Gain [default=%(default)r]")
    parser.add_argument(
        "--zmq-tx-address", dest="zmq_tx_address", type=str, default='tcp://*:5001',
        help="Set ZMQ Tx Address [default=%(default)r]")
    return parser


def main(top_block_cls=tx_ofdm, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(args=options.args, duration=options.duration, freq=options.freq, samp_rate=options.samp_rate, source=options.source, tx_gain=options.tx_gain, zmq_tx_address=options.zmq_tx_address)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
