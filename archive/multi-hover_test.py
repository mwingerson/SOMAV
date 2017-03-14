#multi-hover test

import subprocess
import time
import dronekit
from dronekit import connect, VehicleMode, LocationGlobalRelative

vehicle_ID_1="COM3"
vehicle_ID_2="COM9"

UAV_alt_1 = 3
UAV_alt_2 = 3

def arm(num):
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("\n\nWaiting for vehicle %s to initialise...", num)
        time.sleep(1)   

#def main():
print"connecting to vehicle 1"
UAV1 = connect('tcp:127.0.0.1:5760', wait_ready=True)
#UAV1 = connect("COM3",  baud=57600, wait_ready=True)

print"connection to vehicle 2"
UAV2 = connect('tcp:127.0.0.1:5770', wait_ready=True)
#UAV2 = connect("COM9",  baud=57600, wait_ready=True)

#Arms vehicle and fly to aTargetAltitude.
print"Basic pre-arm checks"
print"Arming vehicle 1"

while not UAV1.is_armable:
     print "\n\nWaiting for vehicle 1 to initialise..."
     time.sleep(1)  

print "Arming vehicle 2"
while not UAV2.is_armable:
     print "\n\nWaiting for vehicle 2 to initialise..."
     time.sleep(1) 

print"Both vehicles armed"


print "Arming motors"
# Copter should arm in GUIDED mode
UAV1.mode    = VehicleMode("GUIDED")
UAV1.armed   = True

    # Copter should arm in GUIDED mode
UAV2.mode    = VehicleMode("GUIDED")
UAV2.armed   = True

# Confirm vehicle armed before attempting to take off
while not UAV1.armed:
    print " Waiting for arming..."

    print "Mode: %s" % UAV1.mode.name    # settable
    time.sleep(1)

# Confirm vehicle armed before attempting to take off
while not UAV2.armed:
    print " Waiting for arming..."

    print "Mode: %s" % UAV2.mode.name    # settable
    time.sleep(1)

print "Taking off!"
UAV1.simple_takeoff(UAV_alt_1) # Take off to target altitude
UAV2.simple_takeoff(UAV_alt_2) # Take off to target altitude

flight_time = time.time()
# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
#  after Vehicle.simple_takeoff will execute immediately).
while True:
    print "UAV1 Altitude: ", UAV1.location.global_relative_frame.alt
    print "UAV2 Altitude: ", UAV2.location.global_relative_frame.alt
    #Break and return from function just below target altitude.
    if (UAV1.location.global_relative_frame.alt>=UAV_alt_1*0.95) and (UAV2.location.global_relative_frame.alt>=UAV_alt_2*0.95):
        print "Reached target altitude"
        break
    if((time.time() - flight_time) > 30): 
		break

    print"UAV1 Mode: %s" % UAV1.mode.name    # settable
    print"UAV2 Mode: %s" % UAV2.mode.name    # settable
    time.sleep(1)

print("Setting LAND mode...")
UAV1.mode = VehicleMode("LAND")
UAV2.mode = VehicleMode("LAND")

print"Winning!!!"


#if (__name__ == "__main__"):
 #   main()