import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pedido import calcular_total
from models import db, Pedido  # aqui se importa la base de datos y el modelo ojo al piojo

# Configuración de la aplicación y la ruta de las plantillas
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='../templates')

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'ingeniosnack.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la base de datos con la aplicación
db.init_app(app)

# Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('cliente/index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
    
