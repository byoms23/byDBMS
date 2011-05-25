# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de modificación: viernes, 20 de mayo de 2011
# Tabla.py
# Contine el esquema y la información general del manejo de las tablas.

import logging, os, shutil, copy, calendar
from Excepciones import *
from Resultados import *
from analizadorSintactico import * 
from Registro import *

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
        self.cantidadRegistros = 0
        self.registros = []
    
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
        # Crear variables
        resp = Tabla(self.nombre, self.db)
        
        # Clonar propiedades más importantes
        resp.setAtributos(copy.copy(self.atributos))
        resp.setRestricciones(copy.copy(self.restricciones))
        resp.setDependientes(copy.copy(self.dependientes))
        resp.setCantidadRegistros(copy.copy(self.cantidadRegistros))
        
        # Devolver nuevo objeto
        return resp
        
    # Obtener el nombre de la tabla
    def getNombre(self):
        return self.nombre
        
    # Cambair el nombre de la tabla
    def setNombre(self, nombre):
        self.nombre = nombre
        
        self.log  = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+self.db.getNombre()+').Tabla('+str(self.nombre)+')')
        self.path = self.db.getPath() +  self.nombre + '.tbl'
        
    # Obtener los atributos de la tabla
    def getAtributos(self):
        return self.atributos
        
    # Obtener los atributos de la tabla
    def setAtributos(self, atributos):
        self.atributos = atributos

    # Obtener las restricciones de la tabla
    def getRestricciones(self):
        return self.restricciones
    
    # Colocar las restricciones de la tabla
    def setRestricciones(self, restricciones):
        self.restricciones = restricciones
    
    # Obtener la cantidad de registros que contiene la tabla
    def getCantidadRegistros(self):
        return self.cantidadRegistros
    
    # Colocar la cantidad de registros que contiene la tabla
    def setCantidadRegistros(self, cant):
        self.cantidadRegistros = cant
    
    # Obtener los registros de esta tabla
    def getRegistros(self):
        return self.registros
    
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
                a = "CH%.3i" % contador 
            elif restriccion == 'PRIMARY KEY':
                a = "PK%.3i" % contador 
            else:
                a = "FK%.3i" % contador
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
        tempPrimariasForaneas = copy.deepcopy(primariasForaneas)
        for i in xrange(len(tiposLocales)):
            # Revisar el tipo
            if tiposLocales[i] != tiposForaneos[i]:
                ex = ColumnTypeNotMatchException(listaLocal[i], tiposLocales[i], self, listaForanea[i], tiposForaneos[i], tabForanea)
                self.log.error(ex)
                raise ex
                
            # Revisar que sea parte de la llame primaria
            if not listaForanea[i] in tempPrimariasForaneas:
                ex = ColumnIsNotPrimaryKeyException(listaForanea[i], tabForanea)
                self.log.error(ex)
                raise ex
            else:
                tempPrimariasForaneas.remove(listaForanea[i])
        
        # Revisar que la referencia a la llave primaria (foranea) se completa
        if(len(tempPrimariasForaneas) > 0):
            ex = ColumnIsPrimaryKeyException(nombre, self, tempPrimariasForaneas[0], tabForanea)
            self.log.error(ex)
            raise ex
        
        # Agregar clave foranea
        self.restricciones.append(["FOREIGN KEY", nombre, listaLocal, tabla, listaForanea])
        tabForanea.addDependiente(self.getNombre())
        self.log.debug("Restricción agregada: " + str(self.restricciones[-1]) + ".")
        
    # Agregar un chequeo
    def agregar_chequeo(self, nombre, exp, requerido = None):
        # Formato de los nombres
        nombre = nombre.lower()
        requerido = requerido.lower() if requerido != None else None
        
        # Revisar si el nombre de restricción ya existe
        if self.existe_nombre(nombre):
            ex = ConstraintNameAlreadyException(nombre, self)
            self.log.error(ex)
            raise ex
            
        # Revisar que la expresion sea de tipo booleana
        t, dic = self.evaluarExpresion(exp)
        
        # Revisar si es requerido el campo/atributo
        if requerido != None:
            if not requerido in dic:
                ex = ColumnNotUsedException(requerido, nombre, self)
                self.log.error(ex)
                raise ex
        
        # Agregar clave foranea
        self.restricciones.append(["CHECK", nombre, exp])
        self.log.debug("Restricción agregada: " + str(self.restricciones[-1]) + ".")
        
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
        
    # Evaluar tipos
    def evaluarExpresion(self, exp):
        if type(exp) in [AST.Exp, AST.AndExp, AST.NotExp]:
            # Evaluar primer expresión
            t, d = self.evaluarExpresion(exp[0])
            if(len(exp) == 3):
                # Evaluar segunda expresión
                t2, d2 = self.evaluarExpresion(exp[2])
                d.extend(d2)
            return t, d
            
        elif type(exp) == AST.PredExp:
            if (len(exp) == 1):
                # Verificar que el tipo no sea nulo
                return self.evaluarExpresion(exp[0])
            elif(len(exp) == 3):
                op = exp[1]
                t1, d1 = self.evaluarExpresion(exp[0])
                t2, d2 = self.evaluarExpresion(exp[2])
                
                # Revisar segun operadores validos
                if t1 == "NULL" and op in ['=', '!=', '<>']:
                    pass
                elif t2 == "NULL" and op in ['=', '!=', '<>']:
                    pass
                elif t1 == t2:
                    pass    
                elif t1 == "DATE" and t2 == "CHAR":
                    pass
                elif t1 == "CHAR" and t2 == "DATE":
                    pass
                elif t1 == "INT" and t2 == "FLOAT":
                    pass
                elif t1 == "FLOAT" and t2 == "INT":
                    pass
                else:
                    # Caualquier otra combinación es invalida
                    ex = TypeMistmatchException(exp[0].toString(), t1, op, exp[2].toString(), t2, self)
                    self.log.error(ex)
                    raise ex
                
                # Devolver tipo e identificadores
                d1.extend(d2)
                return "BOOL", d1
            
        elif type(exp) == AST.Identificador:
            # Revisar que sea un identificador valido
            atributo = exp.toString().lower()
            self.contiene_atributos([atributo])
            
            # Devolver tipo
            tipo = self.tipo_de_atributos([atributo])[0]
            return tipo, [atributo]
        else:
            # Devolver tipo y diccionario vacio
            return (AST.equivale(type(exp)), [])
            
    # Quitar un atributo
    def quitar_atributo(self, idAtributo):
        # Declavar variables
        idAtributo = idAtributo.lower()
        
        # Buscar restriccion
        for rest in self.restricciones:
            if rest[0] == "PRIMARY KEY":
                if idAtributo in rest[2]:
                    ex = ColumnInConstraintException(idAtributo, rest[1], self)
                    self.log.error(ex)
                    raise ex
            elif rest[0] == "FOREIGN KEY":
                if idAtributo in rest[2] or idAtributo in rest[4]:
                    ex = ColumnInConstraintException(idAtributo, rest[1], self)
                    self.log.error(ex)
                    raise ex
            else:
                tipo, atributos = self.evaluarExpresion(rest[2])
                if idAtributo in atributos:
                    ex = ColumnInConstraintException(idAtributo, rest[1], self)
                    self.log.error(ex)
                    raise ex
                
        # Quitar el atributo especificado
        for atributo in self.atributos:
            if atributo[0] == idAtributo:
                self.atributos.remove(atributo)
        
    # Quitar una restriccion
    def quitar_restriccion(self, idRestriccion):
        # Declarar variables
        idRestriccion = idRestriccion.lower()
        encontrado = False
        
        # Buscar restriccion
        for rest in self.restricciones:
            if rest[1] == idRestriccion:
                self.restricciones.remove(rest)
                encontrado = True
                break
        
        # Verificar que idRestriccion exista
        if not encontrado:
            ex = ConstraintNotExistsException(idRestriccion, self) 
            self.log.error(ex)
            raise ex

    # ==================================================================
    # Método de registros
    # ==================================================================
    
    # Cargar registros desde el disco duro
    def cargar_registros(self):
    
    # Agregar un registro a la tabla seleccionada
    def agregar_registro(self, atributos, valoresList):
        # Revisar si específico atributos
        for valores in valoresList:
            # Crear nuevo registro
            r = Registro(self)
            
            # Verificar si viene la lista o se asume completa
            if not atributos:
                # Revisar si mando la cantidad de valores esperados
                if len(self.atributos) != len(valores):
                    ex = ValuesNotMatchException(self.nombre, len(self.atributos), len(valores))
                    self.log.error(ex)
                    raise ex
                
                # Revisar el tipo de cada atributo
                for i in xrange(len(self.atributos)):
                    nombre, tipo, tam = self.atributos[i]
                    valor = valores[i]
                    tipoValor = AST.equivale(type(valor))
                    valor = str(valor[0])
                    
                    val = r.validar_valor(nombre, tipo, tam, i, valor, tipoValor)
                    
                    r[nombre] = val
            else:
                # Revisar el tamaño de ambas listas
                if len(atributos) != len(valores):
                    ex = ValuesNotMatchException(self.nombre, len(atributos), len(valores))
                    self.log.error(ex)
                    raise ex
                
                # Instanciar todas los atributos
                for atributo in self.atributos:
                    r[atributo[0]] = None
                
                # Dar los valores asignados por cada atributo
                for i in xrange(len(atributos)):
                    atributo = atributos[i].lower()
                    valor = valores[i]
                    
                    # Buscar el atributo
                    for i in xrange(len(self.atributos)):
                        nombre, tipo, tam = self.atributos[i]
                        if nombre == atributo:
                            break;
                    
                    # Revisar si se encontró el atributo
                    if atributo != nombre:
                        ex = AttributeDoesNotException(self.nombre, atributo)
                        self.log.error(ex)
                        raise ex
                    
                    tipoValor = AST.equivale(type(valor))
                    valor = str(valor[0])
                    
                    val = r.validar_valor(nombre, tipo, tam, i, valor, tipoValor)
                    
                    r[nombre] = val
                
            # Revisar restricciones para cada registro 
            r.validar_restricciones()
            # Agregar registro a la tabla (memoria)
            self.registros.append(r)
            # TODO # Agregar registro a la tabla (disco duro)
            
            linea = self.formar_texto(r)
            with open(self.db.get_table_path(self.nombre), 'a') as archivo:
                archivo.write(linea)
            
            print r
            print self.registros
            
        
        # TODO Agregar registros a la tabla (memoria y disco duro).
        
    # Dar formato a un registro
    def formar_texto(self, registro, separador = '|'):
        r = ''
        for atributo in self.atributos:
            print atributo
            if atributo[1] == 'CHAR' or atributo[1] == 'DATE':
                r += "'" + str(registro[atributo[0]]) + "'"
            else:
                r += str(registro[atributo[0]]) 
            r += separador 
        s = (-1 * len(separador))
        if len(r) >= (-1 * s):
            r = r[:s] + '\n'
        return r
