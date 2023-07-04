import sqlite3

datos = [("11", "EMPANADA DE SALMÓN", "30", "500"), ("12", "EMPANADA DE VERDURA","20","500")]

# Conectarse a la base de datos
conn = sqlite3.connect('platos.db')

# Crear una tabla llamada "platos"
conn.execute('''CREATE TABLE platos
                (codigo TEXT, descripcion TEXT, cantidad TEXT, precio TEXT)''')

# Insertar los datos en la tabla
for dato in datos:
    conn.execute("INSERT INTO platos VALUES (?,?,?,?)", dato)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()