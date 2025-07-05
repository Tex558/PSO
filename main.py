import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Obtener ruta absoluta del archivo acciones.sh
script_dir = os.path.dirname(os.path.abspath(__file__))
ruta_script = os.path.join(script_dir, 'acciones.sh')

def ejecutar_comando(comando):
    try:
        print("Ruta al script:", ruta_script)  # Depuración
        resultado = subprocess.run(['bash', ruta_script, comando], capture_output=True, text=True)

        if resultado.returncode == 0:
            messagebox.showinfo("Resultado", resultado.stdout.strip())
        else:
            messagebox.showerror("Error en ejecución", resultado.stderr.strip())
    except Exception as e:
        print("Error en subprocess:", str(e))
        messagebox.showerror("Error", str(e))

# Interfaz simple
app = tk.Tk()
app.title("Mini Git - Controlador de Versiones")
app.geometry("400x400")

acciones = [
    ("Diff archivos", "diff"),
    ("Copiar archivo", "cp"),
    ("Mover archivo", "mv"),
    ("MD5SUM archivo", "md5sum"),
    ("SHA256SUM archivo", "sha256sum"),
    ("Fecha actual", "date"),
    ("Mostrar contenido (cat)", "cat"),
    ("Escribir en archivo (echo)", "echo")
]

for texto, cmd in acciones:
    tk.Button(app, text=texto, width=30, command=lambda c=cmd: ejecutar_comando(c)).pack(pady=5)

app.mainloop()
