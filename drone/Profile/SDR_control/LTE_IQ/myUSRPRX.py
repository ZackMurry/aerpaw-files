# generic USRP code

import uhd
from uhd import libpyuhd as lib
import numpy as np
import threading
from six.moves import queue
import time
import math
from myConstants import *

class UHDError(Exception):
    pass

class Device:

    def __init__(self):
        #self.usrp = uhd.usrp.MultiUSRP("serial=31EAC18")
        self.usrp = uhd.usrp.MultiUSRP()
        self.rx_lock = threading.Lock()
        self.rx_event = threading.Event()
        #self.rx_fifo = queue.Queue(maxsize=n_rep)
        self.debug = False

    # print('USRP device created (Serial =', serial, ')')

    def chg_rx_freq(self, fc):
        with self.rx_lock:
            # self.rx_fc = fc
            for k in range(len(self.rx_channels)):
                self.usrp.set_rx_freq(lib.types.tune_request(fc), self.rx_channels[k])
        print('RX freq changed to', fc)

    def set_rx_config(self, fc, fs, channels, gains):
        # with self.rx_lock:
        self.rx_fc = fc
        self.rx_fs = fs
        self.rx_channels = channels
        self.rx_gains = gains

        for k in range(len(channels)):
            self.usrp.set_rx_rate(fs, channels[k])
            self.usrp.set_rx_freq(lib.types.tune_request(fc), channels[k])
            self.usrp.set_rx_gain(gains[k], channels[k])
            print('RX configured')

        if self.debug:
            print('RX configured')

    def get_jumbo_rx_buffer(self, n_samp):
        with self.rx_lock:
            st_args = lib.usrp.stream_args("fc32", "sc16")
            st_args.channels = self.rx_channels
            self.rx_streamer = self.usrp.get_rx_stream(st_args)

            stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.start_cont)
            stream_cmd.stream_now = (len(self.rx_channels) == 1)
            stream_cmd.time_spec = lib.types.time_spec(self.usrp.get_time_now().get_real_secs() + 0.05)
            self.rx_streamer.issue_stream_cmd(stream_cmd)

        if self.debug:
            print('__jumbo_rx_loop() started')

        with self.rx_lock:
            self.rx_metadata = lib.types.rx_metadata()
            buffer_samps = self.rx_streamer.get_max_num_samps()
            

        recv_buffer = np.zeros(
            (len(self.rx_channels), buffer_samps), dtype=np.complex64)
        recv_jumbo_buffer = np.zeros(
            (len(self.rx_channels), math.ceil(n_samp/buffer_samps) * buffer_samps), dtype=np.complex64)
        recv_jumbo_buffer_timestamps = np.zeros(
            (len(self.rx_channels), math.ceil(n_samp/buffer_samps)), dtype=np.float_)

        cnt = 0
        # while not(self.rx_event.isSet()):
        while True:

            with self.rx_lock:
                cnt=cnt+1
                if cnt == math.ceil(n_samp/buffer_samps)+1:
                    print(cnt)
                    break

                samps = self.rx_streamer.recv(recv_buffer, self.rx_metadata)
                if self.debug:
                    print(self.rx_metadata)
                    print('\n')
                if self.rx_metadata.error_code != lib.types.rx_metadata_error_code.none:
                    print(cnt)
                    print(self.rx_metadata.strerror())
                    # # Clean up buffer
                    stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.stop_cont)
                    self.rx_streamer.issue_stream_cmd(stream_cmd)
                    while True:
                       samps = self.rx_streamer.recv(recv_buffer, self.rx_metadata)
                       print(samps)
                       if samps == 0:
                          break
                    raise UHDError


            try:

                recv_jumbo_buffer[:, (cnt - 1) * (buffer_samps):cnt * buffer_samps] = recv_buffer
                recv_jumbo_buffer_timestamps[:, cnt - 1] = self.rx_metadata.time_spec.get_real_secs()
            except queue.Full:
                pass

        # End of RX msg
        with self.rx_lock:
            stream_cmd = lib.types.stream_cmd(lib.types.stream_mode.stop_cont)
            self.rx_streamer.issue_stream_cmd(stream_cmd)


        if self.debug:
            print('__rx_loop() end')
        return recv_jumbo_buffer, recv_jumbo_buffer_timestamps
