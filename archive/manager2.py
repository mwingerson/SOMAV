#!/usr/bin/env python

import sys
import platform
import serial.tools.list_ports
import time
from dronekit.mavlink import MAVConnection
from pymavlink import mavutil, mavwp
from dronekit import connect

import classes
import threading
from threading import Thread
from subprocess import Popen

CLOSE_MSG = "1"
INIT_MSG = "2"
ARM_MSG = "3"
TAKEOFF_MSG = "4"
LANDDISARM_MSG = "5"
MOVE_NED_MSG = "6"
MOVE_GPS_MSG = "7"

man_name = ("Rick", "Morty", "Beth", "Jerry", "Summer", "snuggles/Snowball", "Mr. PB", "Amish Cyborg")

select_ports = ("COM3", "COM3", "COM3")

move_north = 10
move_east = 10
move_down = 0

enum_UAS = []

drone_num = 2

def wait_till_UAS_unlocked(flag):
	pass_flag = False
	while not pass_flag:
		for i in range(drone_num):
			pass_flag = True
			#print "In %s wait - %s - %d" % (flag, enum_UAS[i].UAS_name, enum_UAS[i].UAV_locked)
			if enum_UAS[i].UAV_locked == True:
				pass_flag = False

		time.sleep(0.5)

#initialize instances of UAS class
for i in range(drone_num):
	t = classes.UAS()
	enum_UAS += [t]
	t.start()

#initialize UAS
#simulation
for i in range(drone_num):
	enum_UAS[i].mailbox.put((INIT_MSG, 
	  			  i, 
	  			  57600,
	  			  "UAS IP unused in sim", 
	  			  "udp:127.0.0.1:1455%d" % i, 
	  			  "udp:127.0.0.1:1555%d" % i, 
	  			  True, 
	  			  man_name[i]))

	enum_UAS[i].UAV_locked = True

#IRL
# for i in range(drone_num):
# 	enum_UAS[i].mailbox.put((INIT_MSG, 
# 	  			  i, 
# 	  			  57600,
# 	  			  "UAS IP unused in sim", 
# 	  			  "udp:127.0.0.1:1455%d" % i, 
# 	  			  "udp:127.0.0.1:1555%d" % i, 
# 	  			  True, 
# 	  			  man_name[i]))

# 	enum_UAS[i].UAV_locked = True

for i in range(drone_num):
	enum_UAS[i].mailbox.put((ARM_MSG, ))
	enum_UAS[i].UAV_locked = True

wait_till_UAS_unlocked("arming")

for i in range(drone_num):
	enum_UAS[i].mailbox.put((TAKEOFF_MSG, 10))
	enum_UAS[i].UAV_locked = True

time.sleep(10)

wait_till_UAS_unlocked("takeoff")

for i in range(drone_num):
	enum_UAS[i].mailbox.put((MOVE_NED_MSG,move_north, move_east, move_down))
	enum_UAS[i].UAV_locked = True

wait_till_UAS_unlocked("first move")

for i in range(drone_num):
	enum_UAS[i].mailbox.put((MOVE_NED_MSG,-1*move_north,-1*move_east, 0))
	enum_UAS[i].UAV_locked = True

wait_till_UAS_unlocked("second move")

for i in range(drone_num):
	enum_UAS[i].mailbox.put((LANDDISARM_MSG,))
	enum_UAS[i].UAV_locked = True

wait_till_UAS_unlocked("landing")

# wait for the windows to be closed
raw_input("Press Enter to continue...")

for i in range(drone_num):
	enum_UAS[i].stop()

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)

