from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/inventario.db'
db = SQLAlchemy(app)

class Producto(db.Model):
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100))
    cantidad = db.Column(db.String(50))
    precio = db.Column(db.String(50))

def create_database():
    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute("""CREATE TABLE productos (
                            codigo INTEGER PRIMARY KEY,
                            descripcion TEXT,
                            stock INTEGER,
                            precio REAL
                        )""")
        datos = [
            ("11", "EMPANADA DE SALMÓN", 30, 500),
            ("12", "EMPANADA DE VERDURA", 20, 500),
            ("13", "BURRATA DE CAMPO", 10, 1000),
            ("21", "POLLO A LA CREMA", 15, 2000),
            ("22", "BONDIOLA CON PURÉ", 15, 2500),
            ("23", "TALLARINES CON FILETTO", 20, 1800),
            ("24", "RAVIOLONES DE VERDURA CON SALSA 4 QUESOS", 20, 2000),
            ("25", "BIFE DE CHORIZO", 30, 2500),
            ("26", "BIFE DE LOMO", 30, 2800),
            ("27", "MATAMBRITO DE CERDO", 30, 2600),
            ("31", "PAPAS BASTÓN", 40, 800),
            ("32", "BATATAS FRITAS", 40, 700),
            ("33", "PURÉ DE PAPA", 50, 700),
            ("41", "ENSALADA CAESAR", 30, 2000),
            ("51", "TIRAMISU", 30, 1000),
            ("52", "FLAN CASERO", 45, 900),
            ("53", "MOUSSE DE CHOCOLATE", 50, 900),
            ("61", "COCA COLA", 100, 600),
            ("62", "FANTA", 100, 600),
            ("63", "SEVEN UP", 150, 600),
            ("64", "AGUA MINERAL", 160, 400),
            ("65", "SABORIZADA MANZANA", 80, 500),
            ("66", "SABORIZADA NARANJA", 80, 500)
        ]
        cursor.executemany("INSERT INTO productos (codigo, descripcion, stock, precio) VALUES (?, ?, ?, ?)", datos)

    conn.commit()
    conn.close()

create_database()

@app.route('/')
def mostrar_productos():
    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():

    if request.method == 'GET':
        return render_template('agregar_producto.html')
 
    if request.method == 'POST':
        # codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        conn = sqlite3.connect('database/inventario.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (descripcion, stock, precio) VALUES (?, ?, ?)", (descripcion, stock, precio))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/editar/<int:codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
    producto = cursor.fetchone()
    
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']

        cursor.execute("UPDATE productos SET descripcion=?, stock=?, precio=? WHERE codigo=?",
                    (descripcion, stock, precio, codigo))
        conn.commit()
        conn.close()

        return redirect('/')

    conn.close()
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:codigo>', methods=['POST'])
def eliminar_producto(codigo):
    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()
    return redirect('/')

#--------------RUTAS-------------------------------------------#
@app.route('/templates/productos.html')
def productos():
    return mostrar_productos()

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/carta.html')
def carta():
    return render_template('carta.html')

@app.route('/reservas.html')
def reservas():
    return render_template('reservas.html')

@app.route('/experiencias.html')
def experiencicas():
    return render_template('experiencias.html')

@app.route('/delivery.html')
def delivery():
    return render_template('delivery.html')

@app.route('/contacto.html')
def contacto():
    return render_template('contacto.html')

@app.route('/ubicacion.html')
def ubicacion():
    return render_template('ubicacion.html')

#@app.route('/name.html')
#def name():
#    return render_template('name.html')

#y en el html <h2><a href="/index.html">
#el style <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">

#como enganchar imagenes de static
#style="background-image: url('/static/Imagenes/tabla%20de%20comida.jpg');"

if __name__ == '__main__':
    app.run(debug=True)