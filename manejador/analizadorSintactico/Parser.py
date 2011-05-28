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
    return Drop(text)

# ----------------------------------------------------------------------
# Construye el analizador sintactico.
# ----------------------------------------------------------------------

# Devuelve árbol sintáctico para leer registros
def buildRegistro(separador = '|'):
    def get_None(arg):
        return None
    def get_str(arg):
        return '' if len(arg) == 0 else arg[0]
    dateQuote = Drop("'")
    separator = Drop("-")
    entero = Integer() >> int
    real = Real() >> float
    null = Apply('NULL', get_None)
    fecha = dateQuote & Integer() & separator & Integer() & separator & Integer() & dateQuote > (lambda x : ("-".join(x)))
    texto = Apply(String(quote="'"), get_str)
    
    valor = entero | real | fecha | null | texto
    valores = (valor & (~Literal(separador) & valor)[:] & ~Literal('\n')[:])[:] > List
    return valores

# Devuelve el analizador sintáctico para expresiones booleanas admitidas
def buildExp():
    # Definir tokens    
    dateQuote = Drop("'")
    separator = Drop("-")
    punto = Drop('.')
    ident  = Word(Letter() | '_',
                  Letter() | '_' | Digit())         
    identi = ident                                  > Identificador
    integer = Integer()                             > Int
    real = Real()                                   > Float
    null = Literal("NULL")                          > Null
    s = String(quote="'")                           > Char
    
    # Definicion de expresiones aceptadas
    spaces = ~Regexp('[\s\t\n\r]')[:]
    with DroppedSpace(spaces):
        fecha = dateQuote & Integer() & separator & Integer() & separator & Integer() & dateQuote > (lambda x : Fecha("'" + "-".join(x) + "'"))
        identiCompleto = ident & punto & ident    > IdentificadorCompleto
        value = ( 
                  identiCompleto 
                | identi
                | integer
                | real
                | null 
                | fecha
                | s 
                )
        
        predExp = ( (value & ("=")  & value) 
                  | (value & ("<>") & value) 
                  | (value & ("!=") & value) 
                  | (value & (">")  & value) 
                  | (value & (">=") & value) 
                  | (value & ("<")  & value) 
                  | (value & ("<=") & value) 
                  | value 
                  ) > PredExp
        
        notExp = (("NOT") & predExp) | predExp > NotExp

        andExp = Delayed()
        andExp += (notExp & ("AND") & andExp) | notExp > AndExp

        exp = Delayed()
        exp += (andExp & ("OR") & exp) | andExp > Exp
    
    #~ exp = spaces & exp & spaces
    return exp

# Devuelve el analizar sintactico para SQL.
def build():
    # Definir tokens    
    identi = Word(Letter() | '_',
                  Letter() | '_' | Digit())
    number = UnsignedInteger() >> int
    simbolo = lambda x : Literal(x)
    dateQuote = Drop("'")
    separator = Drop("-")

    # Definiciones de SQL
    spaces = ~Regexp('[\s\t\n\r]')[:]
    with DroppedSpace(spaces):
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
        tipo = ( Literal('INT') 
               | Literal('FLOAT') 
               | Literal('DATE') 
               | (Literal('CHAR') & ~simbolo('(') & number & ~simbolo(')'))
               ) > Node
        constraintColumna = ( (Literal("PRIMARY") & txt("KEY")) 
                            | (Literal("REFERENCES") & identi & ~simbolo("(") & (identi) & ~simbolo(")"))
                            | (Literal("CHECK") & ~simbolo("(") & (exp) & ~simbolo(")"))
                            ) > Node
        listConstraintColumna = constraintColumna[:] > Node 
        descColumna = identi & tipo & listConstraintColumna > Columna
        descConstraint = ( (Literal("PRIMARY") & txt("KEY") & identi & listaIdentificadores)
                         | (Literal("FOREIGN") & txt("KEY") & identi & listaIdentificadores & txt("REFERENCES") & identi & listaIdentificadores)
                         | (Literal("CHECK") & identi & ~simbolo("(") & (exp) & ~simbolo(")"))
                         ) > Restriccion
        listaDescColumna += (descColumna | descConstraint) & (~simbolo(",") & (descColumna | descConstraint))[:] > Node

        # Definicion de acciones para el ALTER
        accion = ( (Literal("ADD") & Literal("COLUMN") & descColumna)
                 | (Literal("ADD") & descConstraint)
                 | (Literal("DROP") & Literal("COLUMN") & identi)
                 | (Literal('DROP') & Literal("CONSTRAINT") & identi )
                 ) > Node
        listaAccion += accion & (~txt(',') & accion)[:] > Node
        
        # TODO Definición para INSERT 
        integer = Integer() > Int
        real = Real() > Float
        null = Literal("NULL") > Null
        date = dateQuote & Integer() & separator & Integer() & separator & Integer() & dateQuote > (lambda x : Fecha("'" + "-".join(x) + "'"))
        s = String(quote="'") > Char
        default = Literal("DEFAULT") > Default
        
        valor = integer | real | null | default | date | s 
        valores = ~simbolo('(') & (valor & (~simbolo(',') & valor)[:]) & ~simbolo(')') > Node
        
        listaValores = valores & ( ~simbolo(',') & valores )[:] > Node
        rowInsert = txt("INSERT") & txt("INTO") & identi & listaIdentificadores[:1] & txt("VALUES") & listaValores > RowInsert
        
        # TODO Definición para UPDATE 
        cambio = identi & txt('=') & valor > Node
        listaCambios = cambio & ((~simbolo(",") & cambio)[:]) > Node
        rowUpdate = txt("UPDATE") & identi & txt('SET') & listaCambios & (txt('WHERE') & exp)[:1] > RowUpdate
        
        # TODO Definición para DELETE 
        rowDelete = txt("DELETE") & txt("FROM") & identi & (txt('WHERE') & exp)[:1] > RowDelete
        
        # TODO Definicion para SELECT 
        identiCompleto = identi & Drop(".") & identi    > IdentificadorCompleto
        identificador = identi | identiCompleto
        identificadores = identificador [:, ~simbolo(',')]
        columnas = simbolo("*") | identificadores > Node
        listaIdenti = identi & (~simbolo(',') & identi)[:] > Node
        where = Literal('WHERE') & exp > Node
        ordenador = exp & (Literal("ASC") | Literal("DESC"))[:1] > Node
        listaOrdenador = ordenador & (~simbolo(',') & ordenador)[:] > Node
        order = (Literal('ORDER') & txt('BY') & listaOrdenador) > Node
        rowSelect = txt("SELECT") & columnas & txt("FROM") & listaIdenti & where[:1] & order[:1] > RowSelect
        
        #~ print where.parse('WHERE  c.s = 1')[0]
        #~ print order.parse('ORDER BY NULL')[0]
        #~ print rowSelect.parse("SELECT    *    FROM    TABLA0")[0]
        
        # Definir SQL
        consultaSql = ~Space('[\s\t\n\r]')[:] & Star(  
                            ( dataBaseCreate 
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
                            ) & ~(simbolo(';')[:] & ~Space('[\s\t\n\r]')[:]) ) & Eos() > SQLQuery
        
    return consultaSql

#~ with DroppedSpace():
    #~ a = buildExp() & Eos()
    #~ print a.parse("identi . bla < 10 AND 3 = 'cosa'OR ident < 3 OR '1456 -     65-45' < 3.0  ")[0]
#~ 
#~ b = build()
#~ print b.parse("UPDATE bla SET kill = 5.1;")[0]
#~ print b.parse("""
#~ INSERT INTO bla VALUES (1, 2.0, NULL, '2012-12-13')
#~ INSERT INTO bla (kill, bla, kick, kiki, kak) VALUES (1, 2.0, '2012-12-04', 'BLA', NULL, '9')
#~ UPDATE bla SET kill = 5.1;
#~ 
#~ 
#~ UPDATE bla SET kill = 6.1 WHERE bla = 3;
#~ UPDATE bla SET kill = 5.1, kick = 3
#~ UPDATE bla SET kill = 6.1, kick = 6 WHERE bla = 3
#~ DELETE FROM BLA WHERE kick = 2
#~ DELETE FROM bla
#~ SELECT * FROM BLA
#~ SELECT * FROM BLA WHERE KICK = 2
#~ SELECT * FROM BLA ORDER BY kick ASC
#~ SELECT * FROM BLA ORDER BY kick DESC
#~ SELECT * FROM BLA WHERE KICK = 2 ORDER BY bla.kick ASC
#~ """)[0]
#~ print b.parse("INSERT INTO bla VALUES (1, 2.0, 'BLA', NULL, '2012-12-04'),(1, 2.0, 'BLAesdg', NULL, '2012-12-04')")[0]
#~ c = buildRegistro()
#~ print c.parse("0|.1|NULL|'1234-43-22'|'0HOLA'\n")[0]
