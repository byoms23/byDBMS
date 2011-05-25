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
            elif (tipoValor == 'CHAR' == tipo) or (tipoValor == 'DATE' and tipo == 'CHAR'):
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
    def validar_restricciones(self):
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
                repetidos = [r for r in self.tabla.getRegistros() if valor_primario == r.get_values_from(restriccion[2])]
                
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
                
                
    # Revisar expresiones
    def revisar_expresion(self, exp):
        return False
        
