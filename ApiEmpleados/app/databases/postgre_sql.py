import psycopg2
import threading

from decouple import config


class PostgreSQL(object):
	bloqueo_instancia = threading.Lock()
	instancia = None

	def __init__(self) -> None:
		self.ip: str = config("IP_POSTGRESQL")
		self.puerto: int = config("PUERTO_POSTGRSQL")
		self.usuario: str = config("USUARIO_POSTGRESQL")
		self.contrasenia: str = config("CONTRASENIA_POSTGRESQL")
		self.base_datos: str = config("BASE_DATOS_POSTGRESQL")
		self.esquema: str = config("ESQUEMA_BASE_DATOS_POSTGRESQL")
		self.conexion = None

	@classmethod
	def crear_instancia(cls) -> "PostgreSQL":
		if (cls.instancia is None):
			with (cls.bloqueo_instancia):
				if (cls.instancia is None):
					cls.instancia = cls()
		return cls.instancia

	def abrir_conexion(self) -> psycopg2.extensions.connection:
		if (self.conexion is None) or (self.conexion.closed != 0):
			try:
				self.conexion = psycopg2.connect(host = self.ip, port = self.puerto, database = self.base_datos, user = self.usuario, password = self.contrasenia, options = f'-c search_path="{ self.esquema }"')
				print('Conexión a PostgreSQL establecida correctamente')
			except Exception as ex:
				print('Error al conectar a PostgreSQL: ' + str(ex))
				self.conexion = None
		return self.conexion

	def cerrar_conexion(self) -> None:
		self.conexion = None
		self.instancia = None
		print('Conexión a PostgreSQL cerrada correctamente')