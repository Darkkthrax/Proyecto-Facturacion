import tkinter as tk
from tkinter import ttk
import os
from DBmanager.DBfacturacion import traer_facturas_db
from utils.utils import regresar_menu
from utils.arboles import *
from gui.facturacion import abrir_pdf

#! FUNCIONES PARA BOTÓN ADMINISTRAR FACTURAS
def administrar_facturas_realizadas(root):
    headers = ['ID', 'Id_Factura', 'Cliente', 'Documento', 'Dirección', 'Telefono', 'Fecha_Emisión', 'Impuesto', 'Total_sin_impuesto', 'Total_impuesto', 'Total_final']
    ventana_admin_facturas = tk.Toplevel(root)
    ventana_admin_facturas.title("Administrar Facturas")
    ventana_admin_facturas.state(newstate='zoomed')
    ttk.Label(ventana_admin_facturas, text="Administrar Facturas", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    tabla_facturas = ttk.Treeview(ventana_admin_facturas, columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10'))
    tabla_facturas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    scrollbar = ttk.Scrollbar(ventana_admin_facturas, orient=tk.VERTICAL, command=tabla_facturas.yview)
    tabla_facturas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_facturas.yview)
    scrollbar.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="nse")
    tabla_facturas.bind("<MouseWheel>", lambda e: on_mousewheel(e, tabla_facturas))
    
    for i in range(len(headers)):
        tabla_facturas.heading(f'#{i}', text=headers[i])
        tabla_facturas.column(f'#{i}', minwidth=50, width=100)
    
    facturas = traer_facturas_db()
    for fila in facturas:
        tabla_facturas.insert('', tk.END, text=str(facturas.index(fila)), values=fila)
    
    frame_opciones = ttk.Frame(ventana_admin_facturas)
    frame_opciones.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
    
    btn_regresar = tk.Button(frame_opciones, text="Volver", bg='skyblue', command=lambda: regresar_menu(root, ventana_admin_facturas))
    btn_regresar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    btn_revisar_factura = tk.Button(frame_opciones, text="Revisar Factura", state='disabled', command=lambda: abrir_factura(tabla_facturas))
    btn_revisar_factura.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
    
    ventana_admin_facturas.grid_rowconfigure(1, weight=1)
    ventana_admin_facturas.grid_columnconfigure(0, weight=3)
    ventana_admin_facturas.grid_columnconfigure(1, weight=1)
    
    frame_opciones.grid_columnconfigure(1, weight=1)
    
    tabla_facturas.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tabla_facturas, btn_revisar_factura))

# Función para abrir la factura guardada localmente
def abrir_factura(tabla):
    producto_seleccionado = tabla.selection()[0]
    info_producto_seleccionado = tabla.item(producto_seleccionado, 'values')
    
    ruta = os.path.join('src/Facturas', f"{info_producto_seleccionado[0]}.pdf")
    abrir_pdf(ruta)