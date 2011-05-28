# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: viernes, 7 de abril de 2011
# console.py
# Contiene a la consola interactiva

# Importar modulos necesarios
import logging, sys, cmd 
import byDBMS

# Función que pregunta al usuario si desea eliminar la base de datos

# Crear clase para la consola interactiva
class Console(cmd.Cmd, object):

    # Crear log de la consola.
    log = logging.getLogger('byDBMS.console')
    prompt = 'byDBMS> '
    
    def do_ayuda(self, line):
        """
        Sintaxis: ayuda
        Devuelve el mensaje de ayuda que se le muestra al usuario. Contiene las instrucciones acceptadas por la consola.
        """
        print """¡Bienvenido a byDBMS 0.1!

Esta es la consola interactiva del manejador de bases de datos byDBMS. La consola interactiva puede ser activada en uno de varios niveles de ejecución, cuando se invoca a la consola (mediante python console.py) se le puede agregar una de las siguientes opciones: 
 *    debug     muestra hasta mensajes internos de depuración.
 * -v info      muestra hasta mensajes internos de información.
 *    warning   muestra hasta mensajes de advertencia (activado por defecto).
 *    error     muestra hasta mensajes de error.
 *    critical  muestra sólo mensajes críticos, causantes de errores de ejecución del gestor.
Sin importar el nivel de ejecución activo, el gestor guarda toda la información hasta el nivel de depuración en un archivo de log (especificado en el archivo de configuración, ver abajo). 

Para el correcto funcionamiento del gestor se utiliza un archivo de configuración (byDBMS.conf), contiene la información necesaria para la configuración inicial del gestor. El archivo de configuración debe contener las siguientes variables:
 * path     Contiene el path donde se encuentra el punto inicial de las bases de datos, la carpeta donde se encuentra el archivo maestro de metadata de las bases de datos y las mismas bases de datos que utilizará el gestor.
 * logFile  Indica el path al archivo en el cual se desea que se guarde el log generado por el gestor.

A continuacion se muestra la lista de instrucciones aceptadas por la consola:
 * cargar <archivo> - Abre el archivo especificado en <archivo> e intenta ejecutar los comandos SQL que se encuentren en él.
 * ayuda            - Muestra este mensaje de ayuda.
 * instrucciones    - Muestra el conjunto de instrucciones SQL que son reconocidas por byDBMS.
 * salir            - Abandona byDBMS de forma segura.

Cualquier otro texto ingresado será tratado como un comando SQL (ver 'instrucciones' para ver el conjunto de comandos SQL reconocidos).
"""
    
    # instrucciones: 
    def do_instrucciones(self, line):
        """
        Sintaxis: instrucciones
        Muestra el conjunto de instrucciones SQL que son reconocidas por byDBMS.
        """
        print """¡Bienvenido a byDBMS 0.1!

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

Por el momento las instrucciones son case sensitive, por lo que deben estar escritas en mayúsculas (de lo contrario no serán instrucciones válidas). Tampoco se cuenta para soporte para comentarios, por lo que los archivos que sean cargados no deben tener comentarios en ellos.

Cualquier texto ingresado no válido se mostrará un error.
"""
    
    def do_salir(self, line):
        """
        Sintaxis: salir
        Abandona byDBMS de forma segura.
        """
        print 
        print "¡¡¡ Adios !!!"
        print 
        return True
    
    do_EOF = do_salir
    
    def do_cargar(self, line):
        """
        Sintaxis: cargar <archivo>
        Abre el archivo especificado en <archivo> e intenta ejecutar los comandos SQL que se encuentren en él.
        """
        print byDBMS.ejecutarDesdeArchivo(line)
    
    def default(self, line):
        print byDBMS.ejecutar(line)
    
    def emptyline(self):
        pass
        
# Revisar si el modulo se importado o se ha ejecutado directamente
if __name__ == '__main__':
    # Verificar si se debe activar el modo DEBUG
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        byDBMS.configure(tipo=level_name)
    else:
        byDBMS.configure()
        
    
    # Mensaje de bienvenida
    men = """=============================================================== 
 /$$                 /$$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$ 
| $$                | $$__  $$| $$__  $$| $$$    /$$$ /$$__  $$
| $$$$$$$  /$$   /$$| $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \__/
| $$__  $$| $$  | $$| $$  | $$| $$$$$$$ | $$ $$/$$ $$|  $$$$$$ 
| $$  \ $$| $$  | $$| $$  | $$| $$__  $$| $$  $$$| $$ \____  $$
| $$  | $$| $$  | $$| $$  | $$| $$  \ $$| $$\  e$ | $$ /$$  \ $$
| $$$$$$$/|  $$$$$$$| $$$$$$$/| $$$$$$$/| $$ \/  | $$|  $$$$$$/
|_______/  \____  $$|_______/ |_______/ |__/     |__/ \______/ 
           /$$  | $$                                           
          |  $$$$$$/                                           
           \______/                                            
===============================================================
Versión 0.2
Escriba 'ayuda' e 'instrucciones' para mayor información.
===============================================================
"""
    
    # Crear nueva consola
    c = Console()
    c.cmdloop(men)
    
