import os
import tkinter as tk
from tkinter import simpledialog, ttk, filedialog

# Nombre del archivo de historial
HISTORIAL_FILE = "historial_rutas.txt"

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Rutas")
root.geometry("600x400")

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
    try:
        for dirpath, _, filenames in os.walk(ruta):
            for filename in filenames:
                archivos.append(os.path.join(dirpath, filename))
    except Exception as e:
        print(f"Error al acceder al directorio: {e}")
    return archivos


# Función para mostrar archivos en la lista
def mostrar_archivos(archivos):
    archivos_listbox.delete(0, tk.END)  # Limpiar lista actual
    for archivo in archivos:
        archivos_listbox.insert(tk.END, archivo)


# Nueva ventana para ingresar la ruta o buscar carpeta
def ventana_buscar_ruta():
    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
        if carpeta:
            ruta_entry.delete(0, tk.END)
            ruta_entry.insert(0, carpeta)

    ventana = tk.Toplevel(root)
    ventana.title("Buscar Rutas o Carpeta")
    ventana.geometry("400x200")

    label = tk.Label(ventana, text="Introduce la dirección o selecciona una carpeta:")
    label.pack(pady=10)

    ruta_entry = tk.Entry(ventana, width=50)
    ruta_entry.pack(pady=5)

    buscar_carpeta_button = tk.Button(
        ventana, text="Buscar Carpeta", command=seleccionar_carpeta
    )
    buscar_carpeta_button.pack(pady=5)

    def confirmar_ruta():
        ruta = ruta_entry.get()
        if ruta:
            archivos = obtener_archivos(ruta)
            mostrar_archivos(archivos)
            if ruta not in historial:
                historial.append(ruta)
                historial_listbox.insert(tk.END, ruta)  # Agregar la ruta al historial
                escribir_historial()  # Guardar el historial en el archivo
        ventana.destroy()

    confirmar_button = tk.Button(ventana, text="Confirmar Ruta", command=confirmar_ruta)
    confirmar_button.pack(pady=10)


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
        archivos = obtener_archivos(ruta)
        mostrar_archivos(archivos)


# Crear los widgets sin estilos adicionales para los botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

buscar_button = tk.Button(
    frame_botones, text="Buscar Rutas", command=ventana_buscar_ruta
)
buscar_button.pack(side=tk.LEFT, padx=5)

copiar_button = tk.Button(frame_botones, text="Copiar Rutas", command=copiar_rutas)
copiar_button.pack(side=tk.LEFT, padx=5)

archivos_listbox = tk.Listbox(root, width=80, height=10)
archivos_listbox.pack(pady=10)

historial_label = ttk.Label(root, text="Historial de Rutas Buscadas")
historial_label.pack()

historial_listbox = tk.Listbox(root, width=80, height=5)
historial_listbox.pack(pady=5)
historial_listbox.bind("<<ListboxSelect>>", seleccionar_historial)

# Etiqueta para la notificación temporal
notificacion_label = tk.Label(root, text="", fg="green")

# Cargar historial desde el archivo txt
historial = leer_historial()
for ruta in historial:
    historial_listbox.insert(tk.END, ruta)

# Ejecutar la ventana
root.mainloop()
