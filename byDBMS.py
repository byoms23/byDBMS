# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: domingo, 10 de abril de 2011
# byDBMS.py
# Contiene el core del manejador de datos

# Importar modulos, funciones y clases
import logging
import sys, os
import Parser
import lepl
from lepl import Node
from AST import *
from Manejador import ManejadorBaseDatos
from Excepciones import *

# Carga la configuracion inicial del modulo
def configure(tipo="info"):
    # Variables del modulo
    global path, log, manejador
    
    # Configurar el log
    configLogger(tipo)
    
    # Abrir el archivo de configuracion
    try:
        f = open('byDBMS.conf')
        dic = {}
        for line in f:
            # Leer cada linea
            line = line.strip()
            if line.startswith("#"):
                continue
            elif len(line) == 0:
                continue
            else:
               # Extraer el valor
               tempList = line.split("=")
               dic[tempList[0].strip()] = tempList[1].strip()
        f.close()
        
        # Buscar path
        try:
            path = dic["path"]
        except KeyError, msg:
            log.warning("No se ha especificado un path predefinido.")
            path = './data/'
        
        # Revisar que el path exista
        if os.path.exists(path):
            if not os.path.isdir(path):
                log.error("El path especificado no es un directorio.")
                
                # TODO Crear excepciones para esto
                
            else:
                # Crear manejador
                manejador = ManejadorBaseDatos(mbdPath=path)
                # Configurar manejador
                manejador.cargar()
        else:
            log.warning("El path especificado para iniciar no existe, se ha creado el nuevo directorio.")
            os.makedirs(path)
        
        
                
    except IOError, msg:
        # Mostrar warning por la falta de archivo de configuracion 
        log.warning("Archivo de configuracion byDBMS.conf no existe.")
        
# Configura el logger segun el nivel indicado por nivel_name.
def configLogger(tipo='warning', archivo=None):
    # Traer el log
    global log
    
    # Revisar el archivo de destino
    if archivo == None:
        archivo = 'byDBMS.log'
    
    # Crear diccionario de niveles
    LEVELS = {'-v': logging.DEBUG,
              'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    # Determinar el nivel
    level = LEVELS.get(tipo, logging.NOTSET)
    
    # Congiruar el nivel del log
    log.setLevel(logging.DEBUG)

    # Crear handler de archivo para guardar los mensajes
    fh = logging.FileHandler(archivo)
    fh.setLevel(logging.DEBUG)
    # Crear el handler para la consola con el nivel ingresado
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # Establecer formatos predeterminados para el archivo de log y la consola
    formatter = logging.Formatter("%(asctime)s - %(name)s \n%(levelname)s - %(message)s")
    formatter2 = logging.Formatter("\n%(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter2)
    
    # Agregar handlers al logger
    log.addHandler(ch)
    log.addHandler(fh)

    #~ log.debug('This is a debug message')
    #~ log.info('This is an info message')
    #~ log.warning('This is a warning message')
    #~ log.error('This is an error message')
    #~ log.critical('This is a critical error message')

# Recorre el AST, realiza el análisis semántico
def verificacion(ast):
    # Verificar el tipo del nodo del árbol
    log.debug ('Procesando árbol: \n' + str(ast))
    
    # Definir variables
    r = None
    
    # Revisar cuando es un conjunto de consultas sql
    if type(ast) == SQLQuery:
        log.debug('Se detectó un conjunto de consultas SQL.')
        for nodo in ast:
            verificacion(nodo)
    
    # Verificar cuando es una instrucción de creación de base de datos
    elif type(ast) == DataBaseCreate:
        log.debug('Se detectó una consulta SQL: Crear base de datos.')
        manejador.agregar_base_de_datos(ast[0].lower())
    
    # Verificar cuando se renombra una base de datos
    elif type(ast) == DataBaseAlter:
        log.debug('Se detectó una consulta SQL: Cambiar nombre de base de datos.')
        manejador.renombrar_base_de_datos(ast[0].lower(), ast[1].lower())
        
    # Verificar cuando se borra una base de datos
    elif type(ast) == DataBaseDrop:
        log.debug('Se detectó una consulta SQL: Eliminar base de datos.')
        manejador.eliminar_base_de_datos(ast[0].lower())
        
    # Verificar cuando es mostrar bases de datos
    elif type(ast) == DataBaseShow:
        log.debug('Se detectó una consulta SQL: Mostrar bases de datos.')
        r = manejador.mostrar_bases_de_datos()
    
    # Verificar cuando es utilizar base de datos
    elif type(ast) == DataBase:
        log.debug('Se detectó una consulta SQL: Utilizar base de datos.')
        manejador.utilizar_base_de_datos(ast[0].lower())

    # Devolver el resultado
    return r

# ejecutar: Ejecuta las instrucciones SQL especificadas en 'cadena'. 
# Devuelve el resultado de ejecutar las instrucciones dadas, como texto.
def ejecutar(cadena):
    # Traer variables de modulo
    global parser
    
    # Crear variables
    r = ''
    
    # Análisis de la cadena enviada
    try:
        # Analizar cadena enviada (análisis léxico y sintáctico)
        log.debug('Inicio análisis léxico y sintáctico.')
        ast = parser.parse(cadena)[0]
        log.debug('Fin análisis léxico y sintáctico.')
        
        # Verificar instrucciones (análisis semántico)
        log.debug('Inicio análisis semántico.')
        r = verificacion(ast)
        r = r if r else ''
        log.debug('Fin análisis semántico.')
    except lepl.stream.maxdepth.FullFirstMatchException, msg:
        log.debug('Fin análisis léxico y sintáctico.')
        r = msg
    except DataBaseAlreadyExistException, msg:
        r = msg
        log.debug('Fin análisis semántico.')
    except DataBaseNotExistException, msg:
        r = msg
        log.debug('Fin análisis semántico.')
    
    # Devolver resultado de la ejecución
    return r
    
def ejecutarDesdeArchivo(archivo):
    # Traer variables de modulo
    global parser, log
    
    # Crear variables
    r = ''
    
    # Abrir el archivo enviado y parsearlo (análisis léxico y sintáctico)
    log.debug('Inicio análisis léxico y sintáctico.')
    ast = Node()
    try:
        with open(archivo) as entrada:
            print parser.get_parse_file()
            if parser is lepl.matchers.transform.Transform:
                print "lepl.matchers.transform.Transform"
            #~ print parser.parse_file
            #~ ast = parser.parse_file(entrada)
        ast = parser.parse_file(open(archivo))
    except IOError, msg:
        r = "El archivo '"+archivo+"' no existe o no es un archivo valido."
    except lepl.stream.maxdepth.FullFirstMatchException, msg:
        r = msg
        log.debug('Fin análisis léxico y sintáctico.')
    except DataBaseAlreadyExistException, msg:
        r = msg
    
    # Verificar instrucciones (análisis semántico)
    log.debug('Inicio análisis semántico.')
    verificacion(ast)
    log.debug('Fin análisis semántico.')
    
    # Devolver resultado de la operación
    return r

# Definir variables de modulo
parser = Parser.build()
log = logging.getLogger('byDBMS')
path = "./data/"
manejador = None
