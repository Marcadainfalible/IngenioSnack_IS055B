from flask import Flask, render_template, request
from pedido import calcular_total

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    # Obtener los datos del formulario HTML
    items_seleccionados = request.form.getlist('producto')
    tiene_cupon = 'cupon' in request.form
    
    # Formatear los productos para nuestra función calcular_total
    productos = []
    for item in items_seleccionados:
        nombre, precio = item.split(',')
        productos.append({"nombre": nombre, "precio": float(precio)})
        
    # Usar la función XP refactorizada
    total = calcular_total(productos, tiene_cupon)
    
    return render_template('exito.html', total=total)

@app.route('/admin')
def admin():
    return """
    <div style='font-family: Arial; text-align: center; padding: 50px; background: #e0f7fa;'>
        <h1 style='color: #333;'>IngenioSnack - Panel de Control 👨‍🍳</h1>
        <div style='background: white; padding: 20px; border-radius: 10px; display: inline-block;'>
            <h3>Pedidos Pendientes: 1 (Simulado)</h3>
            <p>1x Sándwich de Pollo, 1x Café - <b>Total: S/ 15.00</b></p>
            <button style='background: #4CAF50; color: white; padding: 5px 10px; border: none;'>Marcar Entregado</button>
            <hr>
            <h3>Control de Menú</h3>
            <button style='background: #f44336; color: white; padding: 5px 10px; border: none;'>Apagar Sándwich de Atún (Agotado)</button>
        </div>
        <br><br><a href='/'>Volver a la tienda</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)
    
