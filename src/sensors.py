#!/usr/bin/env python
# coding=utf-8

import serial


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


class HallSensor(BaseSensor):

    # override
    def get_data(self):
        data = {"rpm": 0.0, "speed": 0.0, "errors": ""}
        raw_read = self.serial_conn.readline().split(b',')
        if len(raw_read) == 2:
            try:
                data["rpm"] = float(raw_read[0])
            except ValueError as e:
                # this is a warning
                data["errors"] += "corrupt_serial_read: %s\n" % str(e)
            try:
                data["speed"] = float(raw_read[1])
            except ValueError as e:
                data["errors"] += "corrupt_serial_read: %s\n" % str(e)
        else:
            data["errors"] += "corrupt_serial_read: %s\n" % str(raw_read)

        return data

    # override
    def get_keys(self):
        return ["speed", "rpm"]


class GenericSensor(BaseSensor):

    # override
    def get_data(self):
        data = {"data": 0.0, "errors": ""}
        # assume line delimited numbers
        raw_read = self.serial_conn.readline()
        try:
            data["data"] = float(raw_read)
            if data["data"].is_integer():
                data["data"] = int(data["data"])
        except ValueError:
            data["errors"] += "corrupt_serial_read: %s\n" % str(raw_read)
            data["data"] = raw_read

        return data

    # override
    def get_keys(self):
        return ["data"]


"""
integration test client for hall effect sensor
quit with CTRL-C (^C)
run on the raspberry pi or any device with the wheel hall-effect sensing arduino connected on the
top USB port.
"""
if __name__ == "__main__":
    h = HallSensor("/dev/ttyUSB0")
    try:
        while 1:
            print(h.get_data())
    except KeyboardInterrupt as keyboard_interrupt:
        print("exiting...")


