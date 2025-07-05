import tkinter as tk
from tkinter import messagebox
import subprocess

def ejecutar_comando(comando):
    try:
        resultado = subprocess.run(['bash', './acciones.sh', comando], capture_output=True, text=True)
        messagebox.showinfo("Resultado", resultado.stdout if resultado.stdout else resultado.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Mini Git - Controlador de Versiones")
app.geometry("400x400")

etiqueta = tk.Label(app, text="Selecciona una acción:", font=("Arial", 14))
etiqueta.pack(pady=10)

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
    boton = tk.Button(app, text=texto, width=30, command=lambda c=cmd: ejecutar_comando(c))
    boton.pack(pady=5)

app.mainloop()
