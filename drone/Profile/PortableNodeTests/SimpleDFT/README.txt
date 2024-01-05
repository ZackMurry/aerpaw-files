

From Ozgur:

There is a console only spectrum analyzer named "rx_ascii_art_dft". UHD installs this by default into the folder 
/usr/local/lib/uhd/examples/
The usage is as follows
./rx_ascii_art_dft --freq 98e6 --rate 5e6 --gain 20 --bw 5e6 --ref-lvl -30
There exists some info on
https://kb.ettus.com/Verifying_the_Operation_of_the_USRP_Using_UHD_and_GNU_Radio
We however noticed it does not work properly on same machines we tried (In particular, it worked on aerpaw21 but did not work on aerpaw18) where it starts normally but the image freezes.
Anyalyzer and jammer should be able to work on the same B205 as one of them is TX only and the other one is RX only.


For the terminal spectrum analyzer you can specify the USRP by the --args
"serial=XXXXXX" where you can find the serial number using uhd_find_devices

As an example

oozdemi@aerpaw18:~$ uhd_find_devices
[INFO] [UHD] linux; GNU C++ version 7.5.0; Boost_106501;
UHD_4.0.0.HEAD-0-g90ce6062
--------------------------------------------------
-- UHD Device 0
--------------------------------------------------
Device Address:
    serial: 31E74C2
    name: B205i
    product: B205mini
    type: b200

./rx_ascii_art_dft --freq 98e6 --rate 5e6 --gain 20 --bw 5e6 --ref-lvl
-30 --args "serial=31E74C2"
To run this command you need to go to the folder /usr/local/lib/uhd/examples

