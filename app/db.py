import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

#CONEXION A LA BD
def conectar_bd():
    print("DB_HOST =", os.getenv("DB_HOST"))  # 👈 para debug
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )