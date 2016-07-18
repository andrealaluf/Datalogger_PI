# -*- coding: utf-8 -*-
#!/usr/bin/python
import time, datetime
import os
import json
from class_sensor import Sensor
from class_Medicion import Medicion
from class_Alarma import Alarma
import logging
import urllib2


class TemperatureDHT11(Sensor):

		def __init__(self, frec=0):
		
			# Instancia de un sensor
			Sensor.__init__(self,"TemperatureDHT11")

			# Actualizo la frecuencia de censado del sensor
			self.frecuencia = frec


		def getValor(self):

			resource_url = "http://192.168.1.103:8080/temperatura"
			response = json.loads(urllib2.urlopen(resource_url).read()).get("value")
			print "Valor :", response

			# Chequeo valor para alarma
			try:
				valorAlarma=self.alarma.CheckValue(int(response))
			except:
				valorAlarma = "ok"
		
			if valorAlarma == "ok":
				# Devuelvo el objeto DATO y la ALARMA en None
				return Medicion(self.getName(),response,self.unit), None	
	
			else:
				valorAlarma=valorAlarma+" "+self.unit
				# Devuelvo el objeto DATO y la ALARMA generada
				return Medicion(self.getName(),response,self.unit), valorAlarma
			
			#return response


		def getFrecuencia(self):
			return self.frecuencia

		def setFrecuencia(self, newfrec):
			self.frecuencia = newfrec
