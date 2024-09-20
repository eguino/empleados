import redis
from decouple import config 
import threading

class RedisDB:
    bloqueo_instancia = threading.Lock()
    instancia = None

    def __init__(self) -> None:
        self.ip = config('IP_REDIS')
        self.puerto = int(config('PUERTO_REDIS'))  
        self.tiempo_vida_clave = int(config('TIEMPO_DE_VIDA_CLAVE_REDIS'))  
        self.contrasenia = config('CONTRASENIA', default=None)
        self.conexion = None
        
    @classmethod
    def crear_instancia(cls):
        if (cls.instancia is None):
            with cls.bloqueo_instancia:
                if(cls.instancia is None):
                    cls.instancia = cls()
        return cls.instancia
        
    def abrir_conexion(self):
        if self.conexion is None or not self.conexion.ping():
            try:
                self.conexion = redis.StrictRedis(
                    host=self.ip,
                    port=self.puerto,
                    password=self.contrasenia,
                    decode_responses=True  
                )
                print('Conexión a Redis establecida correctamente')
            except redis.ConnectionError as e:
                print(f"Error al conectar con Redis: {e}")
        return self.conexion
    
    def cerrar_conexion(self):
        if self.conexion is not None:
            self.conexion = None  
            print('Conexión a Redis cerrada correctamente')
        else:
            print('No hay conexión activa para cerrar')
    
    
   