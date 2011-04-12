# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: domingo, 10 de abril de 2011
# byDBMS.py
# Contiene el core del manejador de datos

# Importar modulos
import logging
import sys, os
import Parser

# Carga la configuracion inicial del modulo
def configure(tipo="info"):
    # Variables del modulo
    global path, log
    
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
        else:
            log.warning("El path especificado no existe, se ha creado el nuevo directorio.")
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
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s \n%(levelname)s - %(message)s")
    formatter2 = logging.Formatter("\n%(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter2)
    # add the handlers to logger
    log.addHandler(ch)
    log.addHandler(fh)

    #~ log.debug('This is a debug message')
    #~ log.info('This is an info message')
    #~ log.warning('This is a warning message')
    #~ log.error('This is an error message')
    #~ log.critical('This is a critical error message')

def execute(string):
    pass
    
def executeFromFile(file):
    pass

# Definir variables de modulo
parser = Parser.build()
log = logging.getLogger('byDBMS')
path = "./"
dbActual = None
