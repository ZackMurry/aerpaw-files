 #!/usr/bin/env octave -q
  clear all
  close all

  M=1;
  %Initialization
  %graphics_toolkit("gnuplot")
  total_length=4095*M;
  RxData=zeros(1,total_length);
  pkg load zeromq
  cnt1=0;
  gain = 40;
  msignal=zeros(1,100);
  while 1
    cnt1=cnt1+1;
    sock1 = zmq_socket(ZMQ_SUB);  % socket-connect-opt-close = 130 us
    zmq_connect   (sock1,"tcp://127.0.0.1:5555");
    zmq_setsockopt(sock1, ZMQ_SUBSCRIBE, "");
    recv=zmq_recv(sock1, total_length*8*2, 0); % *2: interleaved channels
    RxData=typecast(recv,"single complex"); % char -> float
    [a b]=max(abs(RxData));
    Res(cnt1,:)=[RxData(mod(b-2,4095)+1) RxData(b) RxData(mod(b,4095)+1)];
    Resi=[RxData(mod(b-2,4095)+1) RxData(b) RxData(mod(b,4095)+1)];
    20*log10(abs(Resi(1)+Resi(2)+Resi(3)));
    rssi(cnt1)=20*log10(abs(Resi(1)+Resi(2)+Resi(3)));

    msignal(mod(cnt1,100)+1)=rssi(cnt1);
    figure(2)
    plot(msignal,'x-')
    title(['Current Signal Level dB:'  num2str(msignal(mod(cnt1,100)+1))])
    grid on
    %ylim([0 70]-gain)

    figure(1)
    clf
    plot(real(RxData),'rx')
    hold on
    plot(imag(RxData),'gd')
    pause(0.1)
    drawnow
    zmq_close (sock1);
  end
