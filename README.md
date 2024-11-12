# Gestor de Rutas y Generador de Prompts Detallado

Este proyecto es una aplicación gráfica avanzada desarrollada en Python, que utiliza `Tkinter` para ofrecer una interfaz intuitiva y poderosa para gestionar y explorar la estructura de directorios de proyectos. Además, permite generar prompts descriptivos y organizados, útiles para comprender y documentar proyectos complejos con múltiples microservicios.

## Características

- **Búsqueda de Carpetas**: Selecciona una carpeta desde la interfaz gráfica para listar todos los archivos, incluidas las subcarpetas. Permite ignorar carpetas específicas como `node_modules`, `.git`, `build`, `dist` y `venv` para agilizar la exploración.
- **Historial de Búsquedas**: Las rutas buscadas se almacenan automáticamente y pueden seleccionarse de nuevo desde el historial, facilitando el acceso a proyectos previamente explorados.
- **Copia de Rutas al Portapapeles**: Permite copiar al portapapeles todas las rutas de los archivos listados, lo que facilita su uso en otras aplicaciones o documentos.
- **Generación de Prompts Informativos**: Crea un prompt detallado con la estructura y configuración del proyecto, ideal para documentar y compartir el proyecto. El prompt incluye:
  - **Estructura General del Proyecto**: Listado de archivos y carpetas detectados en el proyecto.
  - **Dependencias Clave**: Extrae y resalta las dependencias principales desde archivos `package.json` para tener una vista rápida del stack tecnológico del proyecto.
  - **Scripts de Ejecución Clave**: Identifica scripts importantes en `package.json` (como `start`, `build`, `test`), para ver rápidamente cómo ejecutar y construir el proyecto.
  - **Resumen de Rutas de la API**: Extrae y organiza las rutas principales de archivos `routes.ts` o `controllers`, agrupándolas por método HTTP (GET, POST, PUT, DELETE) y URL.

- **Interfaz Gráfica Intuitiva**: Basada en `Tkinter`, ofrece un manejo fácil y rápido de carpetas y archivos, sin necesidad de usar la terminal.

## Requisitos

Este proyecto utiliza bibliotecas estándar de Python, por lo que **no es necesario instalar dependencias externas adicionales**.

### Requisitos del Sistema

- Python 3.x
- Tkinter (incluido en la mayoría de las instalaciones de Python)

## Instalación y Ejecución

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/YukiRito2/ListarRutasArchivos.git
