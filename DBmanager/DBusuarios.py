import sqlite3
import bcrypt
import os
from dotenv import load_dotenv
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
def registrar_usuario_db(root, documento, nombre, apellidos, telefono, correo, contrasena, tipo_usuario, ventana):
    from auth.auth import iniciar_sesion
    from gui.facturacion import verificar_entradas_registro
    #* Validación de entradas
    if verificar_entradas_registro(documento, nombre, apellidos, telefono, correo, contrasena, tipo_usuario):
        messagebox.showwarning("Campos vacíos", "Verifique que todos los campos esté llenos.", parent=ventana)
        return
    #* Validación de existencia de usuario
    if verificar_usuario_db(documento):
        messagebox.showwarning("Usuario duplicado", "Ya existe un usuario con el mismo documento. Modifique el documento", parent=ventana)
        return
    #* Validación de correo
    if '@' not in correo or verificar_dominios(correo) or '.com' not in correo:
        messagebox.showerror("Registro", "Agregue un correo disponible", parent=ventana)
        return
    #* Validación de contraseña vacía
    if contrasena == 'Dejar vacío si es cliente':
        messagebox.showwarning("Contraseña", "Ingrese una contraseña", parent=ventana)
        return
    #* Validación de tipo de usuario y caracteres de contraseña
    if tipo_usuario != 2  and len(contrasena) < 8:
        messagebox.showwarning("Contraseña", "Ingrese una contraseña de al menos 8 dígitos", parent=ventana)
        return
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO tbl_usuarios (documento_identidad, nombre, apellidos, contrasena, telefono, correo, tipo_usuario) VALUES ('{documento}', '{nombre}', '{apellidos}', '{encriptar_contrasena(contrasena) if contrasena != '' else ''}', '{telefono}', '{correo}', '{tipo_usuario}')")
        messagebox.showinfo("Base de datos", "Usuario agregado correctamente", parent=ventana)
        ventana.destroy()
        if not get_sesion(): iniciar_sesion(root)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)


#! FUNCIÓN PARA ENCRIPTAR CONTRASEÑAS CON PEPPER Y SALT
def encriptar_contrasena(contrasena):
    load_dotenv()                                                   # Trae la información del archivo .env
    pepper = os.getenv('PASSWORD_PEPPER')
    salt = bcrypt.gensalt(rounds=int(os.getenv('SALT_ROUNDS')))
    password = (contrasena + pepper).encode('utf-8')
    contrasena_hash = bcrypt.hashpw(password, salt)
    print(contrasena_hash.decode('utf-8'))
    return contrasena_hash.decode('utf-8')

#! FUNCIÓN PARA VERIFICAR DOMINIOS DE CORREOS
def verificar_dominios(correo):
    dominios = ['gmail', 'hotmail', 'outlook', 'yahoo']
    for dominio in dominios:
        if dominio in correo:
            return False
    return True