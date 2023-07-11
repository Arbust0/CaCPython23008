from flask import Flask, render_template, flash, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/inventario.db'
app.secret_key = 'maguu'  # Reemplaza esto con tu propia clave secreta
db = SQLAlchemy(app)
app.static_folder = 'static'

class Producto(db.Model):
    codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100))
    cantidad = db.Column(db.String(50))
    precio = db.Column(db.String(50))
    imagen = db.Column(db.String(100))
    
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
                            precio REAL,
                            imagen TEXT
                        )""")
        datos = [
            ("11", "EMPANADA DE SALMÓN", 30, 500,"/static/Imagenes/carrito/empsalmon.jpg"),
            ("12", "EMPANADA DE VERDURAS", 30, 500,"/static/Imagenes/carrito/empverd.jpg"),
            ("13", "BURRATA DE CAMPO", 10, 1000,"/static/Imagenes/carrito/burrata.jpg"),
            ("21", "POLLO A LA CREMA", 15, 2000, "/static/Imagenes/carrito/pollo.jpg"),
            ("22", "BONDIOLA CON PURÉ", 15, 2500, "/static/Imagenes/carrito/bondiola.jpg"),
            ("23", "TALLARINES CON FILETTO", 20, 1800,"/static/Imagenes/carrito/tallarines.jpg"),
            ("24", "RAVIOLONES DE VERDURA CON SALSA 4 QUESOS", 20, 2000,"/static/Imagenes/carrito/ravioles.jpg"),
            ("25", "BIFE DE CHORIZO", 30, 2500,"/static/Imagenes/carrito/bifechorizo.jpg"),
            ("26", "BIFE DE LOMO", 30, 2800,"/static/Imagenes/carrito/bifelomo.jpg"),
            ("27", "MATAMBRITO DE CERDO", 30, 2600,"/static/Imagenes/carrito/matambrecerdo.jpg"),
            ("31", "PAPAS BASTÓN", 40, 800,"/static/Imagenes/carrito/papasbaston.jpg"),
            ("32", "BATATAS FRITAS", 40, 700,"/static/Imagenes/carrito/batatas.jpg"),
            ("33", "PURÉ DE PAPA", 50, 700,"/static/Imagenes/carrito/purepapas.jpg"),
            ("41", "ENSALADA CAESAR", 30, 2000,"/static/Imagenes/carrito/cesar.jpg"),
            ("51", "TIRAMISU", 30, 1000,"/static/Imagenes/carrito/tiramisu.jpg"),
            ("52", "FLAN CASERO", 45, 900,"/static/Imagenes/carrito/flan.jpg"),
            ("53", "MOUSSE DE CHOCOLATE", 50, 900,"/static/Imagenes/carrito/mousse.jpg"),
            ("61", "COCA COLA", 100, 600,"/static/Imagenes/carrito/cocacola.jpg"),
            ("62", "FANTA", 100, 600,"/static/Imagenes/carrito/fanta.jpg"),
            ("63", "SEVEN UP", 150, 600,"/static/Imagenes/carrito/sevenup.jpg"),
            ("64", "AGUA MINERAL", 160, 400,"/static/Imagenes/carrito/agua.jpg"),
            ("65", "SABORIZADA MANZANA", 80, 500,"/static/Imagenes/carrito/sabmanzana.jpg"),
            ("66", "SABORIZADA NARANJA", 80, 500,"/static/Imagenes/carrito/sabnaranja.jpg")
        ]
        cursor.executemany("INSERT INTO productos (codigo, descripcion, stock, precio, imagen) VALUES (?, ?, ?, ?, ?)", datos)

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
        descripcion = request.form['descripcion']
        stock = request.form['stock']
        precio = request.form['precio']
        imagen = request.files['imagen']

        if imagen.filename == '':
            flash('Debes seleccionar una imagen.', 'error')
            return redirect(request.url)

        imagen.save('static/Imagenes/carrito/' + imagen.filename)
        conn = sqlite3.connect('database/inventario.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (descripcion, stock, precio, imagen) VALUES (?, ?, ?, ?)",
                       (descripcion, stock, precio, '/static/Imagenes/carrito/' + imagen.filename))
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
        imagen_path = producto[4]  # Retain the existing image path

        # Check if a new image is selected
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                imagen.save('static/Imagenes/carrito/' + imagen.filename)
                imagen_path = '/static/Imagenes/carrito/' + imagen.filename

        cursor.execute("UPDATE productos SET descripcion=?, stock=?, precio=?, imagen=? WHERE codigo=?",
                       (descripcion, stock, precio, imagen_path, codigo))

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

@app.route('/productos.html')
def productoss():
    return productos()

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


#---------------CARRITO---------------------------------------------------------#

@app.route('/delivery.html')
def delivery():
    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    carrito = request.cookies.get('carrito')
    if carrito:
        carrito = json.loads(carrito)
        total = sum(item['precio'] * item['cantidad'] for item in carrito)
    else:
        carrito = []
        total = 0

    return render_template('delivery.html', productos=productos, carrito=carrito, total=total)


@app.route('/agregar_al_carrito/<int:codigo>', methods=['POST'])
def agregar_al_carrito(codigo):
    cantidad = int(request.form['cantidad'])

    conn = sqlite3.connect('database/inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
    producto = cursor.fetchone()
    conn.close()

    if producto:
        producto_carrito = {
            'codigo': producto[0],
            'descripcion': producto[1],
            'cantidad': cantidad,
            'precio': float(producto[3])  # Convertir el precio a float
        }

        carrito = request.cookies.get('carrito')
        if carrito:
            carrito = json.loads(carrito)
            carrito.append(producto_carrito)
        else:
            carrito = [producto_carrito]

        response = make_response(redirect('/delivery.html'))
        response.set_cookie('carrito', json.dumps(carrito))

        return response
    else:
        return jsonify({'error': 'El producto no existe.'}), 404

@app.route('/checkout', methods=['POST'])
def checkout():
    carrito = request.cookies.get('carrito')
    if carrito:
        carrito = json.loads(carrito)
        carrito = [item for item in carrito if item['cantidad'] > 0]
        total = sum(item['precio'] * item['cantidad'] for item in carrito)

        conn = sqlite3.connect('database/inventario.db')
        cursor = conn.cursor()

        for item in carrito:
            codigo = item['codigo']
            cantidad = item['cantidad']
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?", (cantidad, codigo))

        conn.commit()
        conn.close()

        response = make_response(render_template('checkout.html', productos=productos, carrito=carrito, total=total))
        response.delete_cookie('carrito')  # Eliminar la cookie del carrito

        return response
    else:
        carrito = []
        total = 0

    if total > 0:
        return render_template('checkout.html', productos=productos, carrito=carrito, total=total)
    else:
        return redirect('/delivery.html')

@app.route('/reiniciar_carrito')
def reiniciar_carrito():
    response = make_response(redirect('/delivery.html'))
    response.delete_cookie('carrito')
    return response

if __name__ == '__main__':
    app.run(debug=True)