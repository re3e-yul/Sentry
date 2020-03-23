#!/usr/bin/python3
import logging
import datetime
from datetime import datetime as dt
import time
import os
import sys
from pijuice import PiJuice # Import pijuice module
import mysql.connector


pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object

def convertTuple(data): 
	data =  ''.join(str(data)) 
	return data



while True:
	now = dt.now()
	now = now.strftime("%Y-%m-%d %H:%M:%S")
	charge_level = pijuice.status.GetChargeLevel().get('data', -1)
	device_status = pijuice.status.GetStatus().get('data', -1)
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
	logging.basicConfig(filename='Sentry.log',level=logging.DEBUG)
	logging.debug(data)
	data = convertTuple(data)
	vbat = vbat/1000
	vio = vio/1000
	wbat = round (vbat*ibat,2)
	wio = round (vio*iio,2)
	os.system('clear')
	print (now)
	print ("")
	print ("PIJuice Supply\t", HatPower)
	print ("PI Supply:\t", RPIPower)
	print ("")
	print ("Charge Level:\t",charge_level, "%\t", charge_status)
	print ("Vbat: \t", vbat, "v \t IBat: \t ",ibat, " mA \t Pbat: \t", wbat, "mW")
	print ("Vio : \t", vio, "v \t Iio: \t ", iio, "mA \t Pio: \t", wio, "mW")

	Sen = mysql.connector.connect(
		host="localhost",
               	user="pi",
                passwd="a-51d41e",
                database="Sentry"
        )

	data = Sen.cursor()
	sql = "INSERT INTO Sentry.BattDATA (date,ChargeLevel,ChargeStatus,Vbat,IBat,Wbat,Vio,Iio,Wio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (now,charge_level,charge_status,vbat,ibat,wbat,vio,iio,wio)
	data.execute(sql, val)
	Sen.commit()
	data.close



	time.sleep(5)
