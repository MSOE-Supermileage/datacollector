#!/usr/bin/env python3
# coding=utf-8

# authors: austin hartline, matt manhke, wyatt stark

import RPi.GPIO as GPIO
import math
import time
import socket

print('start time: ' + time.strftime('%x %X'))

# circumference of the wheel (20") (2*pi*r*1ft/12in*1mi/5280ft)
CIRCUMFERENCE = 2.0 * math.pi * 10.0 / 12.0 / 5280

# array max size
SPEEDS_MAX_SIZE = 6

# socket / network config for client subscribers
HOST = ''
PORT = 12100
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
except socket.error as msg:
    print("socket error! " + str(msg[0]) + " " + msg[1])

# data
counter = 0
speed = 0.0
last_time = time.time()
prev_time = time.time() - 1
other_interrupt = False
speeds = []

# Log file setup
# we need the log file to graph the complete set
# of interrupts to post mortem analyze speed and acceleration
# also for debugging and electrical system triage
# if the system becomes desperately slow or we run out of
# disk space, remove logging
LOG_FILE_NAME = 'DAQ.log' + time.strftime('%b%d.%H.%M') + '.csv'

# a = append
# 0 = size 0 buffer, write immediately
logfile = open(LOG_FILE_NAME, 'a', 0)


# callback for each interrupt
def event_callback(channel):
    global counter
    global prev_time
    global last_time
    global logfile
    global other_interrupt
    if other_interrupt:
        counter += 1
        prev_time = last_time
        last_time = time.time()
        # basically System.currentTimeMillis()
        logfile.write(str(int(round(last_time * 1000))) + '\n')
        other_interrupt = False
    else:
        other_interrupt = True


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4, GPIO.RISING, callback=event_callback, bouncetime=33)


# return the AROC between two times in milliseconds as mph
def get_speed(prev_time, current_time):
    # 3600 seconds / hour
    # 2 magnets per cycle means each interrupt implies 
    # half a rotation (half circumference) -> divide by 2
    return CIRCUMFERENCE / (current_time - prev_time) * 3600 / 2


# now that we have everything else set up, wait for
# speed requests and calculate on the fly
# based on interrupts / request time
while True:

    # blocking
    # wait for a request for speed
    entered, address = sock.recvfrom(256)
    # immediately record the time of the request
    request_time = time.time()

    entered = entered.strip()
    # register ability to quit
    if entered in ["Q", "q"]: break

    if last_time - prev_time > request_time - last_time:
        current_speed = get_speed(prev_time, last_time)
        # else we are decelerating
    else:
        current_speed = get_speed(last_time, request_time)

    if len(speeds) >= SPEEDS_MAX_SIZE:
        speeds.pop(0)

    speeds.append(current_speed)

    # average speeds
    print_speed = sum(speeds) / float(len(speeds))
    # send the speed back to the client
    sock.sendto(str(print_speed), address)

# Cleanup
# cute loading style indication of steps to quitting
print("quitting.")
sock.close()
print(".")
logfile.close()
print(".")
GPIO.cleanup()
print("\ndone.")
