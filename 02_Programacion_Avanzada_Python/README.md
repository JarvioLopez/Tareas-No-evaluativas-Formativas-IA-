# Práctica 02 — Programación Avanzada en Python

Solución de los seis apartados de la práctica: tipado estático y dinámico, duck typing, closures y binding, multiple dispatch, clases abiertas y mixins con traits.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Enunciado_Programacion_Avanzada_Python.docx` | Enunciado original de la práctica. |
| `Solucion_Programacion_Avanzada_Python.docx` | Documento de entrega con explicación, código y salidas. |
| `Solucion_Programacion_Avanzada_Python.pdf` | Versión PDF del documento de entrega. |
| `practica_avanzada.py` | Programa único con todas las soluciones. |
| `requirements.txt` | Dependencia externa `multipledispatch`. |

## Requisitos

- Python 3.14 o compatible.
- `multipledispatch`.

```powershell
py -m pip install -r requirements.txt
```

## Ejecución

```powershell
py practica_avanzada.py
```

El programa es autocontenido y muestra en consola, en orden, la salida de cada parte:

1. Cálculo de suma, promedio, máximo y mínimo con anotaciones de tipo.
2. Clases `Telefono`, `Alarma` y `Computadora` mediante duck typing.
3. Closure incrementador y comparación entre late binding y early binding.
4. Función `mezclar` con multiple dispatch para enteros, listas y cadenas.
5. Incorporación dinámica del método `saludar` a la clase `Usuario`.
6. Mixin `LoggerMixin`, sensor avanzado y trait `MedibleTrait`.

## Resultado esperado

La ejecución termina con las mediciones `23.5` y `61.0`, correspondientes a las dos clases que implementan el trait. No se requieren entradas por teclado.

El código no incluye comentarios ni marcas de edición. La explicación completa está en el documento Word.
