from abc import ABC, abstractmethod
from typing import Protocol

from multipledispatch import dispatch


def procesar_datos(numeros: list[int]) -> dict[str, float | int]:
    if not numeros:
        raise ValueError("La lista no puede estar vacia.")
    suma = sum(numeros)
    return {
        "suma": suma,
        "promedio": suma / len(numeros),
        "maximo": max(numeros),
        "minimo": min(numeros),
    }


class Dispositivo(Protocol):
    def activar(self) -> None:
        ...


class Telefono:
    def activar(self) -> None:
        print("Telefono activado: llamadas y mensajes disponibles.")


class Alarma:
    def activar(self) -> None:
        print("Alarma activada: sistema de seguridad en vigilancia.")


class Computadora:
    def activar(self) -> None:
        print("Computadora activada: sesion iniciada correctamente.")


def ejecutar_dispositivo(dispositivo: Dispositivo) -> None:
    dispositivo.activar()


def crear_incrementador(inicio: int):
    cuenta = inicio

    def incrementar(paso: int = 1) -> int:
        nonlocal cuenta
        cuenta += paso
        return cuenta

    return incrementar


def demostrar_late_binding() -> tuple[list[int], list[int]]:
    funciones_tardias = [lambda: indice for indice in range(3)]
    funciones_tempranas = [lambda indice=indice: indice for indice in range(3)]
    resultados_tardios = [funcion() for funcion in funciones_tardias]
    resultados_tempranos = [funcion() for funcion in funciones_tempranas]
    return resultados_tardios, resultados_tempranos


@dispatch(int, int)
def mezclar(a: int, b: int) -> int:
    return a + b


@dispatch(list, list)
def mezclar(a: list, b: list) -> list:
    return a + b


@dispatch(str, str)
def mezclar(a: str, b: str) -> str:
    return f"{a}-{b}"


class Usuario:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre


def saludar_usuario(self: Usuario) -> None:
    print(f"Hola, soy {self.nombre}")


setattr(Usuario, "saludar", saludar_usuario)


class LoggerMixin:
    def log(self, mensaje: str) -> None:
        print(f"[LOG] {mensaje}")


class Sensor:
    def __init__(self, tipo: str) -> None:
        self.tipo = tipo


class SensorAvanzado(Sensor, LoggerMixin):
    def __init__(self, tipo: str) -> None:
        super().__init__(tipo)
        self.log(f"Sensor de {self.tipo} inicializado")

    def leer(self) -> str:
        return f"Lectura del sensor de {self.tipo}"


class MedibleTrait(ABC):
    @abstractmethod
    def medir(self) -> float:
        raise NotImplementedError


class SensorTemperatura(MedibleTrait):
    def medir(self) -> float:
        return 23.5


class SensorHumedad(MedibleTrait):
    def medir(self) -> float:
        return 61.0


def mostrar_seccion(titulo: str) -> None:
    print("\n" + "=" * 68)
    print(titulo)
    print("=" * 68)


def main() -> None:
    mostrar_seccion("PARTE 1 - TIPADO ESTATICO Y DINAMICO")
    datos = procesar_datos([10, 20, 30, 40, 50])
    for clave, valor in datos.items():
        print(f"{clave.capitalize()}: {valor}")

    mostrar_seccion("PARTE 2 - DUCK TYPING Y PROTOCOLOS ESTRUCTURALES")
    for dispositivo in (Telefono(), Alarma(), Computadora()):
        ejecutar_dispositivo(dispositivo)

    mostrar_seccion("PARTE 3 - CLOSURES Y BINDING")
    incrementador = crear_incrementador(10)
    print(f"Incremento 1: {incrementador()}")
    print(f"Incremento 2: {incrementador(5)}")
    print(f"Incremento 3: {incrementador(2)}")

    tardios, tempranos = demostrar_late_binding()
    print(f"Late binding: {tardios}")
    print(f"Early binding: {tempranos}")

    mostrar_seccion("PARTE 4 - MULTIPLE DISPATCH")
    print(f"Enteros: {mezclar(4, 7)}")
    print(f"Listas: {mezclar([1, 2], [3, 4])}")
    print(f"Strings: {mezclar('Python', 'Avanzado')}")

    mostrar_seccion("PARTE 5 - CLASES ABIERTAS")
    usuario = Usuario("Ana")
    usuario.saludar()

    mostrar_seccion("PARTE 6 - MIXINS Y TRAITS")
    sensor = SensorAvanzado("temperatura")
    print(sensor.leer())

    medibles: list[MedibleTrait] = [SensorTemperatura(), SensorHumedad()]
    for medible in medibles:
        print(f"Medicion: {medible.medir()}")


if __name__ == "__main__":
    main()
