import sqlite3
from flask import Flask,  jsonify, request
from flask_cors import CORS

# Configurar la conexión a la base de datos SQLite
DATABASE = 'productos.db'

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS productos
                (id INT PRIMARY KEY,
                nombre VARCHAR(100),
                precio NVARCHAR(50),
                stock NVARCHAR(50))""")

datos = [
        ("11", "EMPANADA DE SALMÓN", "500", "30"),
        ("12", "EMPANADA DE VERDURA", "500", "20"),
        ("13", "BURRATA DE CAMPO", "1000", "10"),
        ("21", "POLLO A LA CREMA", "2000", "15"),
        ("22","BONDIOLA CON PURÉ", "2500", "15"),
        ("23", "TALLARINES CON FILETTO", "1800", "20"),
        ("24", "RAVIOLONES DE VERDURA CON SALSA 4 QUESOS", "2000", "20"),
        ("25", "BIFE DE CHORIZO", "2500", "30"),
        ("26", "BIFE DE LOMO", "2800", "30"),
        ("27", "MATAMBRITO DE CERDO", "2600", "30"),
        ("31", "PAPAS BASTÓN", "800", "40"),
        ("32", "BATATAS FRITAS", "700","40"),
        ("33", "PURÉ DE PAPA", "700","50"),
        ("41", "ENSALADA CAESAR", "2000", "30"),
        ("51", "TIRAMISU", "1000", "30"),
        ("52", "FLAN CASERO", "900", "45"),
        ("53", "MOUSSE DE CHOCOLATE", "900", "50"),
        ("61", "COCA COLA", "600", "100"),
        ("62", "FANTA", "600", "100"),
        ("63", "SEVEN UP", "600", "150"),
        ("64", "AGUA MINERAL", "400", "160"),
        ("65", "SABORIZADA MANZANA", "500", "80"),
        ("66", "SABORIZADA NARANJA", "500", "80")
        ]

cursor.executemany("""INSERT INTO productos (id, nombre, precio, stock) VALUES (?, ?, ?, ?)""", datos)

conn.commit()
cursor.close()

print("Se ha creado la tabla y se han insertado los datos correctamente.")

conn.close()
