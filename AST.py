# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: viernes, 7 de abril de 2011
# AST.py
# Contiene las clases con las que se genera el arbol sintactico.

from lepl import List, Node 
import logging

# Definicion de SQL
class SQLQuery(Node): pass

# Definicion de clases para manejo de bases de datos

# ----------------------------------
# 1) DDL para bases de datos
# ----------------------------------
# Crear base de datos
class DataBaseCreate(SQLQuery):
    pass

# Modificar base de datos
class DataBaseAlter(SQLQuery):        
    pass

# Clase para eliminar base de datos
class DataBaseDrop(SQLQuery):
    pass
    
# Mostrar bases de datos
class DataBaseShow(SQLQuery):
    pass

# Usar una base de datos
class DataBaseUse(SQLQuery):
    pass
    
# ----------------------------------
# 2) DDL para tablas
# ----------------------------------
# Crear tabla
class TableCreate(SQLQuery):
    pass

# Cambiar el id de una tabla
class TableAlterName(SQLQuery):
    pass
    
# Cambiar estructura de una tabla
class TableAlterStructure(SQLQuery):
    pass

# Borrar una tabla
class TableDrop(SQLQuery):
    pass
    
# Mostar tablas de la base de datos actual
class TableShowAll(SQLQuery):
    pass

# Mostrar columnas de una tabla
class TableShowColumns(SQLQuery):
    pass

# --------------------------------------
# 2.1) Clases para tipos de columnas
# --------------------------------------
# Representa una descripcion de columna
class Columna(Node) : pass
# Representa una descripcion de constraint
class Restriccion(Node) : pass

# --------------------------------------
# 2.2) Clases para expresiones booleanas
# --------------------------------------
# Representa un valor aceptado
class Valor(Node) : pass

# Representa un identificador
class Identificador(Valor): pass

# Representa un INT
class Int(Valor): pass

# Representa un Float
class Float(Valor): pass

# Representa un Char
class Char(Valor) : pass

# Representa NULL
class Null(Valor) : pass

# Representa una expresión de  predicado
class PredExp(Node) : pass

# Representa una expresión negadada
class NotExp(Node) : pass

# Representa una expresión con AND's
class AndExp(Node) : pass

# Una expresión
class Exp(Node): pass

