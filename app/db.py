import psycopg2

#CONEXION A LA BD
def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        database="caja_ahorro",
        user="postgres",
        password="postgres"
    )