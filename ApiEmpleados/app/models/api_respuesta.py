from fastapi.responses import JSONResponse

from typing import Any, Dict, Union, Tuple
from decouple import config

class APIRespuesta(object):

    def __init__(self) -> None:
        pass

    VERSION: str = config('VERSION')
    API: str = config('API')

    @classmethod
    def solicitud_correcta(cls, resultado: Any) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
            'mensaje': 'Operación exitosa'
        }
        tipo_dato = type(resultado)
        if resultado and tipo_dato == list:
            respuesta['resultado'] = {
				'registros': resultado
			}
        elif resultado and tipo_dato == dict:
            respuesta['resultado'] = resultado
        return JSONResponse(content = respuesta, status_code = 200)
    

    @classmethod
    def solicitud_creada(cls) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
            'mensaje': 'Operación exitosa'
        }
        return JSONResponse(content = respuesta, status_code = 201)
    

    @classmethod
    def solicitud_incorrecta(cls, errores: Any) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
  			'codigo': f'400.{ cls.API }.{ cls.VERSION }',
  			'mensaje': 'Petición no válida, favor de validar su información',
  			'detalles': errores
  		}
        return JSONResponse(content = respuesta, status_code = 400)
    

    @classmethod
    def no_autorizada(cls, errores: Any) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
  			'codigo': f'401.{ cls.API }.{ cls.VERSION }',
  			'mensaje': 'Acceso no autorizado al recurso',
  			'detalles': errores
  		}
        return JSONResponse(content = respuesta, status_code = 401)
    

    @classmethod
    def informacion_no_encontrada(cls, error: Any) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
			'codigo': f'404.{ cls.API }.{ cls.VERSION }',
			'mensaje': 'Información no encontrada',
			'detalles': [
				str(error)
			]
		}
        return JSONResponse(content = respuesta, status_code = 404)
    
    @classmethod
    def error_interno_del_servidor(cls, errores: Any) -> JSONResponse:
        respuesta: Dict[str, Union[str, Any]] = {
			'codigo': f'500.{ cls.API }.{ cls.VERSION }',
			'mensaje': 'Error interno del servidor',
			'detalles': [
				str(errores)
			]
		}
        return JSONResponse(content = respuesta, status_code = 500)