import sqlite3                          # Librería SQL para almacenar los productos
import os                               # Librería para manejar el sistema operativo
from tkinter import messagebox          # Messagebox
from auth.auth import iniciar_sesion
from gui.facturacion import registrar_usuario

# Función para crear la base de datos
def crear_db(root):
    try:
        # Verificación de la carpeta "db" para crear la base de datos.
        if not os.path.isdir('db'):
            os.mkdir('db')
        
        #TODO: Mejorar la estructura de la base de datos
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            sql_script = """
                CREATE TABLE IF NOT EXISTS tbl_tipo_usuario (id_tipo INTEGER PRIMARY KEY CHECK(LENGTH(id_tipo) <= 1), nombre TEXT CHECK(LENGTH(nombre) <= 10 AND nombre IS NOT NULL));
                CREATE TABLE IF NOT EXISTS tbl_sucursales (id_sucursal INTEGER PRIMARY KEY CHECK(LENGTH(id_sucursal) <= 2), nombre TEXT CHECK(LENGTH(nombre) <= 25 AND nombre IS NOT NULL), direccion TEXT CHECK(LENGTH(direccion) <= 30 AND direccion IS NOT NULL), telefono TEXT CHECK(LENGTH(telefono) <= 10));
                CREATE TABLE IF NOT EXISTS tbl_unidad_medida (id_unidad INTEGER PRIMARY KEY CHECK(LENGTH(id_unidad) <= 1), nombre TEXT CHECK(LENGTH(nombre) <= 10 AND nombre IS NOT NULL));
                CREATE TABLE IF NOT EXISTS tbl_usuarios (documento_identidad TEXT PRIMARY KEY CHECK(LENGTH(documento_identidad) <= 11), nombre TEXT CHECK(LENGTH(nombre) <= 40 AND nombre IS NOT NULL), apellidos TEXT CHECK(LENGTH(apellidos) <= 40 AND apellidos IS NOT NULL), contrasena TEXT CHECK(LENGTH(contrasena) <= 60), telefono TEXT CHECK(LENGTH(telefono) <= 10), correo TEXT CHECK(LENGTH(correo) <= 50), tipo_usuario INTEGER REFERENCES tbl_tipo_usuario(id_tipo));
                CREATE TABLE IF NOT EXISTS tbl_productos (id_producto TEXT PRIMARY KEY CHECK(LENGTH(id_producto) <= 48 AND id_producto IS NOT NULL), nombre TEXT CHECK(LENGTH(nombre) <= 30 AND nombre IS NOT NULL), descripcion TEXT CHECK(LENGTH(descripcion) <= 50), marca TEXT CHECK(LENGTH(marca) <= 30), cantidad_venta INTEGER CHECK(LENGTH(cantidad_venta) <= 4 AND cantidad_venta IS NOT NULL), unidad_medida INTEGER REFERENCES tbl_unidad_medida(id_unidad), precio_unitario REAL CHECK(LENGTH(precio_unitario) <= 11 AND precio_unitario IS NOT NULL), inventario REAL CHECK(LENGTH(inventario) <= 7 AND inventario IS NOT NULL), estado INTEGER CHECK(LENGTH(estado) <= 1 AND estado IS NOT NULL));
                CREATE TABLE IF NOT EXISTS tbl_factura (id_factura TEXT PRIMARY KEY CHECK(LENGTH(id_factura) <= 10 AND id_factura IS NOT NULL), cedula TEXT REFERENCES tbl_usuarios(documento_identidad), id_sucursal INTEGER REFERENCES tbl_sucursales(id_sucursal), fecha_emision TEXT CHECK(LENGTH(fecha_emision)<= 19 AND fecha_emision IS NOT NULL), impuesto REAL CHECK(LENGTH(impuesto) <= 4 AND impuesto IS NOT NULL), subtotal REAL CHECK(LENGTH(subtotal) <= 12 AND subtotal IS NOT NULL), total_impuesto REAL CHECK(LENGTH(total_impuesto) <= 11 AND total_impuesto IS NOT NULL), total REAL CHECK(LENGTH(total) <= 13 AND total IS NOT NULL));
                CREATE TABLE IF NOT EXISTS tbl_productos_factura (id_factura TEXT REFERENCES tbl_factura(id_factura), id_producto TEXT REFERENCES tbl_productos(id_producto), cantidad REAL CHECK(LENGTH(cantidad) <= 5 AND cantidad IS NOT NULL), subtotal REAL CHECK(LENGTH(subtotal) <= 11 AND subtotal IS NOT NULL), impuesto REAL CHECK(LENGTH(impuesto) <= 10 AND impuesto IS NOT NULL))
            """
            cursor.executescript(sql_script)
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