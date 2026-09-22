import json
import os

def cargar_datos(archivo):
    try:
        with open(archivo, "r", encondinf="utf-8") as f:
            return json.load(F)
    except FileNotFoundError:
        return[]

def guardar_datos(archivo, datos):
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)

productos = cargar_datos("data/productos.json")
lotes = cargar_datos("data/lotes.json")
movimientos = cargar_datos("data/movimientos.json")
ventas = cargar_datos("data/ventas.json")

print("Datos cargados correctamente")