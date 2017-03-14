#import.py

#This script uploads a mission 

from subprocess import Popen
import classes
import time



man = classes.UAS_manager()

filePath = "C:\Users\Marshall\Dropbox\workspace\python\OKSI\classes\mission_file.txt"
#filePath = "C:\Users\marsh\Dropbox\workspace\python\OKSI\classes\mission_file.txt"

man.read_mission_file(filePath)

# man.print_missions()

man.auto_init_UAS(simulation=False)

man.print_UAS_table()

man.wait_till_all_UAS_init()

man.auto_assign_missions()

man.arm_all_UAS()

man.takeoff_all_UAS(20)

man.start_all_missions()

# wait for the windows to be closed
raw_input("Press Enter to continue...")

man.close_all_UAS()

time.sleep(2)

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)

