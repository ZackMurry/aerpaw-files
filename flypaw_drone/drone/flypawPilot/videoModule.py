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
# from util.AESCipher import AESCipher
#from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from base64 import b64encode, b64decode


"""
images_per_second = 10
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(f"sample{time.time()}.mp4", fourcc, images_per_second, (256,144))

for i in range(1,515):
    mat = cv2.imread(f"data/sample-{i}.jpg")
    out.write(mat)

out.release()
"""


use_security = True
video_size = 'SM' # SM or LG
key = b64decode('c8O9Xp7HcudRrY5KcnJdNZeQjAfdFrB4lVBkSjWI0hw=')

private_key = None

def get_config_str():
    if use_security:
        return f"SEC_{video_size}"
    return f"NOSEC_{video_size}"

max_repetitions = 1
if video_size == 'LG':
    max_repetitions = 10

if use_security:
  with open('private_key_dsa.pem', "rb") as file1:
      private_key = DSA.import_key(file1.read(), 'MyPassphrase')
  
def create_signature(message):
  message_hash = SHA256.new(message)
  signer = DSS.new(private_key, 'fips-186-3')
  signature1 = signer.sign(message_hash)
  return signature1

fps_results = []

def get_fps_results():
    return fps_results

should_stop = Event()
def sigint_handler(signum, frame):
  should_stop.set()
  print('SIGINT')
signal.signal(signal.SIGINT, sigint_handler)


def send_image(conn, idx):
    
  
    
  image = cv2.imread(f"data/sample-{idx}.jpg")
  b = bytearray(cv2.imencode('.jpg', image)[1])

  #print("len(b):", len(b))

  if use_security:
    #print(b64encode(b)[-32:])
    #print(len(b))
    #cipher = ChaCha20.new(key=key)
    #b = cipher.encrypt(b)
    
    #b = cipher.nonce + b
    #print(f"nonce length: {len(cipher.nonce)}")
    signature = create_signature(b)
    cipher = ChaCha20.new(key=key)
    b = cipher.encrypt(b)
    
    # print(len(signature)) # 56
    b = bytearray(cipher.nonce + signature + b)
    #print("Encrypted!")

    # nonce = b64encode(cipher.nonce).decode('utf-8')
    # b64t = b64encode(b).decode('utf-8')
    # result = json.dumps({'nonce':nonce, 'ciphertext':b64t})
    # print(result)
    #init_len = len(b)

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
  repetitions = 0
  t0 = time.time()
  while not should_stop.is_set():
    msg = conn.recv_msg()
    if msg is None:
      continue
    if idx > 514:
      repetitions += 1
      if repetitions >= max_repetitions:
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
      idx = 1
    # print(msg.get_type())
    if msg.get_type() == 'DATA_TRANSMISSION_HANDSHAKE':
      send_image(conn, idx)
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
  fps = (idx * max_repetitions) / dt
  print("%.2f FPS | Transferred %d frames in %.1f seconds" % (fps, idx * max_repetitions, dt))
  fps_results.append(fps)
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
    conn = mavutil.mavlink_connection('tcp:192.168.106.2:14541')
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


