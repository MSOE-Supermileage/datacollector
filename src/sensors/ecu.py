#!/usr/bin/env python
# coding=utf-8

from __future__ import division
from sensor import BaseSensor
import serial
import time
import sys


class ECUSensor(BaseSensor):
    SENTINEL = b'X'
    RESPONSE_LENGTH = 91

    def __init__(self, port='/dev/ecu', baudrate=9600, timeout=0.5):
        BaseSensor.__init__(self, port, baudrate, timeout)
        # used for tracking time since last data query, as well as reducing latency
        # of querying too often if the ECU is disconnected.
        # surprise the ECU turns off all the time.
        self.last_query_time = 0.0

    def get_data(self):
        """
        Reads data from the ECU and returns it in a dictionary.
        """
        results = dict()

        current_time = int(time.time() * 1000)
        # HACK because ecu gets killed after each burn
        # assume all 0s
        if not self.serial_conn or not self.serial_conn.isOpen():
            if current_time - self.timeout > self.last_query_time:
                self.reconnect()

        if self.serial_conn and self.serial_conn.isOpen():
            try:
                self.serial_conn.write(self.SENTINEL)
                data = self.serial_conn.read(self.RESPONSE_LENGTH)
            except serial.SerialException:
                data = None
                self.serial_conn.close()
            if not data or len(data.strip()) < 90:
                for dp in self.get_keys():
                    results[dp] = 0.0
            else:
                self.last_query_time = int(time.time() * 1000)
                results = {
                    'ecu_time': self.last_query_time,
                    'air_temp': self.get_air_temp(data),
                    'engine_temp': self.get_engine_temp(data),
                    'vehicle_speed': self.get_vehicle_speed(data),
                    'inj_duration': self.get_inj_duration(data),
                    'engine_rpm': self.get_engine_speed(data),
                    'engine_speed': self.get_engine_speed(data),
                    'throttle_pos': self.get_throttle_pos(data),
                    'voltage': self.get_voltage(data),
                    'fuel': self.get_fuel(data)
                }
        else:
            for dp in self.get_keys():
                results[dp] = 0.0
        return results

    def get_keys(self):
        return [
            'ecu_time',
            'air_temp',
            'engine_temp',
            'vehicle_speed',
            'inj_duration',
            'engine_rpm',
            'engine_speed',
            'throttle_pos',
            'voltage',
            'fuel'
        ]

    @staticmethod
    def get_air_flow(data):
        """ Returns the air flow rate in kg/h """
        return ord(data[83]) * 256 + ord(data[84])

    @staticmethod
    def get_air_temp(data):
        """ Returns the air temperature read by the ECU in degrees Fahrenheit """
        temp_celsius = ord(data[6])
        return (temp_celsius * 1.8) + 32

    @staticmethod
    def get_bar_pressure(data):
        """ Returns the barometric pressure in kPa """
        return ord(data[13]) + ord(data[82]) / 10

    @staticmethod
    def get_engine_rpm(data):
        """ Returns the engine speed in RPM """
        return ord(data[4]) * 50 + ord(data[5])

    @staticmethod
    def get_engine_speed(data):
        """ Returns the engine speed in MPH """
        gear_ratio = 5.54
        wheel_circumference_miles = 0.00099
        minutes_per_hour = 60
        return ord(data[4]) * 50 + ord(data[5]) / gear_ratio * wheel_circumference_miles * minutes_per_hour

    @staticmethod
    def get_engine_temp(data):
        """ Returns the engine temperature in degrees Fahrenheit """
        temp_celsius = ord(data[7])
        return (temp_celsius * 1.8) + 32

    @staticmethod
    def get_inj_duration(data):
        """ Returns the injection duration in microseconds """
        return ord(data[19]) + ord(data[20]) * 256

    @staticmethod
    def get_throttle_pos(data):
        """ Returns the current throttle position as a percentage """
        return ord(data[3]) / 2.5

    @staticmethod
    def get_idle_speed_motor_pos(data):
        """ Returns the idle motor position as a % TODO: learn what this is """
        return ord(data[21]) / 2.5

    @staticmethod
    def get_vehicle_speed(data):
        """ Returns the vehicle speed in MPH (as determined by the ECU) """
        return ord(data[27])

    @staticmethod
    def get_throttle_open_rate(data):
        """ Returns the throttle opening rate in Hz (1/sec) """
        return ord(data[15]) / 100

    @staticmethod
    def get_on_time_enrichment(data):
        """ Returns a percentage % that describes ON-Time Enrichment. TODO: learn what this is """
        return ord(data[35])

    @staticmethod
    def get_ignition_advance(data):
        """ Returns the ignition advance in deg-BTDC. TODO: learn what this is"""
        return ord(data[79]) * 0.353

    @staticmethod
    def get_voltage(data):
        """ Returns the battery voltage in Volts """
        return ord(data[10]) / 10  # note data sheet conflicts, says it's data[11]

    @staticmethod
    def get_fuel(data):
        """ Returns the fuel level by volume (what units, no idea - the data sheet did not say.) """
        return ord(data[62])


"""
integration test client for FCR-5 ECU
quit with CTRL-C (^C)
run on the raspberry pi or any device with the FCR-5 ECU attached via the DB-9 to USB connector
"""
if __name__ == "__main__":
    import sys

    dev = sys.argv[1] if len(sys.argv) > 1 else '/dev/ecu'

    e = ECUSensor(dev, baudrate=9600)
    try:
        print(','.join(str(i) for i in e.get_data().keys()))
        while 1:
            print(','.join(str(i) for i in e.get_data().values()))
            time.sleep(0.25)

    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")
