#!/usr/bin/env python3
# coding=utf-8

import json
import queue
# import socket
import threading
import time
import syslog
import serial

TCP_IP = "localhost"
TCP_PORT = 5001

SPEED_SERIAL_USB = "/dev/ttyUSB0"
speed_arduino = serial.Serial(SPEED_SERIAL_USB, baudrate=9600, timeout=2)

LOG_FILE_NAME = "/usr/local/share/daq/log-%s.csv" % time.strftime("%b%d.%H.%M")
logfile = open(LOG_FILE_NAME, mode='a')

HALT = False

data_points = {
    "time": queue.Queue(maxsize=0),
    "speed": queue.Queue(maxsize=0),
    "rpm": queue.Queue(maxsize=0),
}


def obtain_data():
    # obtain the speed from the arduino (blocking until it writes, up to 2 seconds)
    raw_read = speed_arduino.readline()
    try:
        speed = float(raw_read)
        cur_time = int(time.time() * 1000)

        # write to the queue to be picked up and logged
        data_points["time"].put_nowait(cur_time)
        data_points["speed"].put_nowait(speed)
        data_points["rpm"].put_nowait(0.0)
    except ValueError as e:
        err_msg = "DAQ\\corrupt_serial_read: %s" % str(e)
        syslog.syslog(syslog.LOG_ERR, err_msg)
        if __debug__:
            print(err_msg)


def send_data(sock, data):
    sock.send((json.dumps(data) + "\n").encode("utf-8"))


def log_data(cur_time=0.0, speed=0.0, rpm=0.0):
    log_line = "%d,%d,%d\n" % (cur_time, speed, rpm)
    if __debug__:
        print(log_line, end="", flush=True)
    logfile.write(log_line)


def subscriber_thread():
    while not HALT:
        obtain_data()


def data_publish_thread():
    while not HALT:
        try:
            speed = data_points["speed"].get(timeout=2)
            rpm = data_points["rpm"].get(timeout=2)
            cur_time = int(time.time() * 1000)
            log_data(cur_time, speed, rpm)
        except queue.Empty:
            pass


# def android_connect():
#     while True:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         while True:
#             try:
#                 print("Trying to connect...")
#                 s.connect((TCP_IP, TCP_PORT))
#                 print("Connected")
#                 break
#             except Exception as e:
#                 print(e)
#                 time.sleep(0.5)
#                 continue
#
#         while True:
#             try:
#                 send_data(s)
#                 time.sleep(0.05)
#             except Exception as e:
#                 print(e)
#                 print("Reconnecting")
#                 break
#
#         s.close()


subscriber_pool = {
    "speed": threading.Thread(target=subscriber_thread, args=()),
    "rpm": None
}

if __name__ == '__main__':

    def log_message(message, debug):
        if __debug__ and debug:
            print(message)
            syslog.syslog(syslog.LOG_DEBUG, message)


    logfile.write("time,speed,rpm\n")
    log_data(cur_time=int(time.time() * 1000), speed=0.0, rpm=0.0)

    for k, t in subscriber_pool.items():
        if type(t) == threading.Thread:
            t.start()

    publisher_thread = threading.Thread(target=data_publish_thread, args=())
    publisher_thread.start()

    try:
        while 1:
            # heartbeat every half second
            if __debug__:
                msg = "DAQ\\message_queue_length: %d" % data_points["speed"].qsize()
                log_message(msg, True)
                msg = "DAQ\\subscriber_thread_alive: %r" % subscriber_pool["speed"].is_alive()
                log_message(msg, True)
            # spinlock is bad - this is slightly less bad
            time.sleep(.5)
    except KeyboardInterrupt:
        syslog.syslog(syslog.LOG_INFO, "DAQ\\keyboard_interrupt: quitting...")
        HALT = True
        for k, t in subscriber_pool.items():
            if type(t) == threading.Thread and t.is_alive():
                t.join()
        if publisher_thread.is_alive():
            publisher_thread.join()
        logfile.close()
        syslog.syslog(syslog.LOG_INFO, "DAQ\\keyboard_interrupt: done.")

