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
#from util.AESCipher import AESCipher
from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from base64 import b64encode, b64decode
from Crypto.PublicKey import DSA, RSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import ecdsa
from hashlib import sha256, sha512
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

keyPair = RSA.import_key('-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAs4Kw5qY3Qmry0cx5MJsqbW3JCdOga44rARYaP22EjfMKr9/i\n3MvSymmWtsIRhEOjrtLADJY1IuE/B4iWkUlwjxV/nrde8tEVDDNXjNfBfyQBeeZf\nTt5h7zC9UxEyKV7bQgYc2OKNClscxp7Pn+q8tw/Qw5vgYHklKdP7kle6/KqzqSYf\nLVWisH9hYm8/j5Hx6xMG+loK+rponrd3vMNRrskExwFcpgQkmC9t3gEmCGb4WN9w\nIVRFGCTy/Tx7WBvYVWEIl6p3eJEBdA2Z4xGY6ci9hJ8slo2XI/9cJPgJpMf/eD5F\nIxr+cjc2yzl5rNPFlp87RWCTfGkUjpg0Hf2eSwIDAQABAoIBAAC07v0sKLJn8sq7\nrFS+9g1etmMn82KCn/Qe+YYU399uzdbeKlz/uE9g1+pvKRvlLCXpGNjPkrkeVXM6\nxs9jB96WwD8/1HHW5pHyj4keQlnw5i8fQC4Uv5nlp9zn5boHgXsG5qrom070OtC9\nyFTCBc91PR3RHN1HkzpRGWIJjjCd4I1+ThW4+ovSrImG0/cBQyvKhF0jWEdBQ4HN\nkBrMI5Wj/qETsAGKfLcksjGQqro0o/ywix1lRM/TGYaO+SynYgSi72+44Xo8eQP0\n3aBHG4PSvvfb2G7ks3aoDcwFqsJsbRvb9W5E790Zw3tkx3S/LTv7Ailv4Najl3AZ\npWpfT70CgYEA04/B5EeyS3P2AVFaSrN00eTj+Xmu8+NPHUMh9/G/mzS0RUOIHi9q\nzzfp+h/fIGc4sQRdlvsKkF1Xg1XPV/+Aka2ig387zmqz9z40Hs+5Z6LNwG0h99Bx\n/r1xjLkEVm2W/+coSpaz2B7LP6DlUw3y1XJB0PgXHRrnlNb4vI3xJocCgYEA2Td2\nLQvN//Yb823QPnm8Da7bIY4NqFaK2TKjpVWi7tEC634h9FLbOHEotcpPGtJ0bcLm\nYO6c+HcHfdEQNb1Q5RPdiLWRJ0ScmZvbrkJFg8qKjpCdBzJySILP5ghg+9kenKq2\n+gZM5Fh80NANIcQ/xTnJDSE65xGLWAHy0paA9x0CgYBCWqVafu454h33Xdeu9Egg\niOTD21l3HwUyTVr7FDSfblFYJA0uQnsCkSvuik6GMDnEs3TTJNu0WcJX6/MDS5y8\nlDQTgDV20VquojDgtRAWpCZaQyBTRGpslmhl1aW5odepXYvykP/JOidPRpyGhypx\nrctcymMdetHFigMryG0pQwKBgAzxWhBLEMY8ouO5Wlwuor7p+VKhhTzPk0xn0Qpr\n9N5oA9WGWX2WZkuRqoxSdq4xdhCIOXPzI9VGOmMLzvx0wFo1+dBIiVKeqvoYKFnU\nxxGYQvNFuKWSIu8hJEQfoa+/+yv4nBh/wZsljqJekzm82NPmoo0uurTD/dqLmy1j\nHGIdAoGAPWG3uQ4k2Yr7usaNUtaLgblLe4LLPfgy9GutSYERzA0BajB7c6wdURJV\nOabbZXIWbjNVvUD5Tq6vxhCi3Wq0TVA+lSj1cxq0POD7fXwxzayfapAyujiamxDw\nmY16wTGqqSEgBGsmLUhn2q64cF7MGYgf4qr4J51Vg+RxGbX6a3w=\n-----END RSA PRIVATE KEY-----')

rsa_signer = PKCS115_SigScheme(keyPair)

vkb = b64decode('Il8HQoHsypIg2xmtxJDrPFHW8t1Awi5Dh/8K7EeTkKPbZIU0uodRmFHsTkRh18i9nMHGNb1nLjUJIRboqgd2l4Vw6+k6wnCvnuK69GD72CuO5wlskumlxVTHMsKQ9CTY')
vk = ecdsa.VerifyingKey.from_string(vkb, curve=ecdsa.NIST384p)

sig_len = 256

print('Starting video module...')
conn = mavutil.mavlink_connection('tcpin::14541')

should_stop = Event()
def sigint_handler(signum, frame):
    should_stop.set()
    print('SIGINT')

signal.signal(signal.SIGINT, sigint_handler)

use_encryption = False
use_signature = False

key = b64decode('c8O9Xp7HcudRrY5KcnJdNZeQjAfdFrB4lVBkSjWI0hw=')

public_key = None
with open('public_key.pem', "rb") as file1:
  public_key = DSA.importKey(file1.read())


def is_signature_valid_dss(message, signature1):
  message_hash = SHA256.new(message)
  verifier = DSS.new(public_key, 'fips-186-3')
  try:
    verifier.verify(message_hash, signature1)
    return True
  except ValueError:
    print('Invalid signature!')
    return False

def is_signature_valid_ecdsa(message, signature):
    return vk.verify(signature, message)

def is_signature_valid_rsa(message, signature):
    hash = SHA256.new(message)
    try:
        rsa_signer.verify(hash, signature)
        return True
    except:
        print("Signature is invalid.")
        return False

packets_received = [0] * 360 # index = t
packet_graph_start = 0

def register_packet():
    #print(f"Index: {math.floor(time.time() - packet_graph_start)}")
    #print(f"Packet graph start: {packet_graph_start}")
    #print(f"Time: {time.time()}")
    packets_received[math.floor(time.time() - packet_graph_start)] += 1

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
          continue
        last_seqnr = msg.seqnr
        recvd += 1
        buffer += bytearray(msg.data)
        register_packet()
        #print("buflen:", len(buffer))
      elif msg.get_type() == 'DATA_TRANSMISSION_HANDSHAKE':
        register_packet()
        if msg.size == 0:
          #print('END OF IMAGE')
          break
        else:
          #print('START_OF_IMAGE')
          img_size = msg.size
      elif msg.get_type() == 'CAMERA_CAPTURE_STATUS':
        register_packet()
        print('HALT')
        #should_stop.set()
        return None
      elif msg.get_type() == 'PING':
        register_packet()
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
    images_per_second = 12
    output_images_per_second = 12
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    out = cv2.VideoWriter(f"output-{time_str}.mp4", fourcc, output_images_per_second, (640,360))
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
        

        if use_encryption:
            signature = bytearray()
            if use_signature:
                signature = buffer[:sig_len]
                #print(f"signature: {signature}")
                buffer = buffer[sig_len:]
            #print(f"raw: {b64encode(buffer[:58])}")
            # AES
            #nonce = buffer[:16]
            #tag = buffer[16:32]
            #ciphertext = buffer[32:]

            nonce = buffer[:8]
            ciphertext = buffer[8:]
            #print(f"tag: {b64encode(tag)}")
            #print(f"nonce: {b64encode(nonce)}")
            #print(f"cipher: {b64encode(ciphertext[0:32])}")
            #print(f"len(ciphertext): {len(ciphertext)}")
            cipher = ChaCha20.new(key=key, nonce=nonce)
            plaintext = bytearray(cipher.decrypt(ciphertext))
            #AES
            #cipher = AES.new(key, AES.MODE_EAX, nonce)
            #plaintext = bytearray(cipher.decrypt_and_verify(ciphertext, tag))

            #print(f"len(plaintext): {len(plaintext)}")
            #print(f"plaintext: {plaintext[-30:]}")
            buffer = plaintext
            #if use_signature and not is_signature_valid(buffer, signature):
            if use_signature and not is_signature_valid_rsa(buffer, signature):
                  print('Invalid signature!')
                  break
        elif use_signature:
            #signature = buffer[:56]
            #buffer = buffer[56:]
            signature = buffer[:sig_len]
            buffer = buffer[sig_len:]
            if use_signature and not is_signature_valid_rsa(buffer, signature):
              print('Invalid signature!')
              break

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
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open(f"packets_{time_str}.txt", "w") as file:
        for i in range(len(packets_received)):
            file.write(f"{i}, {packets_received[i]}\n")
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
#    if not is_first_run:
#        print('refreshing conn')
        #conn = refresh_conn(conn)
        #print(dir(serial))
        #print(serial)
        #conn.port = serial.Serial(port_device, 1200, timeout=0, dsrdtr=False, rtscts=False, xonxoff=False)
        #print(conn.listen_addr)
        #conn.listen.bind(conn.listen_addr)
        #print(conn)
#    else: is_first_run = False
    wait_heartbeat(conn)
    if should_stop.is_set():
        break
    print('Heartbeat received!')
    t0 = time.time()
    packet_graph_start = time.time()
    handle_client(conn)
    delta_t = time.time() - t0
    #print_summary(conn, delta_t)


print(should_stop.is_set())

