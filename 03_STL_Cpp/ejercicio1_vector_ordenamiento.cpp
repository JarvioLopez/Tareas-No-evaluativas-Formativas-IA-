#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

namespace {

constexpr int CANTIDAD_NUMEROS = 6;

int leerEntero(const std::string& mensaje) {
    int valor;
    while (true) {
        std::cout << mensaje;
        if (std::cin >> valor) {
            return valor;
        }
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Entrada invalida. Debe ingresar un numero entero.\n";
    }
}

std::vector<int> leerNumeros(int cantidad) {
    std::vector<int> numeros;
    numeros.reserve(cantidad);
    for (int i = 0; i < cantidad; ++i) {
        numeros.push_back(leerEntero("Numero " + std::to_string(i + 1) + ": "));
    }
    return numeros;
}

void mostrarNumeros(const std::vector<int>& numeros, const std::string& etiqueta) {
    std::cout << etiqueta;
    for (int numero : numeros) {
        std::cout << numero << ' ';
    }
    std::cout << '\n';
}

}

int main() {
    std::cout << "Ordenamiento de numeros con std::vector y std::sort\n\n";
    std::vector<int> numeros = leerNumeros(CANTIDAD_NUMEROS);

    mostrarNumeros(numeros, "\nNumeros ingresados: ");
    std::sort(numeros.begin(), numeros.end());
    mostrarNumeros(numeros, "Numeros ordenados: ");

    return 0;
}
