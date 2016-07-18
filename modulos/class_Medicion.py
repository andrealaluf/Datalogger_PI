# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import datetime
import os.path
import glob 
import serial
import os, sys
import json


class Medicion(object):
	'''
	Forma un paquete modular de forma tal de tener contenido en uno 
	varios atributos de un sensor como ser:
	- valor
	- unidad
	- nombre o id
	- valor maximo y valor minimo
	Se pensó en la forma de devolver un objeto dato al solicitar datos
	al sensor y no un valor unico.
	Importante: tiene que existir el archivo sensores_cfg.json para poder
	cargar los datos de un sensor particular al crearse la instancia.
	'''
	
	# Constructor de la clase
	# sensor -> es el nombre del sensor que genera el dato
	# valorSensado
	def __init__(self,sensor,valorSensado,sensor_unidad):
		
		# Obtención de nombre del sensor
		self.idDato = sensor
		
		# Obtención del valor censado
		self.valor = float(valorSensado)
		
		# Obtención de unidad del sensor
		self.unidad = sensor_unidad
		
	
	# Generación de getters
	def getValor(self):
		return self.valor
		
	def getUnidad(self):
		return self.unidad
	
	def getName(self):
		return self.idDato

	# Generación de setters
	def setValor(self,value):
		self.valor = value
	
	def setUnidad(self,unit):
		self.unidad = unit
		
	def setName(self,idSensor):
		self.idDato = idSensor
########################################################################


		

