def calcular_total(productos, tiene_cupon):
    COSTO_DELIVERY = 5.0
    
    total_productos = sum(p["precio"] for p in productos)
    descuento = 3.5 if tiene_cupon and any(p["nombre"] == "Café Americano" for p in productos) else 0.0
    
    return total_productos + COSTO_DELIVERY - descuento