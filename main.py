import json
import os

def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
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

def mostrar_menu():
    print("\n=====AGROCONTROL CBA=====")
    print("1. Gestión de productos")
    print("2. Gestion de lotes")
    print("3. Movimientos de invetario")
    print("4. Registrar venta")
    print("5. Consultar ventas")
    print("6. Alertas y stock")
    print("7. Reportes")
    print("8. Guardar datos")
    print("0. Salir")

opcion = ""

while opcion != "0":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "0":
        print("Programa finalizado.")
    elif opcion == "8":
        guardar_datos("data/productos.json", productos)
        guardar_datos("data/lotes.json", lotes)
        guardar_datos("data/movimientos.json", movimientos)
        guardar_datos("data/ventas.json", ventas)
        print("Datos guardados correctamente")

    elif opcion == "1":
        print("\n===== PRODUCTOS =====")
        print("1. Registrar producto")
        print("2. Listar productos")

        opcion_producto = input("Seleccione una opcion: ")

        if opcion_producto == "1":
            codigo = input("Codigo del producto: ").upper()

            nombre = input("Nombre del producto: ")
            categoria = input("Categoria: ")
            unidad = input("Unidad: ")
            precio = float(input("Precio: "))
            stock_minimo = int(input("Stock minimo: "))

            producto = {
                "codigo": codigo,
                "nombre": nombre,
                "categoria": categoria,
                "unidad": unidad,
                "precio": precio,
                "stock_minimo": stock_minimo,
                "activo": True
                }

            productos.append(producto)
            guardar_datos("data/productos.json", productos)

            print("Producto registrado correctamente")

        elif opcion_producto == "2":
            productos = cargar_datos("data/productos.json")

            if len(productos) == 0:
                print("No hay productos registrados")

            else: 
                print("\n=====PRODUCTOS=====")

                for producto in productos:
                    if producto["activo"]:
                        print("--------------------")
                        print("Codigo: ", producto["codigo"])
                        print("Nombre: ", producto["nombre"])
                        print("Categoria: ", producto["categoria"])
                        print("Precio: ", producto["precio"])
                        print("Stock_minimo: ", producto["stock_minimo"])