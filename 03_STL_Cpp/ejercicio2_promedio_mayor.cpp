#include <algorithm>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <string>
#include <vector>

namespace {

constexpr int CENTINELA = -1;

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

std::vector<int> leerNumeros() {
    std::vector<int> numeros;
    while (true) {
        int valor = leerEntero("Ingrese un numero (-1 para terminar): ");
        if (valor == CENTINELA) {
            break;
        }
        numeros.push_back(valor);
    }
    return numeros;
}

void mostrarNumeros(const std::vector<int>& numeros) {
    std::cout << "Numeros ingresados: ";
    for (int numero : numeros) {
        std::cout << numero << ' ';
    }
    std::cout << '\n';
}

}

int main() {
    std::cout << "Promedio y mayor numero con std::vector\n\n";
    std::vector<int> numeros = leerNumeros();

    if (numeros.empty()) {
        std::cout << "\nNo se ingresaron numeros para analizar.\n";
        return 0;
    }

    const int mayor = *std::max_element(numeros.begin(), numeros.end());
    const double suma = std::accumulate(numeros.begin(), numeros.end(), 0.0);
    const double promedio = suma / static_cast<double>(numeros.size());

    mostrarNumeros(numeros);
    std::cout << "Cantidad de numeros: " << numeros.size() << '\n';
    std::cout << "Numero mayor: " << mayor << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Promedio: " << promedio << '\n';

    return 0;
}
