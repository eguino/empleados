from psycopg2.extensions import cursor as PsycopgCursor
from ..databases.postgre_sql import PostgreSQL
from typing import List, Tuple, Any, Dict, Optional
from datetime import datetime, date


class ServicioEmpleados(object):

    def __init__(self) -> None:
        self.instancia = PostgreSQL.crear_instancia()

    def insertar(self, empleado) -> Dict[str, Optional[Any]]:
        resultado: Dict[str, Optional[Any]] = {
            'mensaje' : None,
            'codigo' : None
        }
        cursor = None
        try:
            try:
                fecha_alta_str = empleado["fechaAlta"]
                fecha_alta_obj = datetime.strptime(fecha_alta_str, '%Y-%m-%d')
                fecha_alta_formateada = fecha_alta_obj.strftime('%Y-%m-%d')
            except ValueError:
                resultado['mensaje'] = 'El formato de la fecha es incorrecto. Debe ser YYYY-MM-DD.'
                resultado['codigo'] = 400
                return resultado
            with self.instancia.abrir_conexion() as conexion:
                if (conexion is None):
                    resultado['mensaje'] = 'No se pudo establecer conexión hacia la base de datos de PostgreSQL'
                    resultado['codigo'] = 500
                else:
                    FUNCION_SQL: str = 'SELECT * from funcion_insertar_empleado(%s, %s, %s, %s, %s, %s, %s, %s)'
                    parametros = (f'{empleado["nombreEmpleado"]}', f'{empleado["apellidoPaterno"]}', f'{empleado["apellidoMaterno"]}', f'{empleado["numeroEmpleado"]}', fecha_alta_formateada, f'{empleado["nss"]}', empleado["rfc"], empleado["curp"],)
                    cursor: PsycopgCursor = conexion.cursor()
                    cursor.execute(FUNCION_SQL, parametros)
                    conexion.commit()
                    resultado['mensaje'] = 'registrado'
                    resultado['codigo'] = 201
        except Exception as ex:
            print(ex)
            resultado['mensaje'] = f'Hubo un error al procesar la solicud en la Base de Datos: {ex}'
            resultado['codigo'] = 500
        finally:
            if (cursor is not None):
                cursor.close()
            self.instancia.cerrar_conexion()
        return resultado
    

    def listar(self) -> Dict[str, Optional[Any]]:
        resultado: Dict[str, Optional[Any]] = {
            'error' : None,
            'datos' : []
        }
        cursor = None
        try:
            with self.instancia.abrir_conexion() as conexion:
                if conexion is None:
                    resultado['error'] = 'No se pudo establecer conexión hacia la base de datos de PostgreSQL'
                else:
                    FUNCION_SQL: str = 'SELECT * FROM funcion_listar_empleados()'
                    cursor: PsycopgCursor = conexion.cursor()
                    cursor.execute(FUNCION_SQL)
                    filas: List[Tuple[Any, ...]] = cursor.fetchall()
                    columnas: List[str] = [desc[0] for desc in cursor.description]
                    for fila in filas:
                        diccionario: Dict[str, Any] = dict(zip(columnas, fila))
                        fecha_alta = diccionario['fecha_alta']
                        if isinstance(fecha_alta, date):
                            fecha_alta = fecha_alta.strftime('%Y-%m-%d')
                        empleado: Dict[Any, Any] = {
                            'idEmpleado': diccionario['id_empleado'],
                            'nombreEmpleado': diccionario['nombre_empleado'],
                            'apellidoPaterno': diccionario['apellido_paterno'],
                            'apellidoMaterno': diccionario['apellido_materno'],
                            'numeroEmpleado': diccionario['numero_empleado'],
                            'fechaAlta': fecha_alta,
                            'nss': diccionario['nss'].upper(),
                            'rfc': diccionario['rfc'].upper(),
                            'curp': diccionario['curp'].upper()
                        }
                        resultado['datos'].append(empleado)
        except Exception as ex:
            resultado['error'] = f'Hubo un error al procesar la solicitud con la información de la Base de Datos: {ex}'
        finally:
            if (cursor is not None):
                cursor.close()
            self.instancia.cerrar_conexion()
        return resultado
    

    def seleccionar_por_id(self, id_empleado: int) -> Dict[str, Optional[Any]]:
        resultado: Dict[str, Optional[Any]] = {
            'error' : None,
            'datos' : None
        }
        cursor = None
        try:
            # Obtiene la conexión de la base de datos usando un contexto "with"
            with self.instancia.abrir_conexion() as conexion:
                if conexion is None:
                    resultado['error'] = 'No se pudo establecer conexión hacia la base de datos de PostgreSQL'
                else:
                    FUNCION_SQL: str = 'SELECT * FROM funcion_obtener_empleado(%s)'
                    parametros = (id_empleado,)
                    cursor: PsycopgCursor = conexion.cursor()
                    cursor.execute(FUNCION_SQL, parametros)
                    fila: List[Tuple[Any, ...]] = cursor.fetchone()
                    columnas: List[str] = [desc[0] for desc in cursor.description]
                    if (fila):
                        diccionario: Dict[str, Any] = dict(zip(columnas, fila))
                        fecha_alta = diccionario['fecha_alta']
                        if isinstance(fecha_alta, date):
                            fecha_alta = fecha_alta.strftime('%Y-%m-%d')
                        empleado: Dict[Any, Any] = {
                            'idEmpleado': diccionario['id_empleado'],
                            'nombreEmpleado': diccionario['nombre_empleado'],
                            'apellidoPaterno': diccionario['apellido_paterno'],
                            'apellidoMaterno': diccionario['apellido_materno'],
                            'numeroEmpleado': diccionario['numero_empleado'],
                            'fechaAlta': fecha_alta,
                            'nss': diccionario['nss'].upper(),
                            'rfc': diccionario['rfc'].upper(),
                            'curp': diccionario['curp'].upper()
                        }
                        resultado['datos'] = empleado
        except Exception as ex:
            resultado['error'] = f'Hubo un error al procesar la solicitud con la información de la Base de Datos: {ex}'
        finally:
            if (cursor is not None):
                cursor.close()
            self.instancia.cerrar_conexion()
        return resultado


    def eliminar(self, idEmpleado) -> Dict[str, Optional[Any]]:
        resultado: Dict[str, Optional[Any]] = {
            'mensaje' : None,
            'codigo' : None
        }
        cursor = None
        try:
            # Obtiene la conexión de la base de datos usando un contexto "with"
            with self.instancia.abrir_conexion() as conexion:
                if (conexion is None):
                    resultado['mensaje'] = 'No se pudo establecer conexión hacia la base de datos de PostgreSQL'
                    resultado['codigo'] = 500
                else:
                    FUNCION_SQL: str = 'SELECT * from funcion_eliminar_empleado(%s)'
                    parametros = (idEmpleado, )
                    cursor: PsycopgCursor = conexion.cursor()
                    cursor.execute(FUNCION_SQL, parametros)
                    conexion.commit()
                    fila: Optional[Tuple[Any, ...]] = cursor.fetchone()
                    if (fila[0] == 1):
                        resultado['mensaje'] = 'eliminado'
                        resultado['codigo'] = 200
                    else:
                        resultado['mensaje'] = 'No se pudo eliminar el registro en la Base de Datos'
                        resultado['codigo'] = 500
        except Exception as ex:
            resultado['mensaje'] = f'Hubo un error al procesar la solicitud con la información de la Base de Datos: {ex}'
            resultado['codigo'] = 500
        finally:
            if (cursor is not None):
                cursor.close()
            self.instancia.cerrar_conexion()
        return resultado
    

    def actualizar(self, empleado) -> Dict[str, Optional[Any]]:
        resultado: Dict[str, Optional[Any]] = {
            'mensaje' : None,
            'codigo' : None
        }
        cursor = None
        try:
            try:
                fecha_alta_str = empleado["fechaAlta"]
                fecha_alta_obj = datetime.strptime(fecha_alta_str, '%Y-%m-%d')
                fecha_alta_formateada = fecha_alta_obj.strftime('%Y-%m-%d')
            except ValueError:
                resultado['mensaje'] = 'El formato de la fecha es incorrecto. Debe ser YYYY-MM-DD.'
                resultado['codigo'] = 400
                return resultado
            with self.instancia.abrir_conexion() as conexion:
                if (conexion is None):
                    resultado['mensaje'] = 'No se pudo establecer conexión hacia la base de datos de PostgreSQL'
                    resultado['codigo'] = 500
                else:
                    FUNCION_SQL: str = 'SELECT * from funcion_actualizar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    parametros = (empleado["idEmpleado"], f'{empleado["nombreEmpleado"]}', f'{empleado["apellidoPaterno"]}', f'{empleado["apellidoMaterno"]}', f'{empleado["numeroEmpleado"]}', fecha_alta_formateada, f'{empleado["nss"]}', empleado["rfc"], empleado["curp"],)
                    cursor: PsycopgCursor = conexion.cursor()
                    cursor.execute(FUNCION_SQL, parametros)
                    conexion.commit()
                    fila: Optional[Tuple[Any, ...]] = cursor.fetchone()
                    if (fila[0] == 1):
                        resultado['mensaje'] = 'actualizado'
                        resultado['codigo'] = 200
                    elif (fila[0] == 2):
                        resultado['mensaje'] = 'El empleados que desea actualizar ya se encuentra registrado en la Base de Datos'
                        resultado['codigo'] = 400
                    else:
                        resultado['mensaje'] = 'No se pudo actualizar el registro en la Base de Datos'
                        resultado['codigo'] = 500
        except Exception as ex:
            resultado['mensaje'] = f'Hubo un error al procesar la solicitud con la información de la Base de Datos: {ex}'
            resultado['codigo'] = 500
        finally:
            if (cursor is not None):
                cursor.close()
            self.instancia.cerrar_conexion()
        return resultado