# A01796262_A5.2

Actividad 5.2 - Ejercicio de programacion 2 y analisis estatico.

## Descripcion del proyecto
Este proyecto implementa `computeSales.py`, un programa en Python que calcula
el total monetario de ventas usando:
- Un catalogo de productos en formato JSON (titulo y precio).
- Un registro de ventas en formato JSON (producto y cantidad).

El script:
- Se ejecuta por linea de comandos con dos archivos de entrada.
- Calcula el total considerando cada venta y el precio del catalogo.
- Reporta errores de datos sin detener toda la ejecucion.
- Muestra resultados en consola y los guarda en `SalesResults.txt`.
- Incluye tiempo de ejecucion en el reporte final.

## Estructura relevante
- `computeSales.py`: programa principal.
- `test_data/`: datos de apoyo y casos de prueba (TC1, TC2, TC3).
- `tests/test_compute_sales.py`: pruebas unitarias automatizadas.
- `TEST_EVIDENCE.md`: evidencia de comandos utilizados.

## Requisitos
- Python 3.10+ (probado con Python 3.12).
- `flake8` y `pylint` instalados para analisis estatico.

## Como ejecutar el programa
Formato minimo solicitado por la actividad:

```bash
python3 computeSales.py <priceCatalogue.json> <salesRecord.json>
```

Ejemplo con TC1:

```bash
python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC1/TC1.Sales.json
```

Ejemplos adicionales:

```bash
python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC2/TC2.Sales.json
python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC3/TC3.Sales.json
```

## Salida esperada
En consola y en `SalesResults.txt` se genera un reporte con:
- Total calculado (`TOTAL`).
- Tiempo de ejecucion (`EXECUTION_TIME_SECONDS`).
- Cantidad de errores detectados (`ERROR_COUNT`).
- Detalle de errores recuperables (por ejemplo, productos no existentes).

## Comandos de validacion
Ejecutar pruebas unitarias:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Revisar estilo con flake8:

```bash
flake8 computeSales.py tests/test_compute_sales.py
```

Revisar analisis estatico con pylint:

```bash
PYLINTHOME=/tmp/pylint pylint computeSales.py tests/test_compute_sales.py
```

## Casos de prueba incluidos
Datos disponibles en `test_data/`:
- `test_data/TC1/TC1.ProductList.json`
- `test_data/TC1/TC1.Sales.json`
- `test_data/TC2/TC2.Sales.json`
- `test_data/TC3/TC3.Sales.json`
- `test_data/expected_results.txt`
