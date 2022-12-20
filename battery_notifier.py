# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:22:55 2022

@author: ACER
"""
import time
import psutil
import serial_connect
import serial.tools.list_ports
import error_statements as er

TURN_ON_THRESH = 45
TURN_OFF_THRESH = 90

counter = [0]


def convert_time(seconds):
    """ Function to cvonvert seconds into HH:MM:S format """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def display_info(percent, plugged_status, time_left):
    """ A simple function to display the availabel information """

    if plugged_status is True:
        time_left = "PC is on Charge"

    if plugged_status is False and int(time_left.split(":")[0]) >= 12:
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
    time_left = convert_time(battery.secsleft)

    return percent, plugged_status, time_left

def mcu_control_logic(mcu, percent, plugged_status):
    """ The function to control MCU for charging purposes """

    if TURN_OFF_THRESH == 100 and percent >= TURN_OFF_THRESH and plugged_status is True:  # 100%
        print("Waiting for full charge @ 100%")
        time.sleep(300)  # 5 * 60 SECS
        print("Removing charger")
        print()
        mcu.write('0'.encode())
        time.sleep(5)

        while 1:
            percent, plugged_status, time_left = get_battery_status()
            if plugged_status is not True:
                break
            print("Its possible bypass switch is ON \n")
            time.sleep(5)

    elif percent >= TURN_OFF_THRESH and plugged_status is True:
        print(f"Removing charger, Treshold reached @ {TURN_OFF_THRESH}")
        print()
        mcu.write('0'.encode())
        time.sleep(5)

        while 1:
            percent, plugged_status, time_left = get_battery_status()
            if plugged_status is not True:
                break
            print("Its possible bypass switch is ON \n")
            time.sleep(5)

    elif percent <= TURN_ON_THRESH and plugged_status is False:
        print(f"Charging On, Treshold Reached @ {TURN_ON_THRESH}")
        print()
        mcu.write('1'.encode())
        time.sleep(5)
        counter[0] += 1

        if counter[0] >= 3 and plugged_status is False:
            print("It's possible power adapter is not yet turned on. \n")

    if plugged_status is True:
        counter[0] = 0



def thresh_valiadte(turn_on_thresh, turn_off_thresh):
    """ A function to validate Turn On and Turn Off thresholds """

    if 5 <= turn_on_thresh <= 100:
        pass
    else:
        raise ValueError("Turn ON threshold should be between 5 - 100 \n")

    if 5 <= turn_off_thresh <= 100:
        pass
    else:
        raise ValueError("Turn OFF threshold should be between 5 - 100 \n")

    if (turn_off_thresh - turn_on_thresh) >= 20:
        pass
    else:
        raise ValueError(
            "There should be minimium gap of 20% between Turn ON and OFF thresholds\n")


try:
    thresh_valiadte(TURN_ON_THRESH, TURN_OFF_THRESH)
    mcu = serial_connect.connect_port(display=True, baud=9600)
    print()

    while 1:

        percent, plugged_status, time_left = get_battery_status()
        display_info(percent, plugged_status, time_left)
        mcu_control_logic(mcu, percent, plugged_status)
        time.sleep(2.5)
        mcu.write('9'.encode())
        time.sleep(2.5)

except ValueError as e:
    print(er.VAL_ERR, e)

except TypeError as e:
    print(er.NO_USB, e)

except NameError as e:
    print(er.PORT_ERR, e)

except serial.serialutil.SerialException as e:
    print(er.SERIAL_ERR, e)
    try:
        mcu.close()
        print("\nConnection closed, safely remove the device.")
    except Exception:
        pass

except Exception as e:
    print(er.UNKNOWN_ERR, e)
