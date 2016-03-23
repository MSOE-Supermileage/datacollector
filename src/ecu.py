#!/usr/bin/env python3
# coding=utf-8

from __future__ import division
import serial
import time


class EcuCollector():
    SENTINEL = b'X'
    RESPONSE_LENGTH = 91

    def __init__(self, port, baudrate=9600):
        self.port = port
        self.serial_conn = serial.Serial(port, baudrate)

    def get_data(self):
        """
        Reads data from the ECU and returns it in a dictionary.
        """
        self.serial_conn.write(self.SENTINEL)
        data = self.serial_conn.read(self.RESPONSE_LENGTH)
        results = {
            'air_flow': get_air_flow(data),
            'air_temp': get_air_temp(data),
            'bar_pressure': get_bar_pressure(data),
            'engine_temp': get_engine_temp(data),
            'vehicle_speed': get_vehicle_speed(data),
            'idle_speed_motor_pos': ord(data[21]) / 2.5,
            'ignition_advance': ord(data[79]) * 0.353,
            'inj_duration': get_inj_duration(data),
            'on_time_enrichment': ord(data[35]),
            'tachometer': get_engine_speed(data),
            'throttle_open_rate': ord(data[15]) / 100,
            'throttle_pos': get_throtle_pos(data),
            'voltage': ord(data[11]) / 10
        }
        return results


def get_air_flow(data):
    """ Returns the air flow rate in kg/h """
    return ord(data[83]) * 256 + ord(data[84])


def get_air_temp(data):
    """ Returns the air temperature read by the ECU in degrees Farenheit """
    temp_celsius = ord(data[6])
    return (temp_celsius * 1.8) + 32


def get_bar_pressure(data):
    """ Returns the barometric pressure in kPa """
    return ord(data[13]) + ord(data[82]) / 10


def get_engine_speed(data):
    """ Returns the engine speed in RPM """
    return ord(data[4]) * 50 + ord(data[5])


def get_engine_temp(data):
    """ Returns the engine temperature in degrees Farenheit """
    temp_celsius = ord(data[7])
    return (temp_celsius * 1.8) + 32


def get_inj_duration(data):
    """ Returns the injection duration in microseconds """
    return ord(data[19]) + ord(data[20]) * 256


def get_throtle_pos(data):
    """ Returns the current throtle position as a percentage """
    return ord(data[3]) / 2.5


def get_vehicle_speed(data):
    """ Returns the vehicle speed in MPH (as determined by the ECU) """
    return ord(data[27])


if __name__ == "__main__":
    e = EcuCollector('/dev/ttyUSB0', 9600)
    try:
        while 1:
            for k, v in e.get_data().items():
                print('{} = {}'.format(k, v))
                time.sleep(0.5)

    except KeyboardInterrupt as keyboard_interrupt:
        print("stopping...")
