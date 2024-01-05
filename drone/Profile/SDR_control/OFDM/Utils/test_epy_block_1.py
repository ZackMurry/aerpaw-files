"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

WORK_DONE = -1 # GRC magic value to stop a block from being queried

class blk(gr.sync_block):  
    """ Sequence number traffic generator: 
        - generates maxCount sequence numbers of length
          digits each (plus a <cr> at the end of each sequence number)
    """

    def __init__(self, maxCount=2000 , digits=9): 
        gr.sync_block.__init__(
            self,
            name='Generator',   # will show up in GRC
            in_sig=None,        # no inputs
            out_sig=[np.byte]   # spits out bytes
        )
        self._maxCount = maxCount # how many lines of output will be generated
        self._counter = 0 # this is the current counter
        self._done = False # True when we're done counting
        self._digits = digits # how many digits for each sequence number
        self._leftOver = [] # handles short requests

    def work(self, input_items, output_items):

        stringLength = self._digits+1  # how long is each string
        howManyNeeded = len(output_items[0])
        numbers = int(np.floor(howManyNeeded/(stringLength)))
        howManyWillGive=numbers*(stringLength)
        fmt='%'+"0%dd\n"%(self._digits)

        if len(self._leftOver) > 0:  # we have bytes left over
            offset = len(self._leftOver)
            output_items[0][0:offset]=self._leftOver
            self._leftOver=[]
#            print(f"Returing left overs {offset}")
            return offset
            
        if self._done:
#            print("I'm done!")
            return WORK_DONE

#        print(f"It wants {howManyNeeded}")
#        print(f"I'll give it {howManyWillGive}")

        for i in range(numbers): # only executed when numbers > 0
            str=fmt%self._counter
            daBytes = np.fromstring(str,dtype=np.byte)
            output_items[0][i*stringLength:(i+1)*stringLength]=daBytes
            self._counter=self._counter+1
            if self._counter >= self._maxCount:
                self._done = True
#                print(f"No more, returning {(i+1)*stringLength}")
                return (i+1)*stringLength

        if (numbers==0): # it wants less than one sequence number
            str=fmt%self._counter
            daBytes = np.fromstring(str,dtype=np.byte)
            output_items[0][:]=daBytes[0:howManyNeeded]
            self._leftOver=daBytes[howManyNeeded:]
            self._counter=self._counter+1
            if self._counter >= self._maxCount:
                self._done = True
#            print(f"Returning {howManyNeeded}")
            return howManyNeeded
        else:
            self._leftOver = []
#            print(f"Lots more, returning {(i+1)*stringLength}")
            return (i+1)*stringLength

