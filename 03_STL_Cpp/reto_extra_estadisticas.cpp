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

void mostrarEstadisticas(const std::vector<int>& numeros) {
    const int mayor = *std::max_element(numeros.begin(), numeros.end());
    const int menor = *std::min_element(numeros.begin(), numeros.end());
    const double suma = std::accumulate(numeros.begin(), numeros.end(), 0.0);
    const double promedio = suma / static_cast<double>(numeros.size());
    const auto pares = std::count_if(numeros.begin(), numeros.end(), [](int numero) {
        return numero % 2 == 0;
    });
    const auto impares = static_cast<long long>(numeros.size()) - pares;

    std::cout << "\nNumeros ingresados: ";
    for (int numero : numeros) {
        std::cout << numero << ' ';
    }

    std::cout << "\nCantidad de numeros: " << numeros.size();
    std::cout << "\nNumero mayor: " << mayor;
    std::cout << "\nNumero menor: " << menor;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "\nPromedio: " << promedio;
    std::cout << "\nNumeros pares: " << pares;
    std::cout << "\nNumeros impares: " << impares << '\n';
}

}

int main() {
    std::cout << "Reto extra: estadisticas de una lista de numeros\n\n";
    std::vector<int> numeros = leerNumeros();

    if (numeros.empty()) {
        std::cout << "\nNo se ingresaron numeros para analizar.\n";
        return 0;
    }

    mostrarEstadisticas(numeros);
    return 0;
}
