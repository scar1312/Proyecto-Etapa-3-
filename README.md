# Progresiva – Sistema de inventario y punto de venta

Proyecto Integrador, Etapa 3 – **II1119 Fundamentos para tecnologías digitales**
Universidad de Costa Rica, Sede Interuniversitaria de Alajuela – II Ciclo 2026 – Grupo 5

Programa de consola en Python para la tienda de ropa "Progresiva". Permite controlar el inventario,
registrar ventas con IVA, recibir mercancía, generar alertas y ver reportes gráficos. Usa el patrón
Modelo-Vista-Controlador (MVC) y guarda los datos en archivos CSV, de modo que se conservan entre sesiones.

## Funcionalidades

- Registro de productos y recepción de mercancía (actualización de stock).
- Ventas con cálculo de IVA (13 %), número de factura consecutivo y descuento automático de stock.
- Alertas de reposición (stock bajo) y de caducidad.
- Persistencia en `datos/inventario.csv` y `datos/ventas.csv`: los datos se cargan al iniciar y se guardan con cada cambio.
- Limpieza de datos al cargar archivos: nulos, duplicados y valores atípicos, con reporte de calidad.
- Filtrado del inventario (categoría, rango de precio, estado de stock) y ordenamiento (nombre, stock, precio).
- Dos gráficos con matplotlib: ventas por categoría y stock actual vs. stock mínimo.

## Requisitos

- Python 3.8 o superior
- matplotlib (se instala con `requirements.txt`)

## Cómo ejecutarlo

1. Descargar o clonar el repositorio.
2. Abrir una terminal en la carpeta principal del proyecto e instalar la dependencia:

   ```
   pip install -r requirements.txt
   ```

3. Entrar a la carpeta `codigo` y ejecutar el programa:

   ```
   cd codigo
   python main.py
   ```

   (En Windows también funciona `py main.py`.)

La primera vez, si el inventario está vacío, se carga automáticamente el catálogo inicial `datos/datos_prueba.csv`.

## Menú principal

| Opción | Qué hace |
|---|---|
| 1 | Registrar producto |
| 2 | Actualizar stock (recepción de mercancía) |
| 3 | Realizar venta |
| 4 | Generar alertas |
| 5 | Consultar inventario |
| 6 | Consultar historial de ventas |
| 7 | Cargar datos de prueba (`datos_prueba.csv` o `datos_sucios.csv`) |
| 8 | Gráfico: ventas por categoría |
| 9 | Gráfico: stock crítico (actual vs. mínimo) |
| 10 | Reporte de calidad de datos |
| 11 | Filtrar inventario |
| 12 | Ordenar inventario |
| 0 | Salir |

## Estructura del proyecto

```
├── README.md
├── requirements.txt
├── codigo/
│   ├── main.py          Punto de entrada
│   ├── modelo.py        Datos en memoria, limpieza y lectura/escritura de CSV
│   ├── vista.py         Menús, tablas, mensajes y gráficos
│   └── controlador.py   Lógica de negocio y validaciones
├── datos/
│   ├── inventario.csv   Catálogo guardado
│   ├── ventas.csv       Historial de ventas
│   ├── datos_prueba.csv Catálogo inicial (13 productos)
│   └── datos_sucios.csv Datos con errores para probar la limpieza
├── diagramas/           Diagramas de componentes y de flujo (.drawio)
├── evidencias/          Capturas de pantalla de las pruebas
└── coevaluacion/        Tabla de coevaluación entre pares
```

La documentación completa (manual de usuario y técnico, y plan de pruebas) se entrega en los archivos
`manual_usuario_tecnico.pdf` y `plan_de_pruebas.pdf`.

## Integrantes

- Melani Mena Sánchez
- Scarlett Fuentes Díaz
- Dariell Herrera Fuentes
- Noelia Hernández Sibaja