import csv
import json
import os
import shutil
from datetime import datetime

def respaldar_archivo(archivo):
    if os.path.exists(archivo):
        if not os.path.exists("backups"):
            os.makedirs("backups")
        nombre_base = os.path.basename(archivo)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = os.path.join("backups", f"{timestamp}_{nombre_base}")
        shutil.copy(archivo, destino)

def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_datos(archivo, datos):
    respaldar_archivo(archivo)
    if not os.path.exists(os.path.dirname(archivo)):
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def calcular_stock(codigo):
    stock = 0
    for movimiento in movimientos:
        if movimiento["producto_codigo"] == codigo:
            if movimiento["tipo"] == "entrada":
                stock += movimiento["cantidad"]
            elif movimiento["tipo"] == "salida":
                stock -= movimiento["cantidad"]
    return stock

def pedir_numero(mensaje):
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        print("Ingrese solamente números enteros.")

USUARIOS = {
    "admin": {"clave": "admin123", "rol": "INSTRUCTOR"},
    "operador": {"clave": "ope123", "rol": "OPERADOR"}
}

def iniciar_sesion():
    print("\n===== AGROCONTROL CBA - INICIO DE SESIÓN =====")
    intentos = 0
    while intentos < 3:
        usuario = input("Usuario: ").strip()
        clave = input("Contraseña: ").strip()
        
        if usuario in USUARIOS and USUARIOS[usuario]["clave"] == clave:
            rol = USUARIOS[usuario]["rol"]
            print(f"\n¡Bienvenido {usuario}! Rol: [{rol}]")
            return usuario, rol
        else:
            print("Usuario o contraseña incorrectos.")
            intentos += 1
            
    print("Demasiados intentos fallidos. Cerrando sistema.")
    exit()

usuario_actual, rol_actual = iniciar_sesion()

productos = cargar_datos("data/productos.json")
lotes = cargar_datos("data/lotes.json")
movimientos = cargar_datos("data/movimientos.json")
ventas = cargar_datos("data/ventas.json")

print("\nDatos cargados correctamente.")

def mostrar_menu():
    print(f"\n===== AGROCONTROL CBA [{rol_actual}] =====")
    print("1. Gestión de productos")
    print("2. Gestión de lotes")
    print("3. Movimientos de inventario")
    print("4. Registrar venta")
    print("5. Consultar ventas")
    print("6. Devolución de ventas")
    print("7. Alertas y stock")
    print("8. Reportes")
    print("9. Exportar inventario a CSV")
    print("10. Guardar datos manual")
    print("0. Salir")

opcion = ""

while opcion != "0":
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "0":
        print("Programa finalizado.")

    elif opcion == "1":
        if rol_actual == "OPERADOR":
            print("\nAcceso denegado: Opción reservada para INSTRUCTOR/ADMINISTRADOR.")
            continue

        print("\n===== PRODUCTOS =====")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Desactivar producto")

        opcion_producto = input("Seleccione una opción: ").strip()

        if opcion_producto == "1":
            codigo = input("Código del producto: ").strip().upper()
            if codigo == "":
                print("El código no puede estar vacío.")
                continue

            existe = any(p["codigo"] == codigo for p in productos)
            if existe:
                print("El código ya existe.")
            else:
                nombre = input("Nombre del producto: ")
                categoria = input("Categoría: ")
                unidad = input("Unidad: ")
                try:
                    precio = float(input("Precio de venta: "))
                    costo = float(input("Costo unitario: "))
                    stock_minimo = int(input("Stock mínimo: "))
                except ValueError:
                    print("Error: El precio, costo y stock deben ser números válidos.")
                else:
                    if precio <= 0 or costo < 0 or stock_minimo < 0:
                        print("Los valores ingresados no son válidos.")
                    else:
                        producto = {
                            "codigo": codigo,
                            "nombre": nombre,
                            "categoria": categoria,
                            "unidad": unidad,
                            "precio": precio,
                            "costo": costo,
                            "stock_minimo": stock_minimo,
                            "activo": True
                        }
                        productos.append(producto)
                        guardar_datos("data/productos.json", productos)
                        print("Producto registrado correctamente.")

        elif opcion_producto == "2":
            productos = cargar_datos("data/productos.json")
            if len(productos) == 0:
                print("No hay productos registrados.")
            else:
                print("\n===== PRODUCTOS =====")
                for producto in productos:
                    if producto.get("activo", True):
                        print("--------------------")
                        print("Código: ", producto["codigo"])
                        print("Nombre: ", producto["nombre"])
                        print("Categoría: ", producto["categoria"])
                        print("Precio: ", producto["precio"])
                        print("Costo: ", producto.get("costo", 0.0))
                        print("Stock mínimo: ", producto["stock_minimo"])

        elif opcion_producto == "3":
            codigo = input("Ingrese el código del producto: ").strip().upper()
            encontrado = False
            for producto in productos:
                if producto["codigo"] == codigo:
                    print("\nProducto encontrado:")
                    print("Código:", producto["codigo"])
                    print("Nombre:", producto["nombre"])
                    print("Categoría:", producto["categoria"])
                    print("Unidad:", producto["unidad"])
                    print("Precio:", producto["precio"])
                    print("Costo:", producto.get("costo", 0.0))
                    print("Stock mínimo:", producto["stock_minimo"])
                    print("Activo:", producto["activo"])
                    encontrado = True
            if not encontrado:
                print("Producto no encontrado.")

        elif opcion_producto == "4":
            codigo = input("Ingrese el código del producto: ").strip().upper()
            encontrado = False
            for producto in productos:
                if producto["codigo"] == codigo and producto.get("activo", True):
                    encontrado = True
                    print("\nDeje vacío si no desea cambiar el dato.")
                    nombre = input("Nuevo nombre: ")
                    categoria = input("Nueva categoría: ")
                    unidad = input("Nueva unidad: ")
                    precio = input("Nuevo precio: ")
                    costo = input("Nuevo costo: ")
                    stock_minimo = input("Nuevo stock mínimo: ")

                    if nombre != "": producto["nombre"] = nombre
                    if categoria != "": producto["categoria"] = categoria
                    if unidad != "": producto["unidad"] = unidad
                    if precio != "": producto["precio"] = float(precio)
                    if costo != "": producto["costo"] = float(costo)
                    if stock_minimo != "": producto["stock_minimo"] = int(stock_minimo)

                    guardar_datos("data/productos.json", productos)
                    print("Producto actualizado correctamente.")

            if not encontrado:
                print("Producto no encontrado o está inactivo.")

        elif opcion_producto == "5":
            codigo = input("Ingrese el código del producto: ").strip().upper()
            encontrado = False
            for producto in productos:
                if producto["codigo"] == codigo:
                    encontrado = True
                    if producto.get("activo", True):
                        producto["activo"] = False
                        guardar_datos("data/productos.json", productos)
                        print("Producto desactivado correctamente.")
                    else:
                        print("El producto ya está desactivado.")

            if not encontrado:
                print("Producto no encontrado.")

    elif opcion == "2":
        print("\n===== LOTES =====")
        print("1. Registrar lote")
        print("2. Listar lotes")
        print("3. Cosechar lote")
        opcion_lote = input("Seleccione una opción: ").strip()

        if opcion_lote == "1":
            id_lote = len(lotes) + 1
            producto_codigo = input("Código del producto: ").strip().upper()
            producto_existe = any(p["codigo"] == producto_codigo and p.get("activo", True) for p in productos)

            if not producto_existe:
                print("El producto no existe o está inactivo.")
                continue

            fecha_siembra = input("Fecha de siembra (AAAA-MM-DD): ")
            try:
                area_m2 = float(input("Área en m2: "))
                cantidad_producida = float(input("Cantidad producida: "))
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")
                continue

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
                    print("Área:", lote["area_m2"], "m2")
                    print("Cantidad producida:", lote["cantidad_producida"])
                    print("Estado:", lote["estado"])

        elif opcion_lote == "3":
            try:
                id_lote = int(input("Ingrese el ID del lote: "))
            except ValueError:
                print("ID no válido.")
                continue

            encontrado = False
            for lote in lotes:
                if lote["id_lote"] == id_lote:
                    encontrado = True
                    if lote["estado"] == "activo":
                        lote["estado"] = "cosechado"
                        movimiento = {
                            "id": "M" + str(len(movimientos) + 1).zfill(4),
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

    elif opcion == "3":
        print("\n===== MOVIMIENTOS DE INVENTARIO =====")
        if len(movimientos) == 0:
            print("No hay movimientos registrados.")
        else:
            for mov in movimientos:
                print("--------------------")
                print("ID Movimiento:", mov.get("id", "N/A"))
                print("Producto:", mov["producto_codigo"])
                print("Tipo:", mov["tipo"].upper())
                print("Cantidad:", mov["cantidad"])
                print("Motivo:", mov.get("motivo", "N/A"))

    elif opcion == "4":
        print("\n===== REGISTRAR VENTA =====")
        items = []
        continuar = "s"

        while continuar == "s":
            codigo = input("Código del producto: ").strip().upper()
            producto_encontrado = next((p for p in productos if p["codigo"] == codigo and p.get("activo", True)), None)

            if producto_encontrado is None:
                print("Producto no encontrado o está inactivo.")
            else:
                cantidad = pedir_numero("Cantidad: ")
                stock = calcular_stock(codigo)

                if cantidad <= stock:
                    subtotal = cantidad * float(producto_encontrado["precio"])
                    costo_unitario = float(producto_encontrado.get("costo", 0.0))

                    item = {
                        "codigo": codigo,
                        "cantidad": cantidad,
                        "precio_unitario": producto_encontrado["precio"],
                        "costo_unitario": costo_unitario,
                        "subtotal": subtotal
                    }
                    items.append(item)
                    print("Producto agregado a la venta.")
                else:
                    print(f"No hay suficiente stock. Stock actual: {stock}")

            continuar = input("¿Desea agregar otro producto? (s/n): ").lower()

        if len(items) > 0:
            total = sum(item["subtotal"] for item in items)
            numero_venta = len(ventas) + 1

            venta = {
                "id": "V" + str(numero_venta).zfill(4),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "items": items,
                "total": total,
                "estado": "completada"
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
            print("Número de venta:", venta["id"])
            print("Total:", total)
        else:
            print("No se registró la venta.")

    elif opcion == "5":
        print("\n===== CONSULTAR VENTAS =====")
        print("1. Ver todas las ventas")
        print("2. Consultar por rango de fechas")

        sub_opcion = input("Seleccione una opción: ").strip()

        if sub_opcion == "1":
            filtradas = ventas
        elif sub_opcion == "2":
            fecha_inicio = input("Fecha inicio (AAAA-MM-DD): ").strip()
            fecha_fin = input("Fecha fin (AAAA-MM-DD): ").strip()
            filtradas = [
                v for v in ventas 
                if fecha_inicio <= v["fecha"].split(" ")[0] <= fecha_fin
            ]
        else:
            print("Opción no válida.")
            continue

        if len(filtradas) == 0:
            print("No se encontraron ventas.")
        else:
            for venta in filtradas:
                print("--------------------")
                print("Venta:", venta["id"])
                print("Fecha:", venta["fecha"])
                print("Estado:", venta.get("estado", "completada").upper())
                print("Total:", venta["total"])
                for item in venta["items"]:
                    print(f"  - Producto: {item['codigo']} | Cantidad: {item['cantidad']} | Precio: {item['precio_unitario']}")

    elif opcion == "6":
        print("\n===== DEVOLUCIÓN DE VENTAS =====")
        id_venta = input("Ingrese el ID de la venta a devolver (ej. V0001): ").strip().upper()
        
        venta_encontrada = next((v for v in ventas if v["id"] == id_venta), None)

        if not venta_encontrada:
            print("Venta no encontrada.")
        elif venta_encontrada.get("estado") == "devuelta":
            print("Esta venta ya fue devuelta previamente.")
        else:
            venta_encontrada["estado"] = "devuelta"
            
            for item in venta_encontrada["items"]:
                movimiento_inverso = {
                    "id": "M" + str(len(movimientos) + 1).zfill(4),
                    "producto_codigo": item["codigo"],
                    "tipo": "entrada",
                    "cantidad": item["cantidad"],
                    "motivo": "Devolución Venta " + venta_encontrada["id"]
                }
                movimientos.append(movimiento_inverso)

            guardar_datos("data/ventas.json", ventas)
            guardar_datos("data/movimientos.json", movimientos)
            print(f"Devolución de la venta {id_venta} realizada correctamente. Stock reincorporado.")

    elif opcion == "7":
        print("\n===== ALERTAS DE STOCK =====")
        productos = cargar_datos("data/productos.json")
        hay_alertas = False

        for producto in productos:
            if producto.get("activo", True):
                stock = calcular_stock(producto["codigo"])
                if stock <= producto["stock_minimo"]:
                    print("--------------------")
                    print("Producto:", producto["nombre"])
                    print("Código:", producto["codigo"])
                    print("Stock actual:", stock)
                    print("Stock mínimo:", producto["stock_minimo"])
                    hay_alertas = True

        if not hay_alertas:
            print("No hay alertas de stock.")

    elif opcion == "8":
        print("\n===== REPORTES =====")
        print("1. Productos")
        print("2. Inventario")
        print("3. Ventas")
        print("4. Reporte de utilidad estimada")

        opcion_reporte = input("Seleccione una opción: ").strip()

        if opcion_reporte == "1":
            print("\n===== REPORTE DE PRODUCTOS =====")
            for producto in productos:
                print("--------------------")
                print("Código:", producto["codigo"])
                print("Nombre:", producto["nombre"])
                print("Categoría:", producto["categoria"])
                print("Precio:", producto["precio"])
                print("Costo:", producto.get("costo", 0.0))
                print("Activo:", producto.get("activo", True))

        elif opcion_reporte == "2":
            print("\n===== REPORTE DE INVENTARIO =====")
            for producto in productos:
                stock = calcular_stock(producto["codigo"])
                print("--------------------")
                print("Producto:", producto["nombre"])
                print("Código:", producto["codigo"])
                print("Stock:", stock)
                print("Stock mínimo:", producto["stock_minimo"])

        elif opcion_reporte == "3":
            total_ventas = 0
            print("\n===== REPORTE DE VENTAS =====")
            for venta in ventas:
                if venta.get("estado") != "devuelta":
                    print("--------------------")
                    print("Venta:", venta["id"])
                    print("Fecha:", venta["fecha"])
                    print("Total:", venta["total"])
                    total_ventas += float(venta["total"])

            print("--------------------")
            print("Total vendido (Ventas válidas):", total_ventas)

        elif opcion_reporte == "4":
            if rol_actual == "OPERADOR":
                print("\nAcceso denegado: Opción reservada para INSTRUCTOR/ADMINISTRADOR.")
                continue

            print("\n===== REPORTE DE UTILIDAD ESTIMADA =====")
            total_ingresos = 0
            total_costos = 0

            for venta in ventas:
                if venta.get("estado") != "devuelta":
                    for item in venta["items"]:
                        ingreso = item["subtotal"]
                        costo_unit = item.get("costo_unitario", 0.0)
                        costo_total_item = costo_unit * item["cantidad"]

                        total_ingresos += ingreso
                        total_costos += costo_total_item

            utilidad_total = total_ingresos - total_costos
            print("--------------------")
            print(f"Total Ingresos: ${total_ingresos:.2f}")
            print(f"Total Costos:   ${total_costos:.2f}")
            print(f"Utilidad Estimada: ${utilidad_total:.2f}")

    elif opcion == "9":
        print("\n===== EXPORTAR INVENTARIO A CSV =====")
        try:
            if not os.path.exists("reportes"):
                os.makedirs("reportes")
            
            archivo_csv = "reportes/inventario.csv"
            
            with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(["Codigo", "Nombre", "Categoria", "Precio", "Costo", "Stock_Actual", "Stock_Minimo", "Estado"])
                
                for p in productos:
                    stock = calcular_stock(p["codigo"])
                    escritor.writerow([
                        p["codigo"],
                        p["nombre"],
                        p["categoria"],
                        p["precio"],
                        p.get("costo", 0.0),
                        stock,
                        p["stock_minimo"],
                        "Activo" if p.get("activo", True) else "Inactivo"
                    ])

            print(f"Inventario exportado exitosamente en: {archivo_csv}")
        except Exception as e:
            print(f"Error al exportar a CSV: {e}")

    elif opcion == "10":
        guardar_datos("data/productos.json", productos)
        guardar_datos("data/lotes.json", lotes)
        guardar_datos("data/movimientos.json", movimientos)
        guardar_datos("data/ventas.json", ventas)
        print("Datos guardados y respaldados correctamente.")