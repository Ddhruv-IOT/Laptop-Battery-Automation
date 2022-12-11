# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:03:43 2022

@author: ACER
"""

import time
import serial
import serial.tools.list_ports


def find_ports(display=False):
    """ A function to find aval. COM Ports """

    ports = serial.tools.list_ports.comports()
    ports_found = []

    for port, desc, hwid in sorted(ports):
        if display:
            print()
            print(f"Port Name  : {port}")
            print(f"Port Desc  : {desc}")
            print(f"Port ID    : {hwid}")
            print()
        ports_found.append(port)

    if ports_found:
        return ports_found

    raise TypeError("No Device Error, Empty COM Port!!\n")


def connect_port(display=False, baud=9600):
    """ Function to connect with the desired MCU over serial COM port """

    port_list = find_ports(display)
    mcu_connected = serial.Serial(port=port_list[0], baudrate=baud)
    return mcu_connected


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
