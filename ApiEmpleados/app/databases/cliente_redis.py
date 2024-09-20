import redis 
import json 
import hashlib
from decouple import config
from typing import Optional
from .redis_db import RedisDB

class ClienteRedis:

    def __init__(self) -> None:
        self.instancia = RedisDB.crear_instancia()
        self.ip = config('IP_REDIS')
        self.puerto = config('PUERTO_REDIS') 
        self.tiempo_vida_clave = config('TIEMPO_DE_VIDA_CLAVE_REDIS')
        self.contrasenia = config('CONTRASENIA', default=None)
        self.api: str = config("API")
        

    def verificar_conexion(self) -> bool:
        try:
            conexion_redis = self.instancia.abrir_conexion()
            respuesta: bool = conexion_redis.ping()
            self.instancia.cerrar_conexion()
            return respuesta 
        except redis.ConnectionError as e:
            print(f"Error de conexión a Redis: {e}")
            return False
    
    def generar_clave(self, id) -> str:
        cadena_clave: str = str(id)
        cadena_clave = self.api + cadena_clave
        return hashlib.sha256(cadena_clave.encode('utf-8')).hexdigest()

    def validar_existencia(self, id) -> bool:
        clave: str = self.generar_clave(id)
        conexion_redis = self.instancia.abrir_conexion()
        respuesta = conexion_redis.exists(clave)
        self.instancia.cerrar_conexion()
        return respuesta

    def guardar_clave(self, id, json_respuesta) -> None:
        conexion_redis = self.instancia.abrir_conexion()
        expiracion = int(self.tiempo_vida_clave)
        json_respuesta: str = json.dumps(json_respuesta)
        clave: str = self.generar_clave(id)
        conexion_redis.set(clave, json_respuesta, ex=expiracion)
        self.instancia.cerrar_conexion()

    def obtener_clave(self, id) -> Optional[dict]:
        conexion_redis = self.instancia.abrir_conexion()
        clave: str = self.generar_clave(id)
        respuesta_redis: Optional[str] = conexion_redis.get(clave)
        self.instancia.cerrar_conexion()
        if respuesta_redis:
            return json.loads(respuesta_redis)
        return None
    
    def eliminar_clave(self, id) -> None:
        conexion_redis = self.instancia.abrir_conexion()
        clave: str = self.generar_clave(id)
        conexion_redis.delete(clave)
        self.instancia.cerrar_conexion