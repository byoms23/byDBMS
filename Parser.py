
from lepl import *
from AST import *

# Definicion de Tokens admitidos
def txt(text):
    return ~Token(text)

# Definir tokens    
identi = Token('[a-zA-Z][0-9a-zA-Z]*')
number = Token(UnsignedInteger()) >> int
simbolo = Token('[^0-9a-zA-Z \t\r\n]')

# Partes de SQL

# Definicion de DDL para bases de datos
dataBaseCreate = txt('CREATE') & txt("DATABASE") & identi > DataBaseCreate
dataBaseAlter  = txt('ALTER')  & txt('DATABASE') & identi & txt('RENAME') & txt('TO') & identi > DataBaseAlter
dataBaseDrop = txt('DROP') & txt("DATABASE") & identi > DataBaseDrop
dataBaseShow = txt('SHOW') & txt("DATABASES") > DataBaseShow
dataBaseUse = txt('USE') & txt("DATABASE") & identi > DataBaseUse

# Definicion de tokens utilizados en DDL para tablas
listaDescColumna = Delayed()
listaAccion = Delayed()

# Definicion de DDL para tablas
tableCreate = txt('CREATE') & txt("TABLE") & identi & ~simbolo('(') & listaDescColumna & ~simbolo(')') > TableCreate
tableAlterName = txt('ALTER')  & txt('TABLE') & identi & txt('RENAME') & txt('TO') & identi > TableAlterName 
tableAlterStructure = txt('ALTER')  & txt('TABLE') & identi & listaAccion > TableAlterStructure 
tableDrop = txt('DROP') & txt("TABLE") & identi > TableDrop
tableShowAll = txt('SHOW') & txt("TABLES") > TableShowAll
tableShowColumns = txt('SHOW') & txt("COLUMNS") & txt("FROM") & identi > TableShowColumns

# Definicion de expresiones
null = Token("NULL")
s = Token("'[A-Za-z0-9]*'")
value = identi | Token(UnsignedInteger()) | Token(UnsignedReal()) | null | s

negateExp = (simbolo("-") & value) | value > Node

multExpTemp = Delayed()
multExpTemp += ( (simbolo('*') & negateExp & multExpTemp)
               | (simbolo('/') & negateExp & multExpTemp)
               ) [:1] > Node
multExp = negateExp & multExpTemp > Node

addExpTemp = Delayed()
addExpTemp += ( (simbolo('+') & multExp & addExpTemp) 
              | (simbolo('-') & multExp & addExpTemp)
              ) [:1] > Node
addExp = multExp & addExpTemp > Node

predExp = ( (addExp & Token("=")  & addExp) 
          | (addExp & Token("<>") & addExp) 
          | (addExp & Token("!=") & addExp) 
          | (addExp & Token(">")  & addExp) 
          | (addExp & Token(">=") & addExp) 
          | (addExp & Token("<")  & addExp) 
          | (addExp & Token("<=") & addExp) 
          | addExp 
          ) > Node

notExp = (Token("NOT") & predExp) | predExp > Node

andExp = Delayed()
andExp += (notExp & Token("AND") & andExp) | notExp > Node

exp = Delayed()
exp += (andExp & Token("OR") & exp) | andExp > Node

# Pruebas para las expresiones
#~ print null.parse ("NULL")
#~ print s.parse(" 'hola' ")
#~ print value[:].parse(" cosa 44443 343.333 NULL ") #'hola'")
#~ print multExp.parse("-33")[0]
#~ print multExp.parse("-33 / 34")[0]
#~ print multExp.parse("-33 / 34 * 34535 * -345435") [0]
#~ print addExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6 ")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  = 3")[0]
#~ print predExp.parse("c5 > 3")[0]
#~ print predExp.parse("c5 >= 3")[0]
#~ print predExp.parse("c5 < 3")[0]
#~ print predExp.parse("c5 <= 3")[0]
#~ print predExp.parse("c5 > 3")[0]
#~ print predExp.parse("c5 > 3")[0]
#~ print predExp.parse("-33 <> 3")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  != 3")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  < 3")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  <= 3")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  > 3")[0]
#~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  >= 3")[0]
#~ print notExp.parse("NOT 3")[0]
print andExp.parse('NOT True AND 3 > 2 AND 2 <= 2')[0]

# Definicion de columnas para el CREATE
listaIdentificadores = ~simbolo("(") & (identi & (~simbolo(",") & identi)[:,...]) & ~simbolo(")") > Node
tipo = Token('INT') | Token('FLOAT') | Token('DATE') | (Token('CHAR') & ~simbolo('(') & number & ~simbolo(')')) > Node
constraintColumna = ( (Token("PRIMARY") & Token("KEY")) 
                    | (Token("REFERENCES") & identi & ~simbolo("(") & (identi) & ~simbolo(")"))
                    | (Token("CHECK") & ~simbolo("(") & (exp) & ~simbolo(")"))
                    ) > Node
descColumna = identi & tipo & constraintColumna[:] > Node
descConstraint = ( (Token("PRIMARY") & Token("KEY") & identi & listaIdentificadores)
                 | (Token("FOREIGN") & Token("KEY") & identi & listaIdentificadores & Token("REFERENCES") & identi & listaIdentificadores)
                 #| (Token("CHECK") & identi & ~simbolo("(") & (exp) & ~simbolo(")"))
                 ) > Node
listaDescColumna += (descColumna | descConstraint) & (~simbolo(",") & (descColumna | descConstraint))[:] > Node

"""
q = listaDescColumna.parse("c1 INT , c2 INT PRIMARY KEY REFERENCES cosita (id), c3 FLOAT")
q = listaDescColumna.parse("PRIMARY KEY clave (c1, c3), FOREIGN KEY claveForanea (c3, c4, c5, c6) REFERENCES cos2 (id, c3,c4,c6)")

print q
for i in q:
    print i 
"""

# Definicion de acciones para el ALTER
listaAccion += txt("ADD")

# Definir SQL
consultaSql = Star(dataBaseCreate 
                 | dataBaseAlter 
                 | dataBaseDrop 
                 | dataBaseShow 
                 | dataBaseUse 
                 | tableCreate
                 | tableAlterName
                 #| tableAlterStructure
                 | tableDrop
                 | tableShowAll
                 | tableShowColumns
                 ) > SQLQuery


print tipo.parse("INT")
print tipo.parse("CHAR( 34 )")
print identi.parse(" hola ")
s = consultaSql.parse(
    """CREATE DATABASE cosa 
    ALTER DATABASE cosa RENAME TO nuevacosa1 
    ALTER DATABASE nuevacosa1 RENAME TO nuevacosa2
    DROP DATABASE cosa
    SHOW DATABASES
    USE DATABASE cosa
    
    CREATE TABLE cos (
        id DATE PRIMARY KEY
    )
    
    CREATE TABLE cos2 (
        id CHAR (3) PRIMARY KEY
    )
    
    CREATE TABLE cosita (
        c1 INT ,
        c2 FLOAT ,
        c3 DATE REFERENCES cos (id),
        c3 CHAR(3),
        PRIMARY KEY clave (c1, c3),
        FOREIGN KEY claveForanea (c3) REFERENCES cos2 (id), 
        c5 INT CHECK (c5 > 3)
        
    )
    
    ALTER TABLE cosita RENAME  TO nuevacosita
    SHOW TABLES
    SHOW COLUMNS FROM cosita
    DROP TABLE cosita
    
    """)[0]
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
