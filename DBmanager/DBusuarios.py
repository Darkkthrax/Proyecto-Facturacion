import sqlite3
from tkinter import messagebox
from models.models import get_sesion

#! FUNCIONES EN DB PARA USUARIOS
# Función para seleccionar todos los elementos de la tabla "tbl_productos"
def traer_usuarios_db():
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_usuarios ORDER BY apellidos")
            return cursor.fetchall()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Verificar si un usuario existe con su id
def verificar_usuario_db(id):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM tbl_usuarios WHERE documento_identidad = '{id}'")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Función para registrar usuarios en la db
def registrar_usuario_db(root, id, nombre, apellidos, telefono, correo, contrasena, tipo_usuario, ventana):
    from auth.auth import iniciar_sesion
    from gui.facturacion import verificar_entradas_registro
    try:
        if '@' not in correo:
            messagebox.showerror("Registro", "Agregue un correo disponible")
        elif verificar_entradas_registro(id, nombre, apellidos, telefono, correo, contrasena, tipo_usuario):
                messagebox.showwarning("Campos vacíos", "Verifique que todos los campos esté llenos.", parent=ventana)
        else:
            if verificar_usuario_db(id):
                messagebox.showwarning("Usuario duplicado", "Ya existe un usuario con la misma ID. Modifique el identificador", parent=ventana)
            else:
                with sqlite3.connect("db/database.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO tbl_usuarios (documento_identidad, nombre, apellidos, contraseña, telefono, correo, tipo_usuario) VALUES ({id}, '{nombre}', '{apellidos}', '{contrasena if contrasena != 'Dejar vacío si es cliente' else ''}', {telefono}, '{correo}', '{tipo_usuario}')")
                messagebox.showinfo("Base de datos", "Usuario agregado correctamente", parent=ventana)
                ventana.destroy()
                if not get_sesion(): iniciar_sesion(root)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)