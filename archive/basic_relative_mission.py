#basic mission plan

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math

DEBUG_FLAG = 1

def print_status(vehicle):
    # Get all vehicle attributes (state)
    # vehicle is an instance of the Vehicle class
    print "Autopilot Firmware version: %s" % vehicle.version
    print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
    print "Global Location: %s" % vehicle.location.global_frame
    print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print "Local Location: %s" % vehicle.location.local_frame    #NED
    print "Attitude: %s" % vehicle.attitude
    print "Velocity: %s" % vehicle.velocity
    print "GPS: %s" % vehicle.gps_0
    print "Groundspeed: %s" % vehicle.groundspeed
    print "Airspeed: %s" % vehicle.airspeed
    print "Battery: %s" % vehicle.battery
    print "EKF OK?: %s" % vehicle.ekf_ok
    print "Last Heartbeat: %s" % vehicle.last_heartbeat
    print "Heading: %s" % vehicle.heading
    print "Is Armable?: %s" % vehicle.is_armable
    print "System status: %s" % vehicle.system_status.state
    print "Mode: %s" % vehicle.mode.name    # settable
    print "Armed: %s" % vehicle.armed    # settable

    #print "\nPrint all parameters (iterate `vehicle.parameters`):"
    #for key, value in vehicle.parameters.iteritems():
        #print " Key:%s Value:%s" % (key,value) 

def init_UAS(vehicle, name):
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print "\n\nWaiting for vehicle to initialise..."
        print_status()
        time.sleep(1)   

    print "%s Initializated" % name

def arm_UAS(vehicle, name):
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "%s armed\n" % name

def takeoff(aTargetAltitude, vehicle, name):
    print "%s Taking off!" % name
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    # #  after Vehicle.simple_takeoff will execute immediately).
    # while True:
    #     print " Altitude: ", vehicle.location.global_relative_frame.alt
    #     #Break and return from function just below target altitude.
    #     if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
    #         print "Reached target altitude"
    #         break

    #     print_status(vehicle)
    #     time.sleep(1)

    # print"%s ready to fly\n" % name

def land_and_disarm(vehicle, name):
	vehicle.mode = VehicleMode("LAND")

	# while vehicle.location.global_relative_frame.alt > 0.3:
	# 	print "Landing %s" % name
	# 	time.sleep(2)

	# while vehicle.armed:
	# 	print "Disarming %s" % name
	# 	time.sleep(2)

	# print "%s disarmed\n" % name
	#BEEP!!!!!!
	#BEEP!!!!!!
	#BEEP!!!!!!

#sets the speed in m/s
def set_groundspeed(vehicle, name, speed):
	vehicle.groundspeed=speed
	print "%s groundspeed set to %dm/s" % (name, speed)

#North East Down NED
def goto_in_ned(vehicle, name, north, east, down):
    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, north, east)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    vehicle.simple_goto(targetLocation)

    # while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
    #     #print "DEBUG: mode: %s" % vehicle.mode.name
    #     remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
    #     print "%s Distance to target: %.1f" % (name, remainingDistance)
    #     #if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
    #     if remainingDistance<=0.3: #Just below target, in case of undershoot.
    #         print "%s Reached target" % name
    #         break;

    #     time.sleep(2)

def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned LocationGlobal has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.

    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.

    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def get_bearing(aLocation1, aLocation2):
    """
    Returns the bearing between the two LocationGlobal objects passed as parameters.

    This method is an approximation, and may not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """	
    off_x = aLocation2.lon - aLocation1.lon
    off_y = aLocation2.lat - aLocation1.lat
    bearing = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
    if bearing < 0:
        bearing += 360.00
    return bearing;

#--------------------------------------------------------
#					MAIN!!!
#--------------------------------------------------------

# #Real UAS
# UAV1 = connect("COM3", baud=57600, wait_ready=True)
# UAV2 = connect("COM9", baud=57600, wait_ready=True)

#no mavproxy
#UAV1 = connect('tcp:127.0.0.1:5760', wait_ready=True)
#UAV2 = connect('tcp:127.0.0.1:5770', wait_ready=True)

#With mavproxy
UAV1 = connect('udp:127.0.0.1:15550', wait_ready=True)
UAV2 = connect('udp:127.0.0.1:15551', wait_ready=True)

init_UAS(UAV1, "Jerry")
init_UAS(UAV2, "Morty")

arm_UAS(UAV1, "Jerry")
arm_UAS(UAV2, "Morty")

takeoff(6, UAV1, "Jerry")
takeoff(6, UAV2, "Morty")

time.sleep(5)
while (UAV1.groundspeed > 0.1) and (UAV2.groundspeed > 0.1):
	pass

set_groundspeed(UAV1, "Jerry", 6)
set_groundspeed(UAV2, "Morty", 6)

goto_in_ned(UAV1, "Jerry", 10, 10, -20)
goto_in_ned(UAV2, "Morty", 10, 10, -20)

time.sleep(10)

while (UAV1.groundspeed > 0.1) and (UAV2.groundspeed > 0.1):
	pass

goto_in_ned(UAV1, "Jerry", -10, -10, 0)
goto_in_ned(UAV2, "Morty", -10, -10, 0)

time.sleep(5)

while (UAV1.groundspeed > 0.1) and (UAV2.groundspeed > 0.1):
	pass

land_and_disarm(UAV1, "Jerry")
land_and_disarm(UAV2, "Morty")

#Close vehicle object before exiting script
print "Closing vehicle objects"
#UAV1.close()
#UAV2.close()

print("Winning!!!")

