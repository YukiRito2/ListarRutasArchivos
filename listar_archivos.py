import os

# Ruta al directorio principal de tu proyecto
ruta_proyecto = r"C:\TuRuta"

# Función para obtener todos los archivos en un directorio y subdirectorios
def obtener_archivos(ruta):
    archivos = []
    try:
        for dirpath, _, filenames in os.walk(ruta):
            for filename in filenames:
                archivos.append(os.path.join(dirpath, filename))
    except Exception as e:
        print(f"Error al acceder al directorio: {e}")
    return archivos

# Obtener todos los archivos en el directorio del proyecto
archivos = obtener_archivos(ruta_proyecto)

# Escribir los nombres de los archivos en un archivo de texto
try:
    with open("archivos.txt", "w") as f:
        for archivo in archivos:
            f.write(archivo + "\n")
    print("Se ha creado el archivo 'archivos.txt' con el listado de archivos.")
except Exception as e:
    print(f"Error al escribir el archivo: {e}")
