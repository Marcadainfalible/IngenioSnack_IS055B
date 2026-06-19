from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

# Inicializamos la extensión de SQLAlchemy
db = SQLAlchemy()

# Generador automático de tickets (Ej: TICK-A1B2)
def generar_ticket():
    caracteres = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TICK-{caracteres}"

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    # Columnas de nuestra tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    ticket = db.Column(db.String(10), unique=True, default=generar_ticket, nullable=False)
    detalle_productos = db.Column(db.String(300), nullable=False) # Guardará: "Sándwich de Pollo, Café"
    total = db.Column(db.Float, nullable=False)
    entregado = db.Column(db.Boolean, default=False) # False = Pendiente, True = Entregado
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Pedido {self.ticket} - S/ {self.total}>'
    
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False) # 'Sándwiches', 'Bebidas' o 'Snacks'
    disponible = db.Column(db.Boolean, default=True) # Para que el Sr. Julio pueda "apagar" un producto si se acaba