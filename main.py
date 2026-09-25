import json
import os
from datetime import datetime

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

def calcular_stock(codigo):
    stock = 0

    for movimiento in movimientos:
        if movimiento["producto_codigo"] == codigo:
            if movimiento["tipo"] == "entrada":
                stock += movimiento["cantidad"]
            elif movimiento["tipo"] == "salida":
                stock -= movimiento["cantidad"]

    return stock

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
    

    elif opcion == "1":
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
            try:
                precio = float(input("Precio: "))
                stock_minimo = int(input("Stock minimo: "))
            except ValueError:
                print("Error: El precio y el stock deben ser números válidos.")
            else:
                
                if precio <= 0 or stock_minimo < 0:
                    print("Los datos ingresados no son validos")
                else:
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
    elif opcion == "2":
        print("\n===== LOTES =====")
        print("1. Registrar lote")
        print("2. Listar lotes")
        print("3. Cosechar lote")
        opcion_lote = input("Seleccione una opcion: ")

        if opcion_lote == "1":
            id_lote = len(lotes) + 1
            producto_codigo = input("Codigo del producto: ").upper()
            fecha_siembra = input("Fecha de siembra: ")
            area_m2 = float(input("Area en m2: "))
            cantidad_producida = float(input("Cantidad producida: "))

            lote = {
                "id_lote": id_lote,
                "producto_codigo": producto_codigo,
                "fecha_siembra": fecha_siembra,
                "area_m2": area_m2,
                "cantidad_producida": cantidad_producida,
                "estado": "activo"
            }
            lotes.append(lote)
            guardar_datos("data/lotes.json", lotes)
            print("Lote registrado correctamente.")

        elif opcion_lote == "2":
            lotes = cargar_datos("data/lotes.json")

            if len(lotes) == 0:
                print("No hay lotes registrados.")
            else:
                print("\n===== LOTES REGISTRADOS =====")

                for lote in lotes:
                    print("--------------------")
                    print("ID lote:", lote["id_lote"])
                    print("Producto:", lote["producto_codigo"])
                    print("Fecha de siembra:", lote["fecha_siembra"])
                    print("Area:", lote["area_m2"], "m2")
                    print("Cantidad producida:", lote["cantidad_producida"])
                    print("Estado:", lote["estado"])

        elif opcion_lote == "3":
            id_lote = int(input("Ingrese el ID del lote: "))
            encontrado = False
            for lote in lotes:
                if lote["id_lote"] == id_lote:
                    encontrado = True
                    if lote["estado"] == "activo":
                        lote["estado"] = "cosechado"
                        movimiento = {
                            "producto_codigo": lote["producto_codigo"],
                            "tipo": "entrada",
                            "cantidad": lote["cantidad_producida"],
                            "motivo": "cosecha",
                            "id_lote": lote["id_lote"]
                        }
                        movimientos.append(movimiento)
                        guardar_datos("data/lotes.json", lotes)
                        guardar_datos("data/movimientos.json", movimientos)
                        print("Lote cosechado correctamente.")
                    else:
                        print("El lote ya fue cosechado.")
            if not encontrado:
                print("Lote no encontrado.")

    elif opcion == "4":
        print("\n===== REGISTRAR VENTA =====")

        items = []
        continuar = "s"

        while continuar == "s":
            codigo = input("Codigo del producto: ").upper()

            producto_encontrado = None

            for producto in productos:
                if producto["codigo"] == codigo and producto["activo"]:
                    producto_encontrado = producto

            if producto_encontrado is None:
                print("Producto no encontrado o esta inactivo.")
            else:
                cantidad = input("Cantidad: ")

                if cantidad.isdigit() and int(cantidad) > 0:
                    cantidad = int(cantidad)
                    stock = calcular_stock(codigo)

                    if cantidad <= stock:
                        subtotal = cantidad * float(producto_encontrado["precio"])

                        item = {
                            "codigo": codigo,
                            "cantidad": cantidad,
                            "precio_unitario": producto_encontrado["precio"],
                            "subtotal": subtotal
                        }

                        items.append(item)

                        print("Producto agregado a la venta.")
                    else:
                        print("No hay suficiente stock.")
                else:
                    print("La cantidad debe ser un numero mayor que 0.")

            continuar = input("¿Desea agregar otro producto? (s/n): ").lower()

        if len(items) > 0:
            total = 0

            for item in items:
                total += item["subtotal"]

            numero_venta = len(ventas) + 1

            venta = {
                "id": "V" + str(numero_venta).zfill(4),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "items": items,
                "total": total
            }

            ventas.append(venta)

            for item in items:
                movimiento = {
                    "id": "M" + str(len(movimientos) + 1).zfill(4),
                    "producto_codigo": item["codigo"],
                    "tipo": "salida",
                    "cantidad": item["cantidad"],
                    "motivo": "Venta " + venta["id"]
                }

                movimientos.append(movimiento)

            guardar_datos("data/ventas.json", ventas)
            guardar_datos("data/movimientos.json", movimientos)

            print("\nVenta registrada correctamente.")
            print("Numero de venta:", venta["id"])
            print("Total:", total)
        else:
            print("No se registro la venta.")

    elif opcion == "5":
        print("\n===== CONSULTAR VENTAS =====")

        ventas = cargar_datos("data/ventas.json")

        if len(ventas) == 0:
            print("No hay ventas registradas.")
        else:
            for venta in ventas:
                print("--------------------")
                print("Venta:", venta["id"])
                print("Fecha:", venta["fecha"])
                print("Total:", venta["total"])

                for item in venta["items"]:
                    print("Producto:", item["codigo"])
                    print("Cantidad:", item["cantidad"])
                    print("Precio:", item["precio_unitario"])

    elif opcion == "6":
        print("\n===== ALERTAS DE STOCK =====")

        productos = cargar_datos("data/productos.json")

        hay_alertas = False

        for producto in productos:
            if producto["activo"]:
                stock = calcular_stock(producto["codigo"])

                if stock <= producto["stock_minimo"]:
                    print("--------------------")
                    print("Producto:", producto["nombre"])
                    print("Codigo:", producto["codigo"])
                    print("Stock actual:", stock)
                    print("Stock minimo:", producto["stock_minimo"])

                    hay_alertas = True

        if not hay_alertas:
            print("No hay alertas de stock.")

    elif opcion == "8":
            guardar_datos("data/productos.json", productos)
            guardar_datos("data/lotes.json", lotes)
            guardar_datos("data/movimientos.json", movimientos)
            guardar_datos("data/ventas.json", ventas)
            print("Datos guardados correctamente")