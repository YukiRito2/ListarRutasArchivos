# Gestor de Rutas y Generador de Prompts Detallado

Este proyecto es una aplicación gráfica avanzada desarrollada en Python, que utiliza `Tkinter` para ofrecer una interfaz intuitiva para gestionar y explorar la estructura de directorios de proyectos. Además, permite generar prompts descriptivos y organizados, útiles para documentar y compartir la configuración de proyectos complejos con múltiples microservicios.

## Características

- **Búsqueda y Listado de Archivos**: Selecciona una carpeta desde la interfaz gráfica para listar todos los archivos y subcarpetas. Las carpetas de uso común en desarrollo, como `node_modules`, `.git`, `build`, `dist` y `venv`, se omiten automáticamente para agilizar la exploración.
- **Historial de Búsquedas**: Las rutas buscadas se almacenan automáticamente y pueden seleccionarse de nuevo desde el historial, facilitando el acceso a proyectos previamente explorados.
- **Copia de Rutas al Portapapeles**: Copia todas las rutas listadas al portapapeles con un solo clic, facilitando su uso en otras aplicaciones o documentos.
- **Generación de Prompts Informativos**: Crea un archivo de texto y copia al portapapeles un prompt detallado con la estructura y configuración del proyecto. Este prompt es ideal para documentar y compartir la estructura del proyecto, incluyendo:
  - **Estructura General del Proyecto**: Listado de archivos y carpetas detectados.
  - **Dependencias Clave**: Extrae y resalta dependencias principales de los archivos `package.json`, proporcionando una vista rápida del stack tecnológico del proyecto.
  - **Scripts de Ejecución Clave**: Identifica y detalla los scripts importantes en `package.json` (como `start`, `build`, `test`) para ver rápidamente cómo ejecutar y construir el proyecto.
  - **Resumen de Rutas de la API**: Extrae y organiza las rutas principales de archivos `routes.ts` o `controllers`, agrupándolas por método HTTP (GET, POST, PUT, DELETE) y URL, facilitando la comprensión de la estructura de la API.

- **Guardado Automático en Archivo `.txt`**: Además de copiar el prompt generado al portapapeles, se guarda automáticamente un archivo `.txt` en la carpeta de Descargas del usuario, titulado con el nombre de la carpeta principal del proyecto.

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
