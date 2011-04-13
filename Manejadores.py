# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Menajadores.py
# Contine la información de los manejadores (tablas de símbolos) para las bases de datos y para las tablas.

# Clase que maneja la información de la base de datos
class Manejador():
    
    def __init__(self, filename=None):
        pass # TODO
    
    def load(self):
        pass # TODO
        
    # Guarda la configuración actual de la base en el archivo designado para este manejador
    def save(self):
        pass # TODO

class ManejadorBaseDatos(Manejador):
    
    def __init__(self):
        # Declarar variables de datos
        filename='bd.schema'
        pass # TODO
    
        
# Contador de manejadores
ContadorManejador = 0

# Pruebas
