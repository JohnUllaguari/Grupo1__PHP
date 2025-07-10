import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os

# === Archivo temporal ===
ARCHIVO_TEMP = "entrada_usuario_temp.php"

def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("PHP Files", "*.php")])
    if archivo:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, archivo)

        # Leer contenido y ponerlo en área de código
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            area_codigo.delete(1.0, tk.END)
            area_codigo.insert(tk.END, contenido)

def ejecutar_analisis(tipo, text_widget):
    archivo = entry_ruta.get().strip()
    usuario = entry_usuario.get().strip()
    codigo = area_codigo.get(1.0, tk.END).strip()

    # === Validar usuario ===
    if not usuario:
        messagebox.showerror("Error", "Ingresa un nombre de usuario.")
        return

    # === Prioridad: Si hay código escrito, se usa ===
    if codigo:
        with open(ARCHIVO_TEMP, 'w', encoding='utf-8') as f:
            f.write(codigo)
        ruta_analizar = ARCHIVO_TEMP
    elif archivo:
        ruta_analizar = archivo
    else:
        messagebox.showerror("Error", "Selecciona un archivo o escribe código para analizar.")
        return

    try:
        if tipo == 'lexico':
            subprocess.run(["python", "lexico.py", ruta_analizar, usuario], check=True)
            carpeta_logs = "logs"
            patron_log = f"lexico-{usuario}-"
        elif tipo == 'sintactico':
            subprocess.run(["python", "sintactico_php_ply.py", ruta_analizar, usuario], check=True)
            carpeta_logs = "logsSintactico"
            patron_log = f"sintactico-{usuario}-"
        elif tipo == 'semantico':
            subprocess.run(["python", "semantico.py", ruta_analizar, usuario], check=True)
            carpeta_logs = "logsSemantico"
            patron_log = f"semantico-{usuario}-"
        else:
            messagebox.showerror("Error", "Tipo de análisis desconocido.")
            return
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Fallo en análisis {tipo}:\n{e}")
        return

    archivos = [f for f in os.listdir(carpeta_logs) if f.startswith(patron_log)]
    if not archivos:
        messagebox.showerror("Error", "No se encontró archivo de log.")
        return

    archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta_logs, x)), reverse=True)
    ruta_log = os.path.join(carpeta_logs, archivos[0])

    with open(ruta_log, 'r', encoding='utf-8') as f:
        contenido = f.read()
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, contenido)
        text_widget.config(state='disabled')

    messagebox.showinfo("Éxito", f"Análisis {tipo} completado y resultados actualizados.")


def limpiar_codigo():
    area_codigo.delete(1.0, tk.END)

root = tk.Tk()
root.title("Analizador PHP con Interfaz Gráfica")

# === Sección de selección de archivo ===
frame_archivo = tk.Frame(root)
frame_archivo.pack(fill='x', padx=10, pady=5)

entry_ruta = tk.Entry(frame_archivo, width=60)
entry_ruta.pack(side='left', padx=5)

btn_abrir = tk.Button(frame_archivo, text="Seleccionar Archivo PHP", command=abrir_archivo)
btn_abrir.pack(side='left', padx=5)

# === Campo Usuario ===
frame_usuario = tk.Frame(root)
frame_usuario.pack(fill='x', padx=10, pady=5)

tk.Label(frame_usuario, text="Usuario:").pack(side='left', padx=5)
entry_usuario = tk.Entry(frame_usuario, width=30)
entry_usuario.insert(0, "JohnUllaguari")
entry_usuario.pack(side='left', padx=5)

# === Área para escribir código ===
frame_codigo = tk.Frame(root)
frame_codigo.pack(fill='both', expand=True, padx=10, pady=5)

tk.Label(frame_codigo, text="O escribe tu código PHP aquí:").pack(anchor='w')
area_codigo = scrolledtext.ScrolledText(frame_codigo, width=120, height=15)
area_codigo.pack(fill='both', expand=True)
btn_limpiar = tk.Button(frame_codigo, text="Limpiar Código", command=limpiar_codigo)
btn_limpiar.pack(anchor='e', pady=5)

# === Pestañas ===
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

analizadores = ['lexico', 'sintactico', 'semantico']
text_widgets = {}

for tipo in analizadores:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tipo.capitalize())

    btn = tk.Button(frame, text=f"Ejecutar Análisis {tipo.capitalize()}",
                    command=lambda t=tipo: ejecutar_analisis(t, text_widgets[t]))
    btn.pack(pady=5)

    area_texto = scrolledtext.ScrolledText(frame, width=100, height=30)
    area_texto.pack(fill='both', expand=True, padx=10, pady=5)
    area_texto.config(state='disabled')

    text_widgets[tipo] = area_texto

root.mainloop()
