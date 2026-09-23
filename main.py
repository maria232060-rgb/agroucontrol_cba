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

    if opcion == "1":
        print("\n===== PRODUCTOS =====")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Desactivar producto")

        opcion_producto = input("Seleccione una opcion: ")

        if opcion_producto == "1":
            codigo = input("Codigo del producto: ").upper()
            existe = False
            for producto in productos:
                if producto["codigo"] == codigo:
                    existe = True
            if existe:
                print("El codigo ya existe")
            else:
                nombre = input("Nombre del producto: ")
                categoria = input("Categoria: ")
                unidad = input("Unidad: ")
                precio = float(input("Precio: "))
                stock_minimo = int(input("Stock minimo: "))
                if precio <= 0 or stock_minimo < 0:
                    print("Los datos ingresados no son validos")
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

        elif opcion_producto == "3":
            codigo = input("Ingrese el codigo del producto: ").upper()
            encontrado= False
            for producto in productos:
                if producto["codigo"] == codigo:
                    print("\nProducto encontrado:")
                    print("Codigo:", producto["codigo"])
                    print("Nombre:", producto["nombre"])
                    print("Categoria:", producto["categoria"])
                    print("Unidad:", producto["unidad"])
                    print("Precio:", producto["precio"])
                    print("Stock minimo:", producto["stock_minimo"])
                    print("Activo:", producto["activo"])
                    encontrado = True
            if not encontrado:
                print("Producto no encontrado.")
        elif opcion_producto == "4":
            codigo = input("Ingrese el codigo del producto: ").upper()
            encontrado = False
            for producto in productos:
                if producto["codigo"] == codigo and producto["activo"]:
                    encontrado = True
                    print("\nDeje vacio si no desea cambiar el dato.")
                    nombre = input("Nuevo nombre: ")
                    categoria = input("Nueva categoria: ")
                    unidad = input("Nueva unidad: ")
                    precio = input("Nuevo precio: ")
                    stock_minimo = input("Nuevo stock minimo: ")

                    if nombre != "":
                        producto["nombre"] = nombre

                    if categoria != "":
                        producto["categoria"] = categoria

                    if unidad != "":
                        producto["unidad"] = unidad

                    if precio != "":
                        producto["precio"] = float(precio)

                    if stock_minimo != "":
                        producto["stock_minimo"] = int(stock_minimo)

                    guardar_datos("data/productos.json", productos)
                    print("Producto actualizado correctamente.")

            if not encontrado:
                print("Producto no encontrado o esta inactivo.")

        elif opcion_producto == "5":
            codigo = input("Ingrese el codigo del producto: ").upper()
            encontrado = False
            for producto in productos:
                if producto["codigo"] == codigo:
                    encontrado = True

                    if producto["activo"]:
                        producto["activo"] = False
                        guardar_datos("data/productos.json", productos)
                        print("Producto desactivado correctamente.")
                    else:
                        print("El producto ya esta desactivado.")

            if not encontrado:
                print("Producto no encontrado.")