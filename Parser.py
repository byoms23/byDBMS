
from lepl import *
from AST import *

# Definicion de Tokens admitidos
def txt(text):
    return ~Token(text)

# Definir tokens    
symbol = Token('[^0-9a-zA-Z \t\r\n]')
identi = Token('[a-zA-Z][0-9a-zA-Z]*')

# Partes de SQL

# Definicion de DDL para bases de datos
dataBaseCreate = txt('CREATE') & txt("DATABASE") & identi > DataBaseCreate
dataBaseAlter  = txt('ALTER')  & txt('DATABASE') & identi & txt('RENAME') & txt('TO') & identi > DataBaseAlter
dataBaseDrop = txt('DROP') & txt("DATABASE") & identi > DataBaseDrop
dataBaseShow = txt('SHOW') & txt("DATABASES") > DataBaseShow
dataBaseUse = txt('USE') & txt("DATABASE") & identi > DataBaseUse

# Definicion de DDL para tablas
tableCreate = 
tableAlterName = txt('ALTER')  & txt('TABLE') & identi & txt('RENAME') & txt('TO') & identi > TableAlterName
tableAlterStructure =
tableDrop = txt('DROP') & txt("TABLE") & identi > TableDrop
tableShowAll = txt('SHOW') & txt("TABLES") > TableShowAll
tableShowColumns = txt('SHOW') & txt("COLUMNS") & txt("FROM") & identi > TableShowColumns

# Definir SQL
consultaSql = Star(dataBaseCreate 
                 | dataBaseAlter 
                 | dataBaseDrop 
                 | dataBaseShow 
                 | dataBaseUse 
                 ) > SQLQuery


print identi.parse("hola")
s = consultaSql.parse(
    """CREATE DATABASE cosa 
    ALTER DATABASE cosa RENAME TO nuevacosa1 
    ALTER DATABASE nuevacosa1 RENAME TO nuevacosa2
    DROP DATABASE cosa
    SHOW DATABASES
    USE DATABASE cosa"""
    )[0]
print s

"""
value = Token(UnsignedReal())
symbol = Token('[^0-9a-zA-Z \t\r\n]')
number = Optional(symbol('-')) + value >> float
expr = Delayed()
add = number & symbol('+') & expr > List
sub = number & symbol('-') & expr > List
expr += add | sub | number
print expr.parse('1+2-3 +4-5')

ast = expr.parse('1+2-3 +4-5')[0]

print ast
"""

# Abrir el archivo enviado
#~ with open('myfile') as input:
    #~ return matcher.parse_file(input)
