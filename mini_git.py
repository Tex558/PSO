import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import csv
from datetime import datetime

# Verifica si .mini-git existe, si no lo crea
def crear_repositorio():
    repo_path = os.path.join(os.getcwd(), '.mini-git')
    if not os.path.exists(repo_path):
        os.makedirs(os.path.join(repo_path, 'versions'))
        os.makedirs(os.path.join(repo_path, 'log'))
        os.makedirs(os.path.join(repo_path, 'hashes'))
        os.makedirs(os.path.join(repo_path, 'branches'))
        print("Repositorio inicializado correctamente.")  # Imprimir en la consola
    else:
        print("Repositorio ya existe.")  # Imprimir en la consola

# Ejecuta los comandos del script Bash
def ejecutar_comando(comando):
    try:
        # Seleccionar el archivo
        archivo = seleccionar_archivo()
        
        if archivo:  # Si se ha seleccionado un archivo
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ruta_script = os.path.join(script_dir, 'acciones.sh')

            # Ejecutar el comando en el script Bash con el archivo seleccionado
            resultado = subprocess.run(['bash', ruta_script, comando, archivo], capture_output=True, text=True)

            # Imprimir resultados en la consola (o mensaje de éxito)
            if resultado.returncode == 0:
                print(f"Resultado: {resultado.stdout.strip()}")
            else:
                print(f"Error en ejecución: {resultado.stderr.strip()}")
        else:
            print("No se ha seleccionado ningún archivo.")  # Imprimir en la consola si no se seleccionó archivo
    except Exception as e:
        print(f"Error en subprocess: {str(e)}")  # Imprimir cualquier error en la consola

# Función para seleccionar archivo para las acciones
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de texto", "*.txt")])
    return archivo

# Función para exportar historial a CSV
def exportar_historial():
    try:
        with open('.mini-git/log.txt', 'r') as file:
            lines = file.readlines()

        with open('historial.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Fecha', 'Acción', 'Archivo', 'Hash'])
            for line in lines:
                # Suponemos que cada línea tiene el formato: "fecha acción archivo hash"
                parts = line.split()
                writer.writerow(parts)
        print("Historial exportado a historial.csv")  # Imprimir en la consola
    except Exception as e:
        print(f"Error al exportar el historial: {e}")  # Imprimir el error en la consola

# Función para comparar archivos
def comparar_archivos():
    archivo = seleccionar_archivo()  # Selecciona el archivo actual
    if archivo:
        # Pide al usuario que seleccione la versión con la que desea comparar
        archivo_version = filedialog.askopenfilename(title="Selecciona una versión para comparar", filetypes=[("Archivos de texto", "*.txt")])
        if archivo_version:
            # Ejecutar el comando compare con los dos archivos seleccionados
            ejecutar_comando(f"compare {archivo} {archivo_version}")
        else:
            print("No se ha seleccionado una versión para comparar.")
    else:
        print("No se ha seleccionado ningún archivo.")

# Función para escribir en archivo
def escribir_en_archivo():
    archivo = seleccionar_archivo()  # Selecciona el archivo donde escribir
    if archivo:
        # Crear una ventana emergente para que el usuario ingrese el texto
        def agregar_texto():
            texto = entrada_texto.get("1.0", "end-1c")  # Obtener el texto del cuadro de texto
            if texto:
                # Ejecutar el comando echo para agregar el texto al archivo
                ejecutar_comando(f"echo {texto} {archivo}")
                ventana_texto.destroy()  # Cerrar la ventana después de agregar el texto
            else:
                print("No se ha introducido ningún texto.")
        
        # Crear la ventana para ingresar el texto
        ventana_texto = tk.Toplevel(app)
        ventana_texto.title("Escribir en archivo")
        
        etiqueta = tk.Label(ventana_texto, text="Introduce el texto a agregar al archivo:")
        etiqueta.pack()
        
        # Crear un cuadro de texto donde el usuario puede escribir
        entrada_texto = tk.Text(ventana_texto, height=10, width=40)
        entrada_texto.pack()

        # Botón para agregar el texto al archivo
        boton_agregar = tk.Button(ventana_texto, text="Agregar texto", command=agregar_texto)
        boton_agregar.pack()

    else:
        print("No se ha seleccionado ningún archivo.")

# Función para crear rama
def crear_rama():
    # Crear una ventana emergente para que el usuario ingrese el nombre de la rama
    def crear():
        branch_name = entrada_rama.get()  # Obtener el nombre de la rama del cuadro de entrada
        if branch_name:
            # Ejecutar el comando para crear la rama
            ejecutar_comando(f"create_branch {branch_name}")
            ventana_rama.destroy()  # Cerrar la ventana después de crear la rama
        else:
            print("No se ha introducido el nombre de la rama.")

    # Crear la ventana para ingresar el nombre de la rama
    ventana_rama = tk.Toplevel(app)
    ventana_rama.title("Crear Rama")

    etiqueta = tk.Label(ventana_rama, text="Introduce el nombre de la rama:")
    etiqueta.pack()

    # Crear un cuadro de entrada donde el usuario puede escribir el nombre de la rama
    entrada_rama = tk.Entry(ventana_rama, width=40)
    entrada_rama.pack()

    # Botón para crear la rama
    boton_crear = tk.Button(ventana_rama, text="Crear rama", command=crear)
    boton_crear.pack()

# Interfaz gráfica
app = tk.Tk()
app.title("Mini Git - Controlador de Versiones")
app.geometry("500x500")

# Menú de acciones
acciones = [
    ("Inicializar Repositorio", "init"),
    ("Guardar versión", "save_version"),
    ("Comparar archivos", "compare"),
    ("Ver historial", "history"),
    ("Generar MD5", "md5sum"),
    ("Generar SHA256", "sha256sum"),
    ("Mostrar archivo", "cat"),
    ("Escribir en archivo", "echo"),
    ("Crear Rama", "create_branch"),
    ("Fusionar Rama", "merge_branch"),
    ("Comprimir versiones viejas", "compress_versions"),
    ("Exportar historial a CSV", "export_csv"),
    ("Hacer Backup Local", "backup_local"),
    ("Hacer Backup en Google Drive", "backup_cloud")
]

# Crear botones para cada acción
for texto, cmd in acciones:
    tk.Button(app, text=texto, width=30, command=lambda c=cmd: ejecutar_comando(c)).pack(pady=5)

# Botón para inicializar repositorio si no existe
crear_repositorio()

app.mainloop()
