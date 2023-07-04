import sqlite3

datos = [("11", "EMPANADA DE SALMÓN", "30", "500"), ("12", "EMPANADA DE VERDURA","20","500"), ("13", "BURRATA DE CAMPO", "10", "1000"), ("21", "POLLO A LA CREMA", "15", "2000"), ("22","BONDIOLA A LA CERVEZ CON PURÉ DE BATATAS", "15", "2500"), ("23", "TALLARINES CAMPESTRES CORTADOS A CUCHILLO CON FILETTO", "20", "1800"),  ("24", "RAVIOLONES DE PAVITA Y VERDURA CON SALSA 4 QUESOS", "20", "2000"), ("25", "BIFE DE CHORIZO", "30", "2500"), ("26", "BIFE DE LOMO", "30", "2800"), ("27", "MATAMBRITO DE CERDO", "30", "2600"), ("31", "PAPAS BASTÓN", "40", "800"), ("32", "BATATAS FRITAS", "40", "700"), ("33", "PURÉ DE PAPA", "50", "700"), ("41", "ENSALADA CAESAR", "30", "2000"), ("51", "TIRAMISU", "30", "1000"), ("52", "FLAN CASERO", "45", "900"), ("53", "MOUSSE DE CHOCOLATE", "50", "900"), ("61", "COCA COLA", "100", "600"), ("62", "FANTA", "100", "600"), ("63", "SEVEN UP", "100", "600"), ("64", "AGUA MINERAL", "100", "400"), ("65", "SABORIZADA MANZANA", "100", "500"), ("66", "SABORIZADA NARANJA", "100", "500"),]

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