#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import os.path
import glob 
import serial
import os, sys
import json

class Alarma(object):
	'''
	Se encarga de gestionar las alarmas/alertas generadas por los 
	sensores. Se definen 4 tipos de las mismas en base al rango entre
	valor maximo/minimo	de alerta y valor maximo/minimo de alarma.
		- Alarma baja
		- Alarma media
		- Alarma alta
		- Alarma urg
	'''

	
	
	def __init__(self,sensorID,alertaMin,alarmaMin,alertaMax,alarmaMax):
		
		# Nombre del sensor correspondiente
		self.idsensor=sensorID
		
		# Configuración de las alarmas 
		'''ALARMAS DE MAXIMO '''
		self.MaxAlarmaUrg = alarmaMax # MaxUrg
		self.MaxAlarmaAlta =  0# MaxAlta
		self.MaxAlarmaMedia = 0 #MaxMedia
		self.MaxAlarmaBaja = alertaMax # MaxBaja
		
		'''ALARMAS DE MINIMO '''
		self.MinAlarmaUrg = alarmaMin   # MinUrg
		self.MinAlarmaAlta = 0 # MinAlta
		self.MinAlarmaMedia = 0 # MinMedia
		self.MinAlarmaBaja = alertaMin# MinBaja
		
		# Almacena los ultimos N estados de alarma de los valores sensados
		self.historicos = []
		
		# Asocia cada alarma con una función
		self.alarma_cod = {}
		
		'''Set de las funciones de los niveles de la alarma '''
		#self.setAlarmas(self.idsensor)
		
		
	def setMaxAlarmaBaja(self,valor):
		self.MaxAlarmaBaja = valor

	def setMaxAlarmaMedia(self,valor):
		self.MaxAlarmaMedia = valor

	def setMaxAlarmaAlta(self,valor):
		self.MaxAlarmaAlta = valor

	def setMaxAlarmaUrg(self,valor):
		self.MaxAlarmaUrg = valor
	
	def setMinAlarmaBaja(self,valor):
		self.MinAlarmaBaja = valor

	def setMinAlarmaMedia(self,valor):
		self.MinAlarmaMedia = valor

	def setMinAlarmaAlta(self,valor):
		self.MinAlarmaAlta = valor
	
	def setMinAlarmaUrg(self,valor):
		self.MinAlarmaUrg = valor							
	'''#################################################################
	Chequea el valor censado para generar la alarma correspondiente
	####################################################################
	'''
	def CheckValue(self,valorCensado):
		print "Valor Censado: %.2f \n" %valorCensado
		## Generacion de hora para guardar en archivo
		#ts = time.time()
		fecha = time.strftime('%Y-%m-%d-%H:%M:%S')
		
		if valorCensado < self.MaxAlarmaBaja and valorCensado > self.MinAlarmaBaja:
			print "Rango normal"
			return "ok"
		else:
			'''ALARMAS BAJA'''
			if (valorCensado >= self.MaxAlarmaBaja and valorCensado < self.MaxAlarmaMedia) or (valorCensado <= self.MinAlarmaBaja and valorCensado > self.MinAlarmaMedia):
				if valorCensado >=self.MaxAlarmaBaja:
					print "Alarma Baja Max"
					self.historicos.append("AlarmaMaxBaja")
				else:
					print "Alarma Baja Min"
					self.historicos.append("AlarmaMinBaja")
			
			'''ALARMAS MEDIA'''		
			if (valorCensado >= self.MaxAlarmaMedia and valorCensado < self.MaxAlarmaAlta) or (valorCensado <= self.MinAlarmaMedia and valorCensado > self.MinAlarmaAlta):
				if valorCensado >= self.MaxAlarmaMedia:
					print "Alarma Media Max"
					self.historicos.append("AlarmaMaxMedia")
				else:
					print "Alarma Media Min"
					self.historicos.append("AlarmaMinMedia")
			
			'''ALARMAS ALTA'''
			if (valorCensado >= self.MaxAlarmaAlta and valorCensado < self.MaxAlarmaUrg) or (valorCensado <= self.MinAlarmaAlta and valorCensado > self.MinAlarmaUrg):
				if valorCensado >= self.MaxAlarmaAlta:
					print "Alarma Alta Max"
					self.historicos.append("AlarmaMaxAlta")
				else:
					print "Alarma Alta Min"
					self.historicos.append("AlarmaMinAlta")
			
			'''ALARMAS URG'''
			if valorCensado >= self.MaxAlarmaUrg or valorCensado <= self.MinAlarmaUrg:
				if valorCensado >= self.MaxAlarmaUrg:
					print "Alarma Urgente Max" 
					self.historicos.append("AlarmaMaxUrg")
				else:
					print "Alarma Urgente Min"
					self.historicos.append("AlarmaMinUrg")
				
			
			'''#########################################################
			Registro de alarmas disparadas en archivo logAlarmas.txt
			############################################################ '''
			cadena=self.idsensor+" "+self.historicos[-1]+" "+str(valorCensado)
			return cadena
	'''
	def setAlarmas(self, idsensor):
		lista=self.alarmasEstado[idsensor]
		#print "Values: %s \n" % lista
		# A partir de archivo de configuración seteo las funciones de los
		# niveles de alarma
		for i in range(len(lista)):
			nivelAlarma,funcion=lista[i].split(':',1)
			self.alarma_cod[nivelAlarma]=funcion
		
		#print self.alarma_cod
	'''
	# Modifica el diccionario de niveles-función de alarma
	def setFuncionAlarma(self,dictAlarmas):
		lista=dictAlarmas[self.idsensor]
		for i in range(len(dictAlarmas)):
			nivelAlarma,funcion=lista[i].split(':',1)
			self.alarma_cod[nivelAlarma]=funcion

		print self.alarma_cod

