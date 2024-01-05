import math
gainRX = (40,)
fs = (2e6, 2e6) #sampling_rate
fLO = (3500e6, 3510e6)
IQ_duration=(20,20) #in ms
wait_duration=77 #in ms
total_duration=0.5 #measurement duration in seconds
channelsRX = (0,)
n_samp=[0]*len(fLO)
for i in range(len(fLO)):
    n_samp[i]=math.ceil(IQ_duration[i]*1e-3*fs[i])
