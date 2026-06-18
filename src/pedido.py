def calcular_total(productos, tiene_cupon):
    
    if not productos:
        return 0.0
        
    total = sum(item['precio'] for item in productos)
    
    if tiene_cupon:
        total = total * 0.90
        
    total = total + 5.00
    
    return round(total, 2)