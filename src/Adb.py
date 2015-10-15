import threading
import socket
import time
import json
import math

TCP_IP = "localhost"
TCP_PORT = 5001

speed_data = {"data": "speed", "value": 0}
rpm_data = {"data": "rpm", "value": 3500}
time_data = {"data": "time", "value": int(time.time())}

log_file_time = int(time.time())

#Whenever we get a pulse from GPIO, start a new thread and do the calculations and logging

def obtain_data():
    _time = 0
    
    while True:
        angle = int((60.0 / 2.0) * math.sin((1.0 / 2.0) * _time - (1.0 / 2.0) * math.pi) + 30.0)
        speed_data["value"] = angle

        _time += 0.1
        time_data["value"] = int(time.time())
        
        open(("LogData-%d.csv" % log_file_time), "a").write("\n" + str(speed_data["value"]) + "," + str(rpm_data["value"]) + "," + str(time_data["value"]))
        
        time.sleep(0.2)
        
def android_connect():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while True:
            try:
                print("Trying to connect...")
                
                s.connect((TCP_IP, TCP_PORT))
                
                print("Connected")
                
                break
            except Exception as e:
                print(e)
                
                time.sleep(0.5)
                
                continue
        
        while True:
            try:
                #print("Sending message")
                
                s.send((json.dumps([speed_data, rpm_data, time_data]) + "\n").encode("utf-8"))
                
                time.sleep(0.05)
            except Exception as e:
                print("Reconnecting")
                
                break
        
        s.close()

if __name__ == '__main__':
    open(("LogData-%d.csv" % log_file_time), "w").write("Speed,RPM,Timestamp")
    
    dataThread = threading.Thread(target = obtain_data, args = ())
    dataThread.start()
    
    dataThread = threading.Thread(target = android_connect, args = ())
    dataThread.start()
    
    while True:
        pass