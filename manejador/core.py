# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Menajadores.py
# Contine la información de los manejadores (tablas de símbolos) para las bases de datos y para las tablas.

# Importar modulos
import logging, os, shutil, copy
from analizadorSintactico import * 
from BaseDeDatos import *

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
        self.base_de_datos_actual = None
        
    # Cargar configuración desde el archivo asignado al manejador
    def cargar(self):
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
               self.bases_de_datos.append(BaseDeDatos(self, tempList[0].strip(), self.path, int( tempList[1].strip())))
        arch.close()
        
    # Guarda la configuración actual de la base en el archivo designado para este manejador
    def salvar(self):
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
                    BaseDeDatos(self, tempList[0].strip(), self.path, int( tempList[1].strip())))
        arch.close()
        
    # Agrega la base de datos especificada en db.
    def agregar_base_de_datos(self, db):
        # Definir archivo
        dbo = BaseDeDatos(self, db, self.path, 0)
        
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
        
    # Cambia el nombre de la base de datos especificada por dbAntigua por dbNueva
    def renombrar_base_de_datos(self, dbAntigua, dbNueva):
        # Definir Base de datos
        dboAnt = BaseDeDatos(self, dbAntigua, self.path, 0)
        dboNue = BaseDeDatos(self, dbNueva,   self.path, 0)
        
        # Revisar que no se renombre al mismo nombre de la base de datos
        if dbAntigua == dbNueva:
            self.log.info("Base de datos '"+str(dbAntigua)+"' renombrada a '"+str(dbNueva)+"'.")
            return
        
        # Revisar si la base de datos antigua existe
        if not dboAnt in self.bases_de_datos:
            self.log.error("Base de datos '"+dbAntigua+"' no existe.")
            raise DataBaseNotExistException(dbAntigua)
        
        # Revisar si la nueva base de datos existe
        if dboNue in self.bases_de_datos:
            self.log.error("Base de datos '"+dbNueva+"' ya existe.")
            raise DataBaseAlreadyExistException(dbNueva)
        
        # Eliminar base de datos del disco duro
        shutil.move(self.path + '/' + dbAntigua + '/', self.path + '/' + dbNueva + '/')
        
        # Eliminar base de datos del registro
        with open(self.schema_file_name) as esquema:
            dataBases = esquema.readlines()
        # Revisar cada base de datos almacenada
        self.log.debug("Antes: \n" + str(dataBases))
        for temp in dataBases:
            # Buscar base de datos
            try:
                t = temp.split('=')
                if t[0].strip() == dbAntigua:
                    dataBases.remove(temp)
                    dataBases.append(dbNueva + ' = ' + t[1].strip())
                    break
            except:
                pass
        # Guardar en el archivo
        self.log.debug("Después: \n" + str(dataBases))
        with open(self.schema_file_name, 'w') as esquema:
            esquema.writelines(dataBases)
        
        # Eliminar base de datos del manejador
        db = self.bases_de_datos[self.bases_de_datos.index(dboAnt)]
        db.setNombre(dbNueva)
        self.log.info("Base de datos '"+str(dbAntigua)+"' renombrada a '"+str(dbNueva)+"'.")
        
    # Elimina la base de datos seleccionada en db
    def eliminar_base_de_datos(self, db):
        # Definir Base de datos
        dbo = BaseDeDatos(self, db, self.path, 0)
        
        # Revisar si la base de datos ya existe
        if not dbo in self.bases_de_datos:
            self.log.error("Base de datos '"+db+"' no existe.")
            raise DataBaseNotExistException(db)
        
        # Eliminar base de datos del manejador
        self.bases_de_datos.remove(dbo)
        
        # Eliminar base de datos del registro
        with open(self.schema_file_name) as esquema:
            dataBases = esquema.readlines()
        # Revisar cada base de datos almacenada
        self.log.debug("Antes: \n" + str(dataBases))
        for temp in dataBases:
            # Buscar base de datos
            try:
                t = temp.split('=')[0].strip()
                if t == db:
                    dataBases.remove(temp)
                    break
            except:
                pass
        # Guardar en el archivo
        self.log.debug("Después: \n" + str(dataBases))
        with open(self.schema_file_name, 'w') as esquema:
            esquema.writelines(dataBases)
        
        # Eliminar base de datos del disco duro
        shutil.rmtree(self.path + db + '/')
        self.base_de_datos_actual = None if self.base_de_datos_actual == dbo else self.base_de_datos_actual
        self.log.info("Base de datos '"+str(db)+"' borrada.")
    
    # Crea el resultado de la información que es presentada
    def mostrar_bases_de_datos(self):
        self.log.debug('Mostrar bases de datos.')
        # Declarar variables
        resp = Resultado()
        
        # Agregar titulos
        resp.addTitulo('Base de datos')
        resp.addTitulo('Cantidad tablas')
        
        # Agregar cada una de las bases de datos
        for db in self.bases_de_datos:
            resp.addContenido([db.getNombre(), db.getCantidadTablas()])
            
        # Regresar respuesta
        return resp
    
    # Cambia la base de datos actual
    def utilizar_base_de_datos(self, db):
        # Declarar variables
        temp = BaseDeDatos(self, db, self.path, 0)
        
        # Buscar la nueva base de datos
        if temp in self.bases_de_datos:
        
            # Guardar y cargar nueva base de datos actual
            self.base_de_datos_actual = self.bases_de_datos[self.bases_de_datos.index(temp)]
            self.base_de_datos_actual.cargar()
            
            # Guardar mensaje de éxito
            self.log.info('Base de datos \''+db+'\' en uso.')
        else:
            # Guardar mensaje de éxito
            self.log.error('Base de datos \''+db+'\' no existe.')
            raise DataBaseNotExistException(db)
    
    # Cambiar la cantidad de tablas en el archivo de metadatos    
    def actualizar_base_de_datos(self, db):
        
        # Actualizar cantidad de tablas de la base de datos en el registro
        with open(self.schema_file_name) as esquema:
            dataBases = esquema.readlines()
        
        # Revisar cada base de datos almacenada
        self.log.debug("Antes: \n" + str(dataBases))
        for temp in dataBases:
            # Buscar base de datos
            try:
                t = temp.split('=')
                if t[0].strip() == db.getNombre():
                    dataBases.remove(temp)
                    dataBases.append(db.getNombre() + ' = ' + str(db.getCantidadTablas()) + '\n')
                    break
            except:
                pass
        
        # Guardar en el archivo de metadatos
        self.log.debug("Después: \n" + str(dataBases))
        with open(self.schema_file_name, 'w') as esquema:
            esquema.writelines(dataBases)
    
    # Verificar si hay una base de datos en uso actualmente, arroja una excepción si no existe
    def verificar_base_de_datos_en_uso(self):
        # Vericar base de datos actual
        if self.base_de_datos_actual == None:
            self.log.error('No hay base de datos en uso.')
            raise DataBaseNotSelectedException()
        
    
    # Crea una nueva tabla en la base de datos actual
    def agregar_tabla(self, tabla, listaDescripciones):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Agregar tabla a la base de datos actual
        self.base_de_datos_actual.agregar_tabla(tabla, listaDescripciones)
        
    # Cambiar el nombre de la tabla descrita en idAntiguo por idNuevo.
    def renombrar_tabla(self, idAntiguo, idNuevo):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        self.base_de_datos_actual.renombrar_tabla(idAntiguo, idNuevo)
        
    # Aplica el conjunto de acciones de listaAcciones a tabla.
    def alterar_estructura_de_tabla(self, tabla, listaAcciones):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        self.base_de_datos_actual.alterar_estructura_de_tabla(tabla, listaAcciones)
        
    # Eliminar la tabla descrita por tabla
    def eliminar_tabla(self, tabla):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        self.base_de_datos_actual.eliminar_tabla(tabla)
        
    # Muestra las tablas de la base de datos actual.
    def mostrar_tablas(self):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        return self.base_de_datos_actual.mostrar_tablas()
        
    # Muestra las columnas de la tabla descrita en tabla.
    def mostrar_columnas_de_tabla(self, tabla): 
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        return self.base_de_datos_actual.mostrar_columnas_de_tabla(tabla)
        
    # Quita dependencias rotas
    def revision(self):
        if self.base_de_datos_actual != None:
            self.base_de_datos_actual.revision()
            
    # ==================================================================
    # Método de registros
    # ==================================================================
    
    # Agregar un registro a la tabla
    def agregar_registro_a_tabla(self, tabla, atributos, valores):
        # Vericar base de datos actual
        self.verificar_base_de_datos_en_uso()
        
        # Renombrar tabla de la base de datos actual
        return self.base_de_datos_actual.agregar_registro_a_tabla(tabla, atributos, valores)
        
