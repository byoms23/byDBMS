# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de creacion: miércoles, 13 de abril de 2011
# Excepciones.py
# Contiene las clases de excepciones utilzados en el proyecto.

# ====================================================
# Excepciones semanticas
# ====================================================
# Clase base para las excepciones semanticas
class SemanticException(Exception): pass

# ====================================================
# Excepciones para bases de datos
# ====================================================
# Clase base para las excepciones de la base de datos
class DataBaseException(SemanticException):
    # Constructor
    def __init__(self, db):
        # Guardar parámetros
        self.db = db

# Contiene excepción para represantar ausencia de base de datos
class DataBaseNotExistException(DataBaseException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "Base de datos '"+self.db+"' no existe."

# Excepción de base de datos existente
class DataBaseAlreadyExistException(DataBaseException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "Base de datos '"+self.db+"' ya existe."

# Excepción de base de datos existente
class DataBaseNotSelectedException(SemanticException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "No hay base de datos en uso."

# ====================================================
# Excepciones para tablas
# ====================================================
# Contiene excepción general para un error en la tabla
class TableException(SemanticException):
    # Contructor
    def __init__(self, tabla, db):
        self.tabla = tabla
        self.db = db

# Contiene excepción para represantar ausencia de tabla
class TableNotExistException(TableException): 
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La tabla '"+self.tabla+"' no existe en la base de datos '"+self.db.getNombre()+"'."

# Excepción de base de datos existente
class TableAlreadyExistException(TableException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La tabla '"+self.tabla+"' ya existe en la base de datos '"+self.db.getNombre()+"'."

# ====================================================
# Excepciones para columnas
# ====================================================
# Contiene excepción general para un error en la tabla
class ColumnException(SemanticException):
    # Contructor
    def __init__(self, columna, tabla):
        self.columna = columna
        self.tabla = tabla
        
# Excepción de base de datos existente
class ColumnAlreadyExistException(ColumnException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La columna '"+self.columna+"' ya existe en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Excepción de base de datos existente
class ColumnNotExistException(ColumnException):
    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La columna '"+self.columna+"' no existe en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# ====================================================
# Excepciones para restricciones
# ====================================================
# Contiene excepción para llave primaria existente
class PrimaryKeyAlreadyException(SemanticException):
    # Contructor
    def __init__(self, tabla):
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "Ya existe una clave primaria en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para nombre de la restricción
class ConstraintNameAlreadyException(SemanticException):
    # Contructor
    def __init__(self, nombre, tabla):
        self.nombre = nombre
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La restricción '"+self.nombre+"' ya existe en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para nombre de la restricción
class ConstraintNotExistsException(SemanticException):
    # Contructor
    def __init__(self, nombre, tabla):
        self.nombre = nombre
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La restricción '"+self.nombre+"' no existe en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para nombre de la restricción
class ColumnTypeNotMatchException(SemanticException):
    # Contructor
    def __init__(self, nombre, tipo, tabla, nombreForanea, tipoForanea, tablaForanea):
        self.nombre = nombre
        self.tipo = tipo
        self.tabla = tabla
        self.nombreForanea = nombreForanea
        self.tipoForanea = tipoForanea
        self.tablaForanea = tablaForanea

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "No se puede crear llave foranea, el atributo '"+self.nombre+"' de tipo '"+self.tipo+"' de la tabla '"+self.tabla.getNombre()+"' no concuerda con el atributo '"+self.nombreForanea+"' de tipo '"+self.tipoForanea+"' de la tabla '"+self.tablaForanea.getNombre()+"', en la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para cantidad de atributos en llave foranea
class AmountsOfColumnsNotMatchException(SemanticException):
    # Contructor
    def __init__(self, nombre, tabla, tablaForanea):
        self.nombre = nombre
        self.tabla = tabla
        self.tablaForanea = tablaForanea

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La llave foranea '"+self.nombre+"' de la tabla '"+self.tabla.getNombre()+"' no tiene la misma cantidad de atributos que la tabla de referencia '"+self.tablaForanea.getNombre()+"', en la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para atributos que no son llaves primaria para llaves foraneas
class ColumnIsNotPrimaryKeyException(SemanticException):
    # Contructor
    def __init__(self, nombre, tabla):
        self.nombre = nombre
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "El atributo '"+self.nombre+"' no es parte de la llave primaria de la tabla '"+self.tabla.getNombre()+"', en la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para atributos que forman parte de una restriccion
class ColumnInConstraintException(SemanticException):
    # Contructor
    def __init__(self, nombre, restriccion, tabla):
        self.nombre = nombre
        self.restriccion = restriccion
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "No se puede eliminar el atributo '"+self.nombre+"' porque es parte de la restricción '"+self.restriccion+"' de la tabla '"+self.tabla.getNombre()+"', en la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."
        
# Contiene excepción para atributos de llaves primaria que no son referenciados
class ColumnIsPrimaryKeyException(SemanticException):
    # Contructor
    def __init__(self, llave, tabla, nombre, tablaForanea):
        self.llave = llave
        self.tabla = tabla
        self.nombre = nombre
        self.tablaForanea = tablaForanea

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "El atributo '"+self.nombre+"' es parte de la llave primaria de la tabla '"+self.tablaForanea.getNombre()+"' y no es referenciado en la llave foranea '"+self.llave+"' de la tabla '"+self.tabla.getNombre()+"'; en la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción para eliminación de una tabla que es referenciada en otra
class NeededTableException(SemanticException):
    # Contructor
    def __init__(self, tabla, dependientes):
        self.tabla = tabla
        self.dependientes = ''
        for d in dependientes:
            self.dependientes += d + ', '
        self.dependientes = self.dependientes[:-2]

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La tabla '"+self.tabla+"' no se puede eliminar, la(s) tabla(s) '"+self.dependientes+"' tienen llaves foraneas que la referencian."

# Contiene excepción para error de tipos 
class TypeMistmatchException(SemanticException):
    # Contructor
    def __init__(self, valor1, tipo1, op, valor2, tipo2, tabla):
        self.valor1 = valor1
        self.tipo1 = tipo1
        self.op = op
        self.valor2 = valor2
        self.tipo2 = tipo2
        self.tabla = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "El valor '"+self.valor1+"' de tipo '"+self.tipo1+"' no puede ser comparado mediante '"+self.op+"' con el valor '"+self.valor2+"' de tipo '"+self.tipo2+"'; en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."

# Contiene excepción que sucede cuando no se utiliza el atributo en el check corto
class ColumnNotUsedException(SemanticException):
    # Contructor
    def __init__(self, valor, nombre, tabla):
        self.valor  = valor
        self.nombre = nombre
        self.tabla  = tabla

    # Genera la cadena que representa a la excepcion
    def __str__(self):
        return "La columna '"+self.valor+"' no fue utilizada en la restricción corta (CHECK '"+self.nombre+"'), en la tabla '"+self.tabla.getNombre()+"' de la base de datos '"+self.tabla.getBaseDeDatos().getNombre()+"'."


# ====================================================
# Excepciones para registros
# ====================================================
class ValuesNotMatchException(SemanticException):
    # Constructor
    def __init__(self, tabla, expected, given):
        self.t = tabla
        self.ex = expected
        self.g = given
        
    # Genera la cadena que representa a la excepción
    def __str__(self):
        return "En la tabla '"+self.t+"' se esperan '"+str(self.ex)+"' valores, se recibieron '"+str(self.g)+"'."
