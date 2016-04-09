#!/usr/bin/env python
# coding=utf-8

from sensor import BaseSensor
import time


class HallSensor(BaseSensor):

    def __init__(self, port='/dev/hallarduino', baudrate=9600, timeout=0.5):
        BaseSensor.__init__(self, port, baudrate, timeout)

    # override
    def get_data(self):
        data = {"hall_time": 0, "rpm": 0.0, "speed": 0.0}
        raw_buffered_read = self.serial_conn.readline()
        while self.serial_conn.inWaiting() > 22:
            raw_buffered_read = self.serial_conn.readline()
        raw_read = raw_buffered_read.split(b',') # grab the last line
        print('raw_read:', raw_read)
        data["hall_time"] = int(time.time() * 1000)
        if len(raw_read) == 2:
            try:
                data["rpm"] = float(raw_read[0])
            except ValueError as e:
                # this is a warning
                if "errors" not in data.keys():
                    data["errors"] = ""
                data["errors"] += "corrupt_serial_read: %s\n" % str(e)
            try:
                data["speed"] = float(raw_read[1])
            except ValueError as e:
                if "errors" not in data.keys():
                    data["errors"] = ""
                data["errors"] += "corrupt_serial_read: %s\n" % str(e)

        return data

    # override
    def get_keys(self):
        return ["hall_time", "speed", "rpm"]


"""
integration test client for Wyatt's hall effect sensing arduino
stick the magnet on the wheel, plug in the hall effect sensor to the arduino, spin the wheel
quit with CTRL-C (^C)
run on the raspberry pi with the arduino attached
"""
if __name__ == "__main__":
    import sys

    dev = sys.argv[1] if len(sys.argv) > 1 else '/dev/hallarduino'

    e = HallSensor(dev, baudrate=9600)
    try:
        print(','.join(e.get_data().keys()))
        while 1:
            print(','.join(e.get_data().values()))
            time.sleep(0.25)

    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")
