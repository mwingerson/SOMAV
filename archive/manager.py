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

man_name = ( "Rick", "Morty", "Jerry", "Beth", "Summer", "snuggles/Snowball", "Mr. PB", "Amish Cyborg")

select_ports = ("25.118.135.27:5770", "25.118.135.27:5760", "COM11")

move_north = 10
move_east = 10
move_down = 0

enum_UAS = []

num_of_UAS = 2

#initializer functions
def initialize_all_UAS(enum_UAS, simulation=False, sequentially=False):
	#initialize instances of UAS class
	for i in range(num_of_UAS):
		t = classes.UAS()
		enum_UAS += [t]
		t.start()

	for i in range(num_of_UAS):
		if simulation:
			enum_UAS[i].mailbox.put((INIT_MSG, 
			  			  i, 
			  			  57600,
			  			  "UAS IP unused in sim", 
			  			  "udp:127.0.0.1:1455%d" % i, 
			  			  "udp:127.0.0.1:1555%d" % i, 
			  			  True, 
			  			  man_name[i]))
		else:
			enum_UAS[i].mailbox.put((INIT_MSG, 
			  			  i, 
			  			  57600,
			  			  select_ports[i], 
			  			  "udp:127.0.0.1:1455%d" % i, 
			  			  "udp:127.0.0.1:1555%d" % i, 
			  			  False, 
			  			  man_name[i]))

		# Option to initialize sequentially
		if sequentially:
			while not enum_UAS[i].get_UAS_init():
				time.sleep(2)

	#wait until all UAS are initialized
	pass_flag = False
	while not pass_flag:
		for i in range(num_of_UAS):
			pass_flag = True
			if not enum_UAS[i].get_UAS_init():
				pass_flag = False

		#print "waiting for unlock"
		time.sleep(1)

def arm_all_UAS():
	for i in range(num_of_UAS):
		enum_UAS[i].mailbox.put((ARM_MSG, ))

	pass_flag = False
	while not pass_flag:
		for i in range(num_of_UAS):
			pass_flag = True
			if not enum_UAS[i].get_UAS_armed():
				pass_flag = False

		#print "waiting for unlock"
		time.sleep(0.5)

def takeoff_all_UAS(enum_UAS):
	for i in range(num_of_UAS):
		enum_UAS[i].mailbox.put((TAKEOFF_MSG, 10))

	pass_flag = False
	while not pass_flag:
		for i in range(num_of_UAS):
			pass_flag = True
			if not enum_UAS[i].get_UAS_RTF():
				pass_flag = False

		#print "waiting for unlock"
		time.sleep(1)

#utility functions
def wait_till_all_UAS_unlocked(enum_UAS):
	pass_flag = False
	while not pass_flag:
		for i in range(num_of_UAS):
			pass_flag = True
			if enum_UAS[i].get_UAS_locked():
				pass_flag = False

		#print "waiting for unlock"
		time.sleep(1)

def check_for_guided_mode(number):

#sets the speed in m/s
def change_groundspeed(number, speed):
	enum_UAS[number].set_groundspeed(speed)

def change_all_groundspeed(speed):
	for i in range(num_of_UAS):
		change_groundspeed(i, speed)

#movement functions
def move_UAS_NED(number, dNorth, dEast, dDown):
	enum_UAS[number].mailbox.put((MOVE_NED_MSG, dNorth, dEast, dDown))

def move_all_NED(dNorth, dEast, dDown):
	for i in range(num_of_UAS):
		enum_UAS[i].mailbox.put((MOVE_NED_MSG, dNorth, dEast, dDown))

#Ending functions
def land_UAS(number):
	enum_UAS[number].mailbox.put((LANDDISARM_MSG,))

def land_all():
	for i in range(num_of_UAS):
		enum_UAS[i].mailbox.put((LANDDISARM_MSG,))

def close_UAS(number):
	enum_UAS[number].stop()

def close_all_UAS():
	for i in range(num_of_UAS):
		enum_UAS[i].stop()




initialize_all_UAS(enum_UAS, simulation=True)

arm_all_UAS()

takeoff_all_UAS()

#move north
move_all_NED(20, 0, -10)

wait_till_all_UAS_unlocked(num_of_UAS, enum_UAS)

#move east
move_all_NED(0, 20, 0)

wait_till_all_UAS_unlocked(num_of_UAS, enum_UAS)

#move_south
move_all_NED(-20, 0, 0)

wait_till_all_UAS_unlocked(num_of_UAS, enum_UAS)

#move west
move_all_NED(0, -20, 0)

wait_till_all_UAS_unlocked(num_of_UAS, enum_UAS)

#land
land_all()

# wait for the windows to be closed
raw_input("Press Enter to continue...")

close_all_UAS()

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)

