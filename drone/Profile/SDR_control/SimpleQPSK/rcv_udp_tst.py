#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kvasude2
# GNU Radio version: 3.9.0.0-git

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class rcv_udp_tst(gr.top_block):

    def __init__(self, node_id=1):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.node_id = node_id

        ##################################################
        # Variables
        ##################################################
        self.UDP_mtu = UDP_mtu = 10000
        self.tap_mtu = tap_mtu = int(UDP_mtu/50)
        self.samp_rate = samp_rate = 1000
        self.port_offset = port_offset = node_id
        self.payload_mod = payload_mod = digital.constellation_qpsk()
        self.TX_mode_sel = TX_mode_sel = [[0, 0, 1]]
        self.TAP_bytes = TAP_bytes = 50
        self.RX_mode_sel = RX_mode_sel = [[0], [0], [1]]

        ##################################################
        # Blocks
        ##################################################
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(payload_mod.base())
        self.digital_chunks_to_symbols_xx_0_0_0_0 = digital.chunks_to_symbols_bc(payload_mod.points(), 1)
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tap000', tap_mtu, False)
        self.blocks_tagged_stream_to_pdu_1 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'rcv_packet_len')
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.complex_t, 'packet_len')
        self.blocks_socket_pdu_0_1 = blocks.socket_pdu('UDP_CLIENT', "172.18.0.100", ""+str(20100+node_id), UDP_mtu, False)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu('UDP_SERVER', '0.0.0.0', ""+str(20200+node_id), UDP_mtu, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu('UDP_CLIENT', "172.18.0."+str(3-node_id), ""+str(20203-node_id), UDP_mtu, False)
        self.blocks_repack_bits_bb_2 = blocks.repack_bits_bb(payload_mod.bits_per_symbol(), 8, "rcv_packet_len", True, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), "packet_len", False, gr.GR_LSB_FIRST)
        self.blocks_pdu_to_tagged_stream_1 = blocks.pdu_to_tagged_stream(blocks.complex_t, 'rcv_packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_1, 'pdus'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_1, 'pdus'), (self.blocks_tuntap_pdu_0, 'pdus'))
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_1, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_chunks_to_symbols_xx_0_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_2, 0), (self.blocks_tagged_stream_to_pdu_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_repack_bits_bb_2, 0))


    def get_node_id(self):
        return self.node_id

    def set_node_id(self, node_id):
        self.node_id = node_id
        self.set_port_offset(self.node_id)

    def get_UDP_mtu(self):
        return self.UDP_mtu

    def set_UDP_mtu(self, UDP_mtu):
        self.UDP_mtu = UDP_mtu
        self.set_tap_mtu(int(self.UDP_mtu/50))

    def get_tap_mtu(self):
        return self.tap_mtu

    def set_tap_mtu(self, tap_mtu):
        self.tap_mtu = tap_mtu

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_port_offset(self):
        return self.port_offset

    def set_port_offset(self, port_offset):
        self.port_offset = port_offset

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_TX_mode_sel(self):
        return self.TX_mode_sel

    def set_TX_mode_sel(self, TX_mode_sel):
        self.TX_mode_sel = TX_mode_sel

    def get_TAP_bytes(self):
        return self.TAP_bytes

    def set_TAP_bytes(self, TAP_bytes):
        self.TAP_bytes = TAP_bytes

    def get_RX_mode_sel(self):
        return self.RX_mode_sel

    def set_RX_mode_sel(self, RX_mode_sel):
        self.RX_mode_sel = RX_mode_sel




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-n", "--node-id", dest="node_id", type=intx, default=1,
        help="Set node_id [default=%(default)r]")
    return parser


def main(top_block_cls=rcv_udp_tst, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(node_id=options.node_id)

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
