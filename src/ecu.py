#!/usr/bin/env python
# coding=utf-8

from __future__ import division
from sensors import *
import time


class ECUSensor(BaseSensor):
    SENTINEL = b'X'
    RESPONSE_LENGTH = 91

    def get_data(self):
        """
        Reads data from the ECU and returns it in a dictionary.
        """
        self.serial_conn.write(self.SENTINEL)
        data = self.serial_conn.read(self.RESPONSE_LENGTH)
        results = dict()
        if not data:
            for dp in self.get_keys(self):
                results[dp] = 0.0
        results = {
            'air_temp': self.get_air_temp(data),
            'engine_temp': self.get_engine_temp(data),
            'vehicle_speed': self.get_vehicle_speed(data),
            'idle_speed_motor_pos': self.get_idle_speed_motor_pos(data),
            'inj_duration': self.get_inj_duration(data),
            'engine_speed': self.get_engine_speed(data),
            'throttle_open_rate': self.get_throttle_open_rate(data),
            'throttle_pos': self.get_throttle_pos(data),
            'voltage': self.get_voltage(data),
            'fuel': self.get_fuel(data)
        }
        return results

    def get_keys(self):
        return [
            'air_temp',
            'engine_temp',
            'vehicle_speed',
            'idle_speed_motor_pos',
            'inj_duration',
            'engine_speed',
            'throttle_open_rate',
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
    def get_engine_speed(data):
        """ Returns the engine speed in RPM """
        return ord(data[4]) * 50 + ord(data[5])

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
        return ord(data[11]) / 10  # note data sheet conflicts - might be data[10] depending on implementation

    @staticmethod
    def get_fuel(data):
        """ Returns the fuel level by volume (what units, no idea - the data sheet did not say.) """
        return ord(data[62])


"""
integration test client for FCR-5G ECU
quit with CTRL-C (^C)
run on the raspberry pi or any device with the FCR-5G ECU attached via the VGA-like cable connector to USB
"""
if __name__ == "__main__":
    e = ECUSensor('/dev/ttyUSB0', 9600)
    try:
        print(','.join(e.get_data().keys()))
        while 1:
            print(','.join(e.get_data().values()))
            time.sleep(0.25)

    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")
