import asyncio
import math
import sys
import time
from functools import reduce
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from utilidades import millas_a_kilometros

BASE_DIR = Path(__file__).resolve().parent
SALIDAS_DIR = BASE_DIR / "salidas"
GRAFICOS_DIR = SALIDAS_DIR / "graficos"


def solicitar_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Entrada invalida. Ingrese un numero.")


def solicitar_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada invalida. Ingrese un numero entero.")


def solicitar_lista_numeros(mensaje: str) -> list[float]:
    texto = input(mensaje)
    return [float(parte.strip()) for parte in texto.split(",") if parte.strip()]


def promedio_tres_numeros(a: float, b: float, c: float) -> float:
    return (a + b + c) / 3


def celsius_a_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def area_triangulo(base: float, altura: float) -> float:
    return base * altura / 2


def puede_votar(edad: int) -> bool:
    if edad < 0:
        raise ValueError("La edad no puede ser negativa.")
    return edad >= 18


def tabla_multiplicar(numero: int, limite: int = 10) -> list[str]:
    return [f"{numero} x {valor} = {numero * valor}" for valor in range(1, limite + 1)]


def menu_calculadora() -> None:
    while True:
        print("\n1. Sumar")
        print("2. Restar")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "3":
            print("Calculadora finalizada.")
            return
        if opcion not in {"1", "2"}:
            print("Opcion invalida.")
            continue
        primer_numero = solicitar_float("Primer numero: ")
        segundo_numero = solicitar_float("Segundo numero: ")
        resultado = (
            primer_numero + segundo_numero
            if opcion == "1"
            else primer_numero - segundo_numero
        )
        print(f"Resultado: {resultado:.2f}")


def factorial(numero: int) -> int:
    if numero < 0:
        raise ValueError("El factorial no esta definido para numeros negativos.")
    resultado = 1
    for valor in range(2, numero + 1):
        resultado *= valor
    return resultado


def es_primo(numero: int) -> bool:
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    limite = math.isqrt(numero)
    for divisor in range(3, limite + 1, 2):
        if numero % divisor == 0:
            return False
    return True


def mayor_lista(numeros: Sequence[float]) -> float:
    if not numeros:
        raise ValueError("La lista no puede estar vacia.")
    return max(numeros)


def mayores_de_edad(personas: dict[str, int]) -> dict[str, int]:
    return {
        nombre: edad
        for nombre, edad in personas.items()
        if edad >= 18
    }


def ordenar_numeros(numeros: Iterable[float]) -> list[float]:
    return sorted(numeros)


def eliminar_duplicados(elementos: Iterable[object]) -> set[object]:
    return set(elementos)


def crear_dataframe_estudiantes() -> pd.DataFrame:
    datos = {
        "Estudiante": ["Ana", "Luis", "Maria", "Carlos", "Sofia", "Diego"],
        "Nota 1": [85, 62, 91, 74, 58, 88],
        "Nota 2": [90, 70, 87, 68, 65, 92],
        "Nota 3": [78, 55, 95, 80, 72, 85],
    }
    dataframe = pd.DataFrame(datos)
    dataframe["Promedio"] = (
        dataframe[["Nota 1", "Nota 2", "Nota 3"]]
        .mean(axis=1)
        .round(2)
    )
    return dataframe


def filtrar_estudiantes_aprobados(
    dataframe: pd.DataFrame, umbral: float = 70
) -> pd.DataFrame:
    return dataframe[dataframe["Promedio"] > umbral].copy()


def agregar_estado(dataframe: pd.DataFrame, umbral: float = 70) -> pd.DataFrame:
    resultado = dataframe.copy()
    resultado["Estado"] = resultado["Promedio"].apply(
        lambda nota: "Aprobado" if nota >= umbral else "Reprobado"
    )
    return resultado


def guardar_csv_estudiantes(dataframe: pd.DataFrame, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(ruta, index=False, encoding="utf-8")


def leer_primeros_registros(ruta: Path, cantidad: int = 5) -> pd.DataFrame:
    return pd.read_csv(ruta, encoding="utf-8").head(cantidad)


def guardar_figura(figura: Figure, nombre: str) -> Path:
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    ruta = GRAFICOS_DIR / nombre
    figura.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close(figura)
    return ruta


def grafico_barras_ventas() -> Path:
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
    ventas = [1200, 1500, 1800, 1650, 2100, 2400]
    figura, eje = plt.subplots(figsize=(8, 4.8))
    barras = eje.bar(meses, ventas, color="#2563EB", edgecolor="#1E3A8A")
    eje.set_title("Ventas mensuales del negocio")
    eje.set_xlabel("Mes")
    eje.set_ylabel("Ventas (USD)")
    eje.grid(axis="y", linestyle="--", alpha=0.4)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    eje.bar_label(barras, fmt="%d", padding=3)
    return guardar_figura(figura, "ventas_mensuales.png")


def grafico_lineas_temperatura() -> Path:
    dias = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
    temperaturas = [22, 24, 23, 25, 27, 26, 24]
    figura, eje = plt.subplots(figsize=(8, 4.8))
    eje.plot(
        dias,
        temperaturas,
        marker="o",
        markersize=7,
        linewidth=2.5,
        color="#DC2626",
    )
    eje.fill_between(dias, temperaturas, color="#DC2626", alpha=0.12)
    eje.set_title("Temperatura promedio durante siete dias")
    eje.set_xlabel("Dia")
    eje.set_ylabel("Temperatura (C)")
    eje.grid(axis="y", linestyle="--", alpha=0.4)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    return guardar_figura(figura, "temperatura_semanal.png")


def grafico_circular_frutas() -> Path:
    frutas = ["Manzana", "Banana", "Naranja", "Uva", "Pera"]
    cantidades = [35, 25, 20, 12, 8]
    colores = ["#EF4444", "#F59E0B", "#FB923C", "#8B5CF6", "#84CC16"]
    figura, eje = plt.subplots(figsize=(6.8, 5.6))
    eje.pie(
        cantidades,
        labels=frutas,
        colors=colores,
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.04] * len(frutas),
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    eje.set_title("Preferencias de fruta del grupo")
    eje.axis("equal")
    return guardar_figura(figura, "preferencias_frutas.png")


class Coche:
    def __init__(self, marca: str, modelo: str) -> None:
        self.marca = marca
        self.modelo = modelo

    def mostrar(self) -> str:
        return f"Coche: {self.marca} {self.modelo}"


class Persona:
    def __init__(self, nombre: str, edad: int) -> None:
        self.nombre = nombre
        self.edad = edad

    def es_mayor_de_edad(self) -> bool:
        return self.edad >= 18

    def describir(self) -> str:
        estado = "mayor de edad" if self.es_mayor_de_edad() else "menor de edad"
        return f"{self.nombre} tiene {self.edad} anos y es {estado}"


class Animal:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def hablar(self) -> str:
        return "Sonido generico"

    def presentarse(self) -> str:
        return f"{self.nombre}: {self.hablar()}"


class Perro(Animal):
    def hablar(self) -> str:
        return "Guau guau"


class EdadInvalidaError(ValueError):
    pass


def validar_edad(edad: int) -> int:
    if edad < 0:
        raise EdadInvalidaError("La edad no puede ser negativa.")
    return edad


def obtener_elemento(secuencia: Sequence[object], indice: int) -> object | None:
    try:
        return secuencia[indice]
    except IndexError:
        print("Error capturado: indice fuera de rango.")
        return None


def guardar_nombres(ruta: Path, nombres: Iterable[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        for nombre in nombres:
            archivo.write(f"{nombre}\n")


def leer_nombres(ruta: Path) -> list[str]:
    with ruta.open("r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def filtrar_pares(numeros: Iterable[int]) -> list[int]:
    return list(filter(lambda numero: numero % 2 == 0, numeros))


def multiplicar_elementos(numeros: Iterable[float]) -> float:
    return reduce(lambda acumulado, numero: acumulado * numero, numeros, 1)


async def tarea_asincrona(nombre: str, duracion: float) -> str:
    print(f"{nombre}: inicio")
    await asyncio.sleep(duracion)
    print(f"{nombre}: fin")
    return nombre


async def ejecutar_tareas_en_paralelo() -> list[str]:
    return await asyncio.gather(
        tarea_asincrona("Tarea A", 1.0),
        tarea_asincrona("Tarea B", 1.0),
    )


async def descargar_archivo(nombre: str, duracion: float) -> str:
    print(f"Descargando {nombre}...")
    await asyncio.sleep(duracion)
    print(f"{nombre} descargado.")
    return nombre


async def simular_descargas() -> list[str]:
    inicio = time.perf_counter()
    resultados = await asyncio.gather(
        descargar_archivo("documento.pdf", 1.2),
        descargar_archivo("imagen.png", 0.8),
        descargar_archivo("datos.csv", 1.0),
    )
    print(f"Tiempo total de descarga: {time.perf_counter() - inicio:.2f} segundos")
    return resultados


def restar(a: float, b: float) -> float:
    return a - b


def esta_ordenada(numeros: Sequence[float]) -> bool:
    return all(
        numeros[indice] <= numeros[indice + 1]
        for indice in range(len(numeros) - 1)
    )


def mostrar_titulo(titulo: str) -> None:
    print("\n" + "=" * 72)
    print(titulo)
    print("=" * 72)


def ejecutar_demo() -> None:
    mostrar_titulo("FUNDAMENTOS DE PYTHON - DEMOSTRACION DE SOLUCIONES")

    print("\n[1] Promedio de tres numeros")
    print(f"Promedio de 8, 9 y 10: {promedio_tres_numeros(8, 9, 10):.2f}")

    print("\n[2] Conversion de Celsius a Fahrenheit")
    print(f"25 C = {celsius_a_fahrenheit(25):.2f} F")

    print("\n[3] Area de un triangulo")
    print(f"Base 10 y altura 6: {area_triangulo(10, 6):.2f}")

    print("\n[4] Validacion para votar")
    for edad in (16, 18, 30):
        print(f"Edad {edad}: {'puede votar' if puede_votar(edad) else 'no puede votar'}")

    print("\n[5] Tabla de multiplicar del 7")
    for linea in tabla_multiplicar(7):
        print(linea)

    print("\n[6] Menu de calculadora")
    print("La calculadora interactiva se ejecuta con la opcion 6 del menu principal.")

    print("\n[7] Factorial")
    for numero in (0, 5, 7):
        print(f"{numero}! = {factorial(numero)}")

    print("\n[8] Numeros primos")
    print(f"17 es primo: {es_primo(17)}")
    print(f"21 es primo: {es_primo(21)}")

    print("\n[9] Mayor de una lista")
    print(f"Mayor de [12, 45, 7, 31]: {mayor_lista([12, 45, 7, 31])}")

    print("\n[10] Personas mayores de edad")
    personas = {"Ana": 17, "Luis": 25, "Maria": 30, "Pedro": 15}
    print(mayores_de_edad(personas))

    print("\n[11] Ordenamiento de una lista")
    print(ordenar_numeros([9, 3, 7, 1, 5]))

    print("\n[12] Eliminacion de duplicados")
    print(sorted(eliminar_duplicados([1, 2, 2, 3, 4, 4, 5])))

    print("\n[13] Modulo utilidades")
    print(f"10 millas = {millas_a_kilometros(10):.2f} kilometros")

    print("\n[14] DataFrame de estudiantes")
    estudiantes = crear_dataframe_estudiantes()
    print(estudiantes.to_string(index=False))
    print(f"Promedio general del curso: {estudiantes['Promedio'].mean():.2f}")

    print("\n[15] Estudiantes con promedio mayor a 70")
    aprobados = filtrar_estudiantes_aprobados(estudiantes)
    print(aprobados[["Estudiante", "Promedio"]].to_string(index=False))

    print("\n[16] Estado academico")
    print(agregar_estado(estudiantes).to_string(index=False))

    ruta_csv = SALIDAS_DIR / "estudiantes.csv"
    guardar_csv_estudiantes(estudiantes, ruta_csv)

    print("\n[17] Lectura de las primeras cinco filas del CSV")
    print(leer_primeros_registros(ruta_csv).to_string(index=False))

    print("\n[18] Graficos con matplotlib")
    rutas = [
        grafico_barras_ventas(),
        grafico_lineas_temperatura(),
        grafico_circular_frutas(),
    ]
    for ruta in rutas:
        print(f"Grafico generado: {ruta.relative_to(BASE_DIR)}")

    print("\n[19] Programacion orientada a objetos")
    coche = Coche("Toyota", "Corolla")
    persona = Persona("Ana", 20)
    perro = Perro("Firulais")
    print(coche.mostrar())
    print(persona.describir())
    print(perro.presentarse())

    print("\n[20] Manejo de excepciones")
    print(f"Elemento en indice 5: {obtener_elemento([10, 20, 30], 5)}")
    try:
        validar_edad(-3)
    except EdadInvalidaError as error:
        print(f"Excepcion personalizada: {error}")

    print("\n[21] Manejo de archivos")
    ruta_nombres = SALIDAS_DIR / "nombres.txt"
    guardar_nombres(ruta_nombres, ["Ana", "Luis", "Maria"])
    print(f"Nombres leidos: {leer_nombres(ruta_nombres)}")

    print("\n[22] Programacion funcional")
    numeros = [1, 2, 3, 4, 5, 6]
    print(f"Pares: {filtrar_pares(numeros)}")
    print(f"Producto: {multiplicar_elementos(numeros)}")

    print("\n[23] Programacion asincrona")
    tareas = asyncio.run(ejecutar_tareas_en_paralelo())
    print(f"Tareas completadas: {tareas}")
    descargas = asyncio.run(simular_descargas())
    print(f"Descargas completadas: {descargas}")

    print("\n[24] Funciones para pruebas unitarias")
    print(f"restar(10, 4) = {restar(10, 4)}")
    print(f"esta_ordenada([1, 2, 3]) = {esta_ordenada([1, 2, 3])}")
    print(f"esta_ordenada([3, 1, 2]) = {esta_ordenada([3, 1, 2])}")

    print("\nDemostracion finalizada correctamente.")


def interactivo_promedio() -> None:
    valores = [solicitar_float(f"Numero {indice}: ") for indice in range(1, 4)]
    print(f"Promedio: {promedio_tres_numeros(*valores):.2f}")


def interactivo_celsius() -> None:
    celsius = solicitar_float("Temperatura en Celsius: ")
    print(f"Temperatura en Fahrenheit: {celsius_a_fahrenheit(celsius):.2f}")


def interactivo_area() -> None:
    base = solicitar_float("Base: ")
    altura = solicitar_float("Altura: ")
    print(f"Area: {area_triangulo(base, altura):.2f}")


def interactivo_votar() -> None:
    edad = solicitar_entero("Edad: ")
    print("Puede votar." if puede_votar(edad) else "No puede votar.")


def interactivo_tabla() -> None:
    numero = solicitar_entero("Numero: ")
    for linea in tabla_multiplicar(numero):
        print(linea)


def interactivo_factorial() -> None:
    numero = solicitar_entero("Numero: ")
    print(f"Factorial: {factorial(numero)}")


def interactivo_primo() -> None:
    numero = solicitar_entero("Numero: ")
    print("Es primo." if es_primo(numero) else "No es primo.")


def interactivo_mayor() -> None:
    numeros = solicitar_lista_numeros("Numeros separados por coma: ")
    print(f"Mayor: {mayor_lista(numeros)}")


def interactivo_colecciones() -> None:
    personas = {}
    for indice in range(1, 4):
        nombre = input(f"Nombre {indice}: ").strip()
        personas[nombre] = solicitar_entero(f"Edad de {nombre}: ")
    print(f"Mayores de edad: {mayores_de_edad(personas)}")
    numeros = solicitar_lista_numeros("Numeros separados por coma: ")
    print(f"Ordenados: {ordenar_numeros(numeros)}")
    print(f"Sin duplicados: {sorted(eliminar_duplicados(numeros))}")


def interactivo_millas() -> None:
    millas = solicitar_float("Millas: ")
    print(f"Kilometros: {millas_a_kilometros(millas):.3f}")


def interactivo_pandas() -> None:
    estudiantes = crear_dataframe_estudiantes()
    print(estudiantes.to_string(index=False))
    print(f"Promedio general: {estudiantes['Promedio'].mean():.2f}")
    print("\nPromedio mayor a 70:")
    print(filtrar_estudiantes_aprobados(estudiantes).to_string(index=False))
    print("\nEstado academico:")
    print(agregar_estado(estudiantes).to_string(index=False))


def interactivo_graficos() -> None:
    rutas = [
        grafico_barras_ventas(),
        grafico_lineas_temperatura(),
        grafico_circular_frutas(),
    ]
    for ruta in rutas:
        print(f"Grafico generado: {ruta}")


def interactivo_poo() -> None:
    coche = Coche("Honda", "Civic")
    persona = Persona("Carlos", 17)
    perro = Perro("Rex")
    print(coche.mostrar())
    print(persona.describir())
    print(perro.presentarse())


def interactivo_excepciones() -> None:
    indice = solicitar_entero("Indice a consultar: ")
    print(f"Resultado: {obtener_elemento([10, 20, 30], indice)}")
    try:
        edad = solicitar_entero("Edad para validar: ")
        validar_edad(edad)
        print("Edad valida.")
    except EdadInvalidaError as error:
        print(f"Error: {error}")


def interactivo_archivos() -> None:
    ruta = SALIDAS_DIR / "nombres.txt"
    nombres = []
    for indice in range(1, 4):
        nombres.append(input(f"Nombre {indice}: ").strip())
    guardar_nombres(ruta, nombres)
    print(f"Nombres guardados y leidos: {leer_nombres(ruta)}")


def interactivo_csv() -> None:
    estudiantes = crear_dataframe_estudiantes()
    ruta = SALIDAS_DIR / "estudiantes.csv"
    guardar_csv_estudiantes(estudiantes, ruta)
    print(leer_primeros_registros(ruta).to_string(index=False))


def interactivo_funcional() -> None:
    numeros = solicitar_lista_numeros("Numeros separados por coma: ")
    enteros = [int(numero) for numero in numeros]
    print(f"Pares: {filtrar_pares(enteros)}")
    print(f"Producto: {multiplicar_elementos(numeros)}")


def interactivo_async() -> None:
    print(asyncio.run(ejecutar_tareas_en_paralelo()))
    print(asyncio.run(simular_descargas()))


def interactivo_testing() -> None:
    import unittest

    from test_soluciones import TestListaOrdenada, TestResta

    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestResta))
    suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestListaOrdenada)
    )
    unittest.TextTestRunner(verbosity=2).run(suite)


OPCIONES = [
    ("Promedio de tres numeros", interactivo_promedio),
    ("Conversion de Celsius a Fahrenheit", interactivo_celsius),
    ("Area de un triangulo", interactivo_area),
    ("Validacion para votar", interactivo_votar),
    ("Tabla de multiplicar", interactivo_tabla),
    ("Menu de calculadora", menu_calculadora),
    ("Factorial de un numero", interactivo_factorial),
    ("Verificacion de numero primo", interactivo_primo),
    ("Mayor de una lista", interactivo_mayor),
    ("Colecciones y duplicados", interactivo_colecciones),
    ("Conversion de millas a kilometros", interactivo_millas),
    ("Ejercicios con Pandas", interactivo_pandas),
    ("Graficos con matplotlib", interactivo_graficos),
    ("Programacion orientada a objetos", interactivo_poo),
    ("Manejo de excepciones", interactivo_excepciones),
    ("Manejo de archivos", interactivo_archivos),
    ("Lectura de CSV con Pandas", interactivo_csv),
    ("Programacion funcional", interactivo_funcional),
    ("Programacion asincrona", interactivo_async),
    ("Pruebas unitarias", interactivo_testing),
]


def menu_principal() -> None:
    while True:
        print("\n" + "=" * 72)
        print("FUNDAMENTOS DE PYTHON - MENU DE EJERCICIOS")
        print("=" * 72)
        for indice, (titulo, _) in enumerate(OPCIONES, start=1):
            print(f"{indice:2d}. {titulo}")
        print(" 0. Salir")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "0":
            print("Programa finalizado.")
            return
        if not opcion.isdigit():
            print("Opcion invalida.")
            continue
        indice = int(opcion)
        if not 1 <= indice <= len(OPCIONES):
            print("Opcion invalida.")
            continue
        try:
            OPCIONES[indice - 1][1]()
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def main() -> None:
    if "--demo" in sys.argv:
        ejecutar_demo()
        return
    menu_principal()


if __name__ == "__main__":
    main()
