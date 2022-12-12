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


def select_port(display=False):
    """ Function to choose the COM port """

    port_list = find_ports(display)

    if port_list:

        if len(port_list) == 1:
            port = port_list[0]

        else:
            print(
                f"Multiple ports detected, select the desired one\n {port_list} \n")
            port = input("Enter the selected port: ")

            if port not in port_list:
                raise NameError("Terminating, port not found. Try Again!!")

    return port


def connect_port(display=False, baud=9600):
    """ Function to connect MCU over selected serial COM port """

    port = select_port(display)
    mcu_connected = serial.Serial(port=port, baudrate=baud)
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
