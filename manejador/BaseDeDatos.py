# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de modificación: viernes, 20 de mayo de 2011
# BaseDeDatos.py
# Contine el esquema y la información general del manejo de las bases de datos.

import logging, os, shutil, copy
from Excepciones import *
from Resultados import *
from Tabla import *
from analizadorSintactico import * 

# Clase que contiene la definición de una base de datos
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
                        exp = Parser.buildExp().parse(config[i])[0]
                        tab.agregar_chequeo(nombre, exp)
                # Cada dependiente
                i += 2
                dependientes = config[i].split(', ') if config[i].strip() != '' else []
                tab.setDependientes(dependientes)
                
                # Cargar registros de la tabla
                tab.cargar_registros()
                # Agregar tabla
                self.tablas.append(tab)
                
                # Ir por la siguiente
                i += 2
        except IOError, msg:
            pass            
        
    # Agregar restriccion
    def agregar_restriccion(self, tab, restriccion, mostrar=False):
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
                
                if mostrar:
                    # Log
                    self.log.info("Tabla '"+str(tab.getNombre())+"' modificada: Se agregó restricción '"+str(nombre)+"'.")
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
                
            if mostrar:
                # Log
                self.log.info("Tabla '"+str(tab.getNombre())+"' modificada: Se agregó restricción '"+str(nombre)+"'.")        
        
        
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
                    pass
        
        # Renombrar en el archivo de metadatos
        self.reemplazar_tabla_metadatos(anterior, tab)
        
        # Log
        self.log.info("Tabla '"+str(idAntiguo)+"' renombrada a '"+str(idNuevo)+"'.")
        
    # Aplica el conjunto de acciones de listaAcciones a tabla.
    def alterar_estructura_de_tabla(self, tabla, listaAcciones):
        # Revisar si la tabla existe
        tabla = self.verificar_tabla(tabla)
        
        # Copiar tabla para realizar cambios
        clone = tabla.__deepcopy__()
        clone.setNombre(clone.getNombre() + '_clone')
        # Actuales
        antiguos = [x[3] for x in tabla.getRestricciones() if x[0] == "FOREIGN KEY"]
        
        # Realizar cada una de las acciones que se solicitan
        for accion in listaAcciones:
            if accion[0] == 'ADD' and accion[1] == 'COLUMN':
                # Agregar columna
                clone.agregar_columna(accion[2][0], accion[2][1][0], (accion[2][1][1] if accion[2][1][0] == 'CHAR' else None))
                # Log
                self.log.info("Tabla '"+str(clone.getNombre())+"' modificada: Se agregó columna '"+str(accion[2][0])+"'.")        
                
                # Agregar restricciones cortas
                self.agregar_restriccion(clone, accion[2], mostrar = True)
            elif accion[0] == 'ADD':
                # Agregar restriccion
                self.agregar_restriccion(clone, accion[1], mostrar = True)
            elif accion[0] == 'DROP' and accion[1] == 'COLUMN':
                clone.quitar_atributo(accion[2])
                
                # Log
                self.log.info("Tabla '"+str(clone.getNombre())+"' modificada: Se quitó la columna '"+str(accion[2])+"'.")        
                
            elif accion[0] == 'DROP' and accion[1] == 'CONSTRAINT':
                clone.quitar_restriccion(accion[2])
                
                # Log
                self.log.info("Tabla '"+str(clone.getNombre())+"' modificada: Se quitó la restricción '"+str(accion[2])+"'.")
                
            #~ # Revision
            #~ self.log.debug("Clone")
            #~ self.log.debug(clone.getAtributos())
            #~ self.log.debug(clone.getRestricciones())
            #~ self.log.debug("Tabla")
            #~ self.log.debug(tabla.getAtributos())
            #~ self.log.debug(tabla.getRestricciones())
                
        # Eliminar base de datos del manejador
        self.tablas.remove(tabla)
        self.tablas.append(clone)

        # Notificar a las tablas de las cuales ya no se hace referencia
        actuales = [x[3] for x in clone.getRestricciones() if x[0] == "FOREIGN KEY"]
        for t in [x for x in antiguos if not x in actuales]:
            tab = self.verificar_tabla(t)
            tab.removeDependiente(tabla.getNombre())
        
        # Cambair dependencias
        for t in self.tablas:
            if not t is clone:
                t.actualizar_dependencia(clone.getNombre(), tabla.getNombre())
                try:
                    t.removeDependiente(clone.getNombre())
                    t.addDependiente(tabla.getNombre())
                except ValueError, msg:
                    pass
        
        # Renombrar en el archivo de metadatos
        clone.setNombre(tabla.getNombre())
        self.reemplazar_tabla_metadatos(tabla, clone)
        
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
                resp.append(rest[2].toString() + '\n')
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
            
    # ==================================================================
    # Método de registros
    # ==================================================================
    
    # Agregar un registro a la tabla seleccionada
    def agregar_registro_a_tabla(self, tabla, atributos, valores):
        # Guardar en log
        self.log.debug("Insertar registros en la tabla '"+tabla+"'.")
        
        # Verificar que la tabla exista
        return self.verificar_tabla(tabla).agregar_registro(atributos, valores)
      
    # Obtener la ruta al archivo que contiene la tabla descrita.
    def get_table_path(self, tabla):
        return self.getPath() + tabla + '.tbl'
        
    # Actualizar registros de la tabla seleccionada
    def actualizar_registros_en_tabla(self, tabla, cambios, condicion):
        # Guardar en log
        self.log.debug("Actualizar registros en la tabla '"+tabla+"'.")
        
        # Verificar que la tabla exista
        return self.verificar_tabla(tabla).actualizar_registros(cambios, condicion)
        
    # Eliminar registros de la tabla seleccionada
    def eliminar_registros_de_tabla(self, tabla, condicion):
        # Guardar en log
        self.log.debug("Eliminar registros en la tabla '"+tabla+"'.")
        
        # Verificar que la tabla exista
        return self.verificar_tabla(tabla).eliminar_registros(condicion)
      
