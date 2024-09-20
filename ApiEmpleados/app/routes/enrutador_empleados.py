import uuid

from fastapi import APIRouter, Body
from typing import Dict, Any, List, Optional
from ..services.servicio_empleados import ServicioEmpleados
from ..databases.cliente_redis import ClienteRedis
from ..models.api_respuesta  import APIRespuesta


rutas: APIRouter  = APIRouter()

@rutas.post('/empleados')
def insertar(cuerpo: Dict[str, Any] = Body(...)): 
    try:
        cliente_redis: ClienteRedis = ClienteRedis()
        servicio_empleados: ServicioEmpleados = ServicioEmpleados()
        resultado: str = servicio_empleados.insertar(cuerpo)
        if (resultado['codigo'] == 201):
            respuesta = APIRespuesta.solicitud_creada()
            respuesta = cliente_redis.validar_existencia("lista_empleados")
            if (respuesta != 0):
                cliente_redis.eliminar_clave("lista_empleados")
        elif (resultado['codigo'] == 400):
            respuesta = APIRespuesta.solicitud_incorrecta([resultado['mensaje']])
        else:
            respuesta = APIRespuesta.error_interno_del_servidor(resultado['mensaje'])
    except Exception as ex:
        print(ex)
        mensaje: List[str] = [f'Su petición no fue ejecutada de manera correcta: {ex}']
        respuesta = APIRespuesta.solicitud_incorrecta(mensaje)
    return respuesta

@rutas.get('/empleados')
def listar():
    try:
        cliente_redis: ClienteRedis = ClienteRedis()
        respuesta = cliente_redis.validar_existencia("lista_empleados")
        if (respuesta == 0):
            servicio_empleados: ServicioEmpleados = ServicioEmpleados()
            resultado = servicio_empleados.listar()
            if(resultado['error'] is not None):
                respuesta = APIRespuesta.error_interno_del_servidor(resultado['error'])
            elif(len(resultado['datos']) <= 0):
                mensaje: str = 'No se encontró información con la combinación de parámetros solicitados'
                respuesta = APIRespuesta.informacion_no_encontrada(mensaje)
            else:
                cliente_redis.guardar_clave("lista_empleados", resultado['datos'])
                respuesta = APIRespuesta.solicitud_correcta(resultado["datos"])
        else:
            #resultado: Dict[str, Optional[str]] = servicio_redis.obtener_clave("lista_empleados")
            respuesta = APIRespuesta.solicitud_correcta(resultado)
    except Exception as ex:
        mensaje: List[str] = [f'Su petición no fue ejecutada de manera correcta: {ex}']
        respuesta = APIRespuesta.solicitud_incorrecta(mensaje)
    return respuesta


@rutas.get('/empleados/{id}')
def seleccionar_por_id(id: int):
    try:
        cliente_redis: ClienteRedis = ClienteRedis()
        respuesta = cliente_redis.validar_existencia(id)
        if (0 == 0):
            servicio_empleados: ServicioEmpleados = ServicioEmpleados()
            resultado = servicio_empleados.seleccionar_por_id(id)
            if(resultado['error'] is not None):
                respuesta = APIRespuesta.error_interno_del_servidor(resultado['error'])
            elif(resultado['datos'] is None):
                mensaje: str = 'No se encontró información con la combinación de parámetros solicitados'
                respuesta = APIRespuesta.informacion_no_encontrada(mensaje)
            else:
                cliente_redis.guardar_clave(id, resultado['datos'])
                respuesta = APIRespuesta.solicitud_correcta(resultado["datos"])
        else:
            resultado: Dict[str, Optional[str]] = cliente_redis.obtener_clave(id)
            respuesta = APIRespuesta.solicitud_correcta(resultado)
    except Exception as ex:
        mensaje: List[str] = [f'Su petición no fue ejecutada de manera correcta: {ex}']
        respuesta = APIRespuesta.solicitud_incorrecta(mensaje)
    return respuesta


@rutas.delete('/empleados/{id}')
def eliminar(id: int):
    try:
        servicio_empleados: ServicioEmpleados = ServicioEmpleados()
        resultado: str = servicio_empleados.eliminar(id)
        if (resultado['codigo'] == 200):
            cliente_redis: ClienteRedis = ClienteRedis()
            cliente_redis.eliminar_clave("lista_empleados")
            respuesta = APIRespuesta.solicitud_correcta(None)
        else:
            respuesta = APIRespuesta.error_interno_del_servidor(resultado['mensaje'])
    except Exception as ex:
        mensaje: List[str] = [f'Su petición no fue ejecutada de manera correcta: {ex}']
        respuesta = APIRespuesta.solicitud_incorrecta(mensaje)
    return respuesta


@rutas.put('/empleados/{id}')
def actualizar(id: int, cuerpo: Dict[str, Any] = Body(...)):
    try:
        servicio_empleados: ServicioEmpleados = ServicioEmpleados()
        cuerpo['idEmpleado'] = id
        resultado: str = servicio_empleados.actualizar(cuerpo)
        if (resultado['codigo'] == 200):
            cliente_redis: ClienteRedis = ClienteRedis()
            cliente_redis.eliminar_clave("lista_empleados")
            cliente_redis.eliminar_clave(id)
            respuesta = APIRespuesta.solicitud_correcta(None)
        elif (resultado['codigo'] == 400):
            respuesta = APIRespuesta.solicitud_incorrecta([resultado['mensaje']])
        else:
            respuesta = APIRespuesta.error_interno_del_servidor(resultado)
    except Exception as ex:
        mensaje: List[str] = [f'Su petición no fue ejecutada de manera correcta: {ex}']
        respuesta = APIRespuesta.solicitud_incorrecta(mensaje)
    return respuesta