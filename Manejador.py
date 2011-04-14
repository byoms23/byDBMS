# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Menajadores.py
# Contine la información de los manejadores (tablas de símbolos) para las bases de datos y para las tablas.

# Importar modulos
import logging
import os
from Excepciones import *

# Clase que administra la información de las bases de datos creadas
class ManejadorBaseDatos():
    # Constructor de la clase
    def __init__(self, mbdPath=None):
        # Detectar path
        if mbdPath == None:
            mbdPath = './'
        
        # Declarar variables globales del manejador
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos')
        self.path = mbdPath + '/'
        self.schema_file_name=self.path + 'bd.schema'
        self.bases_de_datos = []
        
    # Cargar configuración desde el archivo asignado al manejador
    def load(self):
        # Abrir archivo de metadatos
        try:
            arch = open(self.schema_file_name)
        except IOError, msg:
            self.log.warning('Archivo de metadatos "'+self.schema_file_name+'" no existe. Se cargará el manejador vacio.')
            return
        
        for line in arch:
            # Leer cada linea
            line = line.strip()
            if line.startswith("#"):
                continue
            elif len(line) == 0:
                continue
            else:
               # Extraer el valor
               tempList = line.split("=")
               
               # Cargar nueva base de datos
               self.bases_de_datos.append(BaseDeDatos(tempList[0].strip(), self.path, int( tempList[1].strip())))
        arch.close()
        
    # Guarda la configuración actual de la base en el archivo designado para este manejador
    def save(self):
        # Abrir archivo de metadatos
        arch = open(self.filename, 'a')
        
        # Guardar cada una de las bases de datos
        for db in f:
            # Leer cada linea
            line = line.strip()
            if line.startswith("#"):
                continue
            elif len(line) == 0:
                continue
            else:
                # Extraer el valor
                tempList = line.split("=")
                
                # Cargar nueva base de datos
                self.bases_de_datos.append(
                    BaseDeDatos(tempList[0].strip(), self.path, int( tempList[1].strip())))
        arch.close()
        
    # Agrega la base de datos especificada en db.
    def agregar_base_de_datos(self, db):
        # Definir archivo
        dbo = BaseDeDatos(db, self.path, 0)
        
        # Revisar si la base de datos ya existe
        if dbo in self.bases_de_datos:
            self.log.error("Base de datos '"+db+"' ya existe.")
            raise DataBaseAlreadyExistException(db)
            
        # Crear directorio de la base de datos
        path = self.path + db + '/'
        if os.path.exists(path):
            # Eliminar tablas rotas
            for tabla in os.listdir(path):
                os.remove(path + tabla)
            
            # Eliminar base de datos antigua
            os.rmdir(path)
        
        os.mkdir(path)
        
        # Agregar al archivo de metadatos de bases de datos
        with open(self.schema_file_name, 'a') as esquema:
            esquema.write(db + ' = 0 \n' )
        
        # Agregar a la base de datos al manejador
        self.bases_de_datos.append(dbo)
        
        # Mostrar mensaje de éxito
        self.log.info('Base de datos \''+db+'\' creada.')
        
class BaseDeDatos():
    # Contructor
    def __init__(self, nombre, path, cantTablas):
        # Agregar los datos de la base de datos
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+nombre+')')
        self.nombre = nombre
        self.path = path + '/' +  nombre + '.tbl'
        self.cantTablas = cantTablas
        self.tablas = []
    
    # Revisar si dos objetos son iguales
    def __eq__(self, b):
        if type(b) == type(self):
            return self.nombre == b.nombre
        else:
            return False
    
    # Convertir a texto. 
    def forSave(self):
        # Declarar variables
        r = ''
        
        # Formar la cadena de respuesta
        r  = str(self.nombre) + ' = ' + str(len(self.tablas))
        
        # Devolver la cadena de respuesta
        return r
    
class Tabla():
    # Contructor
    def __init__(self, nombre, db):
        # Agregar los datos de la tabla
        self.log = logging.getLogger()
        self.nombre = nombre
        self.db = db
        self.atributos = []
        self.registros = 0
    
    # 