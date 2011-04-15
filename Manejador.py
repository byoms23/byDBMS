# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Menajadores.py
# Contine la información de los manejadores (tablas de símbolos) para las bases de datos y para las tablas.

# Importar modulos
import logging, os, shutil, copy, AST
from Excepciones import *
from Resultados import *

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
        shutil.rmtree(self.path + '/' + db + '/')
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
        
class BaseDeDatos():
    # Contructor
    def __init__(self, manejador, nombre, path, cantTablas):
        # Agregar los datos de la base de datos
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+nombre+')')
        self.manejador = manejador
        self.nombre = nombre
        self.path = path 
        self.schema_file = path + nombre + '/' + nombre + '.schema'
        self.cantTablas = cantTablas
        self.tablas = []
    
    # Revisar si dos objetos son iguales
    def __eq__(self, b):
        if type(b) == type(self):
            return self.nombre == b.nombre
        else:
            return False
    
    # Obtener el nombre de la base de datos
    def getNombre(self):
        return self.nombre
        
    # Cambair el nombre de la base de datos
    def setNombre(self, nombre):
        self.nombre = nombre
    
    # Obtener la cantidad de tablas de la base de datos
    def getCantidadTablas(self):
        return self.cantTablas
        
    # Obtener el path de la base de datos
    def getPath(self):
        return self.path + '/' + self.nombre + '/'
    
    # Carga la base de datos actual desde el archivo de metadados de la bd
    def cargar(self): 
        pass # TODO
        
    # Crea una nueva tabla en la base de datos actual.
    def agregar_tabla(self, tabla, listaDescripciones):
        # Definir tabla temporal
        tab = Tabla(tabla, self)
        
        # Revisar si la tabla ya existe
        if tab in self.tablas:
            self.log.error("La tabla '"+tabla+"' ya existe en la base de datos '"+self.getNombre()+"'.")
            raise TableAlreadyExistException(tabla, self)
            
        # Validar que la definicion de tabla no tenga errores de tipo
        # Separar constraints de columnas
        listaColumnas = []
        listaConstraints = []
        for desc in listaDescripciones:
            if type(desc) == AST.Columna:
                listaColumnas.append(desc)
                
                # Revisar si tiene constrains la columna
                if len(desc[2]) > 0:
                    listaConstraints.append(desc)
            else:
                listaConstraints.append(desc)
        
        # Revisión de columnas
        # Agregar columnas a la tabla
        for columna in listaColumnas:
            tab.agregar_columna(columna[0], columna[1][0], (columna[1][1] if columna[1][0] == 'CHAR' else None))
        # Revisión constraints 
        # TODO
        
        # Crear archivo vacio para la tabla
        path = self.getPath() + tabla + '.tbl'
        with open(path, 'w') as archivo:
            archivo.write('')
        
        # Agregar al archivo de metadatos de bases de datos
        atributos = tab.getAtributos()
        restricciones = tab.getRestricciones()
        with open(self.schema_file, 'a') as esquema:
            esquema.write('# Tabla: ' + tabla + '\n')
            esquema.write(tabla + '\n' )
            esquema.write(str(len(atributos)) + '\n')
            # Guardar cada atributo
            for atr in atributos:
                esquema.write(atr[0] + '\n' )
                esquema.write(atr[1] + ('\t' + str(atr[2]) if atr[2] != None else '') + '\n' )
            esquema.write(str(len(restricciones)) + '\n')
            # Guardar cada restriccion
            for rest in restricciones:
                esquema.write(rest[0] + '\n') # Tipo
                esquema.write(rest[1] + '\n') # Nombre
                if rest[0] == 'PRIMARY KEY': # Si es llave primaria
                    # Guardar lista id's
                    ids = ''
                    for Id in rest[2]:
                        ids += Id + ', '
                    ids = ids[:-2]
                    esquema.write(ids + '\n')
                elif rest[0] == 'FOREIGN KEY': # Si es llave foránea
                    # Guardar lista id's locales
                    ids = ''
                    for Id in rest[2]:
                        ids += Id + ', '
                    ids = ids[:-2]
                    esquema.write(ids + '\n')
                   
                    # Guardar tabla de referencia
                    esquema.write(rest[3] + '\n')
                    
                    # Guardar lista id's foraneos
                    ids = ''
                    for Id in rest[4]:
                        ids += Id + ', '
                    ids = ids[:-2]
                    esquema.write(ids + '\n')
                else: # Si es check
                    # Guardar expresion del check
                    esquema.write(rest[2] + '\n')
        
        # Agregar a la base de datos al manejador
        self.tablas.append(tab)
        self.cantTablas = len(self.tablas)
        
        # Agregar el archivo al archivo de metadatos del manejador
        self.manejador.actualizar_base_de_datos(self)
        
        # Mostrar mensaje de éxito
        self.log.info("Tabla '"+tabla+"' creada.")
        
    # Cambiar el nombre de la tabla descrita en idAntiguo por idNuevo.
    def renombrar_tabla(self, idAntiguo, idNuevo):
        pass # TODO
        
    # Aplica el conjunto de acciones de listaAcciones a tabla.
    def alterar_estructura_de_tabla(self, tabla, listaAcciones):
        pass # TODO
        
    # Eliminar la tabla descrita por tabla
    def eliminar_tabla(self, tabla):
        pass # TODO
        
    # Muestra las tablas de la base de datos actual.
    def mostrar_tablas(self):
        self.log.debug('Mostrar tablas.')
        # Declarar variables
        resp = Resultado()
        
        # Agregar titulos
        resp.addTitulo('Nombre')
        resp.addTitulo('Registros')
        
        # Agregar cada una de las bases de datos
        for tabla in self.tablas:
            resp.addContenido([tabla.getNombre(), tabla.getCantidadRegistros()])
            
        # Regresar respuesta
        self.log.debug(resp)
        return resp
        
    # Muestra las columnas de la tabla descrita en tabla.
    def mostrar_columnas_de_tabla(self, tabla): 
        # Guardar en log
        self.log.debug("Mostrar columnas de la tabla '"+tabla+"'.")
        
        # Verificar que la tabla exista
        self.verificar_tabla(tabla)    
        
        # Regresar respuesta
        return self.tablas[self.tablas.index(tabla)].mostrar_columnas()
        
    # Verifica que la tabla especificada exista
    def verificar_tabla(self, tabla):
        if not tabla in self.tablas:
            ex = TableNotExistException(tabla, self)
            self.log.error(ex)
            raise ex
        
class Tabla():
    # Contructor
    def __init__(self, nombre, db):
        # Agregar los datos de la tabla
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+db.getNombre()+').Tabla('+str(nombre)+')')
        self.nombre = nombre
        self.path = db.getPath() +  nombre + '.tbl'
        self.db = db
        self.atributos = []
        self.restricciones = []
        self.registros = 0
    
    # Revisar si dos objetos son iguales
    def __eq__(self, b):
        if type(b) == type(self):
            return self.nombre == b.nombre
        elif type(b) == str:
            return self.nombre == b
        else:
            return False
    
    # Copia profunda de la tabla
    def __deepcopy__(self):
        pass # TODO
        
    # Obtener el nombre de la tabla
    def getNombre(self):
        return self.nombre
        
    # Cambair el nombre de la tabla
    def setNombre(self, nombre):
        self.nombre = nombre
        
    # Obtener los atributos de la tabla
    def getAtributos(self):
        return self.atributos
        
    # Obtener las restricciones de la tabla
    def getRestricciones(self):
        return self.restricciones
    
    # Obtener la cantidad de registros que contiene la tabla
    def getCantidadRegistros(self):
        return self.registros
    
    # Obtener la base de datos a la cual pertene
    def getBaseDeDatos(self):
        return self.db
    
    # Agregar la columna específicada
    def agregar_columna(self, columna, tipo, valor=None):
        # Verificar que la columna no exista
        self.log.debug("Agregar columna '"+columna+"' a la tabla '"+self.getNombre()+"'.")
        existe = False
        for col in self.atributos:
            if col[0] == columna:
                existe = True
                break
        if existe:
            ex = ColumnAlreadyExistException(columna, self)
            self.log.error(ex)
            raise ex
            
        # Agregar la nueva columna
        self.atributos.append((columna, tipo, valor))
        self.log.debug("Columna '"+columna+"' agregada a la tabla '"+self.getNombre()+"'.")
        
    # Muestra las columnas de la tabla descrita en tabla.
    def mostrar_columnas(self): 
        self.log.debug('Mostrar columnas de la tabla.')
        # Declarar variables
        resp = Resultado()
        
        # Agregar titulos
        resp.addTitulo('Nombre')
        resp.addTitulo('Tipo')
        resp.addTitulo('Tamaño')
        resp.addTitulo('EsRestriccion')
        resp.addTitulo('Valor1')
        resp.addTitulo('Valor2')
        resp.addTitulo('Valor3')
        
        # Agregar cada una de las restricciones
        for atributo in self.atributos:
            resp.addContenido([atributo[0], atributo[1], atributo[2] if atributo[1] == 'CHAR' else 'NULL', 'False', 'NULL', 'NULL', 'NULL'])
            
        # Agregar cada una de las restricciones
        for restriccion in self.restricciones:
            resp.addContenido([restriccion[1], restriccion[0], 'NULL', 'True', (
                (restriccion[2], restriccion[3], restriccion[4]) if restriccion[0] == "FOREIGN KEY" else (restriccion[2], 'NULL', 'NULL')
                )])

        # Regresar respuesta
        return resp
