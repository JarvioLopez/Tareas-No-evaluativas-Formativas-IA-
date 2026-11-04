from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_DATOS = BASE_DIR / "datos_ficticios.xlsx"
CARPETA_SALIDAS = BASE_DIR / "salidas"
CARPETA_GRAFICOS = CARPETA_SALIDAS / "graficos"
COLUMNAS_REQUERIDAS = {"Nombre", "Apellidos", "Edad", "Salario ($)"}
ETIQUETAS_EDAD = ["18-29", "30-39", "40-49", "50-59", "60-70"]


def cargar_datos(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo {ruta.name}. Ejecute primero generar_datos.py."
        )
    dataframe = pd.read_excel(ruta, sheet_name="Empleados")
    faltantes = COLUMNAS_REQUERIDAS - set(dataframe.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {sorted(faltantes)}")
    return dataframe


def limpiar_datos(dataframe: pd.DataFrame) -> pd.DataFrame:
    empleados = dataframe.copy()
    empleados.columns = (
        empleados.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("($)", "usd", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    for columna in ("nombre", "apellidos"):
        empleados[columna] = empleados[columna].astype("string").str.strip()

    empleados["edad"] = pd.to_numeric(empleados["edad"], errors="coerce")
    empleados["salario_usd"] = pd.to_numeric(empleados["salario_usd"], errors="coerce")
    empleados = (
        empleados
        .dropna(subset=["nombre", "apellidos", "edad", "salario_usd"])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    empleados["edad"] = empleados["edad"].astype(int)
    empleados["salario_usd"] = empleados["salario_usd"].astype(float)

    empleados["nombre_completo"] = (
        empleados["nombre"] + " " + empleados["apellidos"]
    )
    empleados["grupo_edad"] = pd.cut(
        empleados["edad"],
        bins=[17, 29, 39, 49, 59, 70],
        labels=ETIQUETAS_EDAD,
    )

    q1 = empleados["salario_usd"].quantile(0.25)
    q3 = empleados["salario_usd"].quantile(0.75)
    empleados["nivel_salarial"] = empleados["salario_usd"].apply(
        lambda salario: "Bajo" if salario <= q1 else ("Alto" if salario >= q3 else "Medio")
    )
    return empleados


def resumen_general(empleados: pd.DataFrame) -> pd.Series:
    return empleados["salario_usd"].agg(
        ["count", "mean", "median", "min", "max", "std"]
    ).round(2)


def resumen_por_grupo_edad(empleados: pd.DataFrame) -> pd.DataFrame:
    return (
        empleados
        .groupby("grupo_edad", observed=True)
        .agg(
            cantidad=("salario_usd", "count"),
            salario_promedio=("salario_usd", "mean"),
            salario_mediano=("salario_usd", "median"),
            salario_minimo=("salario_usd", "min"),
            salario_maximo=("salario_usd", "max"),
            salario_desviacion=("salario_usd", "std"),
        )
        .round(2)
    )


def crear_tabla_dinamica(empleados: pd.DataFrame) -> pd.DataFrame:
    return pd.pivot_table(
        empleados,
        values="salario_usd",
        index="grupo_edad",
        columns="nivel_salarial",
        aggfunc="count",
        fill_value=0,
        observed=True,
    )


def ajustar_ancho_columnas(writer: pd.ExcelWriter, nombre_hoja: str) -> None:
    hoja = writer.sheets[nombre_hoja]
    for columna in hoja.columns:
        longitud = max(
            len(str(celda.value)) if celda.value is not None else 0
            for celda in columna
        )
        hoja.column_dimensions[columna[0].column_letter].width = min(
            max(longitud + 2, 12), 34
        )


def exportar_resultados(
    empleados: pd.DataFrame,
    resumen: pd.DataFrame,
    tabla: pd.DataFrame,
    ruta: Path,
) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        empleados.to_excel(writer, sheet_name="Datos_limpios", index=False)
        resumen.to_excel(writer, sheet_name="Resumen_grupo_edad")
        tabla.to_excel(writer, sheet_name="Tabla_dinamica")
        for hoja in ("Datos_limpios", "Resumen_grupo_edad", "Tabla_dinamica"):
            ajustar_ancho_columnas(writer, hoja)
        writer.sheets["Datos_limpios"].freeze_panes = "A2"


def configurar_estilo() -> None:
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "figure.dpi": 110,
        }
    )


def guardar_figura(figura: plt.Figure, ruta: Path) -> Path:
    figura.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close(figura)
    return ruta


def generar_graficos(empleados: pd.DataFrame, carpeta: Path) -> dict[str, Path]:
    carpeta.mkdir(parents=True, exist_ok=True)
    configurar_estilo()
    rutas = {}

    figura, eje = plt.subplots(figsize=(9, 5))
    sns.histplot(
        data=empleados,
        x="salario_usd",
        bins=20,
        kde=True,
        color="#2563EB",
        ax=eje,
    )
    eje.set_title("Distribución de salarios")
    eje.set_xlabel("Salario en dólares")
    eje.set_ylabel("Cantidad de personas")
    figura.tight_layout()
    rutas["histograma"] = guardar_figura(
        figura, carpeta / "histograma_salarios.png"
    )

    correlacion = empleados["edad"].corr(empleados["salario_usd"])
    figura, eje = plt.subplots(figsize=(9, 5))
    sns.regplot(
        data=empleados,
        x="edad",
        y="salario_usd",
        scatter_kws={"alpha": 0.55, "color": "#2563EB"},
        line_kws={"color": "#DC2626"},
        ax=eje,
    )
    eje.set_title(f"Relación entre edad y salario (r = {correlacion:.3f})")
    eje.set_xlabel("Edad")
    eje.set_ylabel("Salario en dólares")
    figura.tight_layout()
    rutas["dispersion"] = guardar_figura(
        figura, carpeta / "edad_vs_salario.png"
    )

    figura, eje = plt.subplots(figsize=(9, 5))
    sns.barplot(
        data=empleados,
        x="grupo_edad",
        y="salario_usd",
        estimator="mean",
        errorbar=None,
        color="#0F766E",
        ax=eje,
    )
    eje.set_title("Salario promedio por grupo de edad")
    eje.set_xlabel("Grupo de edad")
    eje.set_ylabel("Salario promedio")
    figura.tight_layout()
    rutas["barras"] = guardar_figura(
        figura, carpeta / "promedio_grupo_edad.png"
    )

    figura, eje = plt.subplots(figsize=(9, 5))
    sns.boxplot(
        data=empleados,
        x="grupo_edad",
        y="salario_usd",
        color="#7C3AED",
        ax=eje,
    )
    eje.set_title("Dispersión salarial por grupo de edad")
    eje.set_xlabel("Grupo de edad")
    eje.set_ylabel("Salario en dólares")
    figura.tight_layout()
    rutas["boxplot"] = guardar_figura(
        figura, carpeta / "boxplot_salarios.png"
    )

    correlacion_numerica = empleados[["edad", "salario_usd"]].corr()
    figura, eje = plt.subplots(figsize=(6.4, 4.6))
    sns.heatmap(
        correlacion_numerica,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        square=True,
        ax=eje,
    )
    eje.set_title("Matriz de correlación")
    figura.tight_layout()
    rutas["correlacion"] = guardar_figura(
        figura, carpeta / "correlacion.png"
    )

    figura, ejes = plt.subplots(2, 2, figsize=(14, 9))
    sns.histplot(
        data=empleados,
        x="salario_usd",
        bins=20,
        kde=True,
        color="#2563EB",
        ax=ejes[0, 0],
    )
    ejes[0, 0].set_title("Distribución de salarios")
    ejes[0, 0].set_xlabel("Salario en dólares")
    ejes[0, 0].set_ylabel("Cantidad")

    sns.boxplot(
        data=empleados,
        x="grupo_edad",
        y="salario_usd",
        color="#7C3AED",
        ax=ejes[0, 1],
    )
    ejes[0, 1].set_title("Salarios por grupo de edad")
    ejes[0, 1].set_xlabel("Grupo de edad")
    ejes[0, 1].set_ylabel("Salario en dólares")

    sns.scatterplot(
        data=empleados,
        x="edad",
        y="salario_usd",
        hue="nivel_salarial",
        hue_order=["Bajo", "Medio", "Alto"],
        palette={"Bajo": "#DC2626", "Medio": "#F59E0B", "Alto": "#16A34A"},
        alpha=0.75,
        ax=ejes[1, 0],
    )
    ejes[1, 0].set_title("Edad vs salario por nivel salarial")
    ejes[1, 0].set_xlabel("Edad")
    ejes[1, 0].set_ylabel("Salario en dólares")

    conteo_nivel = (
        empleados["nivel_salarial"]
        .value_counts()
        .reindex(["Bajo", "Medio", "Alto"])
    )
    sns.barplot(
        x=conteo_nivel.index,
        y=conteo_nivel.values,
        hue=conteo_nivel.index,
        palette={"Bajo": "#DC2626", "Medio": "#F59E0B", "Alto": "#16A34A"},
        legend=False,
        ax=ejes[1, 1],
    )
    ejes[1, 1].set_title("Cantidad por nivel salarial")
    ejes[1, 1].set_xlabel("Nivel salarial")
    ejes[1, 1].set_ylabel("Cantidad")

    figura.suptitle("Dashboard exploratorio de empleados", fontsize=16, fontweight="bold")
    figura.tight_layout()
    rutas["dashboard"] = guardar_figura(
        figura, carpeta / "dashboard_empleados.png"
    )
    return rutas


def main() -> None:
    print("=" * 74)
    print("ANALISIS EXPLORATORIO DE EMPLEADOS CON PANDAS")
    print("=" * 74)

    if not ARCHIVO_DATOS.exists():
        from generar_datos import generar_dataframe, guardar_excel

        guardar_excel(generar_dataframe(), ARCHIVO_DATOS)
        print(f"Dataset generado automaticamente: {ARCHIVO_DATOS.name}")

    dataframe = cargar_datos(ARCHIVO_DATOS)
    print("\n[1] Carga y vista previa del archivo Excel")
    print(f"Dimensiones: {dataframe.shape[0]} filas x {dataframe.shape[1]} columnas")
    print(dataframe.head(8).to_string(index=False))

    print("\n[2] Información general del DataFrame")
    dataframe.info()

    print("\n[3] Valores faltantes por columna")
    print(dataframe.isna().sum().to_string())

    empleados = limpiar_datos(dataframe)
    print("\n[4] Limpieza y columnas calculadas")
    print(f"Columnas normalizadas: {empleados.columns.tolist()}")
    print(f"Registros útiles: {len(empleados)}")

    print("\n[5] Estadísticas descriptivas de variables numéricas")
    print(empleados[["edad", "salario_usd"]].describe().round(2).to_string())

    print("\n[6] Resumen general del salario")
    print(resumen_general(empleados).to_string())

    resumen_grupo = resumen_por_grupo_edad(empleados)
    print("\n[7] Resumen salarial por grupo de edad")
    print(resumen_grupo.to_string(line_width=110))

    tabla = crear_tabla_dinamica(empleados)
    print("\n[8] Tabla dinámica: grupo de edad por nivel salarial")
    print(tabla.to_string())

    correlacion = empleados["edad"].corr(empleados["salario_usd"])
    print("\n[9] Analisis de Relación entre edad y salario")
    print(f"Coeficiente de correlación de Pearson: {correlacion:.3f}")

    mejor_grupo = resumen_grupo["salario_promedio"].idxmax()
    grupo_disperso = resumen_grupo["salario_desviacion"].idxmax()
    print("\n[10] Respuestas a las preguntas de análisis")
    print(f"Edad promedio: {empleados['edad'].mean():.1f} años")
    print(f"Salario promedio: ${empleados['salario_usd'].mean():,.2f}")
    print(f"Salario mediano: ${empleados['salario_usd'].median():,.2f}")
    print(
        f"Grupo con mayor salario promedio: {mejor_grupo} "
        f"(${resumen_grupo.loc[mejor_grupo, 'salario_promedio']:,.2f})"
    )
    print(
        f"Grupo con mayor dispersión salarial: {grupo_disperso} "
        f"(desviación estándar ${resumen_grupo.loc[grupo_disperso, 'salario_desviacion']:,.2f})"
    )
    print(
        "La media y la mediana pueden diferir porque la media es sensible a "
        "salarios extremos, mientras que la mediana representa el valor central."
    )
    print(
        f"La edad explica parcialmente el salario: la correlación es {correlacion:.3f}, "
        "por lo que existen otros factores no incluidos en el dataset."
    )

    ruta_excel = CARPETA_SALIDAS / "resumen_empleados.xlsx"
    exportar_resultados(empleados, resumen_grupo, tabla, ruta_excel)
    print(f"\n[11] Resultados exportados: {ruta_excel.relative_to(BASE_DIR)}")

    rutas = generar_graficos(empleados, CARPETA_GRAFICOS)
    print("\n[12] Gráficos generados")
    for nombre, ruta in rutas.items():
        print(f"{nombre}: {ruta.relative_to(BASE_DIR)}")

    print("\n[13] Conclusión ejecutiva")
    print(
        f"Se analizaron {len(empleados)} empleados con una edad promedio de "
        f"{empleados['edad'].mean():.1f} años. El salario promedio es de "
        f"${empleados['salario_usd'].mean():,.2f} y la mediana de "
        f"${empleados['salario_usd'].median():,.2f}. El grupo {mejor_grupo} "
        "concentra el mayor salario promedio, mientras que la correlación entre "
        f"edad y salario es {correlacion:.3f}. Esto sugiere una relación positiva "
        "alta: la edad aporta información, pero no determina por sí sola el "
        "salario. El dataset es ficticio y no incorpora experiencia, cargo, "
        "ubicación ni antigüedad, por lo que sus hallazgos son exploratorios."
    )


if __name__ == "__main__":
    main()



