from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from configuracion import entorno
from consul import Consul, Check
from app import iniciar
from typing import Dict, Any

desarrollo: Dict[str, Any] = entorno['entorno']
aplicacion: FastAPI = iniciar(desarrollo)

# Configuración de CORS
aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes agregar más dominios si es necesario
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

if not aplicacion:
    raise ValueError('No se pudo iniciar la aplicación FastAPI')

RUTA_BASE: str = str(desarrollo.RUTA_BASE)

definiciones: Dict[str, Any] = {
    'tags': [
        f'urlprefix-/dev{ RUTA_BASE }/status strip=/dev',
        f'urlprefix-/dev{ RUTA_BASE }/empleados strip=/dev',
        f'urlprefix-/dev{ RUTA_BASE }/empleados/* strip=/dev'
    ]
}
