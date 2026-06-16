# tests/test_app.py
from src.app import app

def test_pagina_principal_carga():
    # Simulamos un navegador web
    cliente = app.test_client()
    respuesta = cliente.get('/')
    
    # Verificamos que la página responda bien (Código 200) y muestre el nombre
    assert respuesta.status_code == 200
    assert b"IngenioSnack" in respuesta.data