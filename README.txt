Universidad del Valle de Guatemala
CC3010 Administracion de la informacion (Seccion 10)
Byron Orlando Morales Sequen (08414)
README.txt

======
byDBMS
======

byDBMS es un sistema administrados de bases de datos. Reconoce una gramática pseudo-SQL similar a la que reconoce Post-Gree.

--------------
Requerimientos
--------------

* Python >= 2.6
  - byDBMS fue desarrollado sobre Python 2.6.
  - Descarga:
  - Instrucciones de instalación: 

* LEPL >= 5.0
  - byDBMS utiliza LEPL para el analisis sintactico de las consultas realizadas. 
  - Descarga:
  - Instrucciones de instalación: 
  
  NOTA: La version de Sakai no necesita instalarlo.
  
-----------------
¿Como utilizarlo?
-----------------

¿Cómo obtenerlo?
El código fuente se puede encontrar en el repositorio oficial del proyecto https://github.com/byoms23/byDBMS . 

¿Cómo inicio?
Lo unico que se tiene que hacer para correr el programa es iniciar el archivo de console.py (descrito abajo), cuando se cumple con los requerimientos. 

----------
console.py
----------

Contiene la consola interactiva necesaria para interactuar con el manejador de base de datos.

La consola interactiva puede ser activada en uno de varios niveles de ejecución, cuando se invoca a la consola (mediante python console.py) se le puede agregar una de las siguientes opciones: 
 *    debug     muestra hasta mensajes internos de depuración.
 * -v info      muestra hasta mensajes internos de información.
 *    warning   muestra hasta mensajes de advertencia (activado por defecto).
 *    error     muestra hasta mensajes de error.
 *    critical  muestra sólo mensajes críticos, causantes de errores de ejecución del gestor.
Sin importar el nivel de ejecución activo, el gestor guarda toda la información hasta el nivel de depuración en un archivo de log (especificado en el archivo de configuración, ver abajo). 
  
Para información sobre los comandos que se pueden utilizar dentro de la consola interactiva, utilice el comando 'ayuda' dentro de ella. Para conocer la sintaxis de SQL reconocida por el gestor introduzca 'instrucciones' dentro de la consola interactiva.

------------------------
Archivo de configuración
------------------------

Para el correcto funcionamiento del gestor se utiliza un archivo de configuración (byDBMS.conf), contiene la información necesaria para la configuración inicial del gestor. El archivo de configuración debe contener las siguientes variables:
 * path     Contiene el path donde se encuentra el punto inicial de las bases de datos, la carpeta donde se encuentra el archivo maestro de metadata de las bases de datos y las mismas bases de datos que utilizará el gestor.
 * logFile  Indica el path al archivo en el cual se desea que se guarde el log generado por el gestor.
