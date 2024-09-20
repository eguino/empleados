from decouple import config

class Configuracion(object):
    RUTA_BASE: str = config('RUTA_BASE')

entorno: dict = {
    'entorno': Configuracion
}