# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: viernes, 7 de abril de 2011
# console.py
# Contiene a la consola interactiva

# Importar modulos necesarios
import logging
import sys
import byDBMS

# Verificar si se debe activar el modo DEBUG
if len(sys.argv) > 1:
    level_name = sys.argv[1]
    byDBMS.configure(tipo=level_name)
else:
    byDBMS.configure()

# Crear log de la consola
log = logging.getLogger('byDBMS.console')    

# Definir funciones especiales para la consola
# ayuda: Devuelve el mensaje de ayuda que se le muestra al usuario. Contiene las instrucciones acceptadas por 
def ayuda():
    return """
¡Bienvenido a byDBMS 0.1!

Esta es la consola interactiva del manejador de bases de datos byDBMS. La consola interactiva puede ser activada en uno de varios niveles de ejecución, cuando se invoca a la consola (mediante python console.py) se le puede agregar una de las siguientes opciones: 
 *    debug     muestra hasta mensajes internos de depuración.
 * -v info      muestra hasta mensajes internos de información.
 *    warning   muestra hasta mensajes de advertencia (activado por defecto).
 *    error     muestra hasta mensajes de error.
 *    critical  muestra sólo mensajes críticos, causantes de errores de ejecución del gestor.

A continuacion se muestra la lista de instrucciones aceptadas por la consola:
 * leer <archivo> - Abre el archivo especificado en <archivo> e intenta ejecutar los comandos SQL que se encuentren en él.
 * ayuda          - Muestra este mensaje de ayuda.
 * instrucciones  - Muestra el conjunto de instrucciones SQL que son reconocidas por byDBMS.
 * salir          - Abandona byDBMS de forma segura.

Cualquier otro texto ingresado será tratado como un comando SQL (ver 'instrucciones' para ver el conjunto de comandos SQL reconocidos).
"""
    
# instrucciones: Devuelve 
def instrucciones():
    return """
¡Bienvenido a byDBMS 0.1!

A continuacion se muestra la lista de instrucciones SQL aceptadas por byDBMS:
 =====================
 = Para bases de datos
 =====================
 * Crear base de datos
    CREATE DATABASE <idDB> [;]
 * Cambiar nombre de una base de datos
    ALTER DATABASE <idDB> RENAME TO <nuevoIdDB> [;]
 * Eliminar una base datos
    DROP DATABASE <idDB> [;]
 * Mostrar bases de datos
    SHOW DATABASES [;]
 * Seleccionar una base de datos
    USE DATABASE <idDB> [;]
    
 Donde <idDB> y <nuevoIdDB> son identificadores.
 =========================
 = Para tablas (entidades)
 =========================
 * Crear tabla
    CREATE TABLE <idTabla> ( <listaDescColumna> ) [;]
 * Modificar una tabla
    + Renombrar una tabla
        ALTER TABLE <idTabla> RENAME TO <nuevoIdTabla> [;] 
    + Agregar una columna
        ALTER TABLE <idTabla> ADD COLUMN <descColumna> [;] 
    + Agregar una restricción (constraint)
        ALTER TABLE <idTabla> ADD <descConstraint> [;] 
    + Eliminar una columna
        ALTER TABLE <idTabla> DROP COLUMN <idColumna> [;]
    + Eliminar una restricción (constraint)
        ALTER TABLE <idTabla> DROP CONSTRAINT <idConstraint> [;]
 * Eliminar una tabla
    DROP TABLE <idTabla> [;]
 * Obtener informacion de tablas
    + Mostrar tablas existentes
        SHOW TABLES [;]
    + Mostrar columnas de una tabla
        SHOW COLUMNS FROM <idTabla> [;]
        
 Donde 
 * <listaDescColumna> es
      <descColumnaConstraint> <descColumnaConstraintComa>*
        + <descColumnaConstraintComa> es
            , <descColumnaConstraint>
        + <descColumnaConstraint> es
            <descColumna> | <descConstraint>
 * <tipo> es
    INT | FLOAT | DATE | CHAR ( <cantidad> )
        + <cantidad> es un numero entero positivo.
 * <descColumna> es
    <idColumna> <tipo> <constraintCorto>*
 * <constraintCorto> es
    PRIMARY KEY | REFERENCES <idTablaReferencia> ( <idColumnaReferencia> ) | CHECK ( <exp> )
 * <descConstraint> es
    PRIMARY KEY <idConstraint> ( <listaIdent> )
    | FOREIGN KEY <idConstraint> REFERENCES <idTablaReferencia> ( <idColumnaReferencia> ) 
    | CHECK <idConstraint> ( <exp> )
 * <idTabla>, <nuevoIdTabla>, <idColumna>, <idConstraint>, <idTablaReferencia>, <idColumnaReferencia> son identificadores
 * <exp> es una expresión booleana.
 * <listaIdent> es una lista de identificadores seprados por comas.

Por el momento las instrucciones son case sensitive, por lo que deben estar escritas en mayúsculas (de lo contrario no serán instrucciones válidas). 

Cualquier texto ingresado no válido se mostrará un error.
"""

# Crear variable de entrada
entrada = ''

# Mensaje de bienvenida
print """=============================================================== 
 /$$                 /$$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$ 
| $$                | $$__  $$| $$__  $$| $$$    /$$$ /$$__  $$
| $$$$$$$  /$$   /$$| $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \__/
| $$__  $$| $$  | $$| $$  | $$| $$$$$$$ | $$ $$/$$ $$|  $$$$$$ 
| $$  \ $$| $$  | $$| $$  | $$| $$__  $$| $$  $$$| $$ \____  $$
| $$  | $$| $$  | $$| $$  | $$| $$  \ $$| $$\  $ | $$ /$$  \ $$
| $$$$$$$/|  $$$$$$$| $$$$$$$/| $$$$$$$/| $$ \/  | $$|  $$$$$$/
|_______/  \____  $$|_______/ |_______/ |__/     |__/ \______/ 
           /$$  | $$                                           
          |  $$$$$$/                                           
           \______/                                            
===============================================================
Versión 0.1
Escriba 'ayuda' e 'instrucciones' para mayor información.
===============================================================
"""

# Ciclo principal
while entrada.lower() != 'salir':
    # Solicitar nueva entrada
    entrada =  raw_input("byDBMS> ").strip()
    
    # Evaluar entrada ingresada
    if entrada.lower() == 'ayuda':
        print ayuda()
    elif entrada.lower() == 'instrucciones':
        print instrucciones()
    elif entrada.lower() == 'salir':
        print "¡¡¡ Adios !!!"
    elif entrada.lower().startswith('leer '):
        print byDBMS.executeFromFile(entrada[5:].strip())
    else:
        print byDBMS.execute(entrada)
