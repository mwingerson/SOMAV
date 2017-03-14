#Flight Test

#This is the python script that operates
#on the manager which in turn controls the UAS

from subprocess import Popen
import classes
import time

man = classes.UAS_manager()

man.init_UAS(simulation=False, init_num=2)

man.change_all_groundspeed(5)

man.arm_all_UAS()

man.takeoff_all_UAS(15)

man.move_UAS_NED(0, 20, 0, -30)
man.move_UAS_NED(1, 20, 0, -30)

man.wait_till_all_UAS_unlocked()

man.change_all_groundspeed(10)

man.move_UAS_NED(0, 0, 20, 30)
man.move_UAS_NED(1, 0, 20, 30)

man.wait_till_all_UAS_unlocked()

man.change_all_groundspeed(15)

man.move_UAS_NED(0, -20, 0, -30)
man.move_UAS_NED(1, -20, 0, -30)

man.wait_till_all_UAS_unlocked()

man.change_all_groundspeed(20)

man.move_UAS_NED(0, 0, -20, 30)
man.move_UAS_NED(1, 0, -20, 30)

man.wait_till_all_UAS_unlocked()

man.return_to_launch(0)
man.return_to_launch(1)

#man.land_all()

man.wait_till_all_UAS_unlocked()

# wait for the windows to be closed
raw_input("Press Enter to continue...")

man.close_all_UAS()

time.sleep(2)

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)

