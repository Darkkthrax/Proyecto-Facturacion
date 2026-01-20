import tkinter as tk                    # Librería de interfaz gráfica
from tkinter import ttk
from utils.arboles import *
from utils.entradas import on_focus_in, on_focus_out
from gui.unidades_medida import crear_admin_unidades_medida

#! FUNCIONES PARA BOTÓN ADMINISTRAR PRODUCTOS
# Función para crear árbol de "administrar productos"
def crear_admin_productos(root):
    from utils.utils import regresar_menu, eliminar_producto
    from DBmanager.DBproductos import traer_productos_db
    headers = ['ID', 'Id_Producto', 'Nombre_Producto', 'Descripción', 'Inventario', 'Precio_Unitario']
    ventana_productos = tk.Toplevel(root)
    ventana_productos.title("Administrar productos")
    ventana_productos.state(newstate='zoomed')
    
    titulo_admin_productos = ttk.Label(ventana_productos, text="Administrar productos", font=("Arial", 16, "bold"))
    titulo_admin_productos.grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    frame_opciones = tk.Frame(ventana_productos)
    frame_opciones.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
    
    tabla_productos = ttk.Treeview(ventana_productos, columns=('#1', '#2', '#3', '#4', '#5'))
    tabla_productos.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    scrollbar = ttk.Scrollbar(ventana_productos, orient=tk.VERTICAL, command=tabla_productos.yview)
    tabla_productos.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_productos.yview)
    scrollbar.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="nse")
    tabla_productos.bind("<MouseWheel>", lambda e: on_mousewheel(e, tabla_productos))
    
    for i in range(len(headers)):
        tabla_productos.heading(f'#{i}', text=headers[i])
        tabla_productos.column(f'#{i}', minwidth=100)
    productos = traer_productos_db()
    for fila in productos:
        tabla_productos.insert('', tk.END, text=str(productos.index(fila)), values=fila)
    
    btn_regresar = tk.Button(frame_opciones, text="Volver", bg='skyblue', command=lambda: regresar_menu(root, ventana_productos))
    btn_regresar.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    btn_agregar_producto = tk.Button(frame_opciones, text="Agregar Producto", bg='lightgreen', command=lambda: agregar_productos(root, tabla_productos))
    btn_agregar_producto.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    btn_editar_producto = tk.Button(frame_opciones, text="Editar", command=lambda: editar_producto(root, tabla_productos), state='disabled')
    btn_editar_producto.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    btn_eliminar_producto = tk.Button(frame_opciones, text="Eliminar", bg="pink", command=lambda: eliminar_producto(tabla_productos, ventana_productos, db= True), state='disabled')
    btn_eliminar_producto.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
    
    btn_ver_unidades = tk.Button(frame_opciones, text="Ver Unidades Medida", command=lambda: crear_admin_unidades_medida(ventana_productos))
    btn_ver_unidades.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
    
    ventana_productos.grid_rowconfigure(1, weight=1)
    ventana_productos.grid_columnconfigure(0, weight=3)
    ventana_productos.grid_columnconfigure(1, weight=1)
    
    frame_opciones.grid_columnconfigure(1, weight=1)
    
    tabla_productos.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tabla_productos, btn_editar_producto, btn_eliminar_producto))

# Función para actualizar los productos en el arbol de "administrar productos"
def actualizar_datos_admin_productos(tabla):
    from DBmanager.DBproductos import traer_productos_db
    for item in tabla.get_children():
        tabla.delete(item)
    productos = traer_productos_db()
    for fila in productos:
        tabla.insert('', tk.END, text=str(productos.index(fila)), values=fila)

# Función para agregar productos
def agregar_productos(root, tabla):
    from DBmanager.DBproductos import agregar_producto_db
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.geometry("400x300")
    titulo_agregar=ttk.Label(ventana_agregar, text="Agregar producto")
    titulo_agregar.grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    label_id_producto = ttk.Label(ventana_agregar, text="ID del Producto:")
    label_id_producto.grid(row=1, column=0, padx=10, pady=5)
    input_id_producto = tk.Entry(ventana_agregar, width=30)
    input_id_producto.grid(row=1, column=1, padx=10, pady=5)

    label_nombre_producto = ttk.Label(ventana_agregar, text="Nombre del Producto:")
    label_nombre_producto.grid(row=2, column=0, padx=10, pady=5)
    input_nombre_producto = tk.Entry(ventana_agregar, width=30)
    input_nombre_producto.grid(row=2, column=1, padx=10, pady=5)
    
    label_descripcion = ttk.Label(ventana_agregar, text="Descripción:")
    label_descripcion.grid(row=3, column=0, padx=10, pady=5)
    input_descripcion = tk.Entry(ventana_agregar, width=30)
    input_descripcion.grid(row=3, column=1, padx=10, pady=5)
    
    label_inventario = ttk.Label(ventana_agregar, text="Inventario:")
    label_inventario.grid(row=4, column=0, padx=10, pady=5)
    input_inventario = tk.Entry(ventana_agregar, width=30)
    input_inventario.grid(row=4, column=1, padx=10, pady=5)
    
    label_precio = ttk.Label(ventana_agregar, text="Precio Unitario:")
    label_precio.grid(row=5, column=0, padx=10, pady=5)
    input_precio = tk.Entry(ventana_agregar, width=30)
    input_precio.grid(row=5, column=1, padx=10, pady=5)
    
    btn_agregar = ttk.Button(ventana_agregar, text="Agregar", command=lambda: agregar_producto_db(input_id_producto.get(), input_nombre_producto.get(), input_descripcion.get(), input_inventario.get(), input_precio.get(), tabla, ventana_agregar, [input_id_producto, input_nombre_producto, input_descripcion, input_inventario, input_precio]))
    btn_agregar.grid(row=6, column=1, padx=10, pady=5)

def verificar_entradas_productos(id, nombre, descripcion, inventario, precio):
    return str(id).strip == '' or nombre.strip() == '' or descripcion.strip() == '' or str(inventario).strip() == '' or str(precio).strip() == ''

# Función para editar el producto
def editar_producto(root, tabla):
    from DBmanager.DBproductos import editar_producto_db
    producto_seleccionado = tabla.selection()[0]
    info_producto_seleccionado = tabla.item(producto_seleccionado, 'values')
    ventana_editar_producto = tk.Toplevel(root)
    ventana_editar_producto.title("Editar Producto")
    ventana_editar_producto.geometry("400x300")
    titulo_editar=ttk.Label(ventana_editar_producto, text=f"Editar {info_producto_seleccionado[1]}", font=("Arial", 16, "bold"))
    titulo_editar.grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    ttk.Label(ventana_editar_producto, text="Nuevo nombre:").grid(row=1, column=0, padx=10, pady=5)
    input_nuevo_nombre = tk.Entry(ventana_editar_producto, fg='grey')
    input_nuevo_nombre.insert(0, f"{info_producto_seleccionado[1]}")
    input_nuevo_nombre.bind("<FocusIn>", lambda event: on_focus_in(input_nuevo_nombre, f"{info_producto_seleccionado[1]}"))
    input_nuevo_nombre.bind("<FocusOut>", lambda event: on_focus_out(input_nuevo_nombre, f"{info_producto_seleccionado[1]}"))
    input_nuevo_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(ventana_editar_producto, text="Nueva descripcion:").grid(row=2, column=0, padx=10, pady=5)
    input_nueva_descripcion = tk.Entry(ventana_editar_producto, fg='grey')
    input_nueva_descripcion.insert(0, f"{info_producto_seleccionado[2]}")
    input_nueva_descripcion.bind("<FocusIn>", lambda event: on_focus_in(input_nueva_descripcion, f"{info_producto_seleccionado[2]}"))
    input_nueva_descripcion.bind("<FocusOut>", lambda event: on_focus_out(input_nueva_descripcion, f"{info_producto_seleccionado[2]}"))
    input_nueva_descripcion.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(ventana_editar_producto, text="Nueva cantidad:").grid(row=3, column=0, padx=10, pady=5)
    input_nueva_cantidad = tk.Entry(ventana_editar_producto, fg='grey')
    input_nueva_cantidad.insert(0, f"{info_producto_seleccionado[3]}")
    input_nueva_cantidad.bind("<FocusIn>", lambda event: on_focus_in(input_nueva_cantidad, f"{info_producto_seleccionado[3]}"))
    input_nueva_cantidad.bind("<FocusOut>", lambda event: on_focus_out(input_nueva_cantidad, f"{info_producto_seleccionado[3]}"))
    input_nueva_cantidad.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(ventana_editar_producto, text="Nuevo precio:").grid(row=4, column=0, padx=10, pady=5)
    input_nuevo_precio = tk.Entry(ventana_editar_producto, fg='grey')
    input_nuevo_precio.insert(0, f"{info_producto_seleccionado[4]}")
    input_nuevo_precio.bind("<FocusIn>", lambda event: on_focus_in(input_nuevo_precio, f"{info_producto_seleccionado[4]}"))
    input_nuevo_precio.bind("<FocusOut>", lambda event: on_focus_out(input_nuevo_precio, f"{info_producto_seleccionado[4]}"))
    input_nuevo_precio.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
    
    btn_actualizar = ttk.Button(ventana_editar_producto, text="Actualizar", command=lambda: editar_producto_db(info_producto_seleccionado[0], input_nuevo_nombre.get(), input_nueva_descripcion.get(), input_nueva_cantidad.get(), input_nuevo_precio.get(), tabla, ventana_editar_producto))
    btn_actualizar.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')