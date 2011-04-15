# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Excepciones.py
# Contiene las clases de excepciones utilzados en el proyecto.

# ====================================================
# Excepciones para bases de datos
# ====================================================
# Clase base para las excepciones de la base de datos
class DataBaseException(Exception):
    # Constructor
    def __init__(self, db):
        # Guardar parámetros
        self.db = db

# Contiene excepción para represantar ausencia de base de datos
class DataBaseNotExistException(DataBaseException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: Base de datos '"+self.db+"' no existe."

# Excepción de base de datos existente
class DataBaseAlreadyExistException(DataBaseException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: Base de datos '"+self.db+"' ya existe."

# Excepción de base de datos existente
class DataBaseNotSelectedException(Exception):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: No hay base de datos en uso."

# ====================================================
# Excepciones para tablas
# ====================================================
# Contiene excepción general para un error en la tabla
class TableException(Exception):
    # Contructor
    def __init__(self, tabla, db):
        self.tabla = tabla
        self.db = db

# Contiene excepción para represantar ausencia de tabla
class TableNotExistException(TableException): 
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: La tabla '"+self.tabla+"' no existe en la base de datos '"+self.db.getNombre()+"'."

# Excepción de base de datos existente
class TableAlreadyExistException(TableException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: La tabla '"+self.tabla+"' ya existe en la base de datos '"+self.db.getNombre()+"'."

# ====================================================
# Excepciones para columnas
# ====================================================
# Contiene excepción general para un error en la tabla
class ColumnException(Exception):
    # Contructor
    def __init__(self, columna, tabla):
        self.columna = columna
        self.tabla = tabla
        
# Excepción de base de datos existente
class ColumnAlreadyExistException(TableException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "ERROR: La columna '"+self.columna+"' ya existe en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.getBaseDeDatos().getNombre()+"'."

# ====================================================
# Excepciones para restricciones
# ====================================================
