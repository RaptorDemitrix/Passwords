import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Archivo de la base de datos
DB_FILE = "passwords.db"

def inicializar_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credenciales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sitio TEXT NOT NULL,
                usuario TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error inicializando DB: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Inicializamos la base de datos
inicializar_db()

def guardar_datos():
    sitio = entry_sitio.get()
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Validación básica
    if not sitio or not usuario or not contrasena:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO credenciales (sitio, usuario, contrasena) VALUES (?, ?, ?)", (sitio, usuario, contrasena))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Credenciales guardadas correctamente.")
        
        # Limpiar campos después de guardar
        entry_sitio.delete(0, tk.END)
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")

def ver_registros():
    ventana_registros = tk.Toplevel(root)
    ventana_registros.title("Contraseñas Guardadas")
    ventana_registros.geometry("500x350")

    # Crear Treeview
    tree = ttk.Treeview(ventana_registros, columns=("ID", "Sitio", "Usuario", "Contrasena"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Sitio", text="Sitio / App")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contrasena", text="Contraseña")

    tree.column("ID", width=30, anchor="center")
    tree.column("Sitio", width=150)
    tree.column("Usuario", width=150)
    tree.column("Contrasena", width=150)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Llenar con datos de la DB
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM credenciales")
        filas = cursor.fetchall()
        for fila in filas:
            tree.insert("", tk.END, values=fila)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer la base de datos: {e}")

    # Función para eliminar el registro seleccionado
    def eliminar_registro():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un registro de la tabla.")
            return
        
        # Pedir confirmación
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta contraseña?")
        if respuesta:
            item = tree.item(seleccion[0])
            registro_id = item['values'][0]
            
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM credenciales WHERE id = ?", (registro_id,))
                conn.commit()
                conn.close()
                
                # Remover de la tabla visualmente
                tree.delete(seleccion[0])
                messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")

    # Botón de eliminar
    btn_eliminar = tk.Button(ventana_registros, text="Eliminar Registro Seleccionado", command=eliminar_registro,
                             bg="#f44336", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
    btn_eliminar.pack(pady=10)

# Crear la ventana principal
root = tk.Tk()
root.title("Gestor de Contraseñas")
root.geometry("400x300")
root.resizable(False, False)

# Estilo básico
font_label = ("Arial", 10, "bold")
font_entry = ("Arial", 10)

# Título
titulo = tk.Label(root, text="Gestor de Contraseñas", font=("Arial", 14, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=15)

# Campo Sitio
tk.Label(root, text="Sitio / App:", font=font_label).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_sitio = tk.Entry(root, width=30, font=font_entry)
entry_sitio.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Campo Usuario
tk.Label(root, text="Usuario:", font=font_label).grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_usuario = tk.Entry(root, width=30, font=font_entry)
entry_usuario.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Campo Contrasena
tk.Label(root, text="Contraseña:", font=font_label).grid(row=3, column=0, padx=10, pady=5, sticky="e")
# Nota: show="*" oculta los caracteres tipeados
entry_contrasena = tk.Entry(root, width=30, font=font_entry, show="*")
entry_contrasena.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Botón para guardar
btn_guardar = tk.Button(root, text="Guardar Credenciales", command=guardar_datos, 
                        bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), cursor="hand2")
btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

btn_ver = tk.Button(root, text="Ver Contraseñas", command=ver_registros, 
                    bg="#2196F3", fg="white", font=("Arial", 11, "bold"), cursor="hand2")
btn_ver.grid(row=5, column=0, columnspan=2, pady=5)

# Iniciar la aplicación
if __name__ == "__main__":
    root.mainloop()
