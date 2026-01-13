import sqlite3
from tkinter import messagebox
from .DBproductos import traer_inventario_producto_id_db, editar_inventario_producto
from models.models import info_empresa, impuesto, get_cliente, get_productos_factura

#! FUNCIONES PARA FACTURACIÓN EN DB
# Crear factura en base de datos
def crear_factura_db(id, fecha, total_sin, total_imp, total_final, ventana):
    cliente = get_cliente()
    productos_factura = get_productos_factura()
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO tbl_factura (id_factura, nombre_cliente, identificacion, direccion, telefono, fecha_emision, impuesto, total_sin_impuesto, total_impuesto, total_final) VALUES ({id}, '{cliente[1]} {cliente[2]}', '{cliente[0]}', '{info_empresa[2]}', '{cliente[4]}', '{fecha}', {float(impuesto)}, {float(total_sin)}, {float(total_imp)}, {float(total_final)})")
            conn.commit()
            
            for producto in productos_factura:
                inventario = traer_inventario_producto_id_db(producto[0])[0]
                inventario -= int(producto[3])
                
                cursor.execute(f"INSERT INTO tbl_productos_factura (id_producto, id_factura, nombre_producto, descripcion, cantidad, precio_unitario, subtotal) VALUES ({int(producto[0])}, {id}, '{producto[1]}', '{producto[2]}', {int(producto[3])}, {float(producto[4])}, {float(producto[5])})")
                conn.commit()
                
                editar_inventario_producto(producto[0], inventario, ventana)
                conn.commit()
            
        messagebox.showinfo("Base de datos", "Factura ingresada con éxito", parent=ventana)
        productos_factura = []
        cliente = ()
        ventana.destroy()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)

# Función para llamar a todas las facturas en la base de datos
def traer_facturas_db():
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_factura ORDER BY id_factura")
            return cursor.fetchall()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Función para traer el contador de id_factura
def traer_ultima_id_factura_db():
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_factura FROM tbl_factura ORDER BY id_factura DESC")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")