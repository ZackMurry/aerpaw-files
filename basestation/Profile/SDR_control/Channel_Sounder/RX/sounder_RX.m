  #!/usr/bin/env octave -q
  %clear all
  %close all
  
  M=20;
  %Initialization
  graphics_toolkit("gnuplot")
  total_length=4095*M; %Record 20 frames for measuring foffset
  fs=2e6; %Sampling rate used
  RxData=zeros(1,total_length); 
  fpoints=-fs/2:fs/length(RxData):(fs/2-fs/length(RxData));
   
  pkg load zeromq
  h=Cor_filt; 
  H=fft(h,4095+8190-1);
  cnt1=0;
  %gain=40;
  gain = str2num(argv(){1});
  msignal=zeros(1,100);
  while 1
    cnt1=cnt1+1;
    sock1 = zmq_socket(ZMQ_SUB);  % socket-connect-opt-close = 130 us
    zmq_connect   (sock1,"tcp://127.0.0.1:5555");
    zmq_setsockopt(sock1, ZMQ_SUBSCRIBE, "");
    recv=zmq_recv(sock1, total_length*8*2, 0); % *2: interleaved channels
    RxData=typecast(recv,"single complex"); % char -> float
    [a,b]=max(fftshift(abs(fft(RxData.^2))));
    foffset=fpoints(b)/2;
    RxData=RxData.*exp(-1j*2*pi*foffset*(1:length(RxData))/fs);
    cnt2=0;
    for ii=1:5:M-2
      cnt2=cnt2+1;
      rxData=RxData(4095*(ii-1)+(1:8190));
      rXData=fft(rxData(1:8190),4095+8190-1);
      y1=ifft(rXData.*H);
      y1a=y1(4095+(1:4095));
      [a b]=max(abs(y1a));
      signal_level(cnt2)=(abs(y1a(b)));
  end
  power_dB = 20*log10(mean(signal_level))-gain;
  ['measurement no: ' num2str(cnt1) ' Power in dB: ' num2str(power_dB) ]
  msignal(mod(cnt1,100)+1)=power_dB;
  %plot(msignal,'x-')
  %title(['Current Signal Level dB:'  num2str(msignal(mod(cnt1,100)+1))])
  %ylim([-40 70]-gain)
  %drawnow
  zmq_close (sock1);
  end
