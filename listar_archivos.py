import os
import tkinter as tk
from tkinter import ttk, filedialog
import threading

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


# Función para obtener todos los archivos en un directorio y subdirectorios (en un hilo separado)
def obtener_archivos_en_hilo(ruta):
    def obtener_archivos():
        archivos = []
        try:
            for dirpath, _, filenames in os.walk(ruta):
                for filename in filenames:
                    archivos.append(os.path.join(dirpath, filename))
        except Exception as e:
            print(f"Error al acceder al directorio: {e}")
        mostrar_archivos(archivos)  # Actualizar la lista de archivos en la interfaz

    # Crear y empezar el hilo para obtener los archivos
    threading.Thread(target=obtener_archivos).start()


# Función para mostrar archivos en la lista
def mostrar_archivos(archivos):
    archivos_listbox.delete(0, tk.END)  # Limpiar lista actual
    for archivo in archivos:
        archivos_listbox.insert(tk.END, archivo)


# Función para manejar la búsqueda automática cuando se selecciona una carpeta
def seleccionar_carpeta_y_buscar():
    carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
    if carpeta:
        obtener_archivos_en_hilo(carpeta)
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
            obtener_archivos_en_hilo(ruta)
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
        obtener_archivos_en_hilo(ruta)


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
