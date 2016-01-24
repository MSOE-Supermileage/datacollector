#!/usr/bin/env python3
# coding=utf-8

import os
import json
import queue
import socket
import threading
import time
import syslog
import serial
import math

TCP_IP = "localhost"
TCP_PORT = 5001

SPEED_SERIAL_LOC = "/dev/ttyUSB0"

LOG_FILE_NAME = "/usr/local/share/daq/log-%s.csv" % time.strftime("%b%d.%H.%M")

ELECTRIC_SENSORS = ["speed", "joules"]
GAS_SENSORS = ["speed", "oxy", "temp", "rpm"]

serial_sensors = dict()

data_points = dict(time=queue.Queue(maxsize=0))

data_points_live = dict(time=0.0)


def obtain_data():
    if serial_sensors:
        # obtain the speed from the arduino (blocking until it writes, up to 2 seconds)
        for sens_type, sens in serial_sensors.items():
            raw_read = sens.readline()
            try:
                value = float(raw_read)
                # set the timestamp for the sake of accuracy
                cur_time = int(time.time() * 1000)
                data_points_live["time"] = cur_time
            except ValueError as e:
                err_msg = "corrupt_serial_read: %s" % str(e)
                syslog.syslog(syslog.LOG_ERR, err_msg)
                if __debug__:
                    print(err_msg)
                value = 0.0
            # write to the queue to be picked up and logged
            data_points[sens_type].put_nowait(value)
            # update the data state snapshot for the android publish thread
            data_points_live[sens_type] = value

        # push the timestamp last, the logging thread waits for timestamp first.
        cur_time = int(time.time() * 1000)
        data_points["time"].put_nowait(cur_time)
    else:
        # if we have no sensors to read, wait a second
        time.sleep(1)


def sensor_subscriber_thread():
    while not HALT:
        obtain_data()


# runnable to pull off the data_point queues and log as fast as possible
def log_data_thread():
    while not HALT:
        try:
            values = []
            for k, q in data_points.items():
                # time should be first for sorting reasons
                if k == "time":
                    values = [q.get(timeout=.5)] + values
                else:
                    values.append(q.get(timeout=.5))
            print(values)
            log_data(values)
        except queue.Empty:
            pass


# adb connection thread runnable
# attempts to connect to android phone over adb and send whatever the latest
# data point looked like in JSON form.
# sends as fast as possible.
def adb_publish_thread():
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


def log_data(values):
    log_line = ','.join(str(i) for i in values) + '\n'
    if __debug__:
        print(log_line, end="", flush=True)
    log_file.write(log_line)


def log_message(message):
    syslog.syslog(syslog.LOG_INFO, message)
    if __debug__:
        print(message)


def init_sensor(sensor_type):
    serial_sensors[sensor_type] = serial.Serial(SPEED_SERIAL_LOC, baudrate=9600, timeout=2)
    data_points[sensor_type] = queue.Queue(maxsize=0)
    data_points_live[sensor_type] = 0.0


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
            for sens, dp_queue in data_points.items():
                msg = "dp_queue_length: %s\t%d" % (sens, dp_queue.qsize())
                log_message(msg)
            for t_name, t in all_threads:
                msg = "%s_thread_alive: %r" % (t_name, t.is_alive())
                log_message(msg)
            # spinlock is bad - this is slightly less bad
            time.sleep(1)
    except KeyboardInterrupt:
        syslog.syslog(syslog.LOG_INFO, "keyboard_interrupt: quitting...")
        # queue up quitting
        HALT = True
    finally:
        for t_name, t in all_threads:
            if type(t) == threading.Thread and t.is_alive():
                t.join()
        log_file.flush()
        log_file.close()
        syslog.syslog(syslog.LOG_INFO, "done.")


if __name__ == '__main__':

    # managing and joining multiple async inputs is difficult and messy
    subscriber_pool = {"all": threading.Thread(target=sensor_subscriber_thread, args=())}

    publisher_pool = {
        "android_connection": threading.Thread(target=adb_publish_thread, args=()),
        "logging": threading.Thread(target=log_data_thread, args=())
    }

    # aggregate different sensors based on environment variable describing car type
    car_type = os.environ.get("DAQ_CAR_TYPE")

    if car_type == "electric":
        # TODO add electric car sensor stuff
        sensors = ELECTRIC_SENSORS
    elif car_type == "gas":
        # TODO add gas car sensor stuff
        sensors = GAS_SENSORS
    elif car_type == "speed_only":
        sensors = ["speed"]
    else:
        msg = "environment: DAQ_CAR_TYPE not set. try 'gas' or 'electric'."
        syslog.syslog(syslog.LOG_ERR, msg)
        raise RuntimeError(msg)

    for sensor in sensors:
        init_sensor(sensor)

    log_file = open(LOG_FILE_NAME, mode='a')
    log_file.write("time," + ','.join(sensors) + "\n")

    HALT = False

    main()
