import json
import time
import socket
import threading
from time import sleep
import math

IP, PORT = ("192.168.1.2", 2004)

server_socket = None

speed_data = {"data": "speed", "value": 20}
rpm_data = {"data": "rpm", "value": 3500}
time_data = {"data": "time", "value": int(time.time())}

def handle_data():
    _time = 0
    
    while True:
        speed_data["value"] = int((60 / 2) * math.sin((1 / 2) * _time - (1 / 2) * math.pi) + 30)
        
        _time += 0.1
        
        time_data["value"] = int(time.time())
        
        # Obtain sensor data from the GPIO and send it to the android app encoded in JSON
        
        server_socket.sendto((json.dumps([speed_data, rpm_data, time_data]) + "\n").encode("utf-8"), (IP, PORT))
        
        sleep(0.1)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    data_thread = threading.Thread(target = handle_data, args = ())
    
    data_thread.daemon = True
    data_thread.start()
    
    while True:
        pass