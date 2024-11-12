import os
import tkinter as tk
from tkinter import ttk, filedialog
import json
import re

# Nombre del archivo de historial
HISTORIAL_FILE = "historial_rutas.txt"

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Rutas")
root.geometry("600x400")


# Función para centrar una ventana
def centrar_ventana(ventana, width=600, height=400):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")


# Centrar la ventana principal
centrar_ventana(root)

# Historial de rutas buscadas
historial = []


# Función para leer el archivo de historial
def leer_historial():
    if not os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "w") as f:
            pass  # Crear el archivo vacío si no existe
    else:
        with open(HISTORIAL_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


# Función para escribir el historial en el archivo
def escribir_historial():
    with open(HISTORIAL_FILE, "w") as f:
        for ruta in historial:
            f.write(ruta + "\n")


# Función para obtener todos los archivos en un directorio y subdirectorios
def obtener_archivos(ruta):
    archivos = []
    carpetas_omitidas = {
        "node_modules",
        ".git",
        "build",
        "dist",
        "venv",
    }  # Agregar otras carpetas relacionadas
    try:
        for dirpath, dirnames, filenames in os.walk(ruta):
            # Remover carpetas especificas para no listar su contenido
            for carpeta in carpetas_omitidas:
                if carpeta in dirnames:
                    archivos.append(
                        os.path.join(dirpath, carpeta)
                    )  # Agrega solo el nombre de la carpeta
                    dirnames.remove(
                        carpeta
                    )  # Evita recorrer el contenido de esta carpeta

            # Agrega los archivos encontrados en directorios no omitidos
            for filename in filenames:
                archivos.append(os.path.join(dirpath, filename))

    except Exception as e:
        print(f"Error al acceder al directorio: {e}")
    mostrar_archivos(archivos)  # Actualizar la lista de archivos en la interfaz


# Función para mostrar archivos en la lista
def mostrar_archivos(archivos):
    archivos_listbox.delete(0, tk.END)  # Limpiar lista actual
    for archivo in archivos:
        archivos_listbox.insert(tk.END, archivo)


# Función para manejar la búsqueda automática cuando se selecciona una carpeta
def seleccionar_carpeta_y_buscar():
    carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
    if carpeta:
        obtener_archivos(carpeta)
        if carpeta not in historial:
            historial.append(carpeta)
            historial_listbox.insert(tk.END, carpeta)  # Agregar la carpeta al historial
            escribir_historial()  # Guardar en el archivo
        ventana.destroy()  # Cerrar la ventana de búsqueda


# Nueva ventana para ingresar la ruta o buscar carpeta
def ventana_buscar_ruta():
    global ventana  # Hacer la ventana accesible dentro de la función de búsqueda automática
    ventana = tk.Toplevel(root)
    ventana.title("Buscar o Seleccionar Carpeta")
    ventana.geometry("400x180")

    # Centrar la ventana de búsqueda sobre la ventana principal
    centrar_ventana(ventana, 400, 180)

    label = tk.Label(ventana, text="Pega la ruta o selecciona una carpeta:")
    label.pack(pady=10)

    # Crear un Entry con texto de sugerencia (placeholder)
    ruta_entry = tk.Entry(ventana, width=50)
    ruta_entry.insert(0, "Pega la ruta aquí ")
    ruta_entry.bind(
        "<FocusIn>", lambda event: ruta_entry.delete(0, tk.END)
    )  # Borra el placeholder al hacer clic
    ruta_entry.pack(pady=5)

    # Crear frame para botones alineados
    frame_botones_ventana = tk.Frame(ventana)
    frame_botones_ventana.pack(pady=10)

    buscar_carpeta_button = tk.Button(
        frame_botones_ventana,
        text="Seleccionar Carpeta",
        command=seleccionar_carpeta_y_buscar,
    )
    buscar_carpeta_button.pack(side=tk.LEFT, padx=5)

    def confirmar_ruta():
        ruta = ruta_entry.get()
        if ruta and ruta != "Escribe la ruta aquí":
            obtener_archivos(ruta)
            if ruta not in historial:
                historial.append(ruta)
                historial_listbox.insert(tk.END, ruta)  # Agregar la ruta al historial
                escribir_historial()  # Guardar el historial en el archivo
        ventana.destroy()

    confirmar_button = tk.Button(
        frame_botones_ventana, text="Buscar ruta", command=confirmar_ruta
    )
    confirmar_button.pack(side=tk.LEFT, padx=5)


# Función para copiar rutas con notificación sin ventana
def copiar_rutas():
    rutas = archivos_listbox.get(0, tk.END)
    if rutas:
        root.clipboard_clear()
        root.clipboard_append("\n".join(rutas))
        mostrar_notificacion("Rutas copiadas al portapapeles")


# Función para mostrar una notificación temporal
def mostrar_notificacion(mensaje):
    notificacion_label.config(text=mensaje)
    notificacion_label.pack()
    root.after(2000, ocultar_notificacion)  # Ocultar después de 2 segundos


def ocultar_notificacion():
    notificacion_label.pack_forget()


# Función para seleccionar una ruta del historial y buscar los archivos
def seleccionar_historial(event):
    seleccion = historial_listbox.curselection()
    if seleccion:
        ruta = historial_listbox.get(seleccion)
        obtener_archivos(ruta)


# Función para generar y copiar el prompt al portapapeles con contexto de múltiples microservicios y ruta específica de cada archivo
def generar_prompt():
    rutas = archivos_listbox.get(0, tk.END)
    encabezado = (
        "Hola, a continuación te muestro un resumen detallado de este proyecto. "
        "Úsalo para entender su estructura y responder a mis preguntas sobre su organización y configuración. "
        "Por favor, lee atentamente esta información, ya que te servirá como guía para ayudarme a trabajar con el proyecto. "
        "Aquí está la estructura general del proyecto:"
    )
    contenido_prompt = (
        encabezado
        + "\n\nEstructura General del Proyecto:\n\n"
        + "\n".join(rutas)
        + "\n\n"
    )
    archivos_clave = [
        "package.json",
        "Dockerfile",
        "docker-compose.yml",
        ".env",
        "tsconfig.json",
        ".eslintrc",
        ".prettierrc",
    ]
    dependencias_clave = []
    configuraciones = []
    rutas_api = []
    scripts_importantes = []

    for ruta in rutas:
        for archivo in archivos_clave:
            if ruta.endswith(archivo):
                try:
                    with open(ruta, "r") as file:
                        contenido = file.read()
                        # Determinar el contexto del archivo según su ubicación en la estructura de carpetas
                        nombre_servicio = os.path.basename(
                            os.path.dirname(ruta)
                        )  # Carpeta inmediata
                        contexto = f"{archivo} en el servicio '{nombre_servicio}'"
                        contenido_prompt += f"Este es el contenido de {contexto}:\n{ruta}\n\n{contenido}\n\n"

                        # Extraer dependencias clave del package.json y configuraciones de .env y docker-compose
                        if archivo == "package.json":
                            paquete_json = json.loads(contenido)
                            dependencias = paquete_json.get("dependencies", {})
                            dev_dependencias = paquete_json.get("devDependencies", {})
                            dependencias_clave.extend(dependencias.keys())
                            dependencias_clave.extend(dev_dependencias.keys())
                            # Identificar scripts importantes en package.json
                            scripts = paquete_json.get("scripts", {})
                            scripts_importantes = {
                                k: v
                                for k, v in scripts.items()
                                if k in ["start", "build", "test"]
                            }
                        elif archivo == "docker-compose.yml" or archivo == ".env":
                            configuraciones.append(contenido)

                        # Documentación de rutas en archivos routes.ts o controller
                        if archivo.endswith((".ts", ".js")) and (
                            "route" in archivo or "controller" in archivo
                        ):
                            rutas_encontradas = re.findall(
                                r"(GET|POST|PUT|DELETE)\s+['\"](.+?)['\"]", contenido
                            )
                            for metodo, ruta in rutas_encontradas:
                                rutas_api.append(f"{metodo} {ruta}")

                except Exception as e:
                    print(f"No se pudo leer {archivo}: {e}")

    # Sección de Dependencias Clave
    if dependencias_clave:
        contenido_prompt += (
            "\nDependencias Clave del Proyecto:\n"
            + ", ".join(set(dependencias_clave))
            + "\n\n"
        )

    # Sección de Scripts Importantes
    if scripts_importantes:
        contenido_prompt += "Scripts Clave en package.json:\n"
        for nombre, comando in scripts_importantes.items():
            contenido_prompt += f"{nombre}: {comando}\n"
        contenido_prompt += "\n"

    # Sección de Rutas de la API
    if rutas_api:
        contenido_prompt += "Resumen de Rutas de la API:\n"
        for ruta in rutas_api:
            contenido_prompt += f"{ruta}\n"
        contenido_prompt += "\n"

    # Sección de Notas sobre Configuración y Entorno
    if configuraciones:
        contenido_prompt += "Notas sobre Configuración y Entorno:\n"
        for config in configuraciones:
            contenido_prompt += config + "\n"

    root.clipboard_clear()
    root.clipboard_append(contenido_prompt)
    mostrar_notificacion("Prompt generado y copiado al portapapeles")


# Crear los widgets sin estilos adicionales para los botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

buscar_button = tk.Button(
    frame_botones, text="Buscar Rutas", command=ventana_buscar_ruta
)
buscar_button.pack(side=tk.LEFT, padx=5)

copiar_button = tk.Button(frame_botones, text="Copiar Rutas", command=copiar_rutas)
copiar_button.pack(side=tk.LEFT, padx=5)

generar_prompt_button = tk.Button(
    frame_botones, text="Generar Prompt", command=generar_prompt
)
generar_prompt_button.pack(side=tk.LEFT, padx=5)

archivos_listbox = tk.Listbox(root, width=80, height=10)
archivos_listbox.pack(pady=10)

historial_label = ttk.Label(root, text="Historial de Rutas Buscadas")
historial_label.pack()

# Sección del historial de rutas buscadas con scrollbar
frame_historial = tk.Frame(root)
frame_historial.pack(pady=5)

# Scrollbar para el historial
scrollbar_historial = tk.Scrollbar(frame_historial)
scrollbar_historial.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox del historial con scrollbar
historial_listbox = tk.Listbox(
    frame_historial, width=80, height=7, yscrollcommand=scrollbar_historial.set
)
historial_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar_historial.config(command=historial_listbox.yview)

# Vincular el doble clic en un elemento del historial a la función seleccionar_historial
historial_listbox.bind("<Double-1>", seleccionar_historial)

# Etiqueta para la notificación temporal
notificacion_label = tk.Label(root, text="", fg="green")

# Cargar historial desde el archivo txt
historial = leer_historial()
for ruta in historial:
    historial_listbox.insert(tk.END, ruta)

# Ejecutar la ventana
root.mainloop()
