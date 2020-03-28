#!/usr/bin/python3
from __future__ import print_function
import logging
import datetime
from datetime import datetime as dt
import time
import os
import sys
from pijuice import PiJuice # Import pijuice module
import pijuice
import subprocess
import datetime
import mysql.connector


pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

def convertTuple(data): 
	data =  ''.join(str(data)) 
	return data

def gotobed(pijuice):

	DELTA_MIN=5
	# Rely on RTC to keep the time
	subprocess.call(["sudo", "hwclock", "--hctosys"])
	# Record start time
	txt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' -- Started\n'
	with open('/home/pi/test.log','a') as f:
		f.write(txt)
	# This script is started at reboot by cron.
	# Since the start is very early in the boot sequence we wait for the i2c-1 device
#	while not os.path.exists('/dev/i2c-1'):
#		time.sleep(0.1)
#	try:
#		pijuice = pijuice.PiJuice(1, 0x14)
#	except:
#		print("Cannot create pijuice object")
#		sys.exit()

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
	status = pijuice.rtcAlarm.SetAlarm(a)
	if status['error'] != 'NO_ERROR':
		print('Cannot set alarm\n')
		sys.exit()
	else:
		print('Alarm set for ' + str(pijuice.rtcAlarm.GetAlarm()))
	# Enable wakeup, otherwise power to the RPi will not be
	# applied when the RTC alarm goes off
	pijuice.rtcAlarm.SetWakeupEnabled(True)
	time.sleep(0.4)
	# PiJuice shuts down power to Rpi after 20 sec from now
	# This leaves sufficient time to execute the shutdown sequence
	print ('alarm set ,ready for shut')
	pijuice.power.SetPowerOff(20)
	subprocess.call(["sudo", "poweroff"])


while True:
	now = dt.now()
	now = now.strftime("%Y-%m-%d %H:%M:%S")
	charge_level = pijuice.status.GetChargeLevel().get('data', -1)
	device_status = pijuice.status.GetStatus().get('data', -1)
#	print (device_status)
#	time.sleep(15)
	charge_status = (device_status["battery"])
	HatPower =  (device_status["powerInput"])
	RPIPower = (device_status["powerInput5vIo"])
	if charge_status == 'CHARGING_FROM_5V_IO':
		charge_status = "Charging from RPI"
	elif charge_status == 'CHARGING_FROM_IN':
		charge_status = "Charging from PV"
	elif charge_status == 'NORMAL':
                charge_status = ""
	temp =  pijuice.status.GetBatteryTemperature()
	temp = temp['data'] if temp['error'] == 'NO_ERROR' else temp['error']
	vbat = pijuice.status.GetBatteryVoltage()
	vbat = vbat['data'] if vbat['error'] == 'NO_ERROR' else vbat['error']
	ibat = pijuice.status.GetBatteryCurrent()
	ibat = ibat['data'] if ibat['error'] == 'NO_ERROR' else ibat['error']
	ibat = ibat * -1
	vio =  pijuice.status.GetIoVoltage()
	vio = vio['data'] if vio['error'] == 'NO_ERROR' else vio['error']
	iio = pijuice.status.GetIoCurrent()
	iio = iio['data'] if iio['error'] == 'NO_ERROR' else iio['error']
	iio = iio * -1
	data = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"T=", temp, "Vbat=", vbat, "Ibat=", ibat, "Vio=", vio, "Iio=", iio)
#	logging.basicConfig(filename='Sentry.log',level=logging.DEBUG)
#	logging.debug(data)
	data = convertTuple(data)
	ibat = round(ibat,2)
	iio = round(iio,2)
	vbat = round (vbat/1000,2)
	vio = round (vio/1000,2)
	wbat = round (vbat*ibat,3)
	wio = round (vio*iio,3)
	wnet = round (wbat-wio,2)
	os.system('clear')
	print (now)
	print ("")
	print ("PIJuice Supply\t", HatPower)
	print ("PI Supply:\t", RPIPower)
	print ("")
	print ("Charge Level:\t",charge_level, "%\t", charge_status)
	print ("Vbat: \t", vbat, "v  \t IBat: \t ",ibat, " mA \t Pbat: \t", wbat, "mW")
	print ("Vio : \t", vio, "v  \t Iio : \t ", iio, "mA \t Pio : \t", wio, "mW")
	print ("\t\t\t\t\t\t Wnet: \t", wnet, "mW")
	Sen = mysql.connector.connect(
		host="localhost",
               	user="pi",
                passwd="a-51d41e",
                database="Sentry"
        )

	data = Sen.cursor()
	sql = "INSERT INTO Sentry.BattDATA (date,ChargeLevel,ChargeStatus,Vbat,IBat,Wbat,Vio,Iio,Wio,NetW,RPIPower,HATPower) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (now,charge_level,charge_status,vbat,ibat,wbat,vio,iio,wio,wnet,RPIPower,HatPower)
	data.execute(sql, val)
	Sen.commit()
	data.close
	charge_level = int(charge_level)
	if (charge_level < 20 and  RPIPower != 'PRESENT'):
		gotobed(pijuice)

	time.sleep(4)
