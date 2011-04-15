# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: viernes, 7 de abril de 2011
# Parser.py
# Contiene la definicion del parser que reconoce la gramatica de sql.

# Crear utilitarios, importar modulos
from lepl import *
from AST import *

# Definicion de Tokens admitidos que son omitidos
# text: Conjunto de caracteres que serán reconocidos.
def txt(text):
    return ~Token(text)

# ----------------------------------------------------------------------
# Construye el analizador sintactico.
# ----------------------------------------------------------------------

# Devuelve el analizador sintáctico para expresiones booleanas admitidas
def buildExp():
    # Definir tokens    
    identi = Token('[a-zA-Z][0-9a-zA-Z]*') > Identificador
    integer = Token(Integer()) > Int
    real = Token(Real()) > Float
    null = Token("NULL") > Null
    s = Token("'[A-Za-z0-9]*'") > Char
    
    # Definicion de expresiones aceptadas
    value = ( identi
            | integer
            | real
            | null 
            | s )
    
    predExp = ( (value & Token("=")  & value) 
              | (value & Token("<>") & value) 
              | (value & Token("!=") & value) 
              | (value & Token(">")  & value) 
              | (value & Token(">=") & value) 
              | (value & Token("<")  & value) 
              | (value & Token("<=") & value) 
              | value 
              ) > PredExp

    notExp = (Token("NOT") & predExp) | predExp > NotExp

    andExp = Delayed()
    andExp += (notExp & Token("AND") & andExp) | notExp > AndExp

    exp = Delayed()
    exp += (andExp & Token("OR") & exp) | andExp > Exp
    
    return exp


# Devuelve el analizar sintactico para SQL.
def build():
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

    # Definición de expresiones
    exp = buildExp()
    
    # Definición de columnas para el CREATE
    listaIdentificadores = ~simbolo("(") & (identi & (~simbolo(",") & identi)[:,...]) & ~simbolo(")") > Node
    tipo = (Token('INT') 
           | Token('FLOAT') 
           | Token('DATE') 
           | (Token('CHAR') & ~simbolo('(') & number & ~simbolo(')'))
           ) > Node
    constraintColumna = ( (Token("PRIMARY") & Token("KEY")) 
                        | (Token("REFERENCES") & identi & ~simbolo("(") & (identi) & ~simbolo(")"))
                        | (Token("CHECK") & ~simbolo("(") & (exp) & ~simbolo(")"))
                        ) > Node
    listConstraintColumna = constraintColumna[:] > Node 
    descColumna = identi & tipo & listConstraintColumna > Columna
    descConstraint = ( (Token("PRIMARY") & Token("KEY") & identi & listaIdentificadores)
                     | (Token("FOREIGN") & Token("KEY") & identi & listaIdentificadores & Token("REFERENCES") & identi & listaIdentificadores)
                     | (Token("CHECK") & identi & ~simbolo("(") & (exp) & ~simbolo(")"))
                     ) > Restriccion
    listaDescColumna += (descColumna | descConstraint) & (~simbolo(",") & (descColumna | descConstraint))[:] > Node

    # Definicion de acciones para el ALTER
    accion = ( (Token("ADD") & Token("COLUMN") & descColumna)
             | (Token("ADD") & descConstraint)
             | (Token("DROP") & Token("COLUMN") & identi)
             | (Token('DROP') & Token("CONSTRAINT") & identi )
             ) > Node
    listaAccion += accion & (~txt(',') & accion)[:] > Node

    # Definir SQL
    consultaSql = Star( (dataBaseCreate 
                        | dataBaseAlter 
                        | dataBaseDrop 
                        | dataBaseShow 
                        | dataBaseUse 
                        | tableCreate
                        | tableAlterName
                        | tableAlterStructure
                        | tableDrop
                        | tableShowAll
                        | tableShowColumns
                        ) & ~(simbolo(';')[:]) ) > SQLQuery
    
    return consultaSql


    # Pruebas para las expresiones
    #~ print null.parse ("NULL")
    #~ print s.parse(" 'hola' ")
    #~ print value[:].parse(" cosa 44443 343.333 NULL ") #'hola'")
    #~ print multExp.parse("-33")[0]
    #~ print multExp.parse("-33 / 34")[0]
    #~ print multExp.parse("-33 / 34 * 34535 * -345435") [0]
    #~ print addExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6 ")[0]
    #~ print predExp.parse("3 = 3")[0]
    #~ print predExp.parse("c5 != 3")[0]
    #~ print predExp.parse("-33 <> 3")[0]
    #~ print predExp.parse("c5 > 3")[0]
    #~ print predExp.parse("c5 >= 3")[0]
    #~ print predExp.parse("c5 < 3")[0]
    #~ print predExp.parse("c5 <= 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  = 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  != 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  < 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  <= 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  > 3")[0]
    #~ print predExp.parse("-33 / 34 * 34535 * -345435 + 344 * 4 - 5 / 6  >= 3")[0]
    #~ print notExp.parse("NOT 3")[0]
    #~ print andExp.parse('NOT True AND 3 > 2 AND 2 <= 2')[0]
    #~ print exp.parse('NOT True AND 3 > 2 AND 2 <= 2 OR False')[0]
    #~ 
    #~ q = listaDescColumna.parse("c1 INT , c2 INT PRIMARY KEY REFERENCES cosita (id), c3 FLOAT")
    #~ q = listaDescColumna.parse("PRIMARY KEY clave (c1, c3), FOREIGN KEY claveForanea (c3, c4, c5, c6) REFERENCES cos2 (id, c3,c4,c6)")
    #~ print q
    #~ for i in q:
        #~ print i 
    #~ 
    #~ print tipo.parse("INT")
    #~ print tipo.parse("CHAR( 34 )")
    #~ print identi.parse(" hola ")
    #~ 
    #~ s = consultaSql.parse(
        #~ """
        #~ CREATE DATABASE cosa 
        #~ ALTER DATABASE cosa RENAME TO nuevacosa1 
        #~ ALTER DATABASE nuevacosa1 RENAME TO nuevacosa2
        #~ DROP DATABASE cosa
        #~ SHOW DATABASES
        #~ USE DATABASE cosa
        #~ 
        #~ CREATE TABLE cos (
            #~ id DATE PRIMARY KEY
        #~ )
        #~ 
        #~ CREATE TABLE cos2 (
            #~ id CHAR (3) PRIMARY KEY
        #~ )
        #~ 
        #~ CREATE TABLE cos3 (
            #~ id INT PRIMARY KEY
        #~ )
        #~ 
        #~ CREATE TABLE cosita (
            #~ c1 INT ,
            #~ c2 FLOAT ,
            #~ c3 DATE REFERENCES cos (id),
            #~ c3 CHAR(3),
            #~ PRIMARY KEY clave (c1, c3),
            #~ FOREIGN KEY claveForanea (c3) REFERENCES cos2 (id), 
            #~ c5 INT CHECK (c5 > 3),
            #~ CHECK cosaGrande (c5 > 4343433)
        #~ );
        #~ 
        #~ ALTER TABLE cosita RENAME  TO nuevacosita
        #~ 
        #~ ALTER TABLE cosita ADD COLUMN df INT
        #~ ALTER TABLE cosita ADD COLUMN df1 INT PRIMARY KEY
        #~ ALTER TABLE cosita ADD COLUMN df2 INT REFERENCES cos2 (id)
        #~ ALTER TABLE cosita ADD COLUMN df3 INT CHECK ( df3 > 3)
        #~ ALTER TABLE cosita ADD COLUMN df4 INT PRIMARY KEY REFERENCES cos2 (id) CHECK ( df3 > 3)
        #~ 
        #~ ALTER TABLE cosita ADD PRIMARY KEY key1 (c1)
        #~ ALTER TABLE cosita ADD FOREIGN KEY claveForanea (c40) REFERENCES cos2 (id)
        #~ ALTER TABLE cosita ADD CHECK cosaMuyGrande (c4 > 433 AND c3 > 3)
    #~ 
        #~ ALTER TABLE cosita DROP COLUMN c025
        #~ ALTER TABLE cosita DROP CONSTRAINT cosaMuyGrande
    #~ 
        #~ ALTER TABLE cosita ADD COLUMN df4 INT PRIMARY KEY REFERENCES cos2 (id) CHECK ( df3 > 3), ADD PRIMARY KEY key1 (c1), ADD FOREIGN KEY claveForanea (c40) REFERENCES cos2 (id), ADD CHECK cosaMuyGrande (c4 > 433 AND c3 > 3), DROP COLUMN c025, DROP CONSTRAINT cosaMuyGrande
    #~ 
        #~ SHOW TABLES
        #~ SHOW COLUMNS FROM cosita
        #~ 
        #~ DROP TABLE cosita
        #~ """)[0]
    #~ print s 

