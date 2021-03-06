# -*- coding: utf-8 -*-
# Universidad del Valle de Guatemala
# CC3010 Administracion de la Informacion (Seccion 10)
# Byron Orlando Morales Sequen (08414)
# Fecha de modificación: viernes, 20 de mayo de 2011
# Tabla.py
# Contine el esquema y la información general del manejo de los registros.

import logging, datetime
from Excepciones import *
from Resultados import *

# Clase para cada fila de registros
class Registro(dict):
    
    # Contructor
    def __init__(self, tabla):
        # Agregar los datos del registro
        self.log = logging.getLogger('byDBMS.ManejadorBaseDatos.BaseDeDatos('+tabla.getBaseDeDatos().getNombre()+').Tabla('+tabla.getNombre()+').Registro')
        self.tabla = tabla

    # Obtener el valor predeterminado del tipo seleccionado
    def get_default(self, tipo):
        if tipo == 'INT':
            return 0
        elif tipo == 'FLOAT':
            return 0.0
        elif tipo == 'CHAR':
            return ''
        else:
            return '%.4i-01-01' % datetime.MINYEAR
    
    def validar_valor(self, nombre, tipo, tam, pos, valor, tipoValor):
        # Crear valor de retorno
        ret = None
        
        # Guardar valor del registro
        try:
            if tipoValor == 'DEFAULT':
                ret = self.get_default(tipo)
            elif tipoValor == 'NULL':
                ret = None
            elif (tipoValor == 'CHAR' == tipo):
                # Revisar el tamaño
                tam=int(tam)
                if len(valor) > tam:
                    # Arroja error de tipos
                    ex = ValuesLenNotMatchException(self.tabla.getNombre(), pos, nombre, tipo, tam, valor)
                    self.log.error(ex)
                    raise ex
                
                ret = valor
            elif (tipoValor == 'DATE' and tipo == 'CHAR'):
                # Revisar el tamaño
                valor=valor[1:-1]
                tam=int(tam)
                if len(valor) > tam:
                    # Arroja error de tipos
                    ex = ValuesLenNotMatchException(self.tabla.getNombre(), pos, nombre, tipo, tam, valor)
                    self.log.error(ex)
                    raise ex
                
                ret = valor
            elif tipoValor == 'INT' == tipo:
                ret = int(valor)
            elif tipoValor == 'FLOAT' == tipo:
                ret = float(valor)
            elif tipoValor == 'FLOAT' and tipo == 'INT':
                ret = int(float(valor))
            elif tipoValor == 'INT'   and tipo == 'FLOAT':
                ret = float(valor)
            elif tipoValor == 'CHAR'  and tipo == 'INT':
                ret = int(valor)
            elif tipoValor == 'CHAR'  and tipo == 'FLOAT':
                ret = float(valor)
            elif tipoValor == 'DATE' == tipo: 
                # Verificar que la fecha sea válida:
                valor=valor[1:-1]
                try:
                    fecha = valor.split('-')
                    fecha = map(lambda x: int(x), fecha)
                    f = datetime.date(fecha[0], fecha[1], fecha[2])
                except ValueError, msg:
                    ex =  ValueIsInvalidDateException(self.tabla.getNombre(), pos, nombre, tipo, valor)
                    self.log.debug(msg)
                    self.log.error(ex)
                    raise ex
                    
                # Guardar valor
                ret = valor
            else:
                # Arroja error de tipos
                ex = ValuesTypeNotMatchException(self.tabla.getNombre(), pos, nombre, tipo, valor, tipoValor)
                self.log.error(ex)
                raise ex
                
        except ValueError, msg:
            # Arroja error de tipos
            ex = ValuesTypeNotMatchException(self.tabla.getNombre(), pos, nombre, tipo, valor, tipoValor)
            self.log.debug(msg)
            self.log.error(ex)
            raise ex
        
        # Devolver correcto
        return ret
        
    # Buscar valores en este registro
    def get_values_from(self, atributes):
        r = []
        for atribute in atributes:
            r.append(self[atribute])
        return r
        
    # Validar restricciones
    def validar_restricciones(self, omitir=None):
        # TODO Revisar cada restricción
        for restriccion in self.tabla.getRestricciones():
            self.log.debug('Evaluar restricción: ' + str(restriccion))
            
            if restriccion[0] == "PRIMARY KEY":
                # TODODONE Revisar Primary Key
                valor_primario = []
                
                # Buscar campos de llave primaria
                for atributoPrimario in restriccion[2]:
                    valor = self[atributoPrimario]
                    
                    # Revisar valor nulo en llave primaria
                    if valor == None:
                        ex = ValueNullInPrimaryKeyException(self.tabla.getNombre(), atributoPrimario)
                        self.log.error(ex)
                        raise ex                    
                    # Formar valor de la llave primaria
                    valor_primario.append(valor) 
                    
                # Revisar que el valor sea único en la tabla
                repetidos = [r for r in self.tabla.getRegistros() if valor_primario == r.get_values_from(restriccion[2]) and r != omitir]
                
                # Revisión de que sea único
                if len(repetidos) > 0:
                    ex = ValueNotUniqueForPrimaryKeyException(self.tabla.getNombre(), restriccion[2], valor_primario)
                    self.log.error(ex)
                    raise ex
                
            elif restriccion[0] == "FOREIGN KEY":
                # TODODONE Revisar Foreign Key
                
                # Obtener valores
                valores = self.get_values_from(restriccion[2])
                
                # Buscar tabla en la base de datos
                tablaForanea = self.tabla.getBaseDeDatos().verificar_tabla(restriccion[3])
                encontrado = False
                for registro in tablaForanea.getRegistros():
                    if valores == registro.get_values_from(restriccion[4]):
                        encontrado = True
                        
                if not encontrado:
                    ex = ValueNotExistsForForeignKeyException(self.tabla.getNombre(), restriccion[2], tablaForanea.getNombre(), restriccion[4], valores)
                    self.log.error(ex)
                    raise ex                    
                
            elif restriccion[0] == "CHECK":
                # TODO Revisar Check
                if not self.evaluarExpresion(restriccion[2]):
                    ex = ValueNotTheCheckException(self.tabla.getNombre(), self.keys(), restriccion[1], restriccion[2].toString(), self.values())
                    self.log.error(ex)
                    raise ex                    
                    
                
    # Revisar expresiones (valor)
    def evaluarExpresion(self, exp):
        t = type(exp)
        # Evaluar OR
        if t == AST.Exp: #, AST.AndExp, AST.NotExp]:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluarExpresion(exp[0])
            else:
                return self.evaluarExpresion(exp[0]) or self.evaluarExpresion(exp[2])
        # Evaluar AND
        elif t == AST.AndExp:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluarExpresion(exp[0])
            else:
                return self.evaluarExpresion(exp[0]) and self.evaluarExpresion(exp[2])            
        # Evaluar NOT
        elif t == AST.NotExp:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluarExpresion(exp[0])
            else:
                return not self.evaluarExpresion(exp[1])
        # Evaluar operandos
        elif type(exp) == AST.PredExp:
            if (len(exp) == 1):
                # Verificar que el tipo no sea nulo
                return self.evaluarExpresion(exp[0])
            elif(len(exp) == 3):
                op = exp[1]
                v1 = self.evaluarExpresion(exp[0])
                v2 = self.evaluarExpresion(exp[2])
                r = False
                
                # Revisar el tipo de los datos 
                if type(v1) == str and type(v2) == datetime.date:
                    v2 = str(v2)
                elif type(v2) == str and type(v1) == datetime.date:
                    v1 = str(v1)
                
                # Revisar segun operadores validos
                if op == '=':
                    r = v1 == v2
                elif op == '!=' or op == '<>':
                    r = v1 != v2
                elif op == '>':
                    r = v1 > v2
                elif op == '>=':
                    r = v1 >= v2
                elif op == '<':
                    r = v1 < v2
                elif op == '<=':
                    r = v1 <= v2
                
                # Devolver tipo e identificadores
                return r
                
        elif t == AST.Identificador:
            # Devolver valor
            return self[exp[0].lower()]
        elif t == AST.Identificador:
            # Devolver valor
            return evaluarExpresion(Identificador(exp[1].toString().lower()))
        elif t == AST.Int:
            # Devolver valor
            return int(exp[0])
        elif t == AST.Fecha:
            # Devolver valor
            fecha = exp[0].split('-')
            fecha = map(lambda x: int(x), fecha)
            return datetime.date(fecha[0], fecha[1], fecha[2])
        elif t == AST.Float:
            # Devolver valor
            return float(exp[0])
        elif t == AST.Null:
            # Devolver valor
            return None
        elif t == AST.Char:
            # Devolver valor
            return str(exp[0])
    
    # Verifica si este registro se puede modificar sin perder integridad referencial.
    def es_modificable(self, antiguo):
        db = self.tabla.getBaseDeDatos()
        for tbl in self.tabla.getDependientes():
            tabla = db.verificar_tabla(tbl)
            
            # Buscar restricciones
            listaClaves = []
            for restriccion in tabla.getRestricciones():
                if restriccion[0] == "FOREIGN KEY" and restriccion[3] == self.tabla.getNombre():
                    self.log.debug('Evaluar para la restricción: ' + str(restriccion))
                    listaClaves.append(restriccion)
            
            # Verificar cada registro
            for registro in tabla.getRegistros():
                # Verificar cada restricción
                for rest in listaClaves:
                    valores = antiguo.get_values_from(rest[4])
                    if registro.get_values_from(rest[2]) == valores != self.get_values_from(rest[4]):
                        # Mostrar error
                        ex = ValueIsReferencedException(self.tabla.getNombre(), restriccion[4], tbl, restriccion[4], restriccion[1], valores, "modificar")
                        self.log.error(ex)
                        raise ex
        return True
    
    # Verifica si este registro se puede eliminar sin perder consistencia.
    def es_eliminable(self):
        db = self.tabla.getBaseDeDatos()
        for tbl in self.tabla.getDependientes():
            tabla = db.verificar_tabla(tbl)
            
            listaClaves = []
            for restriccion in tabla.getRestricciones():
                if restriccion[0] == "FOREIGN KEY" and restriccion[3] == self.tabla.getNombre():
                    self.log.debug('Evaluar para la restricción: ' + str(restriccion))
                    listaClaves.append(restriccion)
            
            # Verificar cada registro
            for registro in tabla.getRegistros():
                # Verfica cada restriccion
                for rest in listaClaves:
                    valores = self.get_values_from(rest[4])
                    if valores == registro.get_values_from(rest[2]):
                        # Mostrar error
                        ex = ValueIsReferencedException(self.tabla.getNombre(), restriccion[4], tbl, restriccion[4], restriccion[1], valores, "eliminar")
                        self.log.error(ex)
                        raise ex                    
                    
        return True

    # Revisar expresiones (valor)
    def evaluar_condicion(self, exp):
        t = type(exp)
        # Evaluar OR
        if t == AST.Exp: #, AST.AndExp, AST.NotExp]:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluar_condicion(exp[0])
            else:
                return self.evaluar_condicion(exp[0]) or self.evaluar_condicion(exp[2])
        # Evaluar AND
        elif t == AST.AndExp:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluar_condicion(exp[0])
            else:
                return self.evaluar_condicion(exp[0]) and self.evaluar_condicion(exp[2])            
        # Evaluar NOT
        elif t == AST.NotExp:
            # Evaluar las expresiones
            if(len(exp) == 1):
                return self.evaluar_condicion(exp[0])
            else:
                return not self.evaluar_condicion(exp[1])
        # Evaluar operandos
        elif type(exp) == AST.PredExp:
            if (len(exp) == 1):
                # Verificar que el tipo no sea nulo
                return self.evaluar_condicion(exp[0])
            elif(len(exp) == 3):
                op = exp[1]
                v1 = self.evaluar_condicion(exp[0])
                v2 = self.evaluar_condicion(exp[2])
                r = False
                
                # Revisar el tipo de los datos 
                if type(v1) == str and type(v2) == datetime.date:
                    v2 = str(v2)
                elif type(v2) == str and type(v1) == datetime.date:
                    v1 = str(v1)
                
                # Revisar segun operadores validos
                if op == '=':
                    r = v1 == v2
                elif op == '!=' or op == '<>':
                    r = v1 != v2
                elif op == '>':
                    r = v1 > v2
                elif op == '>=':
                    r = v1 >= v2
                elif op == '<':
                    r = v1 < v2
                elif op == '<=':
                    r = v1 <= v2
                
                # Devolver tipo e identificadores
                return r
                
        elif t == AST.Identificador:
            # Devolver valor
            atributo = exp[0].lower()
            for at in self.tabla.getAtributos():
                if at[0].endswith(atributo):
                    return self[at[0]]
        elif t == AST.IdentificadorCompleto:
            # Devolver valor
            atributo = exp[0].lower() + '.' +exp[1].lower()
            return self[atributo]
        elif t == AST.Int:
            # Devolver valor
            return int(exp[0])
        elif t == AST.Fecha:
            # Devolver valor
            fecha = exp[0].split('-')
            fecha = map(lambda x: int(x), fecha)
            return datetime.date(fecha[0], fecha[1], fecha[2])
        elif t == AST.Float:
            # Devolver valor
            return float(exp[0])
        elif t == AST.Null:
            # Devolver valor
            return None
        elif t == AST.Char:
            # Devolver valor
            return str(exp[0])
