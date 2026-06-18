def calcular_total(productos, tiene_cupon):
    # 1. EL GUARDÍAN: Si la lista de productos está vacía, el costo es 0 absoluto.
    if not productos:
        return 0.0
        
    # 2. Sumar el precio de los productos elegidos
    total = sum(item['precio'] for item in productos)
    
    # 3. Aplicar descuento de fidelidad si existe (ejemplo: 10% de descuento)
    if tiene_cupon:
        total = total * 0.90
        
    # 4. Sumar el costo de delivery (ajustado según la lógica actual de 5 soles fijos)
    # Nota: Si el delivery se vuelve opcional en el futuro (Punto 4 de tu backlog), 
    # aquí agregaremos la condición "if es_delivery:"
    total = total + 5.00
    
    # Devolver el total redondeado a 2 decimales por estética financiera
    return round(total, 2)