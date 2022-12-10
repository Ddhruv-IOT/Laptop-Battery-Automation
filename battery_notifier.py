# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:22:55 2022

@author: ACER
"""

import psutil
import time
import serial_connect
import serial.tools.list_ports
import error_statements as er

TURN_ON_THRESH = 50
TURN_OFF_THRESH = 100


def convertTime(seconds):
    """ Function to cvonvert seconds into HH:MM:S format """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def display_info(percent, plugged_status, time_left):
    """ A simple function to display the availabel information """

    if plugged_status == True:
        time_left = "PC is on Charge"

    if plugged_status == False and int(time_left.split(":")[0]) >= 12:
        time_left = "Estimating..."

    print("Battery percentage : ", percent)
    print("Power plugged in   : ", plugged_status)
    print("Battery left       : ", time_left)
    print()


def get_battery_status():
    """ The core function to get battery levels and charger status """

    battery = psutil.sensors_battery()

    percent = battery.percent
    plugged_status = battery.power_plugged
    time_left = convertTime(battery.secsleft)

    return percent, plugged_status, time_left


def mcu_control_logic(mcu, percent, plugged_status):
    """ The function to control MCU for charging purposes """

    if TURN_OFF_THRESH == 100 and percent >= TURN_OFF_THRESH and plugged_status == True:  # 100%
        print("Waiting for full charge @ 100%")
        time.sleep(300)  # 5 * 60 SECS
        print("Removing charger")
        print()
        mcu.write('0'.encode())
        time.sleep(5)

        while 1:
            percent, plugged_status, time_left = get_battery_status()
            if plugged_status != True:
                break
            print("Its possible bypass switch is ON \n")
            time.sleep(5)

    elif percent >= TURN_OFF_THRESH and plugged_status == True:
        print(f"Removing charger, Treshold reached @ {TURN_OFF_THRESH}")
        print()
        mcu.write('0'.encode())
        time.sleep(5)

        while 1:
            percent, plugged_status, time_left = get_battery_status()
            if plugged_status != True:
                break
            print("Its possible bypass switch is ON \n")
            time.sleep(5)

    elif percent <= TURN_ON_THRESH and plugged_status == False:
        print(f"Charging On, Treshold Reached @ {TURN_ON_THRESH}")
        print()
        mcu.write('1'.encode())
        time.sleep(5)


try:
    mcu = serial_connect.connect_port()

    while 1:

        
        percent, plugged_status, time_left = get_battery_status()
        display_info(percent, plugged_status, time_left)
        mcu_control_logic(mcu, percent, plugged_status)
        time.sleep(2.5)
        mcu.write('9'.encode())
        time.sleep(2.5)

except TypeError as e:
    print(er.no_usb, e)

except serial.serialutil.SerialException as e:
    print(er.serial_err, e)
    try:
        mcu.close()
        print("\nConnection closed, safely remove the device.")
    except:
        pass

except Exception as e:
    print(e)
