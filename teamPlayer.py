import pyvirtualcam
import numpy as np
import cv2
from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')

devices = [{'address': 0}, {'address': 'rtsp://{}:{}@{}:{}/videoMain'.format(config.get('netcam0', 'user'), config.get('netcam0', 'pass'), config.get('netcam0', 'ip'), config.get('netcam0', 'port'))}]

for device in devices:
    device['cap'] = cv2.VideoCapture(device['address'])
    device['cap'].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    device['cap'].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

output = 0

with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    while True:
        for device in devices:
            device['ret'], device['frame'] = device['cap'].read()
            device['frame'] = cv2.cvtColor(device['frame'], cv2.COLOR_RGB2BGRA)
        
        k = cv2.waitKey(1)
        if k > 0:
            if chr(k) == 'q':
                quit()
            try:
                output = int(chr(k)) - 1
            except:
                break
        try:    
            frame_out = devices[output]['frame']
            cv2.imshow('output', frame_out)
            cam.send(frame_out)
            cam.sleep_until_next_frame()
        except:
            quit()