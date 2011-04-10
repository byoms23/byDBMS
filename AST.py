
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

# ----------------------------------
# 2.1) DDL para tablas
# ----------------------------------


"""
class Add(List): pass
...
>>> class Sub(List): pass
...
>>> class Mul(List): pass
...
>>> class Div(List): pass
...

>>> # tokens
>>> value = Token(UnsignedReal())
>>> symbol = Token('[^0-9a-zA-Z \t\r\n]')

>>> number = Optional(symbol('-')) + value >> float
>>> group2, group3 = Delayed(), Delayed()

>>> # first layer, most tightly grouped, is parens and numbers
... parens = ~symbol('(') & group3 & ~symbol(')')
>>> group1 = parens | number

>>> # second layer, next most tightly grouped, is multiplication
... mul = group1 & ~symbol('*') & group2 > Mul
>>> div = group1 & ~symbol('/') & group2 > Div
>>> group2 += mul | div | group1

>>> # third layer, least tightly grouped, is addition
... add = group2 & ~symbol('+') & group3 > Add
>>> sub = group2 & ~symbol('-') & group3 > Sub
>>> group3 += add | sub | group2

>>> ast = group3.parse('1+2*(3-4)+5/6+7')[0]
"""


