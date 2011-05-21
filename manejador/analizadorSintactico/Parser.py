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

    # Definiciones de SQL

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
    listaIdentificadores = ~simbolo("(") & (identi & (~simbolo(",") & identi)[:]) & ~simbolo(")") > Node
    tipo = (Token('INT') 
           | Token('FLOAT') 
           | Token('DATE') 
           | (Token('CHAR') & ~simbolo('(') & number & ~simbolo(')'))
           ) > Node
    constraintColumna = ( (Token("PRIMARY") & txt("KEY")) 
                        | (Token("REFERENCES") & identi & ~simbolo("(") & (identi) & ~simbolo(")"))
                        | (Token("CHECK") & ~simbolo("(") & (exp) & ~simbolo(")"))
                        ) > Node
    listConstraintColumna = constraintColumna[:] > Node 
    descColumna = identi & tipo & listConstraintColumna > Columna
    descConstraint = ( (Token("PRIMARY") & txt("KEY") & identi & listaIdentificadores)
                     | (Token("FOREIGN") & txt("KEY") & identi & listaIdentificadores & txt("REFERENCES") & identi & listaIdentificadores)
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
    
    # TODO Definición para INSERT 
    integer = Token(Integer()) > Int
    real = Token(Real()) > Float
    null = Token("NULL") > Null
    date = ~simbolo("'") & Token("[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]") & ~simbolo("'") > Fecha
    #~ s = Lookahead("'[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]'") & Token("'[^']*'") > Char
    s = Token("'[^0-9][^']*'") > Char
    default = Token("DEFAULT") > Default
    
    valor = integer | real | null | default | date | s 
    valores = ~simbolo('(') & (valor & (~simbolo(',') & valor)[:]) & ~simbolo(')') > Node
    
    listaValores = valores & (~simbolo(',') & valores)[:] > Node
    rowInsert = txt("INSERT") & txt("INTO ") & identi & listaIdentificadores[:1] & txt("VALUES") & listaValores > RowInsert
    
    # TODO Definición para UPDATE 
    cambio = identi & txt('=') & valor > Node
    listaCambios = cambio & ((~simbolo(",") & cambio)[:]) > Node
    rowUpdate = txt("UPDATE") & identi & txt('SET') & listaCambios & (txt('WHERE') & exp)[:1] > RowUpdate
    
    # TODO Definición para DELETE 
    rowDelete = txt("DELETE") & txt("FROM") & identi & (txt('WHERE') & exp)[:1] > RowDelete
    
    # TODO Definicion para SELECT 
    rowSelect = txt("SELECT") & simbolo("*") & txt("FROM") & identi & (Token("WHERE") & exp)[:1] & (Token('ORDER') & txt('BY') & exp & (Token("ASC") | Token("DESC"))[:1] )[:1] > RowSelect
    
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
                        | rowInsert
                        | rowUpdate
                        | rowDelete
                        | rowSelect
                        ) & ~(simbolo(';')[:]) ) > SQLQuery
    
    return consultaSql

#~ b = build()
#~ print b.parse("UPDATE bla SET kill = 5.1;")[0]
#~ print b.parse("""
#~ INSERT INTO bla VALUES (1, 2.0, NULL, '2012-12-13')
#~ INSERT INTO bla (kill, bla, kick, kiki, kak) VALUES (1, 2.0, 'BLA', NULL, '2012-12-04')
#~ UPDATE bla SET kill = 5.1;
#~ UPDATE bla SET kill = 6.1 WHERE bla = 3;
#~ UPDATE bla SET kill = 5.1, kick = 3
#~ UPDATE bla SET kill = 6.1, kick = 6 WHERE bla = 3
#~ DELETE FROM BLA WHERE kick = 2
#~ DELETE FROM bla
#~ SELECT * FROM BLA
#~ SELECT * FROM BLA WHERE KICK = 2
#~ SELECT * FROM BLA ORDER BY kick ASC
#~ SELECT * FROM BLA ORDER BY kick DESC
#~ SELECT * FROM BLA WHERE KICK = 2 ORDER BY kick ASC
#~ """)[0]
#~ print b.parse("INSERT INTO bla VALUES (1, 2.0, 'BLA', NULL, '2012-12-04'),(1, 2.0, 'BLAesdg', NULL, '2012-12-04')")[0]
