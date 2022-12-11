""" A simple module to prvide solutions to errors raised during execution """

NO_USB = """It's likely that the tracker is not yet connected!!

 ************************************
 Did you forget to connect tracker ??
 Check the connections once.
 ************************************

---------------- FULL ERROR ----------------

"""


SERIAL_ERR = """It's likely that you removed the tracker and reconnected it!!

 ************************************
 Disconnect the tracker and reconnect
 it and start the script again.
 Kindly avoid removing the tracker
 when at use.
 ************************************

---------------- FULL ERROR ----------------

"""

VAL_ERR = """It's likely a threshold based error!!

 ************************************
 Keep turn On and Off thresholds
 between 5 to 100
 Make sure there is difference of
 20% between Turn Off and Turn on
 Threshold.
 ************************************

---------------- FULL ERROR ----------------

"""


UNKNOWN_ERR = """We don't know it yet, if you know what happened, kindly share wit us.

 ***************************************
 Email the steps to reproduce the error
 and report it to:
     ddhruvarora2@gmail.com
 ***************************************

---------------- FULL ERROR ----------------

"""
