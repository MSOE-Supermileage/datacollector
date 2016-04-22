#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import traceback

try:
    import queue
except ImportError:
    import Queue as queue
import json
import socket
import threading
import syslog
import time
import sys
import signal
from pyadb import ADB

from sensors.sensor_reader import SensorReader
from sensors.hallsensor import HallSensor
from sensors.ecu import ECUSensor
from sensors.mock_sensor import MockSensor
from sensors.joule_sensor import JouleSensor
from config import ConfigManager

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
            log_error(vals["errors"])
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
                log_error("no data to log")
                for key in sensor_reader.get_keys():
                    data[key] = 0.0
        print(data)  # DEBUG
        # sort
        ordered_values = []
        for header in csv_headers:
            ordered_values.append(data[header])
        # log
        log_data(ordered_values)


def adb_publish_thread():
    """
    adb connection thread runnable
    attempts to connect to android phone over adb and send whatever the latest
    data point looked like in JSON form.
    sends as fast as possible.
    """
    adb = ADB()
    adb.set_adb_path(config_man.get_adb_path())

    hud_inet_addr = config_man.get_android_inet_address()

    while not HALT:
        adb.wait_for_device()  # block until a device comes along
        err, dev = adb.get_devices()
        if len(dev) == 0:
            # avoid the race condition where we get the device but can't list it or it is offline or something stupid
            continue

        # lol don't connect multiple phones m8
        adb.set_target_device(dev[0])
        adb.forward_socket('tcp:' + str(hud_inet_addr[1]), 'tcp:' + str(hud_inet_addr[1]))

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(hud_inet_addr)
            while not HALT:
                s.send((json.dumps(data_points_live) + "\n").encode("utf-8"))
                time.sleep(.1)
        except Exception as e:
            if __debug__:
                traceback.print_exc()
            log_error(str(e))
            time.sleep(1)
        finally:
            s.close()


# endregion threading

# region helpers

def log_data(values):
    """ Log real sensor data to our log file """
    log_line = ','.join(str(i) for i in values) + '\n'
    if __debug__:
        print(log_line, end="")
        sys.stdout.flush()
    log_file.write(log_line)


def log_message(message):
    """ Log an informational message to the syslog and stdout if debug mode is on """
    syslog.syslog(syslog.LOG_INFO, message)
    if __debug__:
        print(message)


def log_error(message):
    """ Log an error to the syslog and stderr if debug mode is on """
    syslog.syslog(syslog.LOG_ERR, message)
    if __debug__:
        print(message, file=sys.stderr)


# noinspection PyUnusedLocal
def sigint_handler(_signo, _stack_frame):
    global HALT
    """
    handle sigint - Ctrl-C / IntelliJ Halt
    :param _signo: not used
    :param _stack_frame: not used
    """
    HALT = True
    for t_name, t in all_threads:
        if type(t) is threading.Thread and t.is_alive():
            t.join()
    if log_file:
        log_file.flush()
        log_file.close()
    syslog.syslog(syslog.LOG_INFO, "done.")

# endregion helpers


def init_log():
    global log_file, csv_headers
    # initialize log file csv header
    log_file = open(config_man.get_log_dir() + "log-%s.csv" % time.strftime("%b%d.%H.%M"), 'a', 0)
    csv_headers = []
    for sr in sensor_readers:
        csv_headers += sr.get_keys()

    log_file.write(','.join(csv_headers) + "\n")


def init_sensors():
    global sensor_readers

    for sensor in config_man.get_sensors():
        if sensor == 'hall':
            sensor_readers.append(SensorReader('hall', HallSensor()))
        elif sensor == 'ecu':
            sensor_readers.append(SensorReader('ecu', ECUSensor()))
        elif sensor == 'joule':
            sensor_readers.append(SensorReader('joule', JouleSensor()))  # in development
        else:
            sensor_readers.append(SensorReader('mock', MockSensor()))


def init_threads():
    global all_threads

    # managing and joining multiple async inputs is difficult and messy
    subscriber_pool = {"subscribers": threading.Thread(target=sensor_subscriber_thread, args=())}

    publisher_pool = {
        "android_connection": threading.Thread(target=adb_publish_thread, args=()),
        "logging": threading.Thread(target=log_data_thread, args=())
    }

    all_threads = list(subscriber_pool.items()) + list(publisher_pool.items())


# region main


def main():
    global HALT
    global all_threads

    init_sensors()
    init_log()
    init_threads()

    # start all of the threads
    for t_name, t in all_threads:
        if type(t) == threading.Thread:
            t.start()

    while not HALT:
        # heartbeat every second
        for t_name, t in all_threads:
            if not t.is_alive():
                log_error("%s thread has entered a faulted state!" % t_name)
        # print("data point live: %s" % data_points_live)
        time.sleep(1)


if __name__ == '__main__':
    if __debug__:
        print("debug mode enabled.")

    signal.signal(signal.SIGINT, sigint_handler)

    # globals
    if len(sys.argv) > 1:
        config_man = ConfigManager(sys.argv[1])
    else:
        config_man = ConfigManager()

    log_file = None
    sensor_readers = []
    csv_headers = []
    HALT = False
    all_threads = []

    # image of latest data query cycle result
    data_points_live = dict(time=0.0)

    main()

# endregion main
