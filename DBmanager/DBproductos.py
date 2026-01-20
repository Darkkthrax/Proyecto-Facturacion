import sqlite3
from tkinter import messagebox
from gui.productos import verificar_entradas_productos, actualizar_datos_admin_productos
from utils.entradas import borrar_entradas

#! FUNCIONES EN DB PARA PRODUCTOS
# Función para seleccionar todos los elementos de la tabla "tbl_productos"
def traer_productos_db():
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_productos ORDER BY nombre")
            return cursor.fetchall()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Función para traer solo 1 producto por ID
def traer_producto_id_db(id):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id_producto, nombre, descripcion, precio_unitario FROM tbl_productos WHERE id_producto = '{id}'")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Funcion para traer el inventario de un producto por su id
def traer_inventario_producto_id_db(id):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT inventario FROM tbl_productos WHERE id_producto = '{id}'")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Funcion para traer el inventario de un producto por su nombre
def traer_inventario_producto_nombre_db(nombre):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT inventario FROM tbl_productos WHERE nombre = '{nombre}'")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Funcion para traer solo 1 producto por su nombre
def traer_producto_nombre_db(nombre):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT id_producto, nombre, descripcion, precio_unitario FROM tbl_productos WHERE nombre = '{nombre}'")
            return cursor.fetchone()
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

# Funcion para agregar un producto nuevo a 'tbl_prodcutos
def agregar_producto_db(id, nombre, descripcion, marca, cantidad_venta, unidad_medida, precio, inventario, tabla, ventana, entradas):
    from utils.utils import verificar_productos
    try:
        if verificar_entradas_productos(id, nombre, descripcion, inventario, precio):
            messagebox.showwarning("Campos vacíos", "Verifique que todos los campos esté llenos.", parent=ventana)
        else:
            if verificar_productos(id, nombre):
                messagebox.showwarning("Producto duplicado", "Ya existe un producto con la misma ID o el mismo nombre. Modifique alguno de los parámetros", parent=ventana)
            else:
                print(f"id:{id}, nombre:{nombre}, descripcion:{descripcion}, inventario:{inventario}, precio:{precio}")
                with sqlite3.connect("db/database.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO tbl_productos (id_producto, nombre_producto, descripcion, inventario, precio_unitario) VALUES ({id}, '{nombre}', '{descripcion}', {inventario}, {precio})")
                actualizar_datos_admin_productos(tabla)
                borrar_entradas(entradas)
                messagebox.showinfo("Base de datos", "Producto agregado correctamente", parent=ventana)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)

# Función para editar un producto
def editar_producto_db(id, nombre, descripcion, inventario, precio, tabla, ventana):
    try:
        if verificar_entradas_productos(id, nombre, descripcion, inventario, precio):
            messagebox.showwarning("Campos vacíos", "Verifique que todos los campos esté llenos.", parent=ventana)
        else:
            print(f"id:{id}, nombre:{nombre}, descripcion:{descripcion}, inventario:{inventario}, precio:{precio}")
            with sqlite3.connect("db/database.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE tbl_productos SET nombre = '{nombre}', descripcion = '{descripcion}', inventario = {inventario}, precio_unitario = {precio} WHERE id_producto = {id}")
            actualizar_datos_admin_productos(tabla)
            messagebox.showinfo("Base de datos", "Producto actualizado correctamente", parent=ventana)
            ventana.destroy()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)

# Funcion para editar el inventario en la base de datos
def editar_inventario_producto(id, inventario, ventana):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE tbl_productos SET inventario = {inventario} WHERE id_producto = {id}")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)

# Función para eliminar un producto
def eliminar_producto_db(id, ventana):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM tbl_productos WHERE id_producto = {id}")
        messagebox.showinfo("Base de datos", "Producto eliminado correctamente", parent=ventana)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)