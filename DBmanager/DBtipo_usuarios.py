import sqlite3
from tkinter import messagebox

def traer_tipos():
    try:
        with sqlite3.connect('db/database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_tipo_usuario ORDER BY id_tipo")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Se produjo un error con la base de datos: {e}")