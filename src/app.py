import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pedido import calcular_total
from models import db, Pedido, Producto  # aqui se importa la base de datos y el modelo ojo al piojo
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración de la aplicación y la ruta de las plantillas
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='../templates')
#llave secreta muy secretita
app.secret_key = 'super_llave_secreta_ingeniosnack_2026'

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'ingeniosnack.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos con la aplicación
db.init_app(app)

# ==========================================
# MODELOS DE SEGURIDAD Y USUARIOS
# ==========================================
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=True)
    codigo_matricula = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    contrasena_hash = db.Column(db.String(256), nullable=True)
    puntos_fidelidad = db.Column(db.Integer, default=0)
    compras_totales = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Administrador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

# Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()
    
    # Verificamos si la tabla de productos está vacía. Si es así, la llenamos.
    if Producto.query.count() == 0:
        productos_iniciales = [
            # Sándwiches
            Producto(nombre="Hamburguesa de carne", precio=3.0, categoria="Sándwiches"),
            Producto(nombre="Pan con pollo", precio=3.0, categoria="Sándwiches"),
            # Bebidas
            Producto(nombre="Café", precio=1.5, categoria="Bebidas"),
            Producto(nombre="Inka Cola", precio=2.0, categoria="Bebidas"),
            Producto(nombre="Coca Cola", precio=2.5, categoria="Bebidas"),
            Producto(nombre="Agua Cielo", precio=1.0, categoria="Bebidas"),
            Producto(nombre="Agua San Mateo", precio=1.0, categoria="Bebidas"),
            Producto(nombre="Agua Puquio", precio=1.0, categoria="Bebidas"),
            # Snacks
            Producto(nombre="Papas Lays", precio=2.0, categoria="Snacks"),
            Producto(nombre="Cuates", precio=1.0, categoria="Snacks"),
            Producto(nombre="Chisitos", precio=1.0, categoria="Snacks"),
            Producto(nombre="Inka Chips", precio=1.5, categoria="Snacks")
        ]
        
        # Agregamos todos los productos de golpe y guardamos
        db.session.bulk_save_objects(productos_iniciales)
        db.session.commit()
        print("¡Catálogo de productos sembrado con éxito en la base de datos!")
    


@app.route('/')
def index():
    
    catalogo_completo = Producto.query.all()
    
    return render_template('cliente/index.html', productos=catalogo_completo)

@app.route('/calcular', methods=['POST'])
def calcular():
    # Obtener los datos del formulario HTML
    items_seleccionados = request.form.getlist('producto')
    tiene_cupon = 'cupon' in request.form
    
    # Formatear los productos para nuestra función calcular_total
    productos = []
    nombres_para_ticket = []  # Extraemos los nombres para guardarlos en la BD
    
    for item in items_seleccionados:
        nombre, precio = item.split(',')
        productos.append({"nombre": nombre, "precio": float(precio)})
        nombres_para_ticket.append(nombre)
        
    # 1. Usar la función XP refactorizada (Lógica de Negocio)
    total = calcular_total(productos, tiene_cupon)
    
    # 2. Guardar en la Base de Datos usando SQLAlchemy (Persistencia)
    detalle_texto = " + ".join(nombres_para_ticket)
    nuevo_pedido = Pedido(detalle_productos=detalle_texto, total=total)
    
    db.session.add(nuevo_pedido)
    db.session.commit()  # Aquí se guarda físicamente en ingeniosnack.db
    
    # Pasamos el número de ticket generado automáticamente a la vista de éxito
    return render_template('cliente/exito.html', total=total, ticket=nuevo_pedido.ticket)

@app.route('/admin')
def admin():   
    # Consultar todos los pedidos de la base de datos (ordenados del más nuevo al más viejo)
    pedidos_reales = Pedido.query.order_by(Pedido.fecha.desc()).all()
    # Enviamos los datos reales a la plantilla del Sr. Julio
    return render_template('admin/panel.html', pedidos=pedidos_reales)
@app.route('/entregar/<int:id>', methods=['POST'])
def entregar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.entregado = True
    db.session.commit()

    # En lugar de recargar la página, enviamos una respuesta silenciosa al navegador
    return jsonify({"success": True})

#aqui mero mero se esta poniendo las rutas para el nuevo servidor del panel admin
@app.route('/admin/inventario')
def admin_inventario():
    # Traemos todos los productos para que el Sr. Julio pueda prenderlos o apagarlos
    todos_los_productos = Producto.query.all()
    return render_template('admin/inventario.html', productos=todos_los_productos)

@app.route('/admin/toggle_producto/<int:producto_id>', methods=['POST'])
def toggle_producto(producto_id):
    # Buscamos el producto, si no existe lanza un error 404
    producto = Producto.query.get_or_404(producto_id)
    
    # Invertimos su estado booleano
    producto.disponible = not producto.disponible
    db.session.commit()
    
    # Respondemos al JavaScript con el nuevo estado
    return {'status': 'success', 'nuevo_estado': producto.disponible}

#========================================Simulacion bien chidori de los productos pq aun no esta en uso y no tenemos conteo real============
#ruta pa las estadisicas mi parcero
@app.route('/admin/estadisticas')
def admin_estadisticas():
    # Simulamos la data de la semana de exámenes parciales
    # Obviamente, el Café es el rey indiscutible de las madrugadas universitarias
    datos_ventas = {
        'labels': ['Café Americano', 'Pan con pollo', 'Inka Cola', 'Papas Lays', 'Sándwich Mixto'],
        'valores': [185, 120, 95, 80, 60] 
    }
    
    return render_template('admin/estadisticas.html', ventas=datos_ventas)

#=======================================Se viene otra simulacion pero ahora de clientes porque aun la web no ta en uso pues mi rey============================
@app.route('/admin/vip')
def admin_vip():
    # Simulamos la base de datos de usuarios fieles
    clientes_vip = [
        {'posicion': 1, 'nombre': 'Ana Sofía', 'carrera': 'Ingeniería de Sistemas', 'compras': 42, 'puntos': 420},
        {'posicion': 2, 'nombre': 'Mateo C.', 'carrera': 'Ingeniería de Software', 'compras': 35, 'puntos': 350},
        {'posicion': 3, 'nombre': 'Lucía M.', 'carrera': 'Ingeniería de Sistemas', 'compras': 28, 'puntos': 280},
        {'posicion': 4, 'nombre': 'Diego F.', 'carrera': 'Ingeniería Industrial', 'compras': 15, 'puntos': 150},
        {'posicion': 5, 'nombre': 'Camila R.', 'carrera': 'Ingeniería Civil', 'compras': 12, 'puntos': 120}
    ]
    
    return render_template('admin/vip.html', clientes=clientes_vip)


#============================Rutas temporales las borraremos luego recordatorio para mi=================================
@app.route('/login')
def login_estudiante():
    return render_template('auth/login_estudiante.html')

@app.route('/login/admin')
def login_admin():
    return render_template('auth/login_admin.html')

# ==========================================
# RUTAS DE AUTENTICACIÓN
# ==========================================

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    # 1. Capturamos los datos que el estudiante escribió en el HTML
    codigo = request.form.get('codigo')
    nombre = request.form.get('nombre')
    password = request.form.get('password')

    # 2. Verificamos que el estudiante no exista ya en la base de datos
    estudiante_existente = Estudiante.query.filter_by(codigo_matricula=codigo).first()
    if estudiante_existente:
        return "Error: Este código de matrícula ya está registrado."

    # 3. Creamos al estudiante y encriptamos su contraseña
    nuevo_estudiante = Estudiante(codigo_matricula=codigo, nombre_completo=nombre)
    nuevo_estudiante.set_password(password)

    # 4. Guardamos en la base de datos
    db.session.add(nuevo_estudiante)
    db.session.commit()

    # 5. Lo mandamos de vuelta al login para que inicie sesión
    return redirect(url_for('login_estudiante'))


@app.route('/procesar_login', methods=['POST'])
def procesar_login():
    codigo = request.form.get('codigo')
    password = request.form.get('password')

    # 1. Buscamos al estudiante por su código
    estudiante = Estudiante.query.filter_by(codigo_matricula=codigo).first()

    # 2. Si existe y la contraseña encriptada coincide...
    if estudiante and estudiante.check_password(password):
        
        # 3. ¡Iniciamos la sesión! Guardamos sus datos en la memoria temporal
        session['estudiante_id'] = estudiante.id
        session['estudiante_nombre'] = estudiante.nombre_completo
        
        # 4. Lo enviamos a la página principal de compras
        return redirect(url_for('index')) 
    else:
        return "Error: Código de matrícula o contraseña incorrectos."

@app.route('/logout')
def logout():
    # Borramos la memoria de la sesión
    session.clear()
    return redirect(url_for('login_estudiante'))

if __name__ == '__main__':
    app.run(debug=True)
    
