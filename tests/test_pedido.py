# tests/test_pedido.py
from src.pedido import calcular_total

def test_calcular_total_con_delivery_y_descuento():
    # Estudiante pide un sándwich (10.0), un café (3.5) y tiene cupón
    productos = [
        {"nombre": "Sándwich de Pollo", "precio": 10.0},
        {"nombre": "Café Americano", "precio": 3.5}
    ]
    tiene_cupon = True
    
    total = calcular_total(productos, tiene_cupon)
    
    # Total esperado: 10 + 3.5 + 5 (delivery) - 3.5 (descuento) = 15.0
    assert total == 15.0