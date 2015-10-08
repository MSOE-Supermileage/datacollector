import json
import socket
import threading
from time import sleep

IP, PORT = ("192.168.1.2", 2004)

server_socket = None

speed_data = {"data": "speed", "value": 20}
rpm_data = {"data": "rpm", "value": 3500}

def handle_data():
    going_up = True;
    
    while True:
        if speed_data["value"] < 65 and going_up:
            speed_data["value"] += 1
        elif speed_data["value"] == 65 and going_up:
            going_up = False
        elif speed_data["value"] > 0 and not going_up:
            speed_data["value"] -= 1
        elif speed_data["value"] == 0 and not going_up:
            going_up = True
            
        # Obtain sensor data from the GPIO and send it to the android app encoded in JSON
        
        server_socket.sendto((json.dumps([speed_data, rpm_data]) + "\n").encode("utf-8"), (IP, PORT))
        
        sleep(0.1)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    data_thread = threading.Thread(target = handle_data, args = ())
    
    data_thread.daemon = True
    data_thread.start()
    
    while True:
        pass