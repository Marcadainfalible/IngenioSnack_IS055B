import sys
import os

# Agregamos la carpeta 'src' a la ruta del sistema para que pytest encuentre los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))