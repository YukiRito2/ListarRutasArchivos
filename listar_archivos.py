import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from ttkthemes import ThemedTk

# Nombre del archivo de historial
HISTORIAL_FILE = "historial_rutas.txt"

# Crear la ventana principal usando ttkthemes para un mejor diseño
root = ThemedTk(theme="radiance")
root.title("Gestor de Rutas")
root.geometry("600x400")

# Estilo para botones y listas
style = ttk.Style()
style.configure(
    "TButton", padding=6, relief="flat", background="#4CAF50", foreground="#FFFFFF"
)
style.configure("TLabel", background="#FFFFFF", font=("Arial", 12))

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
        messagebox.showerror("Error", f"Error al acceder al directorio: {e}")
    return archivos


# Función para mostrar archivos en la lista
def mostrar_archivos(archivos):
    archivos_listbox.delete(0, tk.END)  # Limpiar lista actual
    for archivo in archivos:
        archivos_listbox.insert(tk.END, archivo)


# Función para manejar la búsqueda de rutas
def buscar_rutas():
    ruta = simpledialog.askstring(
        "Introduce la dirección", "Introduce la dirección del proyecto:"
    )
    if ruta:
        archivos = obtener_archivos(ruta)
        mostrar_archivos(archivos)
        historial.append(ruta)
        historial_listbox.insert(tk.END, ruta)  # Agregar la ruta al historial
        escribir_historial()  # Guardar el historial en el archivo


# Función para copiar rutas
def copiar_rutas():
    rutas = archivos_listbox.get(0, tk.END)
    if rutas:
        root.clipboard_clear()
        root.clipboard_append("\n".join(rutas))
        messagebox.showinfo("Éxito", "Las rutas han sido copiadas al portapapeles.")
    else:
        messagebox.showerror("Error", "No hay rutas para copiar.")


# Función para seleccionar una ruta del historial
def seleccionar_historial(event):
    seleccion = historial_listbox.curselection()
    if seleccion:
        ruta = historial_listbox.get(seleccion)
        archivos = obtener_archivos(ruta)
        mostrar_archivos(archivos)


# Crear los widgets
buscar_button = ttk.Button(root, text="Buscar Rutas", command=buscar_rutas)
buscar_button.pack(pady=10)

copiar_button = ttk.Button(root, text="Copiar Rutas", command=copiar_rutas)
copiar_button.pack(pady=10)

archivos_listbox = tk.Listbox(root, width=80, height=10)
archivos_listbox.pack(pady=10)

historial_label = ttk.Label(root, text="Historial de Rutas")
historial_label.pack()

historial_listbox = tk.Listbox(root, width=80, height=5)
historial_listbox.pack(pady=5)
historial_listbox.bind("<<ListboxSelect>>", seleccionar_historial)

# Cargar historial desde el archivo txt
historial = leer_historial()
for ruta in historial:
    historial_listbox.insert(tk.END, ruta)

# Ejecutar la ventana
root.mainloop()
