# Práctica 01 — Fundamentos de Python

Solución completa de los ejercicios de sintaxis, control de flujo, funciones, colecciones, Pandas, visualización, POO, archivos, programación funcional, asincronía y pruebas unitarias.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Enunciado_Fundamentos_Python.docx` | Enunciado original de la práctica. |
| `Solucion_Fundamentos_Python.docx` | Documento de entrega con explicación, código y evidencias. |
| `Solucion_Fundamentos_Python.pdf` | Versión PDF del documento de entrega. |
| `soluciones_fundamentos.py` | Programa principal con las soluciones y el menú interactivo. |
| `utilidades.py` | Módulo de conversión de millas a kilómetros. |
| `test_soluciones.py` | Pruebas unitarias con `unittest`. |
| `requirements.txt` | Dependencias de Python. |
| `salidas/` | Archivos CSV, TXT y gráficos generados al ejecutar. |

## Requisitos

- Python 3.14 o compatible con anotaciones modernas.
- `pandas` y `matplotlib`.

```powershell
py -m pip install -r requirements.txt
```

## Ejecución

Demostración automática de todas las soluciones:

```powershell
py soluciones_fundamentos.py --demo
```

Menú interactivo:

```powershell
py soluciones_fundamentos.py
```

El menú agrupa las soluciones en veinte opciones interactivas. Cada opción solicita los datos necesarios y muestra el resultado en consola; la calculadora y las soluciones que leen datos piden entradas por teclado.

## Pruebas

```powershell
py -m unittest -v
```

Se ejecutan siete pruebas sobre la resta y la verificación de listas ordenadas. El resultado esperado es `OK`.

## Salidas generadas

- `salidas/nombres.txt` y `salidas/nombres_doc.txt`
- `salidas/estudiantes.csv` y `salidas/estudiantes_doc.csv`
- `salidas/graficos/ventas_mensuales.png`
- `salidas/graficos/temperatura_semanal.png`
- `salidas/graficos/preferencias_frutas.png`

El código no incluye comentarios ni marcas de edición. Los nombres de funciones, clases y variables describen su propósito.
