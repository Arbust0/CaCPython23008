import sqlite3

# Configurar la conexión a la base de datos SQLite
DATABASE = 'productos.db'

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

conn = conectar()
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS productos
            (codigo INTEGER NOT NULL,
            nombre VARCHAR(100),
            stock INTEGER NOT NULL,
            precio REAL NOT NULL)"""
            )

conn.commit()
cursor.close()
conn.close()

#-----------------------------------------------------

conn=conectar()
cursor = conn.cursor()

datos = [
    ("1", "EMPANADA DE SALMÓN", "45", "500"),
    ("2", "EMPANADA DE VERDURA", "67", "600")
]

cursor.executemany("""INSERT INTO productos (codigo, nombre, stock, precio) VALUES (?, ?, ?, ?)""", datos)

cursor.close()
conn.commit()
conn.close()

#------------------------------------------------

