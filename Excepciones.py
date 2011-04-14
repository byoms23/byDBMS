# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Excepciones.py
# Contiene las clases de excepciones utilzados en el proyecto.

# Contiene excepción para represantar ausencia de base de datos
class DataBaseNotExistException(Exception):
    # Constructor
    def __init__(self, db):
        # Guardar parámetros
        self.db = db
        
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: La base de datos '"+self.db+"' no existe."

# Excepción de base de datos existente
class DataBaseAlreadyExistException(Exception) :
    # Constructor
    def __init__(self, db):
        # Guardar parámetros
        self.db = db
        
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: La base de datos '"+self.db+"' ya existe."

# Contiene excepción para represantar ausencia de tabla
class TableNotExistException(Exception): pass
