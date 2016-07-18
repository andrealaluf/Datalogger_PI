# -*- coding: utf-8 -*-
import os,glob, sys
import json
import logging
import time,datetime
from array import array
import bottle # Web server
from bottle import run, route, request, response, template, static_file, redirect, get, post, auth_basic, FormsDict
import requests
from bottle_sqlite import SQLitePlugin #Para la base de datos
from bottle import error
import Queue
import ConfigParser 
import platform # para el hostname

#############################################################################
sqlite_plugin = SQLitePlugin(dbfile='/home/cubie/tesis2015/users.db') ##### Plugin para la base de datos de la ruta /configuracion
bottle.install(sqlite_plugin)

# Contiene los niveles de usuarios posibles (usado para comparar el rol 
# de la cookie que le da cuando ingresa al sistema)
privlevel={	'1':'administrador',
			'2':'tecnico',
			'3':'usuario'}

# Guarda el nivel de privilegio que tiene el usuario que ingreso al sistema
global privilegio

idEstacion='Default'


# BASADO EN: http://fledglingpolymath.tumblr.com/post/39977900894/basic-authentication-in-bottle-py
def check_login(user, passwd, db):
	c = db.cursor()
	c.execute("SELECT count(*) from users_table where usuario=? and clave=?", (user,passwd))
	#print c.fetchone()[0]
	# verifico si existe ese usuario y clave
	if c.fetchone()[0] == 1:
		# traigo el rol de ese usuario para administrar sus vistas
		query=c.execute("SELECT rol from users_table where usuario=? and clave=?", (user,passwd))
		for row in query :
			 privilegio=row['rol'] # tengo el tipo de privilegio del usuario
		bottle.response.set_cookie('rol',privilegio)  # Crea una cookie llamada rol con el valor de privilegio dado
		print privilegio
		return True
	
	return False
	c.close()

@route('/')
@route('/login') # or @get('/') 
def login():
	#bottle.response.set_cookie('rol',privilegio)  # Crea una cookie llamada rol con el valor de privilegio dado
	return template("menu_login",template_lookup=['/home/cubie/tesis2015/views'])

@route('/login',apply=[sqlite_plugin], method='POST') # or @post('/') 
#@bottle.auth_basic(check_login) -> genera una ventana de login
def do_login(db):
#	adminuser='admin'
#	adminpass='admin123'
	username = request.forms.get('username')
	password = request.forms.get('password')
	if check_login(username, password, db):
		print "Usuario y clave autenticado"
		redirect('/tiemporeal')
	else:
		print "Fallo login"
		redirect('/login')


@route('/logout')
def logout():
	# Pido datos de la sesion
	s = bottle.request.environ.get('beaker.session')
	print s
	bottle.response.delete_cookie('rol')
	redirect('/login')

@route('/poweroff')
def apagar():
	os.system("sudo halt -p")

@route('/reboot')
def reiniciar():
	os.system("sudo reboot")

@route('/logs')
def logs_menu():
	return template('menu_logs',idplaca=getMAC(),template_lookup=['/home/cubie/tesis2015/views'])

@route('/logs/<name:path>')
def logsSensores(name):
	archivos=[]
	separaPath=[]
	lineasLog=[]
# MUESTRA LAS LINEAS DE UN LOG PARTICULAR
	if '.log' in name: #para cuando solicita un archivo .log 
		separaPath.append(name.split("/")[1:])		
		#print separaPath[:1]
		path_nvo = os.path.join("/home/cubie/tesis2015/logs/",name)
		file2 = open(path_nvo)
		for row in file2:
			lineasLog.append(row)		
		return template('menu_logs_1',idplaca=getMAC(), archivos=archivos, sensorSelected=name, logSelected=lineasLog,template_lookup=['/home/cubie/tesis2015/views'])
		file2.close()
# LISTA TODOS LOS LOGS DE UN SENSOR DADO
	else:
		path_nvo = os.path.join("/home/cubie/tesis2015/logs/",name)
		dirs = os.listdir( path_nvo )
		#print "ENTRE AL LOG"
		for file in dirs:
			if file.endswith('.log'): 
				#print file  
				archivos.append(file)		
				#print file	
		#for i in range(len(archivos)):
		#	print archivos[i]
		return template('menu_logs_1',idplaca=getMAC(), archivos=sorted(archivos), sensorSelected=name, logSelected=" ",template_lookup=['/home/cubie/tesis2015/views'])


@route('/tiemporeal')
def tiemporeal_menu():
	print "cookie: ",bottle.request.get_cookie('rol') # solicita al navegador leer la cookie 
	path="/home/cubie/tesis2015/modulos"
	path_file=os.path.join(path,'sensoresEstado.json')
	
	#### Reviso si existe el archivo en el directorio. Devuelve 0 o 1
	checkFile = len(glob.glob1(path,"sensoresEstado.json"))

	# No existe el archivo, redirije a sensores
	if checkFile == 0:
		return template('menu_tiemporeal',idplaca=getMAC(),cod='1',checkFile=checkFile,sensores={},template_lookup=['/home/cubie/tesis2015/views'])

	# Existe el archivo
	else:
		# Obtengo la fecha de creacion/modificacion del archivo
		file_changeTime=os.stat(path_file)[8]
		# Comparo fecha de archivo contra fecha guardada
		if os.stat(path)[8] == file_changeTime:
			filechange=0 # No se modifico
		else:
			# Actualizo fecha de modificación de sensoresEstado.json
			file_changeTime = os.stat(path)[8]
			filechange=1 # Se modifico
			file_sensores = open(path_file).read()
			dictsensores = json.loads(file_sensores) # creo un diccionario python j		
	
		return template('menu_tiemporeal',idplaca=getMAC(),cod='1',checkFile=checkFile,sensores=dictsensores,template_lookup=['/home/cubie/tesis2015/views'])

@route('/configuracion')
def configuracion_menu():
	print bottle.request.get_cookie('rol')
	# Verifico si el nivel de usuario es Administrador o Tecnico
	if bottle.request.get_cookie('rol')==privlevel.get('1') or bottle.request.get_cookie('rol')==privlevel.get('2'):
		
		cfg = ConfigParser.ConfigParser()
		
		if not cfg.read(["configGeneral.cfg"]):  
			print "No existe el archivo"  
			return template('menu_configuraciones',idplaca=getMAC(),reportdays=1, notific=1,unit="hs",viacom="3G",template_lookup=['/home/cubie/tesis2015/views'])

		else:
			if cfg.has_option("Reportes","reporteDias"):  
				diasreporte = cfg.get("Reportes","reporteDias")  
			else:  
				print "No se encontró el nombre en el archivo de configuración." 

			if cfg.has_option("Reportes","notificaciones"):  
				notificaciones = cfg.get("Reportes","notificaciones")  
			else:  
				print "No se encontró el nombre en el archivo de configuración." 

			if cfg.has_option("Reportes","unidad"):  
				unidad = cfg.get("Reportes","unidad")  
			else:  
				print "No se encontró el nombre en el archivo de configuración." 

			if cfg.has_option("Conectividad","medio"):  
				medio = cfg.get("Conectividad","medio")  
			else:  
				print "No se encontró el nombre en el archivo de configuración." 
		
			#Existe archivo
			return template('menu_configuraciones',idplaca=getMAC(),reportdays=diasreporte, notific=notificaciones,unit=unidad,viacom=medio,template_lookup=['/home/cubie/tesis2015/views'])
	else:
		return template('menu_sin_privil',idplaca=getMAC(), privLevel='3',template_lookup=['/home/cubie/tesis2015/views'])

@route('/configuracion/reporte', method='POST')
def configuracion_menu_2():
	cfg = ConfigParser.ConfigParser() 

	diasReporte = request.forms.get('cantDias')
	print diasReporte
	intervaloNotificacion=request.forms.get('intervaloNotif')
	print intervaloNotificacion
	unidadTiempo=request.forms.get('unidadTiempo_not')
	print unidadTiempo

	modo_con = request.forms.get('modo_com')
	print modo_con

	cfg.add_section("Reportes")  # Agrega un seccion con nombre reportes
	# Agrega a la seccion reporte, la clave reporte y valor diasReporte 
	cfg.set("Reportes","reporteDias", diasReporte)  
	# Agrega a la seccion reporte, la clave notificaciones y valor intervaloNotificacion
  	cfg.set("Reportes","notificaciones",intervaloNotificacion) 
  	# Agrega a la seccion reporte, la clave unidad y valor unidadTiempo
  	cfg.set("Reportes","unidad",unidadTiempo)

  	cfg.add_section("Conectividad")
  	cfg.set("Conectividad","medio",modo_con)

	f = open("configGeneral.cfg", "w")   # Guarda el archivo de configuracion
	cfg.write(f)  
	f.close()  
	
	redirect('/configuracion')


@route('/configuracion/nombre', method='POST')
def change_station_name():
	idEstacion=request.forms.get('nombre_estacion')
	print idEstacion
	os.system('/bin/hostname '+idEstacion)
	redirect('/configuracion')

@route('/sensores')
def config_sensores_status():
	# Verifico si el nivel de usuario es Administrador o Tecnico
	if bottle.request.get_cookie('rol')==privlevel.get('1') or bottle.request.get_cookie('rol')==privlevel.get('2'):
		return template('menu_sensores',idplaca=getMAC(),template_lookup=['/home/cubie/tesis2015/views'])
	else:
		return template('menu_sin_privil',idplaca=getMAC(), privLevel='3',template_lookup=['/home/cubie/tesis2015/views'])


@route('/sensores', method="POST")
def gen_sensores_status_file():
	
	# Genero la fecha en formato epoch
	epochDate = time.time()
	
	# Levanto el archivo de configuracion de los sensores y creo un diccionario python
	#with open("/home/cubie/tesis2015/listadosensores.json", 'r') as fp:
	path=os.path.join(os.getcwd(),'sensores_cfg.json')
	with open(path, 'r') as fp:
		data = json.load(fp)
	print sorted(data)#, type(data)
	fp.close()

	# Genero un nuevo dict
	sensores={}
	
	estados=[] # Array para guardar Estado de cada sensor (lo guarda inversamente)
	estados_rev=[] # Array para invertir el orden de opciones asi estan tan cual
	tiempos=[]
	tiempos_rev=[]
	unidadTiempo=[]
	unidadTiempo_rev=[]

	# Para alarmas min
	valminBaja= []
	valminBaja_rev = []
	valminMed = []
	valminMed_rev = []
	valminAlta= []
	valminAlta_rev = []
	valminUrg = []
	valminUrg_rev = []

	# Para alarmas max
	valmaxBaja= []
	valmaxBaja_rev = []
	valmaxMed = []
	valmaxMed_rev = []
	valmaxAlta= []
	valmaxAlta_rev = []
	valmaxUrg = []
	valmaxUrg_rev = []

	# Lectura del Estado de cada sensor ingresada por el usuario
	for choice in request.forms.getall('Estado'):
		#print choice, type(choice)
		estados.append(choice)
	print estados

	# Lectura del tiempo de cada sensor, usando el dial mas y menos
	for choice in request.forms.getall('cantidadTiempo'):
		#print choice, type(choice)
		tiempos.append(choice)
	print tiempos
	
	# Lectura de unidad de tiempo (segs, min, hs)
	for choice in request.forms.getall('unidadTiempo'):
		#qunidadTiempo.put(choice)
		unidadTiempo.append(choice)
	print unidadTiempo

	######### ALARMAS MIN ###############
	# Lectura de valor alarmas min
	for choice in request.forms.getall('minBaja'):
		#qvalAlertaUnder.put(choice)
		valminBaja.append(choice)
	print valminBaja

	# Lectura de valor de alerta over
	for choice in request.forms.getall('minMed'):
		#qvalAlertaOver.put(choice)
		valminMed.append(choice)
	print valminMed

	# Lectura de valor de alarma under
	for choice in request.forms.getall('minAlta'):
		valminAlta.append(choice)
	print valminAlta

	# Lectura de valor de alarma over
	for choice in request.forms.getall('minUrg'):
		valminUrg.append(choice)
	print valminUrg


	######### ALARMAS MAX ###############
	# Lectura de valor alarmas min
	for choice in request.forms.getall('maxBaja'):
		valmaxBaja.append(choice)
	print valmaxBaja

	# Lectura de valor de alerta over
	for choice in request.forms.getall('maxMed'):
		#qvalAlertaOver.put(choice)
		valmaxMed.append(choice)
	print valmaxMed

	# Lectura de valor de alarma under
	for choice in request.forms.getall('maxAlta'):
		valmaxAlta.append(choice)
	print valmaxAlta

	# Lectura de valor de alarma over
	for choice in request.forms.getall('maxUrg'):
		valmaxUrg.append(choice)
	print valmaxUrg

	
	# Hago esta lista reversa porque el metodo pop saca desde el ultimo
	# de esta manera sacaría el primero ya que la di vuelta. Me permite obtener
	# el verdadero orden de los estados de cada sensor
	for x in reversed(estados):
		estados_rev.append(x) 

	for x in reversed(tiempos):
		tiempos_rev.append(x)

	for x in reversed(unidadTiempo):
		unidadTiempo_rev.append(x)

	###################################

	for x in reversed(valminBaja):
		valminBaja_rev.append(x)
	for x in reversed(valminMed):
		valminMed_rev.append(x)
	for x in reversed(valminAlta):
		valminAlta_rev.append(x)
	for x in reversed(valminUrg):
		valminUrg_rev.append(x)

	for x in reversed(valmaxBaja):
		valmaxBaja_rev.append(x)
	for x in reversed(valmaxMed):
		valmaxMed_rev.append(x)
	for x in reversed(valmaxAlta):
		valmaxAlta_rev.append(x)
	for x in reversed(valmaxUrg):
		valmaxUrg_rev.append(x)

	###################################
	
	# Generador del diccionario con: Estado, tiempo, AlertaUnder, AlertaOver, AlarmaUnder, AlarmaOver
	for key,value in sorted(data.items()):
		tmpEstado = estados_rev.pop() # Estado
		tmpTiempo = tiempos_rev.pop() # Cantidad de Tiempo
		unidad = unidadTiempo_rev.pop() # Unidad

		if tmpEstado == 'Activado':
			if unidad == 'seg':
				sensores[key]=tmpEstado,int(tmpTiempo),valminBaja_rev.pop(), valminMed_rev.pop(), valminAlta_rev.pop(), valminUrg_rev.pop(), valmaxBaja_rev.pop(), valmaxMed_rev.pop(), valmaxAlta_rev.pop(), valmaxUrg_rev.pop()
			else:
				if unidad == 'min':
					sensores[key]=tmpEstado,int(tmpTiempo)*60,valminBaja_rev.pop(), valminMed_rev.pop(), valminAlta_rev.pop(), valminUrg_rev.pop(), valmaxBaja_rev.pop(), valmaxMed_rev.pop(), valmaxAlta_rev.pop(), valmaxUrg_rev.pop()
				if unidad == 'hs':
					sensores[key]=tmpEstado,int(tmpTiempo)*3600,valminBaja_rev.pop(), valminMed_rev.pop(), valminAlta_rev.pop(), valminUrg_rev.pop(), valmaxBaja_rev.pop(), valmaxMed_rev.pop(), valmaxAlta_rev.pop(), valmaxUrg_rev.pop()
		else:
			# Estado Desactivado
			# Estos pop los hago porque sino en los que esten Activos me va a tomar el dato de los anteriores, y si fue
			# desactivado el estado anterior, me toma los valores de este desactivado
			valminBaja_rev.pop(), valminMed_rev.pop(), valminAlta_rev.pop(), valminUrg_rev.pop(), valmaxBaja_rev.pop(), valmaxMed_rev.pop(), valmaxAlta_rev.pop(), valmaxUrg_rev.pop()
			sensores[key]=tmpEstado


	
	# Genero el archivo json de Estado de los sensores
	path=os.path.join(os.getcwd(),'sensoresEstado.json')
	sens_estados = open(path,'w')
	sens_estados.write(json.dumps(sensores,indent=4))
	sens_estados.truncate()
	sens_estados.close()
	'''	
	logging.info('%s requested %s with data %s',
                 bottle.request.headers.get('Host'), bottle.request.fullpath,
                 bottle.request.forms.items())
	'''	
	redirect('/sensores')

@route('/alarmas')
def config_alarmas():
	funciones=['Registrar','EnviarMsj','Llamar','Apagar']
	# Verifico si el nivel de usuario es Administrador o Tecnico
	if bottle.request.get_cookie('rol')==privlevel.get('1') or bottle.request.get_cookie('rol')==privlevel.get('2'):
		return template('menu_configuraciones_alarmas',idplaca=getMAC(), listaFunciones=funciones,template_lookup=['/home/cubie/tesis2015/views'])
	else:
		return template('menu_sin_privil',idplaca=getMAC(), privLevel='3',template_lookup=['/home/cubie/tesis2015/views'])

@route('/alarmas', method='POST')
def config_alarmas_post():

	funciones=[]
	sensores=[]
	alarmaFuncion = {}
	#for choice in request.forms.getall('TS60I_carga'):
	#	print choice, type(choice)

	# Trae para sensor, el valor puesto en el select del formulario
	#print sorted(request.forms.allitems()),'\n' # Es lo mismo que request.forms.items()

	formulario = request.forms.allitems()

	# Obtengo el elemento 0 de la lista formulario y el valor 1 de la tupla
	#print "\n Formulario: ", formulario[0][1]

	# Esta muestra solo los nombres de las funciones del formulario
	#print sorted(request.forms.keys())

	# Obtengo los nombres de cada sensor y las funciones existentes
	for nombreFuncion in sorted(request.forms.keys()):
		sensorName = nombreFuncion.split('-')
		# Guardo el nombre del sensor
		if  sensorName[1] not in sensores:
			sensores.append(sensorName[1])
		# Guardo el nombre de la funcion	
		if sensorName[0] not in funciones:
			funciones.append(sensorName[0])
			pass

	#print sensores
	#print " \n",funciones

	
	cadena=[]
	for i in range(len(sensores)):
		for x in range(len(funciones)):
			for y in range(len(formulario)):
				if funciones[x]+"-"+sensores[i] == formulario[y][0]:
					#cadena += formulario[y][1]+","
					cadena.append(funciones[x]+":"+formulario[y][1])
			alarmaFuncion[sensores[i]] = cadena
		cadena = []

	#print "\n Alarma Funcion :\n",alarmaFuncion
	
	# Genero el archivo json de Estado de las alarmas
	alarmas_estados = open("/home/cubie/tesis2015/modulos/alarmasEstado.json",'w')
	alarmas_estados.write(json.dumps(alarmaFuncion,indent=4))
	alarmas_estados.truncate()
	alarmas_estados.close()

	redirect('/alarmas')
		
@route('/usuarios', apply=[sqlite_plugin])
def usuarios_menu(db):
	# Solo siendo Administrador
	if bottle.request.get_cookie('rol')==privlevel.get('1'):	
		# Voy a buscar todos los usuarios de la bd para mostrarlos
		c = db.cursor()
		c.execute("SELECT * from users_table")
		data = c.fetchall()
		c.close()
		return template('menu_usuarios',idplaca=getMAC(), rows=data,template_lookup=['/home/cubie/tesis2015/views'])
	else:
		return template('menu_sin_privil',idplaca=getMAC(), privLevel='3',template_lookup=['/home/cubie/tesis2015/views'])

@route('/usuarios', apply=[sqlite_plugin], method='POST') #solo a esta ruta le paso el plugin de sqlite3 donde tiene los usuarios
def usuarios_menu_1(db):
	minimo = request.forms.get('minimo') # toma la variable minimo escrita en el template menu_configuracion.tpl
	maximo = request.forms.get('maximo')
	#print maximo, minimo
	nombre = request.forms.get('nombre')
	apellido = request.forms.get('apellido')	
	mail = request.forms.get('mail')
	tel = request.forms.get('telefono')
	user=request.forms.get('usuario')
	password=request.forms.get('contraseña')
	rol=request.forms.get('rol')
	#Agrego el usuario a la bd	
	db.execute("INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave,rol) VALUES (?,?,?,?,?,?,?)",(nombre,apellido,mail,tel,user,password,rol))
	#db.execute("SELECT * from users_table")
	c = db.cursor()
	c.execute("SELECT * FROM users_table")
	data = c.fetchall()
	for row in data:
		print row
	c.close()
	#row = db.execute("SELECT * from users_table where nombre=?", nombre).fetchone()
	#print row
	print nombre, apellido, mail, tel, rol
	redirect('/usuarios') # redirecciona a configuraciones nuevamente


@route('/alertas')
def alertas_menu():
	with open("/home/cubie/tesis2015/modulos/logAlarmas.txt", "r") as f:
		#f.seek (0, 2)           # Seek @ EOF
		#fsize = f.tell()        # Get Size
		#f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
		lines = f.readlines()       # Read to end

	#lines = lines[-10:]    # Get last 10 lines
	return template('menu_alertas',idplaca=getMAC(),lineas=lines,template_lookup=['/home/cubie/tesis2015/views'])

	'''
	path="/home/cubie/tesis2015/modulos/logAlarmas.txt"
	lineasArchivo=[]
	alarmas = open(path)
	for row in alarmas:
		lineasArchivo.append(row)		
	return template('menu_logs_1',idplaca=getMAC(),lineas=lineasArchivo,template_lookup=['/home/cubie/tesis2015/views'])
	'''
@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='/home/cubie/tesis2015/logs/', download=filename,template_lookup=['/home/cubie/tesis2015/views'])
	


###################################################################################

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/cubie/tesis2015/logs',template_lookup=['/home/cubie/tesis2015/views'])
###################################################################################

###################################################################################
# MANEJO DE PAGINAS DE ERROR
###################################################################################
@bottle.error(404)
def error404(error):
	refresh = request.query.refresh or "3"
	return template('menu_404',idplaca=getMAC(),template_lookup=['/home/cubie/tesis2015/views'])
####################################################################################	
    
# Uso la mac para la identificacion de estacion
def getMAC():
	# Read MAC from file
	myMAC = open('/sys/class/net/eth0/address').read()
	return myMAC

def getName():
	hostname = platform.node()
	return hostname



if __name__ == '__main__':        
	print "Proceso: ",os.getpid() 
    # To run the server, type-in $ python server.py
	#bottle.debug(True) # display traceback 
	#app.run(host='192.168.1.250', port=8080, reloader=True) 
	bottle.TEMPLATE_PATH.insert(0,'/home/cubie/tesis2015/views')
	bottle.run(host='0.0.0.0', port=8080, reloader=True)  # Listen to HTTP requests on all interfaces
