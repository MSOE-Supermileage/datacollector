#!/usr/bin/env python3
# coding=utf-8

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
            'engine_speed': __get_vehicle_speed(data),
            'tachometer': __get_engine_speed(data),
            'temp': __get_engine_temp(data)
        }
        return results


def __get_engine_speed(data):
    """ Returns the engine speed in RPM """
    return data[4] * 50 + data[5]

def __get_engine_temp(data):
    """ Returns the engine temperature in degrees Farenheit """
    temp_celsius = data[7]
    return (temp_celsius * 1.8) + 32

def __get_vehicle_speed(data):
    """ Returns the vehicle speed in MPH (as determined by the ECU) """
    return data[27]

