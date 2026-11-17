
MONEDA = "₡"
import matplotlib.pyplot as plt

def pedir_dato(mensaje):
    return input(mensaje)


def mostrar_titulo(titulo):
    print()
    print("=" * 70)
    print(titulo.center(70))
    print("=" * 70)


def mostrar_exito(mensaje):
    print("[OK] " + mensaje)


def mostrar_error(mensaje):
    print("[X] " + mensaje)


def mostrar_aviso(mensaje):
    print("[!] " + mensaje)


def mostrar_info(mensaje):
    print("[i] " + mensaje)


def mostrar_menu():
    mostrar_titulo("PROGRESIVA - INVENTARIO Y PUNTO DE VENTA")
    print("1. Registrar producto")
    print("2. Actualizar stock (recepción de mercancía)")
    print("3. Realizar venta")
    print("4. Generar alertas")
    print("5. Consultar inventario")
    print("6. Consultar ventas del día")
    print("7. Cargar datos de prueba")
    print("8. Generar gráfico: Ventas por categoría")
    print("9. Generar gráfico: Stock crítico (Actual vs Mínimo)")
    print("10. Ver Reporte de Calidad de Datos")
    print("0. Salir")
    print("-" * 70)


def mostrar_despedida():
    print()
    print("Gracias por usar el sistema. ¡Hasta pronto!")


def mostrar_inventario(productos):
    mostrar_titulo("INVENTARIO")
    if len(productos) == 0:
        print("El inventario está vacío.")
        return

    print("-" * 100)
    print(f"{'Código':<8}{'Nombre':<28}{'Categoría':<18}{'Stock':>6}{'Mín':>5}"
          f"{'P.Venta':>12}  {'Vence':<11}{'Aviso'}")
    print("-" * 100)
    cantidad_bajos = 0
    for p in productos:
        aviso = ""
        if p["stock"] <= p["stock_minimo"]:
            aviso = "* STOCK BAJO"
            cantidad_bajos = cantidad_bajos + 1
        vence = p["fecha_vencimiento"]
        if vence == "":
            vence = "-"
        print(f"{p['codigo']:<8}{p['nombre']:<28}{p['categoria']:<18}{p['stock']:>6}"
              f"{p['stock_minimo']:>5}{p['precio_venta']:>12,.2f}  {vence:<11}{aviso}")
    print("-" * 100)
    print("Total de productos:", len(productos))
    print("Productos con stock bajo (*):", cantidad_bajos)


def mostrar_alertas(alertas):
    mostrar_titulo("ALERTAS GENERADAS")
    if len(alertas) == 0:
        print("Stock adecuado: no hay alertas de reposición ni de caducidad.")
        return
    print(f"{'Código':<8}{'Tipo':<22}Mensaje")
    print("-" * 100)
    for a in alertas:
        print(f"{a['codigo_producto']:<8}{a['tipo_alerta']:<22}{a['mensaje']}")
    print("-" * 100)
    print("Total de alertas:", len(alertas))


def mostrar_producto(producto):
    print(f"   {producto['nombre']} | Precio: {MONEDA} {producto['precio_venta']:,.2f}"
          f" | Stock disponible: {producto['stock']}")


def mostrar_resumen_venta(detalle, subtotal, impuesto, totalpagar):
    """detalle es una lista de diccionarios con nombre, cantidad, precio y subtotal."""
    mostrar_titulo("RESUMEN DE LA VENTA")
    print(f"{'Producto':<30}{'Cant.':>6}{'Precio':>14}{'Subtotal':>16}")
    print("-" * 70)
    for d in detalle:
        print(f"{d['nombre']:<30}{d['cantidad']:>6}{d['precio']:>14,.2f}{d['subtotal']:>16,.2f}")
    print("-" * 70)
    print(f"{'Subtotal:':<40}{MONEDA} {subtotal:>14,.2f}")
    print(f"{'IVA (13%):':<40}{MONEDA} {impuesto:>14,.2f}")
    print(f"{'TOTAL A PAGAR:':<40}{MONEDA} {totalpagar:>14,.2f}")


def mostrar_venta_registrada(venta, avisos):
    mostrar_exito("Venta realizada e inventario actualizado. Factura: " + venta["numero_factura"])
    print("   Fecha:", venta["fecha"])
    print(f"   IVA: {MONEDA} {venta['total_impuestos']:,.2f}")
    print(f"   Total: {MONEDA} {venta['total_general']:,.2f}")
    for aviso in avisos:
        mostrar_aviso(aviso)


def mostrar_ventas(ventas, total_impuestos, total_general):
    mostrar_titulo("VENTAS DEL DÍA (SESIÓN ACTUAL)")
    if len(ventas) == 0:
        print("Todavía no se han realizado ventas en esta sesión.")
        return
    print(f"{'Factura':<10}{'Fecha':<21}{'Productos':<28}{'IVA':>12}{'Total':>14}")
    print("-" * 85)
    for v in ventas:
        texto = ""
        for linea in v["productos_vendidos"]:
            texto = texto + linea["codigo"] + " x" + str(linea["cantidad"]) + " "
        print(f"{v['numero_factura']:<10}{v['fecha']:<21}{texto:<28}"
              f"{v['total_impuestos']:>12,.2f}{v['total_general']:>14,.2f}")
    print("-" * 85)
    print("Cantidad de ventas:", len(ventas))
    print(f"IVA acumulado: {MONEDA} {total_impuestos:,.2f}")
    print(f"TOTAL ACUMULADO: {MONEDA} {total_general:,.2f}")

def mostrar_despedida():
     print("\nPrograma finalizado.")


def generar_grafico_ventas_categoria(ventas, inventario):
    """Genera un gráfico de barras con las ventas totales por categoría de producto."""
    cat_totales = {}
    
    prod_cat = {p["codigo"]: p["categoria"] for p in inventario}
    
    for v in ventas:
        for prod_vendido in v.get("productos_vendidos", []):
            cat = prod_cat.get(prod_vendido["codigo"], "General")
            subtotal = prod_vendido.get("subtotal", 0)
            cat_totales[cat] = cat_totales.get(cat, 0.0) + subtotal

    if not cat_totales:
        print("[!] No hay datos de ventas suficientes para generar el gráfico.")
        return

    categorias = list(cat_totales.keys())
    totales = list(cat_totales.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, totales, color="#1f77b4", edgecolor="black")
    plt.title("Ventas Totales por Categoría de Producto", fontsize=14, fontweight="bold")
    plt.xlabel("Categoría", fontsize=12)
    plt.ylabel("Total Ventas (₡)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def generar_grafico_stock_critico(inventario):
    """Genera un gráfico de barras horizontales comparando stock actual vs stock mínimo."""
    criticos = [p for p in inventario if p["stock"] <= p["stock_minimo"]]
    
    if not criticos:
        print("[i] No hay productos en estado de stock crítico actualmente.")
        return

    nombres = [p["nombre"] for p in criticos]
    stocks = [p["stock"] for p in criticos]
    minimos = [p["stock_minimo"] for p in criticos]
    y_pos = range(len(nombres))

    plt.figure(figsize=(9, 5))
    plt.barh(y_pos, stocks, color="#ff7f0e", label="Stock Actual", alpha=0.8)
    plt.barh(y_pos, minimos, color="#2ca02c", label="Stock Mínimo", alpha=0.4, height=0.4)
    
    plt.yticks(y_pos, nombres)
    plt.xlabel("Cantidad de Unidades")
    plt.title("Comparativa de Stock Actual vs. Stock Mínimo (Críticos)", fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
def mostrar_reporte_calidad(reporte):
    mostrar_titulo("REPORTE DE CALIDAD DE DATOS")
    print(f"• Registros con campos nulos o vacíos detectados: {reporte['nulos']}")
    print(f"• Registros duplicados descartados/consolidados: {reporte['duplicados']}")
    print(f"• Productos con valores atípicos (precio/stock): {reporte['atipicos']}")
    print("-" * 70)