# Refactorización (Diseño Simple XP)

## Antes (Código con bucles manuales)
```python
def calcular_total(productos, tiene_cupon):
    total = 0
    for p in productos:
        total = total + p["precio"]
    total = total + 5.0
    if tiene_cupon == True:
        for p in productos:
            if p["nombre"] == "Café Americano":
                total = total - p["precio"]
                break
    return total
```
## Después (Código refactorizado)
```python
def calcular_total(productos, tiene_cupon):
    COSTO_DELIVERY = 5.0
    total_productos = sum(p["precio"] for p in productos)
    descuento = 3.5 if tiene_cupon and any(p["nombre"] == "Café Americano" for p in productos) else 0.0
    return total_productos + COSTO_DELIVERY - descuento
```
Justificación XP:
Se eliminaron los bucles for anidados reemplazándolos por comprensión de listas y la función nativa sum(). Se extrajo el valor numérico directo 5.0 a la constante COSTO_DELIVERY para evitar números mágicos, mejorar la legibilidad y cumplir fielmente con el principio de Diseño Simple.