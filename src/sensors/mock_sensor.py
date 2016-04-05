#!/usr/bin/env python
# coding=utf-8

from sensor import BaseSensor
import time
import random


class MockSensor(BaseSensor):

    # noinspection PyMissingConstructor
    def __init__(self, port=None, baudrate=9600, timeout=1):
        # don't call because this creates a serial reader at the port
        # BaseSensor.__init__(self, port, baudrate, timeout)
        self.speed = random.random() * 20.0
        self.rpm = random.random() * 300.0

    # override
    def get_data(self):
        data = {"time": 0, "rpm": 0.0, "speed": 0.0, "hall_time": int(time.time() * 1000)}

        change = (random.random() - 0.5)
        self.speed += change * 2.0
        self.rpm += change * 30.0

        data["speed"] = self.speed
        data["rpm"] = self.rpm

        return data

    # override
    def get_keys(self):
        return ["time", "speed", "rpm"]

