# tests/test_pedido.py
from src.pedido import calcular_total

def test_calcular_total_con_delivery_y_descuento():
    # Estudiante pide un sándwich, un café (3.5) y tiene un cupón
    productos = [
        {"nombre": "Sándwich de Pollo", "precio": 10.0},
        {"nombre": "Café Americano", "precio": 3.5}
    ]
    tiene_cupon = True
    
    total = calcular_total(productos, tiene_cupon)
    
    # Total esperado: Subtotal 13.5 con 10% dscto (12.15) + 5 delivery = 17.15
    assert total == 17.15

def test_carrito_vacio_no_cobra_delivery():
    productos = []
    tiene_cupon = False
    
    resultado = calcular_total(productos, tiene_cupon)
    
    assert resultado == 0.0, f"Error: Se esperaba 0.0, pero se cobró {resultado}"