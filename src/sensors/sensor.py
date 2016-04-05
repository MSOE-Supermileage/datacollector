#!/usr/bin/env python
# coding=utf-8

import serial
import time


class BaseSensor:

    """
    open a serial connection on provided port and read with provided options.

    will throw exceptions if nothing is connected to that port / device.
    """
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.serial_conn = serial.Serial(port, baudrate=baudrate, timeout=timeout)

    def get_data(self):
        """
        read data via serial, return it as a dictionary keyed off of the type of data it represents.
        """
        pass

    def get_keys(self):
        """
        get the data keys for this sensor
        """
        pass


class GenericSensor(BaseSensor):

    # override
    def get_data(self):
        data = {"data": 0.0, "errors": ""}
        # assume line delimited numbers
        raw_read = self.serial_conn.readline()
        data["time"] = int(time.time() * 1000)
        try:
            data["data"] = float(raw_read)
            if data["data"].is_integer():
                data["data"] = int(data["data"])
        except ValueError:
            data["errors"] = "corrupt_serial_read: %s\n" % str(raw_read)
            data["data"] = raw_read

        return data

    # override
    def get_keys(self):
        return ["time", "data"]


"""
integration test client for generic sensor
quit with CTRL-C (^C)
run on the raspberry pi or any device with your sensor connected
"""
if __name__ == "__main__":
    s = GenericSensor("/dev/ttyUSB0")
    try:
        print(','.join(s.get_data().keys()))
        while 1:
            print(','.join(s.get_data().values()))
            time.sleep(0.25)
    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")
