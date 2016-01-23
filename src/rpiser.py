import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

print("Started listening")

while 1:
    print(ser.readline())

