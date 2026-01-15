from tkinter import messagebox
import sys
from fpdf import FPDF
from DBmanager.DBproductos import traer_productos_db, eliminar_producto_db
from DBmanager.DBfacturacion import traer_ultima_id_factura_db
from gui.facturacion import verificar_producto_usuario_factura
from models.models import productos_factura, get_productos_factura, set_productos_factura, set_cliente

#! FUNCIONES UTILS GENERALES
# Función para finalizar el programa
def finalizar_programa(root):
    if messagebox.askokcancel("Salir", "¿Seguro que deseas salir del programa?"):
        root.destroy()
        sys.exit("Cerrando el programa")

# Funcion para verificar si existen productos iguales
def verificar_productos(id, nombre):
    productos = traer_productos_db()
    return any(int(id) in producto for producto in productos) if id != 'Agregar por código' else any(nombre in producto for producto in productos)

# Función para regresar al menú
def regresar_menu(root, ventana):
    ventana.destroy()
    root.deiconify()
    cliente = ()
    productos_factura = []
    set_cliente(cliente)
    set_productos_factura(productos_factura)

# Funcion para eliminar un producto de las tablas y la base de datos
def eliminar_producto(tabla, ventana, frame = None, db = False):
    productos_factura = get_productos_factura()
    if messagebox.askyesno("Eliminar producto", "Confirme la eliminación del producto", parent=ventana):
        producto_seleccionado = tabla.selection()[0]
        info_producto_seleccionado = tabla.item(producto_seleccionado, 'values')
        if productos_factura != []:
            for i in range(len(productos_factura)):
                if int(info_producto_seleccionado[0]) in productos_factura[i]:
                    del productos_factura[i]
                    set_productos_factura(productos_factura)
                    break
        if db:
            eliminar_producto_db(info_producto_seleccionado[0], ventana)
        else:
            verificar_producto_usuario_factura(frame, ventana)
        tabla.delete(producto_seleccionado)

