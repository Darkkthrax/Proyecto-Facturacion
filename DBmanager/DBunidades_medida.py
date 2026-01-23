import sqlite3
from tkinter import messagebox

def crear_unidad_medida_db(ventana, nombre):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_unidad FROM tbl_unidad_medida ORDER BY id_unidad DESC LIMIT 1")
            ultimo_id = cursor.fetchone()
            if ultimo_id != None:
                cursor.execute(f"INSERT INTO tbl_unidad_medida (id_unidad, nombre) VALUES ({int(ultimo_id[0])+1}, '{nombre}')")
            else:
                cursor.execute(f"INSERT INTO tbl_unidad_medida (id_unidad, nombre) VALUES (1, '{nombre}')")
            messagebox.showinfo("Creación Exitosa", "Se agregó la unidad de medida correctamente", parent=ventana)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}", parent=ventana)

def traer_unidades_medida():
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM tbl_unidad_medida ORDER BY nombre DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

def traer_unidad_medida_nombre(nombre):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM tbl_unidad_medida WHERE nombre = '{nombre}'")
            return cursor.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

def editar_unidad_medida_db(ventana, nombre, nuevo_nombre):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE tbl_unidad_medida SET nombre = '{nuevo_nombre}' WHERE nombre = '{nombre}'")
        messagebox.showinfo("Editar Unidad", "Se actualizó correctamente la unidad de medida", parent=ventana)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")

def eliminar_unidad_medida_db(id):
    try:
        with sqlite3.connect("db/database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM tbl_unidad_medida WHERE id_producto ='{id}'")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"El archivo es corrupto o no es una base de datos {e}")