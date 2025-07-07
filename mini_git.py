import tkinter as tk
from tkinter import filedialog, simpledialog
import subprocess
import os
from datetime import datetime

# Verifica si .mini-git existe, si no lo crea
def crear_repositorio():
    repo_path = os.path.join(os.getcwd(), '.mini-git')
    if not os.path.exists(repo_path):
        os.makedirs(os.path.join(repo_path, 'versions'))
        os.makedirs(os.path.join(repo_path, 'log'))
        os.makedirs(os.path.join(repo_path, 'hashes'))
        os.makedirs(os.path.join(repo_path, 'branches'))
        # Crear archivos base
        open(os.path.join(repo_path, 'log/log.txt'), 'a').close()
        open(os.path.join(repo_path, 'hashes/hashes.txt'), 'a').close()
        print("Repositorio inicializado correctamente.")
    else:
        print("Repositorio ya existe.")

# Ejecuta los comandos del script Bash
def ejecutar_comando(comando):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_script = os.path.join(script_dir, 'acciones.sh')
        
        resultado = subprocess.run(
            ['bash', ruta_script] + comando.split(), 
            capture_output=True, 
            text=True
        )

        if resultado.returncode == 0:
            print(f"Resultado: {resultado.stdout.strip()}")
        else:
            print(f"Error: {resultado.stderr.strip()}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Función para comparar archivos
def comparar_archivos():
    versions_folder = os.path.join(os.getcwd(), '.mini-git', 'versions')
    if not os.path.exists(versions_folder) or not os.listdir(versions_folder):
        print("No hay versiones para comparar.")
        return

    files = os.listdir(versions_folder)
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(versions_folder, x)))
    print(f"Comparando con versión: {latest_file}")
    
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo para comparar",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    
    if archivo:
        version_path = os.path.abspath(os.path.join(versions_folder, latest_file))
        ejecutar_comando(f"compare {os.path.abspath(archivo)} {version_path}")
    else:
        print("Operación cancelada.")

# Función para guardar una versión
def guardar_version():
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo a guardar",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    
    if archivo:
        version = datetime.now().strftime("%Y%m%d%H%M%S")
        version_filename = f"{os.path.basename(archivo)}_v{version}{os.path.splitext(archivo)[1]}"
        ejecutar_comando(f"save_version {os.path.abspath(archivo)} {version_filename}")
    else:
        print("Operación cancelada.")

# Funciones para manejo de ramas
def crear_rama():
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo base",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    
    if archivo:
        nombre_rama = simpledialog.askstring("Crear Rama", "Nombre de la rama:")
        if nombre_rama:
            ejecutar_comando(f"create_branch {os.path.abspath(archivo)} {nombre_rama}")
        else:
            print("Nombre de rama no proporcionado.")
    else:
        print("Operación cancelada.")

def fusionar_rama():
    archivo = filedialog.askopenfilename(
        title="Selecciona archivo destino",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    
    if archivo:
        nombre_rama = simpledialog.askstring("Fusionar Rama", "Nombre de la rama a fusionar:")
        if nombre_rama:
            ejecutar_comando(f"merge_branch {os.path.abspath(archivo)} {nombre_rama}")
        else:
            print("Nombre de rama no proporcionado.")
    else:
        print("Operación cancelada.")

def generar_md5():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*")]
    )
    if archivo:
        ejecutar_comando(f"md5sum {os.path.abspath(archivo)}")
    else:
        print("Operación cancelada.")

def generar_sha256():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*")]
    )
    if archivo:
        ejecutar_comando(f"sha256sum {os.path.abspath(archivo)}")
    else:
        print("Operación cancelada.")

def mostrar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*")]
    )
    if archivo:
        ejecutar_comando(f"cat {os.path.abspath(archivo)}")
    else:
        print("Operación cancelada.")

def escribir_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*")]
    )
    if archivo:
        texto = simpledialog.askstring("Escribir en archivo", "Texto a añadir:")
        if texto:
            texto_escapado = texto.replace('"', '\\"')
            ejecutar_comando(f'echo {os.path.abspath(archivo)} "{texto_escapado}"')
    else:
        print("Operación cancelada.")

# Interfaz gráfica
app = tk.Tk()
app.title("Mini Git - Controlador de Versiones")
app.geometry("500x650")

# Configuración de botones
tk.Button(app, text="Inicializar Repositorio", width=30, command=lambda: ejecutar_comando("init")).pack(pady=5)

tk.Button(app, text="Guardar versión", width=30, command=guardar_version).pack(pady=5)

tk.Button(app, text="Comparar archivos", width=30, command=comparar_archivos).pack(pady=5)

tk.Button(app, text="Ver historial", width=30, command=lambda: ejecutar_comando("history")).pack(pady=5)

tk.Button(app, text="Generar MD5", width=30, command=generar_md5).pack(pady=5)

tk.Button(app, text="Generar SHA256", width=30, command=generar_sha256).pack(pady=5)

tk.Button(app, text="Mostrar archivo", width=30, command=mostrar_archivo).pack(pady=5)

tk.Button(app, text="Escribir en archivo", width=30, command=escribir_archivo).pack(pady=5)

tk.Button(app, text="Crear Rama", width=30, command=crear_rama).pack(pady=5)

tk.Button(app, text="Fusionar Rama", width=30, command=fusionar_rama).pack(pady=5)

tk.Button(app, text="Comprimir versiones viejas", width=30, command=lambda: ejecutar_comando("compress_versions")).pack(pady=5)

tk.Button(app, text="Exportar historial a CSV", width=30, command=lambda: ejecutar_comando("export_csv")).pack(pady=5)

tk.Button(app, text="Hacer Backup Local", width=30, command=lambda: ejecutar_comando("backup_local")).pack(pady=5)

tk.Button(app, text="Hacer Backup en Google Drive", width=30, command=lambda: ejecutar_comando("backup_cloud")).pack(pady=5)

# Inicializar repositorio al inicio
crear_repositorio()

app.mainloop()