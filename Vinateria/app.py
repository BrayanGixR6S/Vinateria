from flask import Flask, flash, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_mysqldb import MySQL
import pdfkit
from io import BytesIO
# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'vinateria'
UPLOAD_FOLDER = 'static/productos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)

@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        if not username or not password:
            flash("Falta ingresar datos.")
            return render_template('index.html')

        user =User(0, request.form['Username'], request.form['Password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('Index'))
            else:
                flash("Contraseña Invalida...")
                return render_template('Index.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('Index.html')
    else:
        return render_template('Index.html')


@app.route('/escritorio')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM proveedores")
    data = cur.fetchall()
    cur.close()
    print("hola")
    return render_template('escritorio.html', proveedores=data)

# Proveedores
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        nombre_pro = request.form['nombre_pro']
        if not nombre_pro:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('Index'))
        telefono = request.form['telefono']
        if not telefono:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('Index'))
        correo = request.form['correo']
        if not correo:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('Index'))
        direccion = request.form['direccion']
        if not direccion:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('Index'))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO proveedores (nombre_pro, telefono, correo, direccion) VALUES (%s, %s, %s, %s)", (nombre_pro, telefono, correo, direccion))
        mysql.connection.commit()
        flash('Proveedor Añadido Correctamente', 'success')
        return redirect(url_for('Index'))

# Eliminar Proveedores
@app.route('/proveedores/delete/<string:id>', methods = ['POST', 'GET'])
def delete_proveedores(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM proveedores WHERE proveedores_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Proveedor Eliminado Correctamente', 'success')
    return redirect(url_for('Index'))

# Editar Proveedores
@app.route('/proveedores/edit/<id>', methods= ['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        nombre_pro = request.form['nombre_pro']
        telefono = request.form['telefono']
        correo = request.form['correo']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE proveedores
            SET nombre_pro = %s,
                telefono = %s,
                correo = %s,
                direccion = %s
            WHERE proveedores_Id = %s
        """, (nombre_pro, telefono, correo, direccion, id,))
        flash('Proveedor Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
# Contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
    
# Volumen
@app.route('/volumen')
def volumen():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM volumen')
    data = cur.fetchall()
    cur.close()
    print("hola")
    return render_template('volumen.html', volumenes=data)

@app.route('/insertVolumen', methods = ['POST'])
def insertVolumen():
    if request.method == "POST":
        contenido = request.form['contenido']
        if not contenido:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('volumen'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO volumen (contenido) VALUES (%s)", (contenido,))
        mysql.connection.commit()
        flash('La Cantidad se Añadio Correctamente', 'success')
        return redirect(url_for('volumen'))

# Eliminar volumen
@app.route('/volumen/delete/<string:id>', methods = ['POST', 'GET'])
def delete_volumen(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM volumen WHERE volumen_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Proveedor Eliminado Correctamente', 'success')
    return redirect(url_for('volumen'))

# Editar volumen
@app.route('/volumen/edit/<id>', methods= ['POST', 'GET'])
def update_volumen(id):
    if request.method == 'POST':
        contenido = request.form['contenido']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE volumen
            SET contenido = %s
            WHERE volumen_Id = %s
        """, (contenido, id,))
        flash('Volumen Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('volumen'))
    
# Marca
@app.route('/marca')
def marca():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM marca')
    data = cur.fetchall()
    cur.close()
    print("hola")
    return render_template('marca.html', marcas=data)

@app.route('/insertMarca', methods = ['POST'])
def insertMarca():
    if request.method == "POST":
        nombre = request.form['nombre']
        if not nombre:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('marca'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO marca (nombre) VALUES (%s)", (nombre,))
        mysql.connection.commit()
        flash('se Añadio la Marca Correctamente', 'success')
        return redirect(url_for('marca'))

# Eliminar Marca
@app.route('/marca/delete/<string:id>', methods = ['POST', 'GET'])
def delete_marca(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM marca WHERE marca_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Marca Eliminada Correctamente', 'success')
    return redirect(url_for('marca'))

# Editar Marca
@app.route('/marca/edit/<id>', methods= ['POST', 'GET'])
def update_marca(id):
    if request.method == 'POST':
        contenido = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE marca
            SET nombre = %s,
            WHERE marca_Id = %s
        """, (contenido, id,))
        flash('Marca Editada Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('marca'))

# Productos   
@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM marca')
    marcas = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM proveedores')
    proveedores = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tipo')
    tipos = cur.fetchall()
    cur.close()
    print("hola")
    return render_template('productos.html', productoss=data, marcas=marcas, proveedores=proveedores, tipos=tipos)

@app.route('/insertProductos', methods = ['POST'])
def insertProductos():
    if request.method == "POST":
        nombre = request.form['nombre']
        if not nombre:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('productos'))
        tipoFK = request.form['tipoFK']
        if not tipoFK:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('productos'))
        marcaFK = request.form['marcaFK']
        if not marcaFK:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('productos'))
        proveedoresFK = request.form['proveedoresFK']
        if not proveedoresFK:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('productos'))
        
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                # Save the image with a secure filename
                filename = secure_filename(imagen.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(filepath)
            else:
                filepath = None
        else:
            filepath = None
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre, tipoFK, marcaFK, proveedoresFK,filepath) VALUES (%s, %s, %s, %s, %s)", (nombre, tipoFK, marcaFK, proveedoresFK, filepath))
        mysql.connection.commit()
        flash('Producto Añadido Correctamente', 'success')
        return redirect(url_for('productos'))

# Eliminar Productos
@app.route('/productos/delete/<string:id>', methods = ['POST', 'GET'])
def delete_productos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE productos_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado Correctamente', 'success')
    return redirect(url_for('productos'))

# Editar Productos
@app.route('/productos/edit/<id>', methods= ['POST', 'GET'])
def update_productos(id):
    if request.method == 'POST':
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                # Save the image with a secure filename
                filename = secure_filename(imagen.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(filepath)
            else:
                filepath = None
        else:
            filepath = None
        nombre = request.form['nombre']
        tipoFK = request.form['tipoFK']
        marcaFK = request.form['marcaFK']
        proveedoresFK = request.form['proveedoresFK']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET nombre = %s,
                tipoFK = %s,
                marcaFK = %s,
                proveedoresFK = %s,
                filepath = %s
            WHERE productos_Id = %s
        """, (nombre, tipoFK, marcaFK, proveedoresFK, filepath, id,))
        flash('Producto Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('productos'))
    
# Tipo
@app.route('/tipo')
def tipo():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tipo')
    data = cur.fetchall()
    cur.close()
    print("hola")
    return render_template('tipo.html', tipos=data)

@app.route('/insertTipo', methods = ['POST'])
def insertTipo():
    if request.method == "POST":
        nombre = request.form['nombre']
        if not nombre:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('tipo'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tipo (nombre) VALUES (%s)", (nombre,))
        mysql.connection.commit()
        flash('Se Añadio el Tipo Correctamente', 'success')
        return redirect(url_for('tipo'))

# Eliminar Tipo
@app.route('/tipo/delete/<string:id>', methods = ['POST', 'GET'])
def delete_tipo(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tipo WHERE tipo_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Tipo Eliminado Correctamente', 'success')
    return redirect(url_for('tipo'))

# Editar Tipo
@app.route('/tipo/edit/<id>', methods= ['POST', 'GET'])
def update_tipo(id):
    if request.method == 'POST':
        contenido = request.form['nombre']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE tipo
            SET nombre = %s,
            WHERE tipo_Id = %s
        """, (contenido, id,))
        flash('Tipo Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('tipo'))
    
# catalogo
@app.route("/catalogo")
def inicio():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT prod_vol.*, productos.nombre AS nombre_producto, productos.filepath
        FROM prod_vol
        INNER JOIN productos ON productos.productos_Id = prod_vol.productosFK
    ''')
    data = cur.fetchall()
    cur.close()
    return render_template('catalogo.html', prod_vols=data)

# prod_vol   
@app.route('/prod_vol')
def prod_vol():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT prod_vol.prod_vol_Id, prod_vol.cantidad, prod_vol.precio, volumen.contenido, productos.nombre AS nombre_producto,productos.productos_Id
        FROM prod_vol
        INNER JOIN productos ON prod_vol.productosFK = productos.productos_Id
        INNER JOIN volumen ON volumen.volumen_Id = prod_vol.volumenFK
    ''')
    prod_vols = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM volumen')
    volumenes = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    print("hola")
    return render_template('prod_vol.html', prod_vols=prod_vols, volumenes=volumenes, productos=data)

@app.route('/insertProd_vol', methods = ['POST'])
def insertprod_vol():
    if request.method == "POST":
        cantidad = request.form['cantidad']
        if not cantidad:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('prod_vol'))
        precio = request.form['precio']
        if not precio:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('prod_vol'))
        volumenFK = request.form['volumenFK']
        if not volumenFK:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('prod_vol'))
        productosFK = request.form['productosFK']
        if not productosFK:
            flash('Por favor, asegurese que esten todos los campos llenos', 'error')
            return redirect(url_for('prod_vol'))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO prod_vol (cantidad, precio, volumenFK, productosFK) VALUES (%s, %s, %s, %s)", (cantidad, precio, volumenFK, productosFK))
        mysql.connection.commit()
        flash('Producto Añadido Correctamente', 'success')
        return redirect(url_for('prod_vol'))

# Eliminar prod_vol
@app.route('/prod_vol/delete/<string:id>', methods = ['POST', 'GET'])
def delete_prod_vol(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM prod_vol WHERE prod_vol_Id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto Eliminado Correctamente', 'success')
    return redirect(url_for('prod_vol'))

# Editar prod_vol
@app.route('/prod_vol/edit/<id>', methods= ['POST', 'GET'])
def update_prod_vol(id):
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        volumenFK = request.form['volumenFK']
        productosFK = request.form['productosFK']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE prod_vol
            SET cantidad = %s,
                precio = %s,
                volumenFK = %s,
                productosFK = %s
            WHERE prod_vol_Id = %s
        """, (cantidad, precio, volumenFK, productosFK, id,))
        flash('Producto Editado Correctamente', 'success')
        mysql.connection.commit()
        return redirect(url_for('prod_vol'))

@app.route("/carrito")
def carrito():
    carrito = session.get("carrito")
    productos = []
        
    total = 0
    if carrito:
       
        for prod_vol in carrito:
            id = prod_vol[0]
            cantidad = prod_vol[1]

            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT prod_vol.prod_vol_Id, prod_vol.cantidad, prod_vol.precio, volumen.contenido,
                       productos.nombre AS nombre_producto, productos.productos_Id
                FROM prod_vol
                INNER JOIN productos ON prod_vol.productosFK = productos.productos_Id
                INNER JOIN volumen ON volumen.volumen_Id = prod_vol.volumenFK
                WHERE prod_vol.prod_vol_Id = %s
            ''', (id,))
            prod = cur.fetchone()
            cur.close()
            res = {
                "id": id,
                "cantidad": cantidad,
                "productosFK": prod[4],
                "volumenFK": prod[3],
                "precio": prod[2],
                "importe": float(prod[2]) * float(cantidad)
            }
            productos.append(res)

            total = total + float(prod[2]) * float(cantidad)
    return render_template('carrito.html', prod_vols = productos, total = total)

@app.route('/catalogo/agregar/carrito/<id>')
def catalogoAgregarCarrito(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prod_vol WHERE prod_vol_Id = %s',(id,))
    prod_vol = cur.fetchone()
    cur.close()

    if prod_vol is None:
        flash('No se encontro el producto', 'danger')
    
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, prod_vol in enumerate(carrito):
            if prod_vol[0] == id:
                carrito[i] = (prod_vol[0], prod_vol[1] + 1)  # Aumentar la cantidad en 1
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if not encontrado:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("carrito"))

@app.route('/catalogo/finalizar-venta')
def catalogoFinalizarVenta():
    # Verificar si el carrito está vacío
    if "carrito" not in session or len(session["carrito"]) == 0:
        flash('El carrito está vacío', 'error')
        return redirect(url_for("carrito"))
    print(7)
    # Obtener el total de la venta
    total = 0
    cur = mysql.connection.cursor()
    for prod_vol in session["carrito"]:
        prod_vol_Id = prod_vol[0]
        print(prod_vol)
        cantidad = prod_vol[1]
        cur.execute("SELECT precio FROM prod_vol WHERE prod_vol_Id = %s", (prod_vol_Id,))
        precio = cur.fetchone()
        if precio is None:
            flash(f'No se encontró el precio del producto {prod_vol_Id}', 'error')
            cur.close()
            return redirect(url_for("carrito"))
        total += cantidad * precio[0]

    cur.close()

    if total <= 0:
        flash('El carrito está vacío', 'error')
        return redirect(url_for("carrito"))

    # Crear una nueva transacción SQL
    cur = mysql.connection.cursor()

    #try:
    # Iniciar la transacción
    cur.execute("START TRANSACTION")

    # Insertar la nueva venta en la tabla 'venta'
    cur.execute("INSERT INTO venta (fecha, hora, venta_total) VALUES (NOW(), NOW(), %s)", (total,))
    # Obtener el ID de la venta recién insertada
    venta_id = cur.lastrowid
    print(1)
    # Insertar los detalles de la venta en la tabla 'det_venta'
    for producto in session["carrito"]:
        prod_vol_id = producto[0]
        cantidad = producto[1]
        cur.execute("SELECT precio FROM prod_vol WHERE prod_vol_Id = %s", (prod_vol_id,))
        precio = cur.fetchone()
        if precio is None:
            flash(f'No se encontró el precio del producto {prod_vol_id}', 'error')
            cur.execute("ROLLBACK")
            cur.close()
            return redirect(url_for("catalogo"))
        importe = cantidad * precio[0]
        cur.execute("INSERT INTO det_venta (cantidad, importe, ventaFK, prod_volFK) VALUES (%s, %s, %s, %s)", (cantidad, importe, venta_id, prod_vol_id))
    # Confirmar la transacción
    cur.execute("COMMIT")

    # Vaciar el carrito de la sesión
    session["carrito"] = []

    # Redirigir al punto de venta con un mensaje de éxito
    flash('Venta finalizada con éxito', 'success')
    return redirect(url_for("catalogoTicketVenta",venta_id=venta_id))

    '''except Exception as e:
        # Deshacer la transacción en caso de error
        cur.execute("ROLLBACK")
        return "Error al finalizar la venta: " + str(e)

    finally:
        cur.close() '''     

@app.route('/catalogo/eliminar/carrito/<id>')
def puntoventaEliminarCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, prod_vol in enumerate(carrito):
            if prod_vol[0] == id:
                del carrito[i]  # Eliminar la tupla correspondiente del carrito
                encontrado = True
                break

        # Si no se encontró el producto, mostrar un mensaje de error
        if not encontrado:
            return "El producto no está en el carrito"

        session["carrito"] = carrito

    return redirect(url_for("carrito"))

@app.route('/catalogo/aumenta/carrito/<id>')
def catalogoAumentaCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, prod_vol in enumerate(carrito):
            if prod_vol[0] == id:
                carrito[i] = (prod_vol[0], prod_vol[1] + 1)  # Aumentar la cantidad en 1
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if not encontrado:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("carrito"))


@app.route('/catalogo/disminuye/carrito/<id>')
def catalogodisminuyeCarrito(id):
    if "carrito" in session:
        carrito = session["carrito"]

        encontrado = False
        for i, prod_vol in enumerate(carrito):
            if prod_vol[0] == id:
                if prod_vol[1] <= 0:
                    flash('El producto ya tiene una cantidad de 0')
                    encontrado = True
                    break
                carrito[i] = (prod_vol[0], prod_vol[1] - 1)  # Disminuye la cantidad en 1
                if prod_vol[1] == 1:
                    del carrito[i]
                encontrado = True
                break

        # Si no se encontró el producto, agregarlo al carrito con una cantidad de 1
        if encontrado is False:
            carrito.append((id, 1))

        session["carrito"] = carrito
    else:
        carrito = []

        carrito.append((id, 1))

        session["carrito"] = carrito

    return redirect(url_for("carrito"))


@app.route('/catalogo/ticket-venta/<int:venta_id>')
def catalogoTicketVenta(venta_id):
    # Obtener los detalles de la venta
    cur = mysql.connection.cursor()
    cur.execute("SELECT productos.nombre, volumen.contenido, det_venta.cantidad, det_venta.importe, prod_vol.precio FROM det_venta INNER JOIN productos ON det_venta.prod_volFK = productos.productos_Id INNER JOIN prod_vol ON det_venta.prod_volFK = prod_vol.prod_vol_Id INNER JOIN volumen ON prod_vol.volumenFK = volumen.volumen_Id WHERE det_venta.ventaFK = %s", (venta_id,))
    productos = cur.fetchall()

    # Obtener el total de la venta
    cur.execute("SELECT venta_total FROM venta WHERE venta_Id = %s", (venta_id,))
    total = cur.fetchone()[0]

    # Renderizar el HTML del ticket de venta con los datos de la venta
    return render_template("ticket.html", prod_vols=productos, total=total, folio=venta_id)


    

# Reportes
@app.route('/informe')
def generar_informe():
   cur = mysql.connection.cursor()
   cur.execute("SELECT DATE(fecha) as fecha, SUM(venta_total) as venta_total "
    "FROM venta "
    "GROUP BY DATE(fecha)"
)
   
   ventass = cur.fetchall()
   cur.close()
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM venta')
   return render_template('informe.html', ventass=ventass)

# Validaciones
@app.route('/validar', methods=['POST'])
def validar():
    # Código para validar los datos
    if validar():
        mensaje = 'Los datos son válidos'
        tipo = 'success'
    else:
        mensaje = 'Los datos son inválidos'
        tipo = 'error'

    # Devolver la respuesta en formato JSON
    return jsonify({'mensaje': mensaje, 'tipo': tipo})
    
if __name__ == '__main__':
    app.run(debug=True)
