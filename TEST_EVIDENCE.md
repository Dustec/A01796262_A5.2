# Evidencia de ejecucion

## Casos de prueba de la actividad
Catalogo usado: `test_data/TC1/TC1.ProductList.json`

1. `python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC1/TC1.Sales.json`
Resultado total esperado: `2481.86`

2. `python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC2/TC2.Sales.json`
Resultado total esperado: `166568.23`

3. `python3 computeSales.py test_data/TC1/TC1.ProductList.json test_data/TC3/TC3.Sales.json`
Resultado total esperado: `165235.37`

## Analisis estatico
1. `flake8 computeSales.py`
2. `PYLINTHOME=/tmp/pylint pylint computeSales.py`

## Pruebas unitarias
`python3 -m unittest discover -s tests -p "test_*.py"`
