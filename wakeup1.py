#!/usr/bin/python3
from __future__ import print_function

import time
import pijuice
import subprocess
import datetime
import os
import sys 

DELTA_MIN=5

# Rely on RTC to keep the time
subprocess.call(["sudo", "hwclock", "--hctosys"])

# Record start time
txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' -- Started\n'
with open('/home/pi/test.log','a') as f:
    f.write(txt)

# This script is started at reboot by cron.
# Since the start is very early in the boot sequence we wait for the i2c-1 device
while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

try:
    pj = pijuice.PiJuice(1, 0x14)
except:
    print("Cannot create pijuice object")
    sys.exit()

# Do the work
for i in range(60):
   print('*', end='')
   sys.stdout.flush()
   time.sleep(1)
print()

# Set RTC alarm 5 minutes from now
# RTC is kept in UTC
a={}
a['year'] = 'EVERY_YEAR'
a['month'] = 'EVERY_MONTH'
a['day'] = 'EVERY_DAY'
a['hour'] = 'EVERY_HOUR'
t = datetime.datetime.utcnow()
a['minute'] = (t.minute + DELTA_MIN) % 60
a['second'] = 0
status = pj.rtcAlarm.SetAlarm(a)
if status['error'] != 'NO_ERROR':
    print('Cannot set alarm\n')
    sys.exit()
else:
    print('Alarm set for ' + str(pj.rtcAlarm.GetAlarm()))

# Enable wakeup, otherwise power to the RPi will not be
# applied when the RTC alarm goes off
pj.rtcAlarm.SetWakeupEnabled(True)
time.sleep(0.4)

# PiJuice shuts down power to Rpi after 20 sec from now
# This leaves sufficient time to execute the shutdown sequence
print ('alarm set ,ready for shut')
pj.power.SetPowerOff(20)
subprocess.call(["sudo", "poweroff"])
