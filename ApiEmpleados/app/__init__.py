from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from decouple import Config
from .routes import enrutador_empleados

def iniciar(ambiente: Config) -> FastAPI:
    
    aplicacion: FastAPI = FastAPI()

    # Habilitar CORS para toda la aplicación
    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins = ['*'],  # Permitir todas las orígenes
        allow_credentials = True,
        allow_methods = ['GET', 'POST', 'PUT', 'DELETE'],  # Permitir todos los métodos
        allow_headers = ['*'],  # Permitir todos los headers
    )

    enrutadores = [
        enrutador_empleados.rutas
    ]
    
    RUTA_BASE: str = ambiente.RUTA_BASE

    for enrutador in enrutadores:
        aplicacion.include_router(enrutador, prefix = RUTA_BASE)
    return aplicacion