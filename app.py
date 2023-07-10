from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/inventario.db'
db = SQLAlchemy(app)

class Producto(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
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
    if request.method == 'POST':
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']

        producto = Producto(codigo=codigo, descripcion=descripcion, cantidad=stock, precio=precio)
        db.session.add(producto)
        db.session.commit()

        return redirect('/')
    
    return render_template('agregar_producto.html')

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

if __name__ == '__main__':
    app.run(debug=True)