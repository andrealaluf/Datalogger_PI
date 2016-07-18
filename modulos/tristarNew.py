# -*- coding: utf-8 -*-
#!/usr/bin/python
import time, datetime
import serial
import os
import json
from class_sensor import Sensor
from class_Dato import Dato
from class_Alarma import Alarma
import logging

''' Esta es la clase generica que va a contener a las clases de abajo.
Es la clase padre
'''
class TristarTS60(Sensor):
	
	# Diccionario que va a contener como key el nombre del sensor o clase
	# y como valor: 1ro el timestamp en que se actualiza y 2do el valor
	# Sirve para evitar siempre estar solicitando datos al serial, si
	# se solicito datos en menos tiempo que se frecuencia, lo saca de aqui
	valorSensor = {}

	# Diccionario que permite mapear un nombre de variable obtenida del
	# serial con un nombre de clase
	mapVariableSensor = {
						'adc_vb_f' : ['TS60V_bat',0],
						'adc_vx_f' : ['TS60V_pan',0],
						'adc_ipv_f' : ['TS60I_carga',0],
						'adc_iload_f' : ['TS60I_load',0],
						'T_hs' : ['TS60T_equipo',0],
						'T_batt' : ['TS60T_bat',0] }
			
	def __init__(self,name,frec):
		
		# Instancia de un sensor
		self.sensor=Sensor.__init__(self,name)

		# Actualizo la frecuencia de censado del sensor
		self.frecuencia = frec
		
	
	def getValor(self):
		
		timemax=0 # Variable para calcular el tiempo mas actual dentro
				  # del diccionario valorSensor
		
		# Obtengo el nombre de la clase
		nombre_sensor = self.__class__.__name__
		
		# Verifico si el nombre del sensor esta en el diccionario sino
		# lo agrego
		if self.valorSensor.has_key(nombre_sensor):
			'''
			El sensor existe en el diccionario, hay que verificar
			sus tiempos respecto a la ultima actualización
			'''
			print "Sensor existe en diccionario"
			# Busco el tiempo mas reciente (tiempo maximo)
			for key,value in self.valorSensor.items():
				if self.valorSensor[key] >= timemax:
					timemax = self.valorSensor[key][0]
			print "Tiempo max :", timemax
			
			# Actualizo el tiempo del sensor
			self.valorSensor[nombre_sensor][0] = int(time.time())	

			# Verifico si la diferencia de tiempo supera su frecuencia		
			if abs(self.valorSensor[nombre_sensor][0]-timemax) >= self.frecuencia:
				# la diferencia es mayor, leo serial y actualizo su tiempo
				self.readRegisters()
				#self.valorSensor[nombre_sensor][0] = int(time.time()) NO IRIA PORQUE YA ACTUALICE ANTES
				print "Tiempo superado: ", abs(self.valorSensor[nombre_sensor][0]-timemax) 
			else:
				# la diferencia es menor, solo actualizo su tiempo (no leo serial)
				# self.valorSensor[nombre_sensor][0] = int(time.time()) NO IRIA PORQUE YA ACTUALICE ANTES
				print "Tiempo no superado: ", abs(self.valorSensor[nombre_sensor][0]-timemax)
				pass
						
		else:
			'''
			El sensor no existe en el diccionario, hay que
			agregarlo a valorSensor y leer puerto serial
			'''
			self.valorSensor[nombre_sensor]=[int(time.time()),0]
			self.readRegisters()
			print "Sensor no existe en diccionario, agregado!"
		
			
		# Chequeo valor para alarma
		valorAlarma=self.alarma.CheckValue(self.valorSensor[nombre_sensor][1])
		
		if valorAlarma == "ok":
			# Devuelvo el objeto DATO y la ALARMA en None
			return Dato(nombre_sensor,self.valorSensor[nombre_sensor][1],self.unit), None	
	
		else:
			valorAlarma=valorAlarma+" "+self.unit
			# Devuelvo el objeto DATO y la ALARMA generada
			return Dato(nombre_sensor,self.valorSensor[nombre_sensor][1],self.unit), valorAlarma

	def getFrecuencia(self):
		return self.frecuencia
	
	def setFrecuencia(self,newfrec):
		self.frecuencia = newfrec
	
	def updateDict(self, dic_mapVariableSensor, dic_valorSensor):
		# Actualizo el diccionario de valorSensor con las key que 
		# existan en el diccionario
		for key,value in sorted(dic_mapVariableSensor.items()):
			# Verifico si en valorSensor existe la key de value mapVariableSensor
			if dic_valorSensor.has_key(dic_mapVariableSensor[key][0]):
				dic_valorSensor[dic_mapVariableSensor[key][0]][1] = dic_mapVariableSensor[key][1]
			else:
				pass
			
	'''#################################################################
	Se encarga de crear la conectividad serial
	###################################################################'''
	def StartSerial(self):
		sp = serial.Serial()
		sp.port = self.ScanSerialPorts()
		sp.baudrate = 9600
		sp.parity = serial.PARITY_NONE
		sp.bytesize = serial.EIGHTBITS
		sp.stopbits = serial.STOPBITS_TWO
		
		sp.open()
		return sp
		
	'''#################################################################
	 Busca los nombres de dispositivos seriales que hay en el sistema
	 ##################################################################'''	
	def ScanSerialPorts(self):
		
		# Variable para la ruta al directorio
		path = "/dev/serial/by-id/"

		# Lista todos los archivos en ese directorio
		lstDir = os.listdir(path)

		serialDevice =''.join(path)
		serialDevice += serialDevice.join(lstDir)
		
		# El nombre del dispositivo serial
		return serialDevice 
	
	'''#################################################################
	Lectura de la trama de datos (holding registers)
	###################################################################'''
	def readRegisters(self):
		
		sp=self.StartSerial()
		
		out = '' # la uso para almacenar la trama recibida
		
		### Solicitud de lectura de Holding Registers ###
		sp.write("010300080009040e".decode('hex'))
		time.sleep(0.5)
		'''Hacerlo con inwaiting porque si leo por una cierta cantidad de bytes
		en algunas ocasiones no llega la trama entera'''
		while sp.inWaiting() > 0:
			out += sp.read(1)
		#out = sp.readline(21) # haciendolo de esta forma evito los ultimos 2 bytes que son CRC (total=23bytes)
		print out.encode('hex'),'\n'                       
		
		#try:
		# Point Addr = 4009 -> Vbat
		
		adc_vb_f=int(out[3:5].encode('hex'),16) # Convierto de string hexa a int
		adc_vb_f= adc_vb_f*96.667*pow(2,-15)# Obtengo el valor decimal
		print "Battery voltage, filtered= %.2f" %adc_vb_f

		# Point Addr = 4010
		adc_vs_f=int(out[5:7].encode('hex'),16)
		adc_vs_f = adc_vs_f*96.667*pow(2,-15)
		print "Battery sense voltage, filtered= %.2f" %adc_vs_f

		# Point Addr = 4011
		# Tension del panel solar
		adc_vx_f=int(out[7:9].encode('hex'),16)
		adc_vx_f = adc_vx_f*139.15*pow(2,-15)
		print "Array/Load voltage, filtered= %.2f" %adc_vx_f


		# Point Addr = 4012
		adc_ipv_f=int(out[9:11].encode('hex'),16)
		adc_ipv_f = adc_ipv_f*66.667*pow(2,-15)
		print "Charging current, filtered= %.2f" %adc_ipv_f

		# Point Addr = 4013
		adc_iload_f=int(out[11:13].encode('hex'),16)
		adc_iload_f = adc_iload_f*316.67*pow(2,-15)
		print "Load current, filtered= %.2f" %adc_iload_f

		# Point Addr = 4014
		Vb_f=int(out[13:15].encode('hex'),16)
		Vb_f = Vb_f*96.667*pow(2,-15)
		print "Battery voltage, slow filter= %.2f V" %Vb_f

		# Point Addr = 4015
		T_hs=int(out[15:17].encode('hex'),16)
		print "Heatsink temperature= ", T_hs

		# Point Addr = 4016
		T_batt=int(out[17:19].encode('hex'),16)
		print "Battery temperature= ",T_batt

		# Point Addr = 4017
		V_ref=int(out[19:21].encode('hex'),16)
		V_ref =V_ref*96.667*pow(2,-15)
		print "Charge regulator reference voltage= %.2f" %V_ref
		
		sp.close()
		'''
		except:
			adc_vb_f=0
			adc_vx_f=0
			adc_ipv_f=0
			adc_iload_f=0
			T_hs=0
			T_batt=0
		'''	
		# Actualizo cada valor del diccionario de mapeo
		self.mapVariableSensor['adc_vb_f'][1]=round(adc_vb_f,2)
		self.mapVariableSensor['adc_vx_f'][1]=round(adc_vx_f,2)
		self.mapVariableSensor['adc_ipv_f'][1]=round(adc_ipv_f,2)
		self.mapVariableSensor['adc_iload_f'][1]=round(adc_iload_f,2)
		self.mapVariableSensor['T_hs'][1]= T_hs
		self.mapVariableSensor['T_batt'][1] = T_batt
		
		# Actualizo los valores en el diccionario de valorSensor
		self.updateDict(self.mapVariableSensor, self.valorSensor)
		
		# Actualizo los valores de cada sensor en el diccionario
		'''
		self.valorSensor['TS60V_bat']=[int(time.time()),round(adc_vb_f,2)]
		self.valorSensor['TS60V_pan']=[int(time.time()),round(adc_vx_f,2)]
		self.valorSensor['TS60I_carga']=[int(time.time()),round(adc_ipv_f,2)]
		self.valorSensor['TS60I_load']=[int(time.time()),round(adc_iload_f,2)]
		self.valorSensor['TS60T_equipo']=[int(time.time()),T_hs]
		self.valorSensor['TS60T_bat']=[int(time.time()),T_batt]
		'''
		

				
		
########################################################################
########## CREACION DE LAS SUBCLASES DE TristarTS60    #################
########################################################################		
class TS60V_bat(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60V_bat",frec)

		#def getValor(self):
		#	return TristarTS60.getValor("TS60-V_bat")
		
class TS60V_pan(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60V_pan",frec)

class TS60I_carga(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60I_carga",frec)
	
class TS60I_load(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60I_load",frec)
		
class TS60T_equipo(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60T_equipo",frec)
	
class TS60T_bat(TristarTS60):
	def __init__(self,frec=0):
		# llamamos al constructor TristarTS60
		TristarTS60.__init__(self,"TS60T_bat",frec)
		

#####################################################################
'''
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('TristarExecution.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
#logger.info('Hello baby')
'''

'''
x=TS60V_pan(25)
y=TS60I_carga(12)
z=TS60T_bat(2)

#print "Nombre: ",x.getName() + " - Frec: " ,x.getFrecuencia() " - Unidad: ", x.getUnit()
print "Nombre: %s - Frecuencia: - %i Unidad: %s" % (x.getName(), x.getFrecuencia(), x.getUnit())
print x.valorSensor
var=x.getValor()
#print x.getValor()
print var
print var.getName()
print var.getValor()
print var.getUnidad()
print x.valorSensor
print "Nombre: %s - Frecuencia: - %i Unidad: %s" % (y.getName(), y.getFrecuencia(), y.getUnit())
print y.valorSensor
print y.getValor()
print y.valorSensor
time.sleep(10)
print x.getValor()
print x.valorSensor
time.sleep(5)
print y.getValor()
print y.valorSensor
'''


