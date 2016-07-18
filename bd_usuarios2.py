#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 
import sys


try:
	# Creates or opens a file called users.db with a SQLite3 DB
	db= sqlite3.connect('users2.db')# or use :memory: to put it in RAM
	# Get a cursor object
	cursor = db.cursor()  
	# Check if table users does not exist and create it
	cursor.execute('''CREATE TABLE users_table 
				(id INTEGER PRIMARY KEY AUTOINCREMENT, 
				nombre CHAR(100) NOT NULL, 
				apellido CHAR(100) NOT NULL, 
				email CHAR(100) NOT NULL,
				tel CHAR(100) NOT NULL,
				usuario CHAR(100) NOT NULL,
				clave CHAR(100) NOT NULL, 
				rol CHAR(50) NOT NULL)''')
	# Commit the change
	db.commit()  

	db.execute('''INSERT INTO users_table (nombre,apellido,email,tel,usuario,clave, rol) 
				VALUES ('administrador','-','admin@efn.uncor.edu','-','admin','admin123','administrador')''')

	db.commit()
        
except sqlite3.Error, e:    
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if db:
        db.close() 
