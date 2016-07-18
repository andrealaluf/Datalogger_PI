import sqlite3
# BASADO EN: http://www.pythoncentral.io/introduction-to-sqlite-in-python/
try:
	# CREACION DE LA BASE DE DATOS Y TABLA
	db = sqlite3.connect('users.db')# or use :memory: to put it in RAM
	db.execute("CREATE TABLE users_table (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre CHAR(100) NOT NULL, apellido CHAR(100) NOT NULL, email CHAR(100) NOT NULL,tel CHAR(100) NOT NULL,usuario CHAR(100) NOT NULL,clave CHAR(100) NOT NULL, rol CHAR(50) NOT NULL)")
	db.commit()

	nombre="ernesto"
	apellido="dondio"
	mail="edondio@gmail.com"
	tel="4683660"
	user="edon"
	password="edon1234"
	rol="usuario"

	# INSERT EN LA TABLA 
	db.execute("INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave, rol) VALUES 	('administrador','-','admin@efn.uncor.edu','-','admin','admin123','administrador')")
	db.execute("INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave, rol) VALUES ('leandro','saavedra','lsaavedra@efn.uncor.edu','4610359','leo','saavedra','administrador')")
	db.execute("INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave, rol) VALUES ('jorge','perez','jperez@efn.uncor.edu','4610359','jorge','perez123', 'tecnico')")
	db.execute("INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave, rol) VALUES (?,?,?,?,?,?,?)",(nombre,apellido,mail,tel,user,password,rol))
	db.commit()
# | id | nombre | apellido | email | tel | usuario | clave |

# Para recuperar los datos puedo hacer: 
#    sqlite3 users.db 'select * from users_table'

# Catch the exception
except Exception as e:
	print "Error %s:" % e.args[0]
    # Roll back any change if something goes wrong
	db.rollback()
	raise e
finally:
	# Close the db connection
	db.close()
