import uhd
from uhd import libpyuhd as lib
import numpy as np
import scipy.io
import threading
#import matplotlib.pyplot as plt
from myConstants import *
import myUSRPRX
import time
from datetime import datetime
import pytz


def getIQ():
    print('Initializing USRP')
    usrpRX = myUSRPRX.Device()
    print('Receiver configuration')
    usrpRX.set_rx_config(fLO[0], fs[0], channelsRX, gainRX)
    start=time.time()
    end=time.time()
    while (end-start)<total_duration:
        try:
            for i in range(len(fLO)):
                if len(fLO)>1:
                    usrpRX.set_rx_config(fLO[i], fs[i], channelsRX, gainRX)
                time.sleep(wait_duration*1e-3)
                meas_x0, ts = usrpRX.get_jumbo_rx_buffer(n_samp[i])
                #print(ts)
                data ={}
                data['IQ'] = meas_x0
                data['time_stamp'] = ts
                filename="/root/Results/results_" +str(int(fLO[i])) +"_" +str(int(fs[i])) +"_" +datetime.now(pytz.timezone("America/New_York")).strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3] + ".mat"
                print(datetime.now(pytz.timezone("America/New_York")).strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3])
                scipy.io.savemat(filename, data, do_compression=True)
                end=time.time()
                # print(end)
                # time.sleep(wait_duration*1e-3)
        except myUSRPRX.UHDError as e:
            print('UHD Error Occured')
            end=time.time()
            time.sleep(0.020)
    #plt.plot( freqs, powers )
    #plt.xlabel('frequency [MHz]')
    #plt.ylabel('PSD Relative dB')
    #plt.show()


if __name__ == "__main__":
    t = threading.Thread(target=getIQ)
    t.start()
    t.join()
    print('Measurement completed')
