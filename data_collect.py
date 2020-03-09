#!/usr/bin/env python
#-*- coding: utf-8 -*-

import bme680
import time

print("""data_collect.py - Affiche la température, pression, le pourcentage d'humidité dans l'air, et la qualité de l'air.
Appuyez sur Ctrl+C pour quitter.
""")

try:
	sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
	sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

print("Calibrage des données: ")
for name in dir(sensor.calibration_data):
	
	if not name.startswith('_'):
		value = getattr(sensor.calibration_data, name)

		if isinstance(value, int):
			print('{}: {}'.format(name, value))

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitialisation des relevés :')
for name in dir(sensor.data):
	value = getattr(sensor.data, name)

	if not name.startswith('_'):
		print('{}:{}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

print('\n\nRécupération:')
try:
	while True:
		if sensor.get_sensor_data():
			output = '{0:.2f}°C,{1:.2f} hPa,{2:.2f} %RH (Relative Humidity)'.format(sensor.data.temperature,sensor.data.pressure, sensor.data.humidity)
			
			if sensor.data.heat_stable:
				print('{0},{1} Ohms'.format(output,sensor.data.gas_resistance))
			else:
				print(output)
		
		time.sleep(1)

except KeyboardInterrupt:
	pass
