#init_test.py

#This script is the testing for happy initialization of the UAS

from subprocess import Popen
import classes
import time

man = classes.UAS_manager()

man.auto_init_UAS(simulation=True)

man.check_all_armable()

man.wait_till_all_UAS_init()

man.arm_all_UAS()

# man.takeoff_all_UAS(20)


# wait for the windows to be closed
raw_input("Press Enter to continue...")

man.close_all_UAS()

time.sleep(2)

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)

