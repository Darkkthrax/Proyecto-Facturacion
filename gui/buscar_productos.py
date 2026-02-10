import tkinter as tk
from tkinter import ttk
from utils.entradas import on_focus_in, on_focus_out
from utils.arboles import *
from DBmanager.DBproductos import traer_productos_busqueda_db

# Función para crear la vista para buscar productos
def buscar_producto(root):
    headers = ['ID', 'Codigo', 'Nombre', 'Descripción', 'Marca', 'Cantidad Venta', 'Precio']
    ventana_buscador = tk.Toplevel(root)
    ventana_buscador.title('Buscar Producto')
    ventana_buscador.geometry('925x512')
    
    frame_opciones = tk.Frame(ventana_buscador)
    frame_opciones.grid(row=0, column=0, sticky='nsew')
    
    btn_volver = tk.Button(frame_opciones, text='Volver', command=ventana_buscador.destroy)
    btn_volver.grid(row=0, column=0, padx=5, pady=5, sticky='nsw')
    
    ttk.Label(frame_opciones, text='Buscar Producto', font=("Arial", 16, "bold")).grid(row=0, column=1, padx=5, pady=20, sticky="nw")
    
    btn_seleccionar = tk.Button(frame_opciones, text='Seleccionar', state='disabled')
    btn_seleccionar.grid(row=0, column=2, padx=5, pady=5, sticky='nse')
    
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
    print('Entra en actualizacion')
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