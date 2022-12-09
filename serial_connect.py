# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:03:43 2022

@author: ACER
"""

import serial
import serial.tools.list_ports
import time


def find_ports():
    """ A function to find aval. COM Ports """

    ports = serial.tools.list_ports.comports()

    ports_found = []

    for port, desc, hwid in sorted(ports):
        print()
        print(f"Port Name  : {port}")
        print(f"Port Desc  : {desc}")
        print(f"Port ID    : {hwid}")
        print()
        ports_found.append(port)

    if len(ports_found) != 0:
        return ports_found


def connect_port():
    """ Function to connect with the desired MCU over serial COM port """

    port_list = find_ports()
    mcu = serial.Serial(port=port_list[0], baudrate=9600)
    return mcu


if __name__ == "__main__":
    try:
        mcu = connect_port()

        while 1:
            mcu.write('1'.encode())
            time.sleep(5)
            mcu.write('0'.encode())
            time.sleep(5)

    except serial.serialutil.SerialException as e:
        print(f"The Error: {e}")
        # mcu.close()
