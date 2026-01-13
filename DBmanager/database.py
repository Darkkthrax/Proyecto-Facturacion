import sqlite3                          # Librería SQL para almacenar los productos
import os                               # Librería para manejar el sistema operativo
from tkinter import messagebox          # Messagebox
from auth.auth import iniciar_sesion
from gui.facturacion import registrar_usuario

# Función para crear la base de datos
def crear_db(root):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS tbl_factura  (id_factura INTEGER  PRIMARY KEY, nombre_cliente TEXT CHECK(LENGTH(nombre_cliente) <= 50 AND nombre_cliente IS NOT NULL), identificacion TEXT CHECK(LENGTH(identificacion) <= 50 AND identificacion IS NOT NULL), direccion TEXT CHECK(LENGTH(direccion) <= 100), telefono TEXT CHECK(LENGTH(telefono) <= 20), fecha_emision TEXT NOT NULL, impuesto REAL NOT NULL, total_sin_impuesto REAL NOT NULL, total_impuesto REAL NOT NULL, total_final REAL NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS tbl_productos_factura (id_producto INTEGER, id_factura INT NOT NULL, nombre_producto TEXT CHECK(LENGTH(nombre_producto) <= 50 AND nombre_producto IS NOT NULL), descripcion TEXT CHECK(LENGTH(descripcion) <= 100), cantidad INTEGER NOT NULL, precio_unitario REAL NOT NULL, subtotal REAL NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS tbl_productos (id_producto INTEGER PRIMARY KEY, nombre_producto TEXT CHECK(LENGTH(nombre_producto) <= 50 AND NOT NULL), descripcion TEXT CHECK(LENGTH(descripcion) <= 100), inventario INTEGER NOT NULL, precio_unitario REAL NOT NULL)")
            cursor.execute("CREATE TABLE IF NOT EXISTS tbl_usuarios (documento_identidad TEXT PRIMARY KEY, nombre TEXT CHECK(LENGTH(nombre) <= 50 AND NOT NULL), apellidos TEXT CHECK(LENGTH(apellidos) <= 100), contraseña TEXT, telefono TEXT NOT NULL, correo TEXT, tipo_usuario TEXT)")
        root.withdraw()     # Se oculta la pestaña principal
        messagebox.showinfo("Base de datos", "La base de datos ha sido creada satisfactoriamente")      # Mensaje cuando la base de datos funciona correctamente.
        registrar_usuario(root, 'admin1')
    except sqlite3.Error as e:
        messagebox.showwarning("Error", f"Error a la hora de crear la base de datos: {e}")

# Función para verificar la base de datos antes de iniciar.
def verificar_db(root):
    if os.path.exists("db/database.db"):
        try:
            with sqlite3.connect("db/database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = cursor.fetchall()
                cursor.execute("SELECT * FROM tbl_usuarios WHERE tipo_usuario = 'admin'")
                admins = cursor.fetchall()
            root.withdraw()
            crear_db(root) if len(tablas) == 0 else messagebox.showinfo("Base de datos", "Base de datos cargada correctamente")
            registrar_usuario(root, 'admin1') if len(admins) == 0  else iniciar_sesion(root)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")
    else:
        crear_db(root)