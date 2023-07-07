#importando Liberia mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mybd = mysql.connector.connect(
        host ="localhost"
        user = "root"
        password = "",
        database = "crud_flask_python" #hay que cambiarle los nombres
    )
if mydb:
    print ("Conexión exitosa a BD")
    return mydb
else:
    print("Error en la conexión a BD")
    