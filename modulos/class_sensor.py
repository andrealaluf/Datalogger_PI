# -*- coding: utf-8 -*-
#!/usr/bin/python
#  sensor.py
#  Copyright 2015 Leandro Saavedra
#  
from class_Medicion import Medicion
from class_Alarma import Alarma
import json, os

class Sensor(object):
	'''
		Permite crear un sensor genérico. 
		Parametros: 
			- nombre -> el mismo que figure en el archivo sensores_cfg.json
		Salida:
			- value -> es un objeto DATO
	'''
	
	#### Lectura de archivo de configuración de los sensores ###########
	path=os.path.abspath('sensores_cfg.json')
	with open(path, 'r') as fp:
		sensoresWithConfig = json.load(fp)
	####################################################################		
	
	# Inicializador objeto Sensor
	def __init__(self,idSensor):
		
		# Nombre del sensor
		self.name = idSensor
		
		# Unidad del sensor
		self.unit = self.sensoresWithConfig[self.name][0] if self.sensoresWithConfig.has_key(self.name) else "nU"
		
		# print "Atributos del Sensor: \n", dir(Dato)
				
		'''Definición de alarmas/alertas'''
		# Obtención de alarmas por encima a partir de diccionario
		self.alarmaMaxBaja = self.sensoresWithConfig[self.name][3] if self.sensoresWithConfig.has_key(self.name) else 0
		self.alarmaMaxMed = 0
		self.alarmaMaxAlta = 0
		self.alarmaMaxUrg = self.sensoresWithConfig[self.name][4] if self.sensoresWithConfig.has_key(self.name) else 0

		
		'''Alarmas por debajo '''
		# Obtención de alarmas por debajo a partir de diccionario
		self.alarmaMinBaja = self.sensoresWithConfig[self.name][1] if self.sensoresWithConfig.has_key(self.name) else 0
		self.alarmaMinMedia = 0
		self.alarmaMinAlta = 0
		self.alarmaMinUrg = self.sensoresWithConfig[self.name][2] if self.sensoresWithConfig.has_key(self.name) else 0
		
		
		# Generación de alarma para el sensor
		self.alarma = Alarma(self.name,self.alarmaMinBaja,self.alarmaMinUrg,self.alarmaMaxBaja,self.alarmaMaxUrg)
		
	####################################################################
	# 					GETTERS										   #		
	####################################################################	
	
	# Devuelve el nombre del sensor	
	def getName(self):
		return self.name

	# Devuelve el valor medido
	def getValue(self):
		# Realizar el chequeo del valor en si para ver si esta en rango
		# caso contrario lanzar alarmas
		# Cada instancia de sensor tiene que tener su metodo getValue donde crea
		# un objeto Dato y obtiene su propio valor para Dato
		# alarma.checkValue(valor)
		return Medicion(self.name,None,self.unit), None #return Dato(self.name,None,self.unit), None

		#pass
		#return self.value
	
	# Devuelve la unidad del sensor
	def getUnit(self):
		return self.unit
	
	# Devuelve el valor maximo permitido de alarma	
	def getalarmaMax(self):
		return self.alarmaMax
	# Devuelve el valor minimo permitido de alarma	
	def getalarmaMin(self):
		return self.alarmaMin
	
	# Devuelve el valor maximo de rango de operación normal 	
	def getalertaMax(self):
		return self.alertaMax
	
	# Devuelve el valor mínimo de rango de operación normal	
	def getalertaMin(self):
		return self.alertaMin
		
	####################################################################
	# 					SETTERS										   #		
	####################################################################
	
	# Modifica el nombre del sensor	
	def setName(self,newname):
		self.name=newname
		
	# Modifica la unidad del sensor
	def setUnit(self,newunit):
		self.unit=newunit
	
	# Modifica el valor maximo de alarma
	def setMaxUrg(self,newval):
		self.alarmaMaxUrg =newval
		self.alarma.setMaxAlarmaUrg(newval)

	def setMaxAlta(self,newval):
		self.alarmaMaxAlta = newval
		self.alarma.setMaxAlarmaAlta(newval)

	def setMaxMed(self,newval):
		self.alarmaMaxMed = newval
		self.alarma.setMaxAlarmaMedia(newval)

	def setMaxBaja(self,newval):
		self.alarmaMaxBaja = newval
		self.alarma.setMaxAlarmaBaja(newval)

	# Modifica el valor minimo de alarma
	def setMinUrg(self,newval):
		self.alarmaMinUrg =newval
		self.alarma.setMinAlarmaUrg(newval)

	def setMinAlta(self,newval):
		self.alarmaMinAlta = newval
		self.alarma.setMinAlarmaAlta(newval)

	def setMinMed(self,newval):
		self.alarmaMinMed = newval
		self.alarma.setMinAlarmaMedia(newval)

	def setMinBaja(self,newval):
		self.alarmaMinBaja = newval
		self.alarma.setMinAlarmaBaja(newval)
