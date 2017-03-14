#kill all 

from subprocess import Popen

Popen("powershell.exe kill -ProcessName apm", shell=False)
Popen("powershell.exe kill -ProcessName mavproxy", shell=False)
Popen("powershell.exe kill -ProcessName python", shell=False)

