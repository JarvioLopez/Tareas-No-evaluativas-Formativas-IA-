from pathlib import Path
import random

import pandas as pd

NOMBRES = [
    "Amber", "George", "Roger", "Albert", "Pamela", "Dylan", "Melissa", "Darius",
    "Laura", "Carlos", "Sofia", "Miguel", "Valeria", "Andres", "Camila", "Javier",
    "Daniela", "Fernando", "Gabriela", "Hector", "Isabel", "Jorge", "Karla", "Luis",
    "Monica", "Nicolas", "Patricia", "Ricardo", "Sandra", "Tomas",
]

APELLIDOS = [
    "Russell Harper", "Wright Marshall", "Henry Jacobs", "Tyler Best", "Watson Delacruz",
    "Wells White", "Burton Howell", "Lewis Gregory", "Ramirez Torres", "Gonzalez Ruiz",
    "Martinez Lopez", "Hernandez Diaz", "Perez Moreno", "Sanchez Romero", "Flores Vargas",
    "Rivera Castro", "Gomez Ortiz", "Diaz Munoz", "Vasquez Rojas", "Rojas Medina",
    "Silva Navarro", "Mendoza Reyes", "Cruz Aguilar", "Ortiz Pena", "Castillo Ramos",
    "Morales Herrera", "Jimenez Vega", "Ruiz Campos", "Chavez Salazar", "Guerrero Luna",
]

COLUMNAS = ["Nombre", "Apellidos", "Edad", "Salario ($)"]
CANTIDAD_REGISTROS = 500
SEMILLA = 2026


def generar_registros(cantidad: int, semilla: int) -> list[dict[str, object]]:
    generador = random.Random(semilla)
    registros = []
    for _ in range(cantidad):
        nombre = generador.choice(NOMBRES)
        apellidos = generador.choice(APELLIDOS)
        edad = generador.randint(18, 70)
        salario_base = 1200 + edad * 55 + generador.gauss(0, 850)
        salario = max(1500, min(9500, round(salario_base / 10) * 10))
        registros.append(
            {
                "Nombre": nombre,
                "Apellidos": apellidos,
                "Edad": edad,
                "Salario ($)": salario,
            }
        )
    return registros


def generar_dataframe(cantidad: int = CANTIDAD_REGISTROS, semilla: int = SEMILLA) -> pd.DataFrame:
    return pd.DataFrame(generar_registros(cantidad, semilla), columns=COLUMNAS)


def guardar_excel(dataframe: pd.DataFrame, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        dataframe.to_excel(writer, sheet_name="Empleados", index=False)
        hoja = writer.sheets["Empleados"]
        for columna in hoja.columns:
            longitud = max(
                len(str(celda.value)) if celda.value is not None else 0
                for celda in columna
            )
            hoja.column_dimensions[columna[0].column_letter].width = min(
                max(longitud + 2, 12), 32
            )


def main() -> None:
    ruta = Path(__file__).with_name("datos_ficticios.xlsx")
    dataframe = generar_dataframe()
    guardar_excel(dataframe, ruta)
    print(f"Archivo generado: {ruta.name}")
    print(f"Registros: {len(dataframe)}")
    print(dataframe.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
