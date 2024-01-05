"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import codecs
from gnuradio import gr


class blk(gr.sync_block):  
    """Just prints to stdout the bytes it receives (as UTF-8 characters)"""

    def __init__(self):  # No parameters
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Print',    # will show up in GRC
            in_sig=[np.byte], # takes in bytes
            out_sig=None     # no output
        )

    def work(self, input_items, output_items):
        dataBytes = bytes(input_items[0]) # converts to an array of bytes
        str = dataBytes.decode(encoding='UTF-8')  # converts to string
        print(str,end='')
        return len(input_items[0])

