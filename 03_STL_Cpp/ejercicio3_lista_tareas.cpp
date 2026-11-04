#include <iostream>
#include <list>
#include <string>

namespace {

constexpr int CANTIDAD_TAREAS = 5;

std::string leerTarea(int numero) {
    std::string tarea;
    while (true) {
        std::cout << "Tarea " << numero << ": ";
        std::getline(std::cin, tarea);
        if (!tarea.empty()) {
            return tarea;
        }
        std::cout << "La tarea no puede estar vacia.\n";
    }
}

void mostrarTareas(const std::list<std::string>& tareas, const std::string& titulo) {
    std::cout << '\n' << titulo << '\n';
    int indice = 1;
    for (const std::string& tarea : tareas) {
        std::cout << indice << ". " << tarea << '\n';
        ++indice;
    }
}

}

int main() {
    std::cout << "Lista de tareas con std::list\n\n";
    std::list<std::string> tareas;

    for (int i = 1; i <= CANTIDAD_TAREAS; ++i) {
        tareas.push_back(leerTarea(i));
    }

    mostrarTareas(tareas, "Tareas registradas:");

    if (!tareas.empty()) {
        tareas.pop_front();
    }

    mostrarTareas(tareas, "Lista actualizada despues de eliminar la primera tarea:");

    return 0;
}
