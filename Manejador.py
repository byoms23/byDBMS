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
        
class BaseDeDatos():
    # Contructor
    def __init__(self, manejador, nombre, path, cantTablas):
        # Agregar los datos de la base de datos
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+nombre+')')
        self.manejador = manejador
        self.nombre = nombre
        self.path = path 
        self.schema_file = path + nombre + '/' + 'tables' + '.schema'
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
        # Cargar desde el esquema
        try:
            with open(self.schema_file) as esquema:
                config = map(lambda x : x[:-1], esquema.readlines())
                
            # Cargar la cantidad de tablas específicada
            self.tablas = []
            i = 1
            for tabs in range(self.getCantidadTablas()):
                # Crear tabla
                tab = Tabla(config[i], self)
                i += 2
                # Registros
                tab.setCantidadRegistros(int(config[i]))
                i += 2
                # Columnas
                for cols in xrange(int(config[i])):
                    i += 1
                    nombre = config[i]
                    i += 1
                    l = config[i].split('\t')
                    tipo = l[0]
                    tamanio = None if len(l) < 2 else l[1]
                    tab.agregar_columna(nombre, tipo, valor=tamanio)
                # Cada restricción
                i += 2
                for rests in xrange(int(config[i])):
                    i += 1
                    if config[i] == 'PRIMARY KEY':
                        i += 1
                        nombre = config[i]
                        i += 1
                        keys = config[i].split(', ')
                        tab.agregar_clave_primaria(nombre, keys)
                    elif config[i] == 'FOREIGN KEY':
                        i += 1
                        nombre = config[i]
                        i += 1
                        local = config[i].split(', ')
                        i += 1
                        tabForanea = config[i]
                        i += 1
                        foranea = config[i].split(', ')
                        tab.agregar_clave_foranea(nombre, local, tabForanea, foranea)
                    else:
                        i += 1
                        nombre = config[i]
                        i += 1
                        exp = config[i]
                        tab.agregar_chequeo(nombre, exp)
                # Cada dependiente
                i += 2
                dependientes = config[i].split(', ') if config[i].strip() != '' else []
                tab.setDependientes(dependientes)
                
                # Agregar tabla
                self.tablas.append(tab)
                
                # Ir por la siguiente
                i += 2
        except IOError, msg:
            pass            
        
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
        for columna in listaColumnas:
            # Agregar columnas a la tabla
            tab.agregar_columna(columna[0], columna[1][0], (columna[1][1] if columna[1][0] == 'CHAR' else None))
        
        # Revisión constraints 
        for restriccion in listaConstraints:
            if type(restriccion) == AST.Columna:
                # Revisar cada restricción corta
                for restriccionCorta in restriccion[2]:
                    tipo = restriccionCorta[0] if restriccionCorta[0] == 'CHECK' else (
                            "PRIMARY KEY" if restriccionCorta[0] == 'PRIMARY' else "FOREIGN KEY")
                    nombre = tab.generar_nombre(tipo)
                    if tipo == 'CHECK':
                        tab.agregar_chequeo(nombre, restriccionCorta[1], requerido=restriccion[0])
                    elif tipo == 'PRIMARY KEY':
                        tab.agregar_clave_primaria(nombre, [restriccion[0]])
                    else:
                        tab.agregar_clave_foranea(nombre, [restriccion[0]], restriccionCorta[1], [restriccionCorta[2]])
                
            else:
                # Agregar alguna de las restricciones validas
                tipo = restriccion[0] if restriccion[0] == 'CHECK' else (restriccion[0] + " KEY")
                nombre = restriccion[1]
                if tipo == 'CHECK':
                    tab.agregar_chequeo(nombre, restriccion[2])
                elif tipo == 'PRIMARY KEY':
                    tab.agregar_clave_primaria(nombre, restriccion[2])
                else:
                    tab.agregar_clave_foranea(nombre, restriccion[2], restriccion[3], restriccion[4])
        
        # Crear archivo vacio para la tabla
        path = self.getPath() + tabla + '.tbl'
        with open(path, 'w') as archivo:
            archivo.write('')
        
        # Agregar al archivo de metadatos de bases de datos
        self.escribir_tabla(tab)
            
        # Agregar a la base de datos al manejador
        self.tablas.append(tab)
        self.cantTablas = len(self.tablas)
        
        # Agregar el archivo al archivo de metadatos del manejador
        self.manejador.actualizar_base_de_datos(self)
        
        # Mostrar mensaje de éxito
        self.log.info("Tabla '"+tabla+"' creada.")
        
    # Cambiar el nombre de la tabla descrita en idAntiguo por idNuevo.
    def renombrar_tabla(self, idAntiguo, idNuevo):
        # Definir tablas
        idAntiguo = idAntiguo.lower()
        idNuevo = idNuevo.lower()
        anterior = Tabla(idAntiguo, self)
        nueva    = Tabla(idNuevo,   self)
        
        # Revisar que no se renombre al mismo nombre de la base de datos
        if idAntiguo == idNuevo:
            self.log.info("Tabla '"+str(dbAntiguo)+"' renombrada a '"+str(dbNuevo)+"'.")
            return
        
        # Revisar si la tabla antigua existe
        if not anterior in self.tablas:
            ex = TableNotExistException(idAntiguo)
            self.log.error(ex)
            raise ex
        
        # Revisar si la tabla nueva existe
        if nueva in self.tablas:
            ex = TableAlreadyExistException(idNuevo)
            self.log.error(ex)
            raise ex
        
        # Renombrar la tabla en el disco duro
        os.rename(self.getPath() + idAntiguo + '.tbl', self.getPath() + idNuevo + '.tbl')
        
        # Eliminar base de datos del manejador
        tab = self.tablas[self.tablas.index(anterior)]
        tab.setNombre(idNuevo)

        # Cambair dependencias
        for t in self.tablas:
            if not t is tab:
                t.actualizar_dependencia(idAntiguo, idNuevo)
                try:
                    t.removeDependiente(idAntiguo)
                    t.addDependiente(idNuevo)
                except ValueError, msg:
                    print msg
                    pass
        
        # Renombrar en el archivo de metadatos
        self.reemplazar_tabla_metadatos(anterior, tab)
        
        # Log
        self.log.info("Tabla '"+str(idAntiguo)+"' renombrada a '"+str(idNuevo)+"'.")
        
    # Aplica el conjunto de acciones de listaAcciones a tabla.
    def alterar_estructura_de_tabla(self, tabla, listaAcciones):
        pass # TODO
        
    # Eliminar la tabla descrita por tabla
    def eliminar_tabla(self, tabla):
        # Revisar si la tabla existe
        tabla = self.verificar_tabla(tabla)
        
        # Revisar que no haya tablas que dependan de esta tabla
        if len(tabla.getDependientes()) > 0:
            ex = NeededTableException(tabla.getNombre(), tabla.getDependientes())
            self.log.error(ex)
            raise ex
        
        # Eliminar tabla de la base de datos
        self.tablas.remove(tabla)
        self.cantTablas = len(self.tablas)
        
        # Eliminar del registro
        self.borrar_tabla_metadatos(tabla)
        
        # Eliminar base de datos del disco duro
        os.remove(self.getPath() + tabla.getNombre() + '.tbl')
        
        # Eliminar dependencias (llaves foraneas)
        for t in self.tablas:
            try:
                t.removeDependiente(tabla.getNombre())
            except ValueError, msg:
                pass
            
            
        # Agregar el archivo al archivo de metadatos del manejador
        self.manejador.actualizar_base_de_datos(self)
        
        # Log
        self.log.info("Tabla '"+str(tabla.getNombre())+"' borrada.")
        
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
            
        return self.tablas[self.tablas.index(tabla)]
        
    # Quita dependencias rotas
    def revision(self):
        for tabla in self.tablas:
            for dep in tabla.getDependientes():
                if not dep in self.tablas:
                    tabla.removeDependiente(dep)
                    
    
    # Guarda la tabla especificada en el archivo de metadatos
    def escribir_tabla(self, tab):
        # Declarar variables
        lista = self.crear_lista_tabla(tab)
        
        with open(self.schema_file, 'a') as esquema:
            esquema.writelines(lista)
    
    # Guarda la tabla especificada en el archivo de metadatos
    def crear_lista_tabla(self, tab):
        # Variables
        atributos = tab.getAtributos()
        restricciones = tab.getRestricciones()
        
        # Crear lista de respuesta
        resp = []
        resp.append('# Tabla: ' + tab.getNombre() + '\n')
        resp.append(tab.getNombre() + '\n' )
        resp.append('## Registros \n' )
        resp.append(str(tab.getCantidadRegistros()) + ' \n')
        resp.append('## Columnas \n' )
        resp.append(str(len(atributos)) + '\n')
        # Guardar cada atributo
        for atr in atributos:
            resp.append(atr[0] + '\n' )
            resp.append(atr[1] + ('\t' + str(atr[2]) if atr[2] != None else '') + '\n' )
        resp.append('## Restricciones \n' )
        resp.append(str(len(restricciones)) + '\n')
        # Guardar cada restriccion
        for rest in restricciones:
            resp.append(rest[0] + '\n') # Tipo
            resp.append(rest[1] + '\n') # Nombre
            if rest[0] == 'PRIMARY KEY': # Si es llave primaria
                # Guardar lista id's
                ids = ''
                for Id in rest[2]:
                    ids += Id + ', '
                ids = ids[:-2]
                resp.append(ids + '\n')
            elif rest[0] == 'FOREIGN KEY': # Si es llave foránea
                # Guardar lista id's locales
                ids = ''
                for Id in rest[2]:
                    ids += Id + ', '
                ids = ids[:-2]
                resp.append(ids + '\n')
               
                # Guardar tabla de referencia
                resp.append(rest[3] + '\n')
                
                # Guardar lista id's foraneos
                ids = ''
                for Id in rest[4]:
                    ids += Id + ', '
                ids = ids[:-2]
                resp.append(ids + '\n')
            else: # Si es check
                # Guardar expresion del check
                resp.append(rest[2] + '\n')
        resp.append('## Tablas que dependen de esta tabla \n' )
        # Guardar lista id's foraneos
        deps = ''
        for dep in tab.getDependientes():
            deps += dep + ', '
        resp.append(deps[:-2] + '\n')
        
        return resp
            
    # Borrar tabla del archivo de metadatos.
    def borrar_tabla_metadatos(self, tabla):
        # Eliminar base de datos del registro
        with open(self.schema_file) as esquema:
            config = map(lambda x : x[:-1], esquema.readlines())
            
        # Buscar tabla especificada
        inicio, fin = self.buscar_tabla_metadatos(config, tabla)
                
        # Guardar en el archivo
        del config[inicio:fin]
        config = map(lambda x : x + '\n', config)
        with open(self.schema_file, 'w') as esquema:
            esquema.writelines(config)
        
    # Busca una tabla en el archivo de metadatos
    def buscar_tabla_metadatos(self, lista, tabla):
        # Buscar tabla
        config = lista
            
        # Buscar tabla especificada
        inicio = None
        fin = None
        
        # Recorrer tablas
        i = 1
        for tabs in range(self.getCantidadTablas() + 1):
            # Revisar por tabla
            if config[i] == tabla.getNombre():
                inicio = i - 1
            # Registros y columnas
            i += 4
            for cols in xrange(int(config[i])):
                i += 2
            # Cada restricción
            i += 2
            for rests in xrange(int(config[i])):
                i += 1
                if config[i] == 'FOREIGN KEY':
                    i += 4
                else:
                    i += 2
            # Cada dependiente e Ir por la siguiente
            i += 4
            
            # Ver si era la tabla especificada
            if inicio != None:
                fin = i - 1
                break 
                
        return inicio, fin
    
    # Reemplazar tabla en el archivo de metadatos.
    def reemplazar_tabla_metadatos(self, tabla1, tabla2):
        # Buscar tabla
        with open(self.schema_file) as esquema:
            config = map(lambda x : x[:-1], esquema.readlines())
            
        # Declarar variables
        inicio, fin = self.buscar_tabla_metadatos(config, tabla1)
                
        # Guardar en el archivo
        listaI = map(lambda x : x + '\n', config[:inicio])
        listaF = map(lambda x : x + '\n', config[fin:])
        lista = listaI
        lista.extend(self.crear_lista_tabla(tabla2))
        lista.extend(listaF)
        
        with open(self.schema_file, 'w') as esquema:
            esquema.writelines(lista)
        
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
        self.dependientes = []
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
    
    # Colocar la cantidad de registros que contiene la tabla
    def setCantidadRegistros(self, cant):
        self.registros = cant

    # Obtener la base de datos a la cual pertene
    def getBaseDeDatos(self):
        return self.db
        
    # Agregar que hace referencia a esta tabla
    def addDependiente(self, tabla):
        if not tabla in self.dependientes:
            self.dependientes.append(tabla)
        
        # Actualizar metadatos
        self.db.reemplazar_tabla_metadatos(self, self)
    
    # Agregar que hace referencia a esta tabla
    def removeDependiente(self, tabla):
        self.dependientes.remove(tabla)

        # Actualizar metadatos
        self.db.reemplazar_tabla_metadatos(self, self)
    
    # Agregar que hace referencia a esta tabla
    def getDependientes(self):
        return self.dependientes
        
    # Guarda que hace referencia a esta tabla
    def setDependientes(self, dependientes):
        self.dependientes = dependientes
    
    # Actualizar dependencia si existe
    def actualizar_dependencia(self, old, new):
        # Recorrer restricciones en busca de FK
        for r in self.restricciones:
            if r[0] == "FOREIGN KEY":
                if r[3] == old:
                    r[3] = new
                    
        # Actualizar metadatos
        self.db.reemplazar_tabla_metadatos(self, self)
        
    # Agregar la columna específicada
    def agregar_columna(self, columna, tipo, valor=None):
        # Verificar que la columna no exista
        columna = columna.lower()
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
        self.atributos.append((columna.lower(), tipo, valor))
        self.log.debug("Columna '"+columna+"' agregada a la tabla '"+self.getNombre()+"'.")
        
    # Busca el nombre dentro de la tabla
    def existe_nombre(self, name):
        # Buscar
        for rest in self.restricciones:
            if rest[1] == name:
                return True
        return False

    # Genera un nombre valido para la restriccion indicada
    def generar_nombre(self, restriccion):
            
        # Declarar variables
        contador = 0
        ret = None
        
        # Crear nuevo nombre de restricción
        while not ret:
            if restriccion == 'CHECK':
                a = "CH_%.3i" % contador 
            elif restriccion == 'PRIMARY KEY':
                a = "PK_%.3i" % contador 
            else:
                a = "FK_%.3i" % contador
            if not self.existe_nombre(a):
                ret = a
            contador += 1
            
        return ret
        
    # Devuelve la lista de los atributos que conforman la llame primaria, si no hay llame primaria devuelve None.
    def get_clave_primaria(self):
        # Declarar variables
        r = None
        
        # Hacer la busqueda
        for rest in self.restricciones:
            if rest[0] == "PRIMARY KEY":
                r = rest[2]
                break
        
        # Devolver el resultado
        return r
        
    # Revisa si cada elemento de la listaAtributos pertenece a la tabla
    def contiene_atributos(self, listaAtributos):
        # Crear lista temporal
        tempList = map(str.lower,listaAtributos)
        
        # Revisar cada atributo
        for at in self.atributos:
            if at[0] in tempList:
                tempList.remove(at[0])
            # Si se encontraron todos los atributos salir
            if len(tempList) == 0:
                break
                
        # Revisar si estaban todos los elementos
        if len(tempList) > 0:
            ex = ColumnNotExistException(tempList[0], self)
            self.log.error(ex)
            raise ex
    
    # Devuelve una lista de los tipos de los atributos enviados en listaAtributos
    def tipo_de_atributos(self, listaAtributos):
        # Crear lista temporal
        listaAtributos = map(str.lower,listaAtributos)
        tempList = []
        
        # Revisar cada atributo
        mapeo = {}
        colocar = lambda atri : mapeo.__setitem__(atri[0], atri[1])
        map(colocar, self.atributos)
        for at in listaAtributos:
            tempList.append(mapeo[at])
                
        # Revisar si estaban todos los elementos
        return tempList

    # Agregar la clave primaria
    def agregar_clave_primaria(self, nombre, listaAtributos):
        # Revisar si la tabla ya tiene llave primaria
        if self.get_clave_primaria() != None:
            ex = PrimaryKeyAlreadyException(self)
            self.log.error(ex)
            raise ex
            
        # Revisar si el nombre de restricción ya existe
        if self.existe_nombre(nombre):
            ex = ConstraintNameAlreadyException(nombre, self)
            self.log.error(ex)
            raise ex
        
        # Revisar si cada elemento de la lista pertenece a esta tabla    
        self.contiene_atributos(listaAtributos)
        
        # Agregar clave primaria
        self.restricciones.append(["PRIMARY KEY", nombre.lower(), map(str.lower, listaAtributos)])
        self.log.debug("Restricción agregada: " + str(self.restricciones[-1]) + ".")

    # Agregar una clave foranea
    def agregar_clave_foranea(self, nombre, listaLocal, tabla, listaForanea):
        # Formato de los nombres
        nombre = nombre.lower()
        listaLocal = map(str.lower, listaLocal)
        tabla = tabla.lower()
        listaForanea = map(str.lower, listaForanea)
        
        # Revisar si el nombre de restricción ya existe
        if self.existe_nombre(nombre):
            ex = ConstraintNameAlreadyException(nombre, self)
            self.log.error(ex)
            raise ex
        
        # Revisar si la tabla foranea existe
        tabForanea = self.db.verificar_tabla(tabla)
        
        # Revisar si cada elemento de la lista local pertenece a esta tabla    
        self.contiene_atributos(listaLocal)
            
        # Revisar si cada elemento de la lista local pertenece a esta tabla    
        tabForanea.contiene_atributos(listaForanea)
        
        # Revisar que tengan el mismo tamaño
        if len(listaLocal) != len(listaForanea):
            ex = AmountsOfColumnsNotMatchException(nombre, self, tabForanea)
            self.log.error(ex)
            raise ex
        
        # Revisar si el tipo de cada atributo es correcto
        tiposLocales = self.tipo_de_atributos(listaLocal)
        tiposForaneos = tabForanea.tipo_de_atributos(listaForanea)
        primariasForaneas = tabForanea.get_clave_primaria()
        for i in xrange(len(tiposLocales)):
            # Revisar el tipo
            if tiposLocales[i] != tiposForaneos[i]:
                ex = ColumnTypeNotMatchException(listaLocal[i], tiposLocales[i], self, listaForanea[i], tiposForaneos[i], tabForanea)
                self.log.error(ex)
                raise ex
                
            # Revisar que sea parte de la llame primaria
            if not listaForanea[i] in primariasForaneas:
                ex = ColumnIsNotPrimaryKeyException(listaForanea[i], tabForanea)
                self.log.error(ex)
                raise ex
        
        # Agregar clave primaria
        self.restricciones.append(["FOREIGN KEY", nombre, listaLocal, tabla, listaForanea])
        tabForanea.addDependiente(self.getNombre())
        self.log.debug("Restricción agregada: " + str(self.restricciones[-1]) + ".")
        
    # Agregar un chequeo
    def agregar_chequeo(self, nombre, exp, requerido = None):
        pass # TODO
        
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
            r = [restriccion[1], restriccion[0], 'NULL', 'True']
            r.extend(((restriccion[2], restriccion[3], restriccion[4]) if restriccion[0] ==     "FOREIGN KEY" else (restriccion[2], 'NULL', 'NULL')))
            resp.addContenido(r)

        # Regresar respuesta
        return resp
