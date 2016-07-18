# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Esta es la ultima versión funcional de datalogger aplicando Threads para la solicitud de datos,
el cual lo realiza Adquisicion y el consumo de datos lo realiza Almacenamiento. Usan una cola en
comun para compartir los datos. Además se generan los objetos sensores en un array previo al
recorrido de sensoresEstado.json

pydon -w nombrearchivo (sin .py)
pyreverse -o png * -> para generar el UML de todo
ES LA ULTIMA VERSION ACTUALIZADA 16-10-2015
'''
import time
import serial
import os, sys, glob
import json
#from tristarNew import *
#from class_Dato import Dato
from class_Medicion import Medicion
from class_sensor import Sensor
from class_baseDatos import BaseDatos
from class_TemperatureDHT11 import *
from class_UltrasonicHC_SR04 import *
from threading import Thread
import threading
import random
import ConfigParser 

from server import *
from Queue import Queue
import logging


def Adquisicion(queueDatos,queueAlarmas,objSensores,queueArchivo,sensores): # Solicita datos a los sensores
		
		tiempo = 1 # utilizado como contador para frecuencia de los sensores

		while True:	
			# Cola que contiene sensoresEstado si se modificó
			if queueArchivo.empty():
			# Verifico si sensores.json se modifico
			#if os.stat(path)[8] == file_changeTime: # FALTARIA VERIFICAR TAMBIEN EL ARCHIVO DE ALARMAS PARA LLAMAR A .setAlarmas()
				# Lectura del diccionario de sensores
				#print sensores,"\r"
				for key,value in sorted(sensores.items()):
					# Se alcanzo el tiempo del sensor y está Activado
					if value[0]=='Activado' and tiempo%value[1]==0:
						for obj in objSensores:
							if key == obj.__class__.__name__:
								#print obj
								#name,frec=obj.getName(), obj.getFrecuencia() # Objeto DATO y Alarma devuelto por el sensor
								##### VOLVER A DESCOMENTAR EL DE ABAJO
								dat,alarma=obj.getValor() # Objeto DATO y Alarma devuelto por el sensor
								#print "Sensor: %s - Frec: %i - Tiempo: %i\r" %(obj.getName(),obj.getFrecuencia(),tiempo)
								pass
							else:
								pass

						###### Meto en la cola el objeto DATO obtenido #####
						queueDatos.put(dat)
						
						##### Meto en la cola la alarma disparada #######
						if alarma is not None:  
							queueAlarmas.put(alarma)
					
					else:
						#print "------------------------------", tiempo
						pass
				tiempo += 1
				#time.sleep(1)
			
			# Se modificó sensores estado, saco el diccionario actualizado de la cola
			else:
				sensores.clear() # Limpio el diccionario viejo
				print "Actualizo diccionario de Adquisicion"
				sensores = queueArchivo.get()
				queueArchivo.task_done()
				#time.sleep(1)
			time.sleep(1)
def Almacenamiento(queueDatos,bd): # Consumidor
	while True:
		dat = queueDatos.get()
		print "Saque un dato de la cola datos \n"
		queueDatos.task_done()
		bd.storeData("%.2f" %dat.getValor(), dat.getName(), dat.getUnidad())
		'''Falta que Base de Datos tome el valor que se configura en configs generales
		'''
		#time.sleep(random.random())
		#time.sleep(1)

'''Se encarga de revisar cambios en los archivos del path y disparar evento si encuentra un cambio'''
def ObserverPath(path,file_changeTime,event,queueFileChange):
	
	files_for_check=["sensoresEstado.json","alarmasEstado.json","configGeneral.cfg"]
	files_date=[] # para guardar las fechas de modificacion/creacion de los archivos a chequear
	path_gral='' # path general donde se encuentran los archivos
	i=0
	
	while True:
		'''VERIFICAR QUE LOS ARCHIVOS NO EXISTAN'''
		for name in files_for_check:
			if not os.path.isfile(name): ## El archivo no existe
				#print "Archivo no existe\r"
				pass
			else:
				# No estan cargadas las fechas, cargarlas
				if not len(files_date):
					for name in files_for_check:
						path_gral=os.path.join(os.getcwd(),name)
						files_date.append(os.stat(path_gral)[8])
						#print "Agregando fecha de: %s " %name
						path_gral=''
						
				# Con las fechas cargadas, verificar si se modificaron
				else:
					# obtengo la posición del archivo a analizar
					i=files_for_check.index(name)
					#print files_date
					#print "i: %i" %i
					# Obtengo el path
					path_gral=os.path.join(os.getcwd(),name)
				
					if os.stat(path_gral)[8] == files_date[i]:
						# Archivo no modificado
						#print "Archivo no modificado\r"
						pass
					else:
						print "Archivo modificado!!!!\r"
						# Archivo modificado actualizo su fecha
						files_date[i]=os.stat(path_gral)[8]
						### Disparo de evento #######
						event.set()
						queueFileChange.put(name)
						event.clear()
				path_gral=''
				
				time.sleep(1)
				
		
'''Se encarga de actualizar los valores de los sensores en los cambios realizados en la web '''
def ConfigSensores(objSensores,sensores,event,path,queueArchivo,queueFileChange,bd):
	path_file=''
	while True:
		print "Esperando evento\r"
		event.wait()
		print "Evento disparado\r"	
		
		# Lectura del nombre de archivo modificado
		filename=queueFileChange.get()
		print "Saque un nombre de archivo modificado :%s\r" %filename
		queueFileChange.task_done()
		
		if filename == "sensoresEstado.json":
		### Configurar frecuencias nuevas ####
		
			with open(path, 'r') as fp: # Se carga nuevamente sensoresEstado.json
				sensores = json.load(fp)
			fp.close()	
			
			print sensores,"\r"
			#### Actualización de la frecuencia nueva #####################
			for key,value in sorted(sensores.items()):
				if value[0]=='Activado':	
					frec=value[1]
					print "Frecuencia a actualizar: %i\r" %frec
					for obj in objSensores:
						if key == obj.__class__.__name__:
							obj.setFrecuencia(frec)
							print "Frec nva: %i\r" %obj.getFrecuencia()
							obj.setMinBaja(value[2])
							obj.setMinMed(value[3])
							obj.setMinAlta(value[4])
							obj.setMinUrg(value[5])
							obj.setMaxBaja(value[6])
							obj.setMaxMed(value[7])
							obj.setMaxAlta(value[8])
							obj.setMinUrg(value[9])
						else:
							pass
			# Meto en la cola el diccionario de sensoresEstado actualizado				
			queueArchivo.put(sensores)
		
		if filename=="alarmasEstado.json":
			path_file=os.path.join(os.getcwd(),filename)
			with open(path_file, 'r') as fp:
				alarmasEstado = json.load(fp)
			#print alarmasEstado
			### Actualizar las funciones de las alarmas
			print "Configurando funciones de alarma\r"
			for obj in objSensores:
				obj.setAlarmaFun(alarmasEstado)
				#print obj.alarma.alarma_cod
			path_file=''	
			
		if filename=="configGeneral.cfg":
			### Actualizar dias de la base de datos
			cfg = ConfigParser.ConfigParser()
			path_file=os.path.join(os.getcwd(),filename)
			cfg.read(path_file)
			if cfg.has_option("Reportes", "reportedias"):  
				days = cfg.get("Reportes", "reportedias") 
				print days
				
			bd.setDayForStore(days)
			path_file=''

def WebServer():
	while True:
		#bottle.debug(True) # display traceback 
		#bottle.TEMPLATE_PATH.insert(0,'/home/cubie/tesis2015/views') # Incluye path de los templates
		#bottle.run(host='0.0.0.0', port=8080, reloader=True)  # Listen to HTTP requests on all interfaces
		bottle.run(host='0.0.0.0', port=8080)

		
def AlarmaReg(queueAlarma): # Se encarga de registrar las alarmas disparadas por los sensores
	while True:
		alarma = queueAlarma.get()
		print "Saque un dato de la cola Alarmas \n"
		queueAlarma.task_done()
		print alarma
		fecha = time.strftime('%Y-%m-%d  %H:%M:%S')
		'''#########################################################
		Registro de alarmas disparadas en archivo logAlarmas.txt
		############################################################ '''
		with open(os.path.join(os.getcwd(),'logAlarmas.txt'), 'a+') as fileAlarma:
			fileAlarma.write(fecha +" "+alarma+'\r\n')
		time.sleep(1)
		

			
def main(args):
	
	# Genero una cola de tamaño fijo donde el modulo adquisición va a obtener
	# los datos de los sensores para mandarselos al modulo base de datos (Objetos DATOS)
	queueDatos = Queue(100)
	queueAlarmas = Queue(60)
	queueArchivo = Queue(1) # Cola para enviar el archivo sensoresEstado nuevo
	queueFileChange = Queue(3) # Cola para para poner el nombre del archivo modificado

	threads = [] # Lista de hilos

	#### Inicializador de logger #####
	LOG_FILENAME = os.path.join(os.getcwd(),'dataloggerApp.log')
	logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
	logger = logging.getLogger(__name__)

	'''############# Inicialización de hilo WebServer ############## '''
	print "Hilo webServer inicializando ... \n"
	logger.info("Inicializando webserver...")
	ws=threading.Thread(target=WebServer, args=())
	ws.start()
	threads.append(ws)
	
	# No lanzo los hilos hasta tanto el archivo sensoresEstado.json no
	# este creado
	while not os.path.isfile("sensoresEstado.json"):
		pass
	print "Archivo encontrado! ... \n"	
	logger.info("Diccionario sensoresEstado.json encontrado! ...")

	# Para listar el directorio actual, usar cualquiera de los dos
	#print os.path.dirname(os.path.abspath(__file__))
	#print os.getcwd()
	#print os.path.abspath('sensoresEstado.json')

	
	####################################################################
	##			Lectura de diccionario de estado de los sensores    #### 
	####################################################################
	path=os.path.join(os.getcwd(),'sensoresEstado.json') # o puedo usar os.path.abspath('sensoresEstado.json')
	with open(path, 'r') as fp:
		sensores = json.load(fp)
	print sensores
	print "Lectura de archivo de sensores finalizada ... \n"
	logger.info("Lectura de archivo de sensores finalizada ...")
	#################################################################### 
	# Información de sensoresEstado.json (Para saber si se modifico)  ##
	####################################################################
	statinfo = os.stat(path)
	file_changeTime = statinfo[8] # st_mtime= fecha de mas reciente modificación
	###################################################################

	####################################################################
	#				 Instancias de los objetos sensores 			  ##
	####################################################################
	print "Creando objetos sensores ... \n"
	logger.info("Creando sensores ...")
	objSensores=[]
	nameSensores=sensores.keys() # obtengo todos los nombres de sensores (claves)
	for name in nameSensores:
		exec("obj=%s()" % name)
		objSensores.append(obj)
		logger.info("Sensor %s creado" % name)
	#print objSensores
	################################################################################
	
	'''#################################################################
	Seteo los tiempos de frecuencia de cada objeto sensor
	####################################################################
	'''
	print "Configurando frecuencia de sensores ... \n"
	logger.info("Configurando frecuencia de sensores ...")
	updateFrecuencia(objSensores,sensores)
		
		
	'''#################################################################
	##################   Lanzamiento de hilos   ########################
	####################################################################
	'''
	# Generación del evento para actualización de parámetros de los sensores
	event = threading.Event()
	
	'''Creacion de objeto base de datos'''
	bd=BaseDatos(5)
	
	# Thread adquisición de datos
	adq = threading.Thread(target=Adquisicion, args=(queueDatos,queueAlarmas,objSensores,queueArchivo,sensores))
	adq.start()
	
	# Thread observer path
	obs= threading.Thread(target=ObserverPath, args=(path,file_changeTime,event,queueFileChange))
	obs.start()

	
	# Thread update configuraciones sensores
	conf= threading.Thread(target=ConfigSensores, args=(objSensores,sensores,event,path,queueArchivo,queueFileChange,bd))
	conf.start()
	
	# Thread almacenamiento
	alm=threading.Thread(target=Almacenamiento, args=(queueDatos,bd))
	alm.start()
	
	# Thread registro de alarmas
	regAlarma=threading.Thread(target=AlarmaReg, args=(queueAlarmas,))
	regAlarma.start()

	#HilosActivos=threading.enumerate()

	
	return 0
	
def updateFrecuencia(arraySensores,sensores):
	'''#################################################################
	Seteo los tiempos de frecuencia de cada sensor (para cambios en el
	archivo sensoresEstado.json o por ser primera vez)
	####################################################################
	'''
	for obj in arraySensores:
		obj.getName()
		frec = sensores[obj.getName()][1]
		exec("obj.setFrecuencia(frec)")
		#print obj.getName(),obj.getFrecuencia()


if __name__ == '__main__':
	main(sys.argv)
