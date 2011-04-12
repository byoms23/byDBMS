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
