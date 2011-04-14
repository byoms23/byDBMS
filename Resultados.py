# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Resultados.py
# Contiene las clases de resultados que serán mostrados al usuario.

class Resultado():
    
    # Constructor de la clase
    def __init__(self):
        # Crear variables
        self.titulos = []
        self.contenido = [[]]
        print "hola"
    
    # Definición de la forma de cadena del objeto
    def __str__(self):
        # Declarar variables
        r = ''
        
        # Montar el string
        tam = len(self.titulos)
        for x in self.titulos:
            r += x + '\t|\t'
            
        r = '='*len(r) + '\n' + r[:-3] + '\n' + '='*len(r) + '\n'
        
        # Recorrer contenido
        for f in self.contenido:
            for c in f:
                r += c + '\t|\t'
            r = r[:-3] + '\n'
        
        # Devolver valor calculado
        return r
    
    # Modificar los titulos
    def setTitulos(self, titles):
        # Hacer el cambio
        self.titulos = titles
    
    # Obtener los titutlos
    def getTitulos(self):
        # Devolver los títulos
        return self.titutlos
    
    # Modificar el contenido
    def setContenido(self, newContent):
        # Hacer el cambio
        self.contenido = newContent
        
    # Obtener el contenido
    def getContenido(self):
        # Devolver el contenido
        return self.contenido

#~ x = Resultado()
#~ x.setTitulos(["Titulo1", "Titulo 2"])
#~ x.setContenido([["Contenido 1", "Contenido 2"], ["Contenido 3", "Contenido 4"], ["Contenido 5", "Contenido 6"]])
#~ print x
