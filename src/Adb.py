import socket
import time

TCP_IP = "localhost"
TCP_PORT = 5001
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            print("Trying to connect...")
            
            s.connect((TCP_IP, TCP_PORT))
            
            print("Connected")
            
            break
        except Exception as e:
            time.sleep(0.1)
            
            continue
    
    while True:
        try:
            print("Sending message")
            
            s.send(MESSAGE.encode('utf_8'))
            
            print("Sent message")
            
            time.sleep(0.5)
        except Exception as e:
            print("Reconnecting")
            
            break
    
    s.close()
    
    print("Received data:", "data")