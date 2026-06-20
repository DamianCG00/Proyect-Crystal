import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="crystal_db", 
        user="postgres",
        password="contrasena"
    )