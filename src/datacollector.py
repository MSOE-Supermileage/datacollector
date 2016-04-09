#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
try:
    import queue
except ImportError:
    import Queue as queue
import json
import socket
import threading
import syslog
import math
import time
import sys
import os

from sensors.sensor_reader import SensorReader
from sensors.hallsensor import HallSensor
from sensors.ecu import ECUSensor
from sensors.mock_sensor import MockSensor
from sensors.joule_sensor import JouleSensor

# region variables

# android connection stuff
TCP_IP = "localhost"
TCP_PORT = 5001

LOG_FILE_NAME = "/daq_data/log-%s.csv" % time.strftime("%b%d.%H.%M")
# LOG_FILE_NAME = "test.log"

# image of latest data query cycle result
data_points_live = dict(time=0.0)

# endregion variables

# region threading
# things that require global access to stuff


def obtain_data():
    """
    hit all of the sensors to query for data
    syslog any errors
    """
    for sensor_reader in sensor_readers:
        vals = sensor_reader.read()
        if 'errors' in vals:
            syslog.syslog(syslog.LOG_ERR, vals["errors"])
            if __debug__:
                print(vals["errors"])
            del vals["errors"]
        data_points_live.update(vals)
    # aggregate timestamp
    data_points_live["time"] = int(time.time() * 1000)


def sensor_subscriber_thread():
    """
    runnable to poll sensors and query for data
    polls every 0.1 seconds (10hz)
    NOTE: frequency needs to be a function of how fast the system can log data and how frequent
            the sensors can output data.
    """
    while not HALT:
        obtain_data()
        # query data at 10hz - may need adjustment
        time.sleep(0.1)


def log_data_thread():
    """
    runnable to pull off the data_point queues and log as fast as possible
    """
    while not HALT:
        # aggregate
        data = dict()
        for sensor_reader in sensor_readers:
            try:
                data.update(sensor_reader.pop_latest())
            except queue.Empty:
                print("null read")
                for key in sensor_reader.get_keys():
                    data[key] = 0.0
        if __debug__:
            print(data)
        # sort
        ordered_values = []
        for header in csv_headers:
            ordered_values.append(data[header])
        # log
        if __debug__:
            print(ordered_values)
        log_data(ordered_values)


def adb_publish_thread():
    """
    adb connection thread runnable
    attempts to connect to android phone over adb and send whatever the latest
    data point looked like in JSON form.
    sends as fast as possible.
    """
    while not HALT:
        try:
            syslog.syslog(syslog.LOG_DEBUG, "Attempting to establish adb connection...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            num_attempts = 0
            while not HALT:
                try:
                    if __debug__:
                        print("Trying to connect...")

                    s.connect((TCP_IP, TCP_PORT))
                    syslog.syslog(syslog.LOG_INFO, "adb connected.")

                    if __debug__:
                        print("Connected")
                    break
                except Exception as e:
                    syslog.syslog(syslog.LOG_ERR, str(e))

                    if __debug__:
                        print(e)

                    num_attempts += 1
                    # wait increases logarithmically, up to 5 seconds
                    wait_time = .5 * int(math.log(num_attempts, 10))
                    time.sleep(wait_time if wait_time < 5.0 else 5.0)
                    continue

            while not HALT:
                try:
                    s.send((json.dumps(data_points_live) + "\n").encode("utf-8"))
                    time.sleep(0.01)
                except Exception as e:
                    syslog.syslog(syslog.LOG_ERR, str(e))
                    if __debug__:
                        print(e)
                        print("Reconnecting")
                    break
        except Exception as sock_create_err:
            syslog.syslog(syslog.LOG_ERR, str(sock_create_err))
        finally:
            s.close()


# endregion threading

# region helpers

def log_data(values):
    log_line = ','.join(str(i) for i in values) + '\n'
    if __debug__:
        print(log_line, end="")
        sys.stdout.flush()
    log_file.write(log_line)


def log_message(message):
    syslog.syslog(syslog.LOG_INFO, message)
    if __debug__:
        print(message)

# endregion helpers


# region main

def main():
    global HALT

    # start all of the threads
    all_threads = list(subscriber_pool.items()) + list(publisher_pool.items())
    for t_name, t in all_threads:
        if type(t) == threading.Thread:
            t.start()

    try:
        while 1:
            # heartbeat every second
            for t_name, t in all_threads:
                msg = "%s_thread_alive: %r" % (t_name, t.is_alive())
                log_message(msg)
            # spinlock is bad - this is slightly less bad
            time.sleep(1)
    except KeyboardInterrupt:  # if we are running headless in the car, it does not shut off until car turnoff.
        syslog.syslog(syslog.LOG_INFO, "keyboard_interrupt: quitting...")
        # queue up quitting
        HALT = True
    finally:
        for t_name, t in all_threads:
            if type(t) is threading.Thread and t.is_alive():
                t.join()
        log_file.flush()
        log_file.close()
        syslog.syslog(syslog.LOG_INFO, "done.")


if __name__ == '__main__':
    if __debug__:
        print("debug mode enabled.")
    
    # initialize thread pooling

    # managing and joining multiple async inputs is difficult and messy
    subscriber_pool = {"all": threading.Thread(target=sensor_subscriber_thread, args=())}

    publisher_pool = {
        "android_connection": threading.Thread(target=adb_publish_thread, args=()),
        "logging": threading.Thread(target=log_data_thread, args=())
    }

    # initialize sensors

    # aggregate different sensors based on environment variable describing car type
    car_type = os.environ.get("DAQ_CAR_TYPE")

    if car_type == "electric":
        sensor_readers = [SensorReader("hall", HallSensor())]
		sensor_readers = [SensorReader("joule", JouleSensor())]
    elif car_type == "gas":
        sensor_readers = [
            SensorReader("hall", HallSensor()),
            SensorReader("ecu", ECUSensor())
        ]
    elif car_type == "development":
        sensor_readers = [SensorReader("mock", MockSensor())]
    else:
        # msg = "environment: DAQ_CAR_TYPE not set. try 'gas' or 'electric'."
        # syslog.syslog(syslog.LOG_ERR, msg)
        # raise RuntimeError(msg)
        sensor_readers = [SensorReader("hall", HallSensor())]

    # initialize log file csv header
    log_file = open(LOG_FILE_NAME, 'a', 0)
    csv_headers = []
    for sr in sensor_readers:
        csv_headers += sr.get_keys()

    log_file.write(','.join(csv_headers) + "\n")

    HALT = False

    main()

# endregion main
