import threading
import socket
import time
import json
import math

TCP_IP = "localhost"
TCP_PORT = 5001

data = {"time": int(time.time())};

speed_data = {"data": "speed", "value": 0}
rpm_data = {"data": "rpm", "value": 3500}
time_data = {"data": "time", "value": int(time.time())}

log_file_time = int(time.time())

#Whenever we get a pulse from GPIO, start a new thread and do the calculations and logging

def obtain_data(): #Have this be the callback from the GPIO pin
    previousTime = -1
    
    while True:
        currentTime = int(round(time.time() * 1000))
        
        if previousTime is not -1:
            timeDifference = (currentTime - previousTime)
            
            data["time"] = timeDifference
        
        previousTime = currentTime
        
        log_data()
        
        time.sleep(0.06)
        
def send_data(sock):
    sock.send((json.dumps(data) + "\n").encode("utf-8"))
    
def log_data():
    data_str = str(speed_data["value"]) + "," + str(rpm_data["value"]) + "," + str(time_data["value"])
    
    open(("LogData-%d.csv" % log_file_time), "a").write("\n" + data_str)

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
                send_data(s)
                
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