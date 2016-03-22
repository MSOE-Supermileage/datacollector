#!/usr/bin/env python3
# coding=utf-8

from __future__ import division
import serial


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
            'air_flow': __get_air_flow(data),
            'air_temp': __get_air_temp(data),
            'bar_pressure': __get_bar_pressure(data),
            'engine_temp': __get_engine_temp(data),
            'engine_speed': __get_vehicle_speed(data),
            'idle_speed_motor_pos': data[21] / 2.5,
            'ignition_advance': data[79] * 0.353,
            'inj_duration': __get_inj_duration(data),
            'on_time_enrichment': data[35],
            'tachometer': __get_engine_speed(data),
            'throttle_open_rate': data[15] / 100,
            'throttle_pos': __get_throtle_pos(data),
            'voltage': data[11] / 10
        }
        return results


def __get_air_flow(data):
    """ Returns the air flow rate in kg/h """
    return data[83] * 256 + data[84]


def __get_air_temp(data):
    """ Returns the air temperature read by the ECU in degrees Farenheit """
    temp_celsius = data[6]
    return (temp_celsius * 1.8) + 32


def __get_bar_pressure(data):
    """ Returns the barometric pressure in kPa """
    return data[13] + data[82] / 10


def __get_engine_speed(data):
    """ Returns the engine speed in RPM """
    return data[4] * 50 + data[5]

def __get_engine_temp(data):
    """ Returns the engine temperature in degrees Farenheit """
    temp_celsius = data[7]
    return (temp_celsius * 1.8) + 32

def __get_inj_duration(data):
    """ Returns the injection duration in microseconds """"
    return data[19] + data[20] * 256


def __get_throtle_pos(data):
    """ Returns the current throtle position as a percentage """
    return data[3] / 2.5

def __get_vehicle_speed(data):
    """ Returns the vehicle speed in MPH (as determined by the ECU) """
    return data[27]
