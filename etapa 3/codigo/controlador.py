import math
import os
import modelo
import vista
from datetime import datetime, date



IVA = 0.13      
DIAS_ALERTA = 7       


def pedir_texto(mensaje):
    """Pide un texto y repite hasta que no venga vacío."""
    while True:
        texto = vista.pedir_dato(mensaje).strip()
        if texto == "":
            vista.mostrar_error("Error: este campo no puede estar vacío.")
        else:
            return texto


def pedir_entero(mensaje, permite_cero):
    """Pide un número entero. Si permite_cero es False, debe ser mayor que cero."""
    while True:
        texto = vista.pedir_dato(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            vista.mostrar_error("Error: debe ingresar un número entero.")
            continue
        if numero < 0:
            vista.mostrar_error("Error: el número no puede ser negativo.")
        elif numero == 0 and not permite_cero:
            vista.mostrar_error("Error: el número debe ser mayor que cero.")
        else:
            return numero


def pedir_decimal(mensaje):
    """Pide un número decimal mayor que cero (acepta coma o punto)."""
    while True:
        texto = vista.pedir_dato(mensaje).strip().replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            vista.mostrar_error("Error: debe ingresar un número válido (ejemplo: 1500.50).")
            continue
        if not math.isfinite(numero) or numero <= 0:
            vista.mostrar_error("Error: el precio debe ser un número mayor que cero.")
        else:
            return round(numero, 2)


def pedir_fecha(mensaje):
    """Pide una fecha YYYY-MM-DD. Si el usuario deja vacío, el producto no vence."""
    while True:
        texto = vista.pedir_dato(mensaje).strip()
        if texto == "":
            return ""
        try:
            datetime.strptime(texto, "%Y-%m-%d")
            if len(texto) == 10:
                return texto
        except ValueError:
            pass
        vista.mostrar_error("Error: la fecha debe tener formato YYYY-MM-DD (ejemplo: 2026-12-31).")


def confirmar(mensaje):
    """Pregunta s/n y devuelve True o False."""
    while True:
        respuesta = vista.pedir_dato(mensaje).strip().lower()
        if respuesta == "s" or respuesta == "si" or respuesta == "sí":
            return True
        if respuesta == "n" or respuesta == "no":
            return False
        vista.mostrar_error("Error: responda con 's' para sí o 'n' para no.")


def registrar_producto():
    vista.mostrar_titulo("REGISTRAR PRODUCTO")
    codigo = pedir_texto("Código del producto: ").upper()
    if modelo.buscar_producto(codigo) is not None:
        vista.mostrar_error("Error: el código ingresado ya existe en el inventario.")
        return

    nombre = pedir_texto("Nombre del producto: ")
    categoria = pedir_texto("Categoría: ")
    stock = pedir_entero("Stock inicial: ", True)
    stock_minimo = pedir_entero("Stock mínimo (umbral de alerta): ", True)
    precio_compra = pedir_decimal("Precio de compra: ")
    precio_venta = pedir_decimal("Precio de venta: ")
    fecha = pedir_fecha("Fecha de vencimiento YYYY-MM-DD (Enter si no tiene): ")

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "stock_minimo": stock_minimo,
        "precio_compra": precio_compra,
        "precio_venta": precio_venta,
        "fecha_vencimiento": fecha,
    }
    modelo.agregar_producto(producto)
    vista.mostrar_exito("Producto registrado exitosamente.")


def actualizar_stock():
    vista.mostrar_titulo("ACTUALIZAR STOCK - RECEPCIÓN DE MERCANCÍA")

    coincideorden = confirmar("¿La mercancía coincide con la orden de compra? (s/n): ")
    if not coincideorden:
        vista.mostrar_error("Lote rechazado, no coincide con la orden. No se modificó el stock.")
        return

    codigo = pedir_texto("Código del producto: ").upper()
    producto = modelo.buscar_producto(codigo)
    if producto is None:
        vista.mostrar_error("Error: el código ingresado no existe.")
        return

    vista.mostrar_info(producto["nombre"] + " - stock actual: " + str(producto["stock"]))
    cantrecibi = pedir_entero("Cantidad recibida: ", False)

    stocknue = modelo.aumentar_stock(codigo, cantrecibi)
    vista.mostrar_exito("Stock actualizado. Nuevo total de " + producto["nombre"] + ": " + str(stocknue))


def cantidad_en_carrito(carrito, codigo):
    """Cuántas unidades de ese producto ya se agregaron a la venta actual."""
    total = 0
    for linea in carrito:
        if linea["codigo"] == codigo:
            total = total + linea["cantidad"]
    return total


def armar_detalle(carrito):
    """Prepara los datos que la vista necesita para mostrar el resumen."""
    detalle = []
    for linea in carrito:
        producto = modelo.buscar_producto(linea["codigo"])
        detalle.append({
            "nombre": producto["nombre"],
            "cantidad": linea["cantidad"],
            "precio": producto["precio_venta"],
            "subtotal": linea["subtotal"],
        })
    return detalle


def realizar_venta():
    vista.mostrar_titulo("REALIZAR VENTA")
    carrito = []
    subtotal = 0.0
    masproductos = True

    while masproductos:
        codigo = pedir_texto("Código del producto: ").upper()
        producto = modelo.buscar_producto(codigo)

        if producto is None:
            vista.mostrar_error("Error: el código ingresado no existe.")
        else:
            vista.mostrar_producto(producto)
            cantsoli = pedir_entero("Cantidad solicitada por el cliente: ", False)
            stockdisponible = producto["stock"] - cantidad_en_carrito(carrito, codigo)

            if cantsoli <= stockdisponible:
                subitem = round(producto["precio_venta"] * cantsoli, 2)
                subtotal = round(subtotal + subitem, 2)
                carrito.append({"codigo": codigo, "cantidad": cantsoli, "subtotal": subitem})
                vista.mostrar_exito("Producto agregado. Subtotal del artículo: " + f"{subitem:,.2f}"
                                    + " | Stock restante: " + str(stockdisponible - cantsoli))
            else:
                vista.mostrar_error("ALERTA: Sin existencias suficientes. Stock actual: "
                                    + str(stockdisponible) + ". No se puede facturar este artículo.")

        masproductos = confirmar("¿Desea agregar otro producto? (s/n): ")

    if subtotal <= 0:
        vista.mostrar_info("No se hizo ninguna compra.")
        return

    impuesto = round(subtotal * IVA, 2)
    totalpagar = round(subtotal + impuesto, 2)
    vista.mostrar_resumen_venta(armar_detalle(carrito), subtotal, impuesto, totalpagar)

    if not confirmar("¿Confirmar y finalizar la venta? (s/n): "):
        vista.mostrar_info("Venta cancelada. No se modificó el inventario.")
        return

    venta = modelo.registrar_venta(carrito, impuesto, totalpagar)

    avisos = []
    for linea in carrito:
        p = modelo.buscar_producto(linea["codigo"])
        if p["stock"] <= p["stock_minimo"]:
            avisos.append(p["nombre"] + " quedó con stock bajo: " + str(p["stock"])
                          + " (mínimo " + str(p["stock_minimo"]) + ")")
    vista.mostrar_venta_registrada(venta, avisos)


def generar_alertas():
    nuevas = []
    hoy = date.today()

    for p in modelo.inventario:
        if p["stock"] <= p["stock_minimo"]:
            nuevas.append({
                "codigo_producto": p["codigo"],
                "tipo_alerta": "stock_bajo",
                "mensaje": "ALERTA DE REPOSICIÓN: " + p["nombre"] + " tiene " + str(p["stock"])
                           + " unidades (mínimo " + str(p["stock_minimo"]) + ").",
            })

        if p["fecha_vencimiento"] != "":
            try:
                fecha = datetime.strptime(p["fecha_vencimiento"], "%Y-%m-%d").date()
            except ValueError:
                continue
            diasvence = (fecha - hoy).days
            if diasvence < 0:
                mensaje = ("ALERTA DE CADUCIDAD: " + p["nombre"] + " ya venció el "
                           + p["fecha_vencimiento"] + ".")
            elif diasvence <= DIAS_ALERTA:
                mensaje = ("ALERTA DE CADUCIDAD: " + p["nombre"] + " vence en "
                           + str(diasvence) + " días (" + p["fecha_vencimiento"] + ").")
            else:
                continue
            nuevas.append({
                "codigo_producto": p["codigo"],
                "tipo_alerta": "vencimiento_proximo",
                "mensaje": mensaje,
            })

    modelo.guardar_alertas(nuevas)
    vista.mostrar_alertas(modelo.alertas)


def consultar_inventario():
    vista.mostrar_inventario(modelo.inventario)


def consultar_ventas():
    total_impuestos = 0.0
    total_general = 0.0
    for v in modelo.ventas:
        total_impuestos = total_impuestos + v["total_impuestos"]
        total_general = total_general + v["total_general"]
    vista.mostrar_ventas(modelo.ventas, round(total_impuestos, 2), round(total_general, 2))


def buscar_archivo_datos():
    """Busca datos_prueba.csv en ../datos/ o en la misma carpeta del código."""
    carpeta = os.path.dirname(os.path.abspath(__file__))
    rutas = [
        os.path.join(carpeta, "..", "datos", "datos_prueba.csv"),
        os.path.join(carpeta, "datos_prueba.csv"),
    ]
    for ruta in rutas:
        if os.path.isfile(ruta):
            return ruta
    return None


def cargar_datos_prueba():
    ruta = buscar_archivo_datos()
    if ruta is None:
        vista.mostrar_error("Error: no se encontró el archivo datos_prueba.csv.")
        return
    try:
        cargados, omitidos = modelo.cargar_desde_csv(ruta)
    except OSError:
        vista.mostrar_error("Error: no se pudo leer el archivo de datos de prueba.")
        return
    vista.mostrar_exito("Datos de prueba cargados: " + str(cargados)
                        + " productos nuevos, " + str(omitidos) + " omitidos.")


def ejecutar():
    if buscar_archivo_datos() is not None:
        cargar_datos_prueba()

    continuar = True
    while continuar:
        vista.mostrar_menu()
        opcion = vista.pedir_dato("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            actualizar_stock()
        elif opcion == "3":
            realizar_venta()
        elif opcion == "4":
            generar_alertas()
        elif opcion == "5":
            consultar_inventario()
        elif opcion == "6":
            consultar_ventas()
        elif opcion == "7":
            cargar_datos_prueba()
        elif opcion == "8":
         vista.generar_grafico_ventas_categoria(modelo.ventas, modelo.inventario)

        elif opcion == "9":
         vista.generar_grafico_stock_critico(modelo.inventario)
        elif opcion == "10":
         vista.mostrar_reporte_calidad(modelo.reporte_calidad_ultimo)
        elif opcion == "0":
            if confirmar("¿Seguro que desea salir? (s/n): "):
                vista.mostrar_despedida()
                continuar = False
        else:
            vista.mostrar_error("Error: opción no válida. Elija un número del menú.")

        if continuar and opcion != "0":
            vista.pedir_dato("\nPresione Enter para volver al menú...")