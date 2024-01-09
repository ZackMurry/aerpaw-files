import os
os.environ['MAVLINK20'] = "1" # Change to MAVLink 20 for video commands
from pymavlink import mavutil
from threading import Thread, Event
import signal
import numpy as np
import time
import math, sys
import cv2
# sys.path.append('.')
#from util.AESCipher import AESCipher
from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from Crypto.PublicKey import DSA, RSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from base64 import b64encode, b64decode
import ecdsa
from hashlib import sha256, sha512
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

#keyPair = RSA.generate(bits=2048)
#print(keyPair.export_key('PEM'))
keyPair = RSA.import_key('-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAs4Kw5qY3Qmry0cx5MJsqbW3JCdOga44rARYaP22EjfMKr9/i\n3MvSymmWtsIRhEOjrtLADJY1IuE/B4iWkUlwjxV/nrde8tEVDDNXjNfBfyQBeeZf\nTt5h7zC9UxEyKV7bQgYc2OKNClscxp7Pn+q8tw/Qw5vgYHklKdP7kle6/KqzqSYf\nLVWisH9hYm8/j5Hx6xMG+loK+rponrd3vMNRrskExwFcpgQkmC9t3gEmCGb4WN9w\nIVRFGCTy/Tx7WBvYVWEIl6p3eJEBdA2Z4xGY6ci9hJ8slo2XI/9cJPgJpMf/eD5F\nIxr+cjc2yzl5rNPFlp87RWCTfGkUjpg0Hf2eSwIDAQABAoIBAAC07v0sKLJn8sq7\nrFS+9g1etmMn82KCn/Qe+YYU399uzdbeKlz/uE9g1+pvKRvlLCXpGNjPkrkeVXM6\nxs9jB96WwD8/1HHW5pHyj4keQlnw5i8fQC4Uv5nlp9zn5boHgXsG5qrom070OtC9\nyFTCBc91PR3RHN1HkzpRGWIJjjCd4I1+ThW4+ovSrImG0/cBQyvKhF0jWEdBQ4HN\nkBrMI5Wj/qETsAGKfLcksjGQqro0o/ywix1lRM/TGYaO+SynYgSi72+44Xo8eQP0\n3aBHG4PSvvfb2G7ks3aoDcwFqsJsbRvb9W5E790Zw3tkx3S/LTv7Ailv4Najl3AZ\npWpfT70CgYEA04/B5EeyS3P2AVFaSrN00eTj+Xmu8+NPHUMh9/G/mzS0RUOIHi9q\nzzfp+h/fIGc4sQRdlvsKkF1Xg1XPV/+Aka2ig387zmqz9z40Hs+5Z6LNwG0h99Bx\n/r1xjLkEVm2W/+coSpaz2B7LP6DlUw3y1XJB0PgXHRrnlNb4vI3xJocCgYEA2Td2\nLQvN//Yb823QPnm8Da7bIY4NqFaK2TKjpVWi7tEC634h9FLbOHEotcpPGtJ0bcLm\nYO6c+HcHfdEQNb1Q5RPdiLWRJ0ScmZvbrkJFg8qKjpCdBzJySILP5ghg+9kenKq2\n+gZM5Fh80NANIcQ/xTnJDSE65xGLWAHy0paA9x0CgYBCWqVafu454h33Xdeu9Egg\niOTD21l3HwUyTVr7FDSfblFYJA0uQnsCkSvuik6GMDnEs3TTJNu0WcJX6/MDS5y8\nlDQTgDV20VquojDgtRAWpCZaQyBTRGpslmhl1aW5odepXYvykP/JOidPRpyGhypx\nrctcymMdetHFigMryG0pQwKBgAzxWhBLEMY8ouO5Wlwuor7p+VKhhTzPk0xn0Qpr\n9N5oA9WGWX2WZkuRqoxSdq4xdhCIOXPzI9VGOmMLzvx0wFo1+dBIiVKeqvoYKFnU\nxxGYQvNFuKWSIu8hJEQfoa+/+yv4nBh/wZsljqJekzm82NPmoo0uurTD/dqLmy1j\nHGIdAoGAPWG3uQ4k2Yr7usaNUtaLgblLe4LLPfgy9GutSYERzA0BajB7c6wdURJV\nOabbZXIWbjNVvUD5Tq6vxhCi3Wq0TVA+lSj1cxq0POD7fXwxzayfapAyujiamxDw\nmY16wTGqqSEgBGsmLUhn2q64cF7MGYgf4qr4J51Vg+RxGbX6a3w=\n-----END RSA PRIVATE KEY-----')





"""
images_per_second = 10
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f"sample{time.time()}.mp4", fourcc, images_per_second, (256,144))

for i in range(1,515):
    mat = cv2.imread(f"data/sample-{i}.jpg")
    out.write(mat)

out.release()
"""


use_encryption = False
use_signature = False
video_size = 'LG' # SM or LG
key = b64decode('c8O9Xp7HcudRrY5KcnJdNZeQjAfdFrB4lVBkSjWI0hw=')

replay_attack = True
replay_attack_start = 20
replay_attack_end = 30

private_key = None

skb = b64decode('Z8vbM8tHLRhV5DueD+7T3BaLJUnEBUnyg4dZHB5nS5j02XcxbHwlHQeiuxT8b4X/')
sk = ecdsa.SigningKey.from_string(skb, curve=ecdsa.NIST384p)

def get_config_str():
    conf = ""
    if use_encryption:
        conf = conf + "CHA_"
    if use_signature:
        conf = conf + "SIG_"
    return f"{conf}_{video_size}"

num_frames = 0
frame_dir = ''
frame_file_start = ''
if video_size == 'LG':
    num_frames = 450
    frame_dir = '/root/flypaw/drone/flypawPilot/data/large'
    frame_file_start = 'large'
else:
    if video_size != 'SM':
        print('UNKNOWN VIDEO SIZE: Defaulting to SM')
    num_frames = 180
    frame_dir = '/root/flypaw/drone/flypawPilot/data/small'
    frame_file_start = 'small'


if use_signature:
  with open('private_key_dsa.pem', "rb") as file1:
      private_key = DSA.import_key(file1.read(), 'MyPassphrase')
  
# 56 bytes
def create_signature_dss(message):
  message_hash = SHA256.new(message)
  signer = DSS.new(private_key, 'fips-186-3')
  signature = signer.sign(message_hash)
  print(f"len(signature): {len(signature)}")
  return signature

# 96 bytes
def create_signature_ecdsa(message):
  return sk.sign(message)

# 256 bytes
def create_signature_rsa(message):
    # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
    hash = SHA256.new(message)
    signer = PKCS115_SigScheme(keyPair)
    return signer.sign(hash)

fps_results = []

def get_fps_results():
    return fps_results

bw_results = []

def get_bandwidth_results():
    return bw_results

time_results = []

def get_time_results():
    return time_results

should_stop = Event()
def sigint_handler(signum, frame):
  should_stop.set()
  print('SIGINT')
signal.signal(signal.SIGINT, sigint_handler)


def send_image(conn, idx, t0):
  print(f"Sending frame {idx}")
  image = cv2.imread(f"{frame_dir}/{frame_file_start}-{idx:04d}.jpg")
  ob = bytearray(cv2.imencode('.jpg', image)[1])
  #print(f"Sending frame {idx}; len: {len(ob)}")

  #print("len(b):", len(b))

  b = ob
  if use_encryption:
    cipher = ChaCha20.new(key=key)
    b = cipher.encrypt(ob)
    # AES
    #cipher = AES.new(key, AES.MODE_EAX)
    #b, tag = cipher.encrypt_and_digest(ob)

    #print(f"len(tag): {len(tag)}") = 16
    #print(f"tag: {b64encode(tag)}")
    #print(f"nonce: {b64encode(cipher.nonce)}")
    #print(f"cipher: {b64encode(b[0:32])}")
    #print(f"len(nonce): {len(cipher.nonce)}")
    #print(f"len(ob): {len(ob)}")
    #print(f"ob: {ob[-30:]}")
    #b = bytearray(cipher.nonce + tag + b)
    b = bytearray(cipher.nonce + b)
    #print(f"leb(b): {len(b)}")

  if use_signature:
    signature = create_signature_rsa(ob)
    #print(f"signature: {signature}")
    #print(f"len(signature): {len(signature)}")
    b = bytearray(signature + b)

  # Send image metadata
  conn.mav.data_transmission_handshake_send(
     0, # Data stream type: JPEG
     len(b), # Total data size (ACK only)
     1280, # Width
     720, # Height
     math.ceil(len(b) / 253), # Number of packets being sent (ACK only)
     253, # Payload size per packet (ACK only)
     100 # JPEG quality
  )
   
  seqnr = 0 # Sequence number for chunk
  
  while len(b) > 0:
      # print(len(b))
      #if len(b) < 253:
      #print(f'Padding with {253 - len(b)} bytes')
      conn.mav.encapsulated_data_send(
          seqnr,
          b[0:253] if len(b) > 253 else b + bytearray((253 - len(b)) * [0])
      )

      if replay_attack:
          dt = time.time() - t0
          
          if dt > replay_attack_start and dt < replay_attack_end:
              conn.mav.encapsulated_data_send(
                  seqnr,
                  b[0:253] if len(b) > 253 else b + bytearray((253 - len(b)) * [0])
              )

      seqnr += 1
      if len(b) >= 253:
        b = b[253:]
      else:
        break


      if seqnr % 20 == 0:
          conn.mav.ping_send(
              int((time.time() - int(time.time())) * 1000000),
              0,
              0,
              0
          )

          while True:
            msg = conn.recv_msg()
            if msg is None:
                continue
            # print(msg.get_type())
            if msg.get_type() == 'PING':
                break 
            
#  print(seqnr)
  if should_stop.is_set():
    conn.mav.camera_capture_status_send(
      (int) (1000 * (time.time() - t0)), # timestamp
      0, # image capturing status = idle
      0, # video capturing status = idle
      0, # image capture interval
      0, # elapsed time since recording started = unavailable
      0, # available storage capacity
      0 # num images captured
    )

  # All zero values to end transmission
  conn.mav.data_transmission_handshake_send(0,0,0,0,0,0,0)
  #print('Sent image')


def handle_client(conn):
  idx = 1
  t0 = time.time()
  while not should_stop.is_set():
    msg = conn.recv_msg()
    if msg is None:
      continue
    if idx > num_frames:
      conn.mav.camera_capture_status_send(
          (int) (1000 * (time.time() - t0)), # timestamp
          0, # image capturing status = idle
          0, # video capturing status = idle
          0, # image capture interval
          0, # elapsed time since recording started = unavailable
          0, # available storage capacity
          0 # num images captured
      )
      break
    # print(msg.get_type())
    if msg.get_type() == 'DATA_TRANSMISSION_HANDSHAKE':
      #send_image(conn, idx, t0)
      send_image(conn, 13, t0)
      idx = idx + 1

  conn.mav.camera_capture_status_send(
    (int) (1000 * (time.time() - t0)), # timestamp
    0, # image capturing status = idle
    0, # video capturing status = idle
    0, # image capture interval
    0, # elapsed time since recording started = unavailable
    0, # available storage capacity
    0 # num images captured
  )
  dt = time.time() - t0
  fps = idx / dt
  print("%.2f FPS | Transferred %d frames in %.1f seconds" % (fps, idx, dt))
  fps_results.append(fps)
  bw_results.append(0.001*(conn.mav.total_bytes_sent)/dt)
  time_results.append(dt)
  conn.port.close()

def print_summary(conn, delta_t):
  print("Overall: %u sent, %u received, %u errors bwin=%.1f kB/s bwout=%.1f kB/s" % (
      conn.mav.total_packets_sent,
      conn.mav.total_packets_received,
      conn.mav.total_receive_errors,
      0.001*(conn.mav.total_bytes_received)/delta_t,
      0.001*(conn.mav.total_bytes_sent)/delta_t))

def wait_heartbeat(conn):
  while not should_stop.is_set():
    # print('waiting for heartbeat')
    if conn.wait_heartbeat(timeout=1):
      print("Heartbeat from system (system %u component %u)" % (conn.target_system, conn.target_component))
      break


def vm_send_video():
    mavutil.set_dialect('common')
    conn = mavutil.mavlink_connection('tcp:192.168.139.2:14541')
    conn.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                    mavutil.mavlink.MAV_AUTOPILOT_INVALID,
                                                            0, 0, 0)

    t0 = time.time()
    handle_client(conn)

    delta_t = time.time() - t0
    print_summary(conn, delta_t)
    mavutil.set_dialect('ardupilotmega')

if __name__ == '__main__':
    vm_send_video()


