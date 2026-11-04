# Práctica 03 — STL en C++

Solución de los ejercicios de `std::vector`, `std::list`, algoritmos de la STL y estadísticas básicas, con proyecto CMake listo para Visual Studio 2022.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `Enunciado_Practica_STL_Cpp.docx` | Enunciado original de la práctica. |
| `Solucion_Practica_STL_Cpp.docx` | Documento de entrega con explicación, código y ejecuciones. |
| `Solucion_Practica_STL_Cpp.pdf` | Versión PDF del documento de entrega. |
| `ejercicio1_vector_ordenamiento.cpp` | Vector de seis enteros, ordenamiento con `std::sort`. |
| `ejercicio2_promedio_mayor.cpp` | Promedio y mayor de una secuencia terminada en `-1`. |
| `ejercicio3_lista_tareas.cpp` | Lista de tareas con `std::list` y `pop_front`. |
| `reto_extra_estadisticas.cpp` | Conteo de pares e impares, mayor, menor y promedio. |
| `CMakeLists.txt` | Cuatro ejecutables independientes con C++17 y advertencias activas. |
| `CMakePresets.json` | Presets para Visual Studio 2022 x64 y compilación Release. |
| `build/PracticaSTL.sln` | Solución de Visual Studio ya generada. |
| `salidas/` | Ejecuciones de ejemplo de los cuatro programas. |

## Abrir en Visual Studio 2022

1. Abrir `build/PracticaSTL.sln`.
2. En el Explorador de soluciones, clic derecho sobre el proyecto que se desea probar y seleccionar **Establecer como proyecto de inicio**.
3. Presionar `Ctrl+F5` para compilar y ejecutar sin depuración.
4. Ingresar los datos solicitados en la consola.

Cada programa es independiente y se ejecuta en su propia consola.

## Compilar desde la terminal

Con CMake disponible en el `PATH`:

```powershell
cmake --preset visual-studio-2022
cmake --build --preset release
```

Los ejecutables se generan en `build/Release/`.

También se puede configurar manualmente:

```powershell
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
```

## Ejecución rápida

```powershell
.\build\Release\ejercicio1_vector_ordenamiento.exe
.\build\Release\ejercicio2_promedio_mayor.exe
.\build\Release\ejercicio3_lista_tareas.exe
.\build\Release\reto_extra_estadisticas.exe
```

Los archivos de `salidas/` conservan entradas y resultados de ejemplo. El código no contiene comentarios ni marcas de edición.
