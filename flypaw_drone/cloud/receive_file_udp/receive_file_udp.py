import sys
import socket
import select
from argparse import ArgumentParser
#import subprocess

#outputDir = "/home/cc/dataset"
#bindIP = "0.0.0.0"
#bindPort = 8096

#            mountStr = outputDir + ":/coconet/dataset"
#            try:
#                with open("/home/cc/darknet.log", "a") as darknetlog:
#                    subprocess.call(['sudo', 'docker', 'run', '-it', '-v', mountStr, 'papajim/detectionmodule:latest', '/coconet/darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', fname], shell=True, stdout=darknetlog, stderr=darknetlog)
#            except IOerror:
#                print("could not open darknet log and run darknet.  Skipped.")
#            break

        
if __name__ == '__main__':
    parser = ArgumentParser(description="File Transfer Server")
    parser.add_argument("-o", "--outputdir", metavar="OUTPUTDIR", type=str, help="directory to write file", required=True)
    parser.add_argument("-a", "--address", metavar="ADDRESS", type=str, help="IP address of server to bind to", required=True)
    parser.add_argument("-p", "--port", metavar="PORT", type=int, help="Server port", required=True)
    parser.add_argument("-b", "--buffersz", metavar="BUFFERSZ", type=int, help="Buffer size for UDP reads", required=True)
    
    args = parser.parse_args()
    outputdir = args.outputdir
    address = args.address
    port = args.port
    buffersz = args.buffersz

    try:
        udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except OSerror:
        print("OSerror: Could not create udpsocket.  Port may not be available.")
        sys.exit()
    except socket.error:
        print("socket error: Could not create udpsocket")
        sys.exit()

    try:
        udpsocket.bind((address, port))
    except socket.error:
        print("socket error: Could not bind to port " + str(port))
        sys.exit()

    while True:
        batch, client = udpsocket.recvfrom(1024)
        if batch:
            decodedBatch = batch.decode('utf-8')
            fname = outputdir + "/" + decodedBatch.strip()

        try:
            ofile = open(fname, 'wb')
        except IOerror:
            print ("could not open file: " + fname)

        while True:
            done = select.select([udpsocket], [], [], 5)
            if done[0]:
                batch, client = udpsocket.recvfrom(buffersz)
                ofile.write(batch)
            else:
                ofile.close()
                print(fname + " written")
                break

