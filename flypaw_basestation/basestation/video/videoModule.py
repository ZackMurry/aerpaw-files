from pymavlink import mavutil
from threading import Thread, Event
import serial
import signal
import cv2
import time
import numpy as np
import math, sys
import datetime
# sys.path.append('.')
# from util.AESCipher import AESCipher
# from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from base64 import b64encode, b64decode
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS


conn = mavutil.mavlink_connection('tcpin::14541')

should_stop = Event()
def sigint_handler(signum, frame):
    should_stop.set()
    print('SIGINT')

signal.signal(signal.SIGINT, sigint_handler)

use_security = '-sec' in sys.argv
key = b64decode('c8O9Xp7HcudRrY5KcnJdNZeQjAfdFrB4lVBkSjWI0hw=')

public_key = None
with open('public_key.pem', "rb") as file1:
  public_key = DSA.importKey(file1.read())


def is_signature_valid(message, signature1):
  message_hash = SHA256.new(message)
  verifier = DSS.new(public_key, 'fips-186-3')
  try:
    verifier.verify(message_hash, signature1)
    return True
  except ValueError:
    print('Invalid signature!')
    return False


def handle_data(data_conn):
  buffer = bytearray()
  img_size = 0
  last_seqnr = -1
  recvd = 0
  looped = 0
  while not should_stop.is_set():
    msg = data_conn.recv_msg()
    looped += 1
    if msg:
      # print(msg.get_type())
      if msg.get_type() == 'ENCAPSULATED_DATA':
          # print('GOOD DATA %d' % msg.seqnr)
          #print('Received', msg.seqnr)
          if msg.seqnr <= last_seqnr:
            print("Warning: sequence numbers not received in order!")
          last_seqnr = msg.seqnr
          recvd += 1
          buffer += bytearray(msg.data)
          #print("buflen:", len(buffer))
      elif msg.get_type() == 'DATA_TRANSMISSION_HANDSHAKE':
           if msg.size == 0:
               #print('END OF IMAGE')
               break
           else:
             #print('START_OF_IMAGE')
             img_size = msg.size
      elif msg.get_type() == 'CAMERA_CAPTURE_STATUS':
          print('HALT')
          #should_stop.set()
          return None
      elif msg.get_type() == 'PING':
          print('PING')
          data_conn.mav.ping_send(
              int((time.time()-int(time.time())) * 1000000),
              0,
              0,
              0
          )
      elif msg.get_type() == 'BAD_DATA':
        print('BAD DATA')

  #print(recvd, len(buffer))
  if recvd == 0 or len(buffer) == 0 or buffer == None:
    print("Returning none")
    return None
  padding_size = len(buffer) - img_size
  #print(f"bs: {len(buffer)}, ps: {padding_size}")
  if padding_size != 0:
      buffer = buffer[:-padding_size]
  return buffer

def handle_video(data_conn):
    images_per_second = 30
    output_images_per_second = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    out = cv2.VideoWriter(f"output-{time_str}.mp4", fourcc, output_images_per_second, (256,144))
    images_received = 0
    last_image_requested_at = 0
    image_interval = 1 / images_per_second # second(s)
    tolerance = image_interval * 0.1
    # print(f"tolerance: {tolerance}")
    t0 = time.time()

    while not should_stop.is_set():
        # print(last_image_requested_at + image_interval - time.time())
        #if last_image_requested_at + image_interval > time.time() + tolerance:
        #    time.sleep(last_image_requested_at + image_interval - time.time() - tolerance/2)
        last_image_requested_at = time.time()
        # Request image
        #print('Requesting image; ' + str(should_stop.is_set()))
        data_conn.mav.data_transmission_handshake_send(
            0, # Data stream type: JPEG
            0, # Total data size (ACK only)
            1280, # Width
            720, # Height
            0, # Number of packets being sent (ACK only)
            0, # Payload size per packet (ACK only)
            100 # JPEG quality
        )

        buffer = handle_data(data_conn)
        if buffer is None or len(buffer) == 0:
            print("nonebuf")
            break
        if use_security:
            nonce = buffer[:8]
            signature = buffer[8:8+56]
            ciphertext = buffer[64:]
            cipher = ChaCha20.new(key=key, nonce=nonce)
            plaintext = bytearray(cipher.decrypt(ciphertext))
            #print("Decrypted!")
          # print(b64encode(plaintext)[-32:])
          # print(len(plaintext))
            buffer = plaintext
            if not is_signature_valid(buffer, signature):
              print('Invalid signature!')
              break
          # print(plaintext)

        mat = cv2.imdecode(np.asarray(buffer), cv2.IMREAD_COLOR)
        out.write(mat)
        images_received += 1
        #print(images_received)
    print('received %d images' % images_received)
    print(f"real images per second: {images_received / (time.time() - t0)}")
    data_conn.port.close()
    out.release()

def handle_client(conn):
    handle_video(conn)
    conn.mav.camera_capture_status_send(
        (int) (1000 * (time.time() - t0)), # timestamp
        0, # image capturing status = idle
        0, # video capturing status = idle
        0, # image capture interval
        0, # elapsed time since recording started = unavailable
        0, # available storage capacity
        0 # num images captured
      )
    #conn.port.close()

def wait_heartbeat(conn):
  while not should_stop.is_set():
    # print('waiting for heartbeat')
    # Heartbeat from last connection still in effect i think
    if conn.wait_heartbeat(timeout=1):
      print("Heartbeat from system (system %u component %u)" % (conn.target_system, conn.target_component))
      break

def refresh_conn(conn):
  while not should_stop.is_set():
    try:
      return conn.listen.accept()
    except Exception as e:
      pass

is_first_run = True
while not should_stop.is_set():
    if not is_first_run:
        print('refreshing conn')
        #conn = refresh_conn(conn)
        #print(dir(serial))
        #print(serial)
        #conn.port = serial.Serial(port_device, 1200, timeout=0, dsrdtr=False, rtscts=False, xonxoff=False)
        #print(conn.listen_addr)
        #conn.listen.bind(conn.listen_addr)
        #print(conn)
    else:
        is_first_run = False
        wait_heartbeat(conn)
    if should_stop.is_set():
        break
    print('Heartbeat received!')
    t0 = time.time()
    handle_client(conn)
    delta_t = time.time() - t0
    #print_summary(conn, delta_t)


print(should_stop.is_set())

