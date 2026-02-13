import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.entradas import on_focus_in, on_focus_out
from utils.arboles import *
from DBmanager.DBproductos import traer_productos_busqueda_db
from models.models import get_productos_factura, set_productos_factura

# Función para crear la vista para buscar productos
def buscar_producto(root, frame, tabla_factura):
    headers = ['ID', 'Codigo', 'Nombre', 'Descripción', 'Marca', 'Cantidad Venta', 'Precio']
    ventana_buscador = tk.Toplevel(root)
    ventana_buscador.title('Buscar Producto')
    ventana_buscador.geometry('925x512')
    
    frame_opciones = tk.Frame(ventana_buscador)
    frame_opciones.grid(row=0, column=0, sticky='nsew')
    
    btn_volver = tk.Button(frame_opciones, text='Volver', command=ventana_buscador.destroy)
    btn_volver.grid(row=0, column=0, padx=5, pady=5, sticky='nsw')
    
    ttk.Label(frame_opciones, text='Buscar Producto', font=("Arial", 16, "bold")).grid(row=0, column=1, padx=5, pady=20, sticky="nw")
    
    ttk.Label(frame_opciones, text='Cantidad:').grid(row=0, column=2, padx=5, pady=5, )
    
    cantidad_producto = tk.Entry(frame_opciones, fg='grey')
    cantidad_producto.grid(row=0, column=3, padx=5, pady=5, sticky='ns')
    cantidad_producto.insert(0, '1')
    cantidad_producto.bind("<FocusIn>", lambda event: on_focus_in(cantidad_producto, "1"))
    cantidad_producto.bind("<FocusOut>", lambda event: on_focus_out(cantidad_producto, "1"))
    
    btn_seleccionar = tk.Button(frame_opciones, text='Seleccionar', state='disabled', command= lambda: seleccionar_producto(ventana_buscador, tabla_resultados, tabla_factura, frame, buscador_producto, cantidad_producto))
    btn_seleccionar.grid(row=0, column=4, padx=5, pady=5, sticky='nse')
    
    buscador_producto = tk.Entry(ventana_buscador)
    buscador_producto.bind('<KeyRelease>', lambda e: retrasar_funcion(ventana_buscador, tabla_resultados, buscador_producto))
    buscador_producto.bind("<FocusIn>", lambda event: on_focus_in(buscador_producto, "Buscar producto"))
    buscador_producto.bind("<FocusOut>", lambda event: on_focus_out(buscador_producto, "Buscar producto"))
    buscador_producto.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    frame_tabla = tk.Frame(ventana_buscador)
    frame_tabla.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    tabla_resultados = ttk.Treeview(frame_tabla, columns=('#1', '#2', '#3', '#4', '#5', '#6'))
    tabla_resultados.column('#0', width=0, stretch=False)
    tabla_resultados.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    tabla_resultados.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tabla_resultados, btn_seleccionar))
    
    for i in range(1, len(headers)):
        tabla_resultados.heading(f'#{i}', text=headers[i])
        tabla_resultados.column(f'#{i}', width=150, minwidth=80, stretch=True)
    
    ventana_buscador.grid_rowconfigure(2, weight=1)
    
    frame_tabla.grid_columnconfigure(0, weight=1)
    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(1, weight=0)

# Funcion para actualizar tabla de búsqueda
def actualizar_busqueda(ventana, tabla, entrada):
    if tabla.get_children():
        for item in tabla.get_children():
            tabla.delete(item)
    
    productos = traer_productos_busqueda_db(entrada.get())
    print(productos)
    for producto in productos:
        valores = []
        for i in range(0, len(producto)):
            if i == 4:
                valores.append(f'{str(producto[i])} {producto[i+1]}')
                continue
            if i == 5:
                continue
            valores.append(producto[i])
        tabla.insert('', tk.END, text=str(productos.index(producto)), values=valores)

# Función para retrasar la búsqueda al pulsar una tecla
def retrasar_funcion(ventana, tabla, entrada):
    print('Entra en retrasar')
    if hasattr(retrasar_funcion, 'timer'):
        entrada.after_cancel(retrasar_funcion.timer)
    
    retrasar_funcion.timer = entrada.after(700, lambda: actualizar_busqueda(ventana, tabla, entrada))

# Función para botón seleccionar
def seleccionar_producto(ventana, tabla, tabla_factura, frame, entrada_producto, entrada_cantidad):
    if int(entrada_cantidad.get()) <= 0:
        messagebox.showerror('Error de cantidad', 'La cantidad seleccionada no puede ser menor a 1.', parent=ventana)
        return

    from .facturacion import actualizar_datos_facturación
    info_producto = tabla.item(tabla.selection()[0], 'values')
    productos_factura = get_productos_factura()
    
    producto = [info_producto[0], info_producto[1], info_producto[2], info_producto[3], int(entrada_cantidad.get()), info_producto[5], int(entrada_cantidad.get()) * float(info_producto[5])]
    
    if productos_factura:
        producto_en_factura = False
        for producto_factura in productos_factura:
            if info_producto[0] in producto_factura:
                producto_factura[4] += int(entrada_cantidad.get())
                producto_factura[6] = float(producto_factura[5]) * int(producto_factura[4])
                producto_en_factura = True
                break
        if not producto_en_factura:
            productos_factura.append(producto)
    else:
        productos_factura.append(producto)
    
    set_productos_factura(productos_factura)
    actualizar_datos_facturación(tabla_factura, frame, True)
    
    entrada_producto.delete(0, tk.END)
    entrada_producto.insert(0, "Buscar producto")
    entrada_producto.config(fg='grey')
    
    for item in tabla.get_children():
        tabla.delete(item)