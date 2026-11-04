# Práctica 04 — Pandas, Excel y gráficos avanzados

Análisis exploratorio de 500 empleados ficticios: carga del Excel, limpieza, estadísticas, agrupaciones, tabla dinámica, correlación, exportación y seis visualizaciones.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Enunciado_Pandas_Excel_Graficos.docx` | Enunciado original de la práctica. |
| `Solucion_Pandas_Excel_Graficos.docx` | Documento de entrega con metodología, resultados y gráficos. |
| `Solucion_Pandas_Excel_Graficos.pdf` | Versión PDF del documento de entrega. |
| `datos_ficticios.xlsx` | Dataset reproducible de 500 empleados. |
| `generar_datos.py` | Genera el Excel con semilla fija. |
| `analisis_empleados.py` | Pipeline completo de análisis y visualización. |
| `salida_analisis.txt` | Evidencia de la ejecución completa. |
| `requirements.txt` | Dependencias del proyecto. |
| `salidas/resumen_empleados.xlsx` | Excel con datos limpios, resumen y tabla dinámica. |
| `salidas/graficos/` | Seis figuras PNG, incluido el dashboard. |

## Requisitos

- Python 3.14 o compatible.
- `pandas`, `openpyxl`, `matplotlib`, `seaborn` y `numpy`.

```powershell
py -m pip install -r requirements.txt
```

## Ejecución

Generar de nuevo el dataset reproducible:

```powershell
py generar_datos.py
```

Ejecutar el análisis completo:

```powershell
py analisis_empleados.py
```

El segundo comando imprime trece bloques de resultados, exporta el Excel y regenera las seis figuras. No requiere entradas por teclado.

## Resultados principales

- 500 registros y 4 columnas originales, sin valores nulos.
- Edad promedio: 44.1 años.
- Salario promedio: $3,585.46; mediana: $3,640.00.
- Grupo con mayor salario promedio: 60-70 ($4,702.72).
- Grupo con mayor dispersión: 40-49 (desviación estándar $887.57).
- Correlación de Pearson entre edad y salario: 0.722.

## Salidas

- `salidas/resumen_empleados.xlsx`
- `salidas/graficos/histograma_salarios.png`
- `salidas/graficos/edad_vs_salario.png`
- `salidas/graficos/promedio_grupo_edad.png`
- `salidas/graficos/boxplot_salarios.png`
- `salidas/graficos/correlacion.png`
- `salidas/graficos/dashboard_empleados.png`

El código no incluye comentarios ni marcas de edición. La explicación metodológica y las respuestas a las preguntas están en el documento Word.
