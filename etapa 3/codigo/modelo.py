import csv
from datetime import datetime
import os

CARPETA_DATOS = "datos"
ARCHIVO_INVENTARIO = os.path.join(CARPETA_DATOS, "inventario.csv")
ARCHIVO_VENTAS = os.path.join(CARPETA_DATOS, "ventas.csv")

def asegurar_archivos():
    """Crea la carpeta datos y los CSV con encabezados si no existen."""
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)
    if not os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["codigo", "nombre", "categoria", "stock", "stock_minimo", "precio_compra", "precio_venta", "fecha_vencimiento"])
    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["numero_factura", "fecha", "codigo_producto", "cantidad", "subtotal", "impuestos", "total"])

def guardar_inventario_csv():
    """Guarda todo el inventario actual en el archivo CSV."""
    asegurar_archivos()
    with open(ARCHIVO_INVENTARIO, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["codigo", "nombre", "categoria", "stock", "stock_minimo", "precio_compra", "precio_venta", "fecha_vencimiento"])
        writer.writeheader()
        for p in inventario:
            writer.writerow(p)

def guardar_venta_csv(venta):
    """Agrega una venta registrada al archivo ventas.csv."""
    asegurar_archivos()
    with open(ARCHIVO_VENTAS, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for prod in venta["productos_vendidos"]:
            writer.writerow([venta["numero_factura"], venta["fecha"], prod["codigo"], prod["cantidad"], prod.get("subtotal", 0), venta["total_impuestos"], venta["total_general"]])
inventario = []   
ventas = []       
alertas = []      
contador_facturas = 0


def buscar_producto(codigo):
    """Devuelve el producto con ese código o None si no existe."""
    for producto in inventario:
        if producto["codigo"] == codigo:
            return producto
    return None


def agregar_producto(producto):
    """Agrega el producto al inventario (el controlador ya verificó que no esté repetido)."""
    inventario.append(producto)
    guardar_inventario_csv()


def aumentar_stock(codigo, cantidad):
    """Suma la cantidad recibida al stock. Devuelve el stock nuevo o None si no existe."""
    producto = buscar_producto(codigo)
    if producto is None:
        return None
    producto["stock"] = producto["stock"] + cantidad
    guardar_inventario_csv()
    return producto["stock"]


def registrar_venta(lineas, total_impuestos, total_general):
    """
    Guarda la venta y descuenta el stock de cada producto vendido.
    lineas es una lista de diccionarios con codigo, cantidad y subtotal.
    """
    global contador_facturas
    contador_facturas = contador_facturas + 1

   
    for linea in lineas:
        producto = buscar_producto(linea["codigo"])
        producto["stock"] = producto["stock"] - linea["cantidad"]

    venta = {
        "numero_factura": "F-" + str(contador_facturas).zfill(4),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "productos_vendidos": lineas,
        "total_impuestos": total_impuestos,
        "total_general": total_general,
    }
    ventas.append(venta)
    guardar_inventario_csv() 
    guardar_venta_csv(venta)
    return venta


def guardar_alertas(nuevas_alertas):
    """Reemplaza las alertas anteriores por las recién generadas (así no se repiten)."""
    alertas.clear()
    for alerta in nuevas_alertas:
        alertas.append(alerta)


def cargar_desde_csv(ruta):
    """
    Lee el archivo de datos de prueba y agrega los productos al inventario.
    Devuelve cuántos se cargaron y cuántos se omitieron (repetidos o con error).
    """
    global reporte_calidad_ultimo
    asegurar_archivos()
    cargados = 0
    omitidos = 0
    nulos = 0
    duplicados = 0
    atipicos = 0
    archivo = open(ruta, newline="", encoding="utf-8")
    lector = csv.DictReader(archivo)
    for fila in lector:
        try:
            #detecta los quen son nulos y atipicos 
            if not fila.get("codigo") or not fila.get("nombre"):
                nulos = nulos + 1
                omitidos = omitidos + 1
                continue
            producto = {
                "codigo": fila["codigo"].strip().upper(),
                "nombre": fila["nombre"].strip(),
                "categoria": fila["categoria"].strip(),
                "stock": int(fila["stock"]),
                "stock_minimo": int(fila["stock_minimo"]),
                "precio_compra": float(fila["precio_compra"]),
                "precio_venta": float(fila["precio_venta"]),
                "fecha_vencimiento": fila["fecha_vencimiento"].strip(),
            }
            #Detecta valores atípicos (precio venta menor a compra o stock negativo)
            if producto["precio_venta"] < producto["precio_compra"] or producto["stock"] < 0:
                atipicos = atipicos + 1
        except (ValueError, KeyError, AttributeError):
            omitidos = omitidos + 1
            continue
        if buscar_producto(producto["codigo"]) is None:
            agregar_producto(producto)
            cargados = cargados + 1
        else:
            omitidos = omitidos + 1
    archivo.close()
    guardar_inventario_csv()
    # Actualiza el reporte con los resultados de la carga
    reporte_calidad_ultimo = {"nulos": nulos, "duplicados": duplicados, "atipicos": atipicos}
    return cargados, omitidos
