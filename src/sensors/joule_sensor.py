#!/usr/bin/env python
# coding=utf-8

from sensor import BaseSensor
import time


class JouleSensor(BaseSensor):

    def __init__(self, port='/dev/joulearduino', baudrate=9600, timeout=0.5):
        BaseSensor.__init__(self, port, baudrate, timeout)
        self.last_query_time = 0.0

    def get_data(self):
        data = {'j_time': 0, "val": 0.0} #CHANGE WHEN WE SEE SOURCE

        curr_time = int(time.time() * 1000)

        if not self.serial_conn or not self.serial_conn.isOpen():
            if curr_time - self.timeout > self.last_query_time:
                print(self.reconnect())

        raw_buffered_read = self.serial_conn.readline()
        while self.serial_conn.inWaiting() > 22: 
            raw_buffered_read = self.serial_conn.readline()
        raw_read = raw_buffered_read.split(b',')

        data['j_time'] = int(time.time() * 1000)

        if len(raw_read) == 1:  #CHANGE WHEN WE SEE SOURCE 
            try:
                data["val"] = float(raw_read[0])
            except ValueError as e:
                if "errors" not in data.keys():
                    data["errors"] = ""
                data["errors"] += "corrupt_serial_read_joule: %s\n" % str(e)

        return data

    def get_keys(self):
        return ['j_time', 'val']  #CHANGE WHEN WE SEE SOURCE

"""
joule meter, don't know how it works yet but his is the start 
"""	
if __name__ == "__main__":
    import sys

    dev = sys.argv[1] if len(sys.argv) > 1 else '/dev/joulearduino'

    e = JouleSensor(dev, baudrate=9600)
    try:
        print(','.join(e.get_data().keys()))
        while 1:
            print(','.join(e.get_data().values()))
            time.sleep(0.25)

    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")