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


