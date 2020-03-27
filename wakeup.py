#!/usr/bin/python3
import pijuice

pj=pijuice.PiJuice(1,0x14)
pj.rtcAlarm.SetWakeupEnabled(True)
pj.rtcAlarm.SetAlarm({'second': 0, 'minute': 1, 'hour': 0, 'weekday': '2;3;4;5;6'})
pj.power.SetPowerOff(20)
subprocess.call(["sudo", "poweroff"])
