#Resource Monitor for NvDA
#Presents basic info on CPU load, memory and disk usage, as well as battery information.
#Authors: Alex Hall, Joseph Lee, Beqa Gozalishvili, Tuukka Ojala
# Copyright 2013-2017, released under GPL.
#converted to standalone cross platform by Mason Armstrong, 2019

import time
try:
	import espeak.core
	espeak.core.set_parameter(espeak.core.parameter_RATE,400)
	is_espeak=True
except:
	is_espeak=False
import subprocess
from datetime import datetime
import sys
import os
import platform
#if platform.system()=="Windows":
from accessible_output2 import outputs
import psutil
# Styles of size calculation/string composition, do not change!
# Treditional style, Y, K, M, G, B, ...
traditional = [
	(1024.0**8.0, 'Y'),
	(1024.0**7.0, 'Z'),
	(1024.0**6.0, 'E'),
	(1024.0**5.0, 'P'),
	(1024.0**4.0, 'T'), 
	(1024.0**3.0, 'G'), 
	(1024.0**2.0, 'M'), 
	(1024.0**1.0, 'K'),
	(1024.0**0.0, 'B'),
	]

# Alternative style (displayed with most PCs): MB, KB, GB, YB, ZB, ...
alternative = [
	(1024.0**8.0, ' YB'),
	(1024.0**7.0, ' ZB'),
	(1024.0**6.0, ' EB'),
	(1024.0**5.0, ' PB'),
	(1024.0**4.0, ' TB'), 
	(1024.0**3.0, ' GB'), 
	(1024.0**2.0, ' MB'), 
	(1024.0**1.0, ' KB'),
	(1024.0**0.0, (' byte', ' bytes')),
	]

# Verbose style: Kilobytes, Megabytes, Gigabytes, ...
verbose = [
	(1024.0**8.0, ' yottabytes'),
	(1024.0**7.0, ' zettabytes'),
	(1024.0**6.0, ' exabytes'),
	(1024.0**5.0, (' petabyte', ' petabytes')),
	(1024.0**4.0, (' terabyte', ' terabytes')), 
	(1024.0**3.0, (' gigabyte', ' gigabytes')), 
	(1024.0**2.0, (' megabyte', ' megabytes')), 
	(1024.0**1.0, (' kilobyte', ' kilobytes')),
	(1024.0**0.0, (' byte', ' bytes')),
	]

# International Electrotechnical Commission (IEC) style: Ki, Mi, Gi, Ti, ...
iec = [
	(1024.0**8.0, 'Yi'),
	(1024.0**7.0, 'Zi'),
	(1024.0**6.0, 'Ei'),
	(1024.0**5.0, 'Pi'),
	(1024.0**4.0, 'Ti'),
	(1024.0**3.0, 'Gi'), 
	(1024.0**2, 'Mi'), 
	(1024.0**1.0, 'Ki'),
	(1024.0**0.0, ''),
	]

# International System of Units (Si) style: each unit is 1000 of another (i.e. 1000 KB is 1 MB)
si = [
	(1000.0**8.0, 'Y'),
	(1000.0**7.0, 'Z'),
	(1000.0**6.0, 'E'),
	(1000.0**5.0, 'P'),
	(1000.0**4.0, 'T'), 
	(1000.0**3.0, 'G'), 
	(1000.0**2.0, 'M'), 
	(1000.0**1.0, 'K'),
	(1000.0**0.0, 'B'),
	]

def size(bytes, system=traditional):
	for factor, suffix in system:
		if float(bytes) >= float(factor):
			break
	amount = float(bytes/factor)
	if isinstance(suffix, tuple):
		singular, multiple = suffix
		if float(amount) == 1.0:
			suffix = singular
		else:
			suffix = multiple
	return "{:.2F}{}".format(float(amount), suffix)

def tryTrunk(n):
	#this method basically removes decimal zeros, so 5.0 will just be 5.
	#If the number ends in anything other than a 0, nothing happens (if the trunkated number is not equal to the decimal).
	if n==int(n): return int(n)
	return n

def announceDriveInfo():
	info = []
	for drive in psutil.disk_partitions():
		if drive.fstype:
			driveInfo=psutil.disk_usage(drive[0])
			if driveInfo[0]>1 and drive[2]!="squashfs":
				info.append(str("{driveName} ({driveType} drive): {usedSpace} of {totalSpace} used {percent}%.").format(driveName=drive[0], driveType=drive[2], usedSpace=size(driveInfo[1], alternative), totalSpace=size(driveInfo[0], alternative), percent=tryTrunk(driveInfo[3])))
		speak(" ".join(info))

def announceNetworkInfo():
	net=psutil.net_io_counters()
	info="Sent since boot: "+size(net[0],alternative)+". Received since boot: "+size(net[1],alternative)
	speak(info)

def announceProcessorInfo():
	cores=psutil.cpu_count() #number of cores
	averageLoad=psutil.cpu_percent()
	averageFreq=round(psutil.cpu_freq()[0]/1024,2)
	perCpuLoad=psutil.cpu_percent(interval=0.2, percpu=True)
	coreLoad = []
	for i in range(len(perCpuLoad)):
		coreLoad.append(str("Core {coreNumber}: {corePercent}%").format(coreNumber=str(i+1), corePercent=tryTrunk(perCpuLoad[i])))
	info="Average CPU load {avgLoad}%, {avgFreq} GHZ. {cores}.".format(avgLoad=tryTrunk(averageLoad), avgFreq=tryTrunk(averageFreq), cores=", ".join(coreLoad))
	speak(info)

def announceRamInfo():
	ram=psutil.virtual_memory()
	info="Physical: {physicalUsed} of {physicalTotal} used ({physicalPercent}%). ".format(physicalUsed=size(ram[3], alternative), physicalTotal=size(ram[0], alternative), physicalPercent=tryTrunk(ram[2]))
	virtualRam=psutil.swap_memory()
	info+="Virtual: {virtualUsed} of {virtualTotal} used ({virtualPercent}%).".format(virtualUsed=size(virtualRam[1], alternative), virtualTotal=size(virtualRam[0], alternative), virtualPercent=tryTrunk(virtualRam[3]))
	speak(info)

def getUptime():
	bootTimestamp = psutil.boot_time()
	if bootTimestamp == 0.0:
		raise TypeError
	uptime = datetime.now() - datetime.fromtimestamp(bootTimestamp)
	hours, remainingMinutes = divmod(uptime.seconds, 3600)
	minutes, seconds = divmod(remainingMinutes, 60)
	hoursMinutesSeconds = "{hours:02}:{minutes:02}:{seconds:02}".format(hours=hours, minutes=minutes, seconds=seconds)
	return str("{days} days, {hoursMinutesSeconds}").format(days=uptime.days, hoursMinutesSeconds=hoursMinutesSeconds)

def announceUptime():
	uptime = getUptime()
	speak(uptime)
def speak(text):
	print(text)
#We use espeak on Linux and other OS's.
#	if platform.system()!="Windows":
#		cmd("espeak -s 350 "+text)
#	else:
	speaker = outputs.auto.Auto()
	speaker.speak(text)
	if is_espeak==True:
		while espeak.core.is_playing()==True:
			time.sleep(0.005)

def main():
	number=int(sys.argv[1])
	if number==1:
		announceProcessorInfo()
	if number==2:
		announceRamInfo()
	if number==3:
		announceDriveInfo()
	if number==4:
		announceUptime()
	if number==5:
		announceNetworkInfo()

def cmd(command):
	output=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result=(output.stdout.read()+output.stderr.read()).strip()
	if result.endswith(b"operable program or batch file."):
		return ""
	elif result.endswith(b"command not found"):
		return ""
	return result

main()