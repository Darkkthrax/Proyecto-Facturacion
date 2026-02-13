import tkinter as tk                    # Librería de interfaz gráfica
from tkinter import messagebox, ttk     # Message Box de Tkinter
import platform
import os
import subprocess
from datetime import datetime
from fpdf import FPDF
from utils.entradas import on_focus_in, on_focus_out, restaurar_entradas
from utils.arboles import *
from utils.comboboxes import actualizar_contraseña_registro
from DBmanager.DBproductos import traer_inventario_producto_id_db, traer_inventario_producto_nombre_db, traer_producto_id_db, traer_producto_nombre_db
from DBmanager.DBfacturacion import traer_ultima_id_factura_db, crear_factura_db
from DBmanager.DBusuarios import verificar_usuario_db, registrar_usuario_db
from DBmanager.DBtipo_usuarios import traer_tipos
from .buscar_productos import buscar_producto
from models.models import get_usuario, set_productos_factura, get_productos_factura, get_cliente, set_cliente, info_empresa

#! FUNCIONES PARA BOTÓN FACTURAR
# Función para la ventana "facturar"
def facturar_productos(root):
    from utils.utils import regresar_menu, eliminar_producto
    headers = ['ID', 'ID', 'Nombre', 'Descripción', 'Marca', 'Cantidad', 'Precio', 'Subtotal']
    ventana_facturacion = tk.Toplevel(root)
    ventana_facturacion.title("Facturación")
    ventana_facturacion.state(newstate='zoomed')
    ttk.Label(ventana_facturacion, text="Facturación", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    tabla_productos_factura = ttk.Treeview(ventana_facturacion, columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7'))
    tabla_productos_factura.column('#0', width=0, stretch=False)
    tabla_productos_factura.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    
    scrollbar = ttk.Scrollbar(ventana_facturacion, orient=tk.VERTICAL, command=tabla_productos_factura.yview)
    tabla_productos_factura.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=tabla_productos_factura.yview)
    scrollbar.grid(row=1, column=0, padx=(0, 5), pady=5, sticky="nse")
    tabla_productos_factura.bind("<MouseWheel>", lambda e: on_mousewheel(e, tabla_productos_factura))
    
    for i in range(1, len(headers)):
        tabla_productos_factura.heading(f'#{i}', text=headers[i])
        tabla_productos_factura.column(f'#{i}', minwidth=50, width=155)
    
    frame_busqueda = ttk.Frame(ventana_facturacion)
    frame_busqueda.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
    
    btn_regresar = tk.Button(frame_busqueda, text="Volver", bg='skyblue', command=lambda: regresar_menu(root, ventana_facturacion))
    btn_regresar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(frame_busqueda, text="Consultar Producto", font=("Arial", 10, "bold"), anchor='center').grid(row=1, column=0, columnspan=2, padx=5)

    ttk.Label(frame_busqueda, text="Por código:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    buscador_codigo = tk.Entry(frame_busqueda, fg='grey')
    buscador_codigo.insert(0, "Agregar por código")
    buscador_codigo.bind("<FocusIn>", lambda event: on_focus_in(buscador_codigo, "Agregar por código"))
    buscador_codigo.bind("<FocusOut>", lambda event: on_focus_out(buscador_codigo, "Agregar por código"))
    buscador_codigo.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    
    btn_buscar_nombre = ttk.Button(frame_busqueda, text='Buscar Nombre', command= lambda: buscar_producto(root, frame_busqueda, tabla_productos_factura))
    btn_buscar_nombre.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
    
    # ttk.Label(frame_busqueda, text="Por nombre:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    # buscador_nombre = tk.Entry(frame_busqueda, fg='grey')
    # buscador_nombre.insert(0, "Agregar por nombre")
    # buscador_nombre.bind("<FocusIn>", lambda event: on_focus_in(buscador_nombre, "Agregar por nombre"))
    # buscador_nombre.bind("<FocusOut>", lambda event: on_focus_out(buscador_nombre, "Agregar por nombre"))
    # buscador_nombre.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(frame_busqueda, text="Cantidad", font=("Arial", 10, "bold"), anchor='center').grid(row=4, column=0, columnspan=2, padx=5, pady=10)
    cantidad_producto = tk.Entry(frame_busqueda)
    cantidad_producto.insert(0, "1")
    cantidad_producto.bind("<FocusIn>", lambda event: on_focus_in(cantidad_producto, "1"))
    cantidad_producto.bind("<FocusOut>", lambda event: on_focus_out(cantidad_producto, "1"))
    cantidad_producto.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    # btn_facturar_producto = ttk.Button(frame_busqueda, text="Agregar", command=lambda: agregar_producto_factura(str(buscador_codigo.get()), str(buscador_nombre.get()), int(cantidad_producto.get()), ventana_facturacion, frame_busqueda, tabla_productos_factura, [buscador_codigo, buscador_nombre, cantidad_producto], ["Agregar por código", "Agregar por nombre", "1"]))
    # btn_facturar_producto.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
    
    btn_editar_cantidad = ttk.Button(frame_busqueda, text="Editar", command=lambda: editar_cantidad_factura(root, tabla_productos_factura, frame_busqueda), state='disabled')
    btn_editar_cantidad.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    btn_eliminar_producto = ttk.Button(frame_busqueda, text="Eliminar", command=lambda: eliminar_producto(tabla_productos_factura, ventana_facturacion, frame_busqueda), state='disabled')
    btn_eliminar_producto.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(frame_busqueda, text="Datos del Cliente", font=("Arial", 10, "bold"), anchor='center').grid(row=9, column=0, columnspan=2, padx=5)
    
    btn_registrar_cliente = ttk.Button(frame_busqueda, text='Registrar Cliente', command=lambda: registrar_usuario(root))
    btn_registrar_cliente.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    buscador_cliente = tk.Entry(frame_busqueda)
    buscador_cliente.bind("<FocusIn>", lambda event: on_focus_in(buscador_cliente, "Documento de identidad"))
    buscador_cliente.bind("<FocusOut>", lambda event: on_focus_out(buscador_cliente, "Documento de identidad"))
    buscador_cliente.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=lambda: verificar_usuario(buscador_cliente.get(), ventana_facturacion, frame_busqueda))
    btn_buscar.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(frame_busqueda, text="Asocia un cliente para facturar", anchor='center').grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    ventana_facturacion.grid_rowconfigure(1, weight=1)
    ventana_facturacion.grid_columnconfigure(0, weight=3)
    ventana_facturacion.grid_columnconfigure(1, weight=1)
    
    frame_busqueda.grid_columnconfigure(1, weight=1)
    
    tabla_productos_factura.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tabla_productos_factura, btn_editar_cantidad, btn_eliminar_producto))

# Función para agregar un producto a la factura
def agregar_producto_factura(id, nombre, cantidad, ventana, frame, tabla, entradas, placeholders):
    productos_factura = get_productos_factura()
    from utils.utils import verificar_productos
    if id == 'Agregar por código' and nombre == 'Agregar por nombre':
        messagebox.showerror("Error", "Verifique que uno de los campos de consulta esté lleno", parent=ventana)
    elif id != 'Agregar por código' and nombre != 'Agregar por nombre':
        messagebox.showerror("Error", "Especifíque solamente 1 método de búsqueda", parent=ventana)
    elif verificar_productos(id, nombre):
        limite = traer_inventario_producto_id_db(id)[0] if id != 'Agregar por código' else traer_inventario_producto_nombre_db(nombre)[0]
        if cantidad <= limite:
            if cantidad <= 0:
                messagebox.showerror("Error", "No se pueden agregar valores negativos o 0 en la cantidad.", parent=ventana)
            else:
                if (any(int(id) in producto for producto in productos_factura) if id != 'Agregar por código' else any(nombre in producto for producto in productos_factura)):
                    for i in range(0, len(productos_factura)):
                        if (int(id) in productos_factura[i] if id != 'Agregar por código' else nombre in productos_factura[i]):
                            if( productos_factura[i][3] + cantidad) <= limite:
                                productos_factura[i][3] += cantidad
                                break
                            else:
                                messagebox.showwarning("Advertencia", f"Límite de producto alcanzado. Inventario: {limite}", parent=ventana)
                elif id != 'Agregar por código':
                    producto_db = list(traer_producto_id_db(id))
                    producto_db.insert(3, cantidad)
                    productos_factura.append(producto_db)
                else:
                    producto_db = list(traer_producto_nombre_db(nombre))
                    producto_db.insert(3, cantidad)
                    productos_factura.append(producto_db)
        else:
            messagebox.showerror("Error", f"Se excede las existencias del producto. Inventario: {limite}", parent=ventana)
    else:
        messagebox.showerror("Error", "No se encontró un producto con la id o el nombre especificado", parent=ventana)
    set_productos_factura(productos_factura)
    actualizar_datos_facturación(tabla)
    restaurar_entradas(entradas, placeholders)
    verificar_producto_usuario_factura(frame, ventana)

# Funcion para verificar si hay al menos 1 producto en la factura
def verificar_producto_usuario_factura(frame, ventana = None):
    productos_factura = get_productos_factura()
    cliente = get_cliente()
    if len(productos_factura) >= 1:
        if cliente != ():
            boton_facturar_productos = tk.Button(frame, text="Facturar", bg='lightgreen', command=lambda: crear_factura_pdf(ventana))
            boton_facturar_productos.grid(row=17, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        else:
            ttk.Label(frame, text="Asigna un usuario", anchor='center', font=("Arial", 10, "bold")).grid(row=16, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        total_a_pagar = 0
        for producto in productos_factura:
            total_a_pagar += float(producto[6])
        ttk.Label(frame, text=f"Total a Pagar: {total_a_pagar:,.2f}", anchor='center', font=("Arial", 10, "bold")).grid(row=16, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    else:
        ttk.Label(frame, text="Agrega mínimo 1 producto", anchor='center', font=("Arial", 10, "bold")).grid(row=16, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Función para crear PDF con paginación
def crear_factura_pdf(ventana):
    cliente = get_cliente()
    fecha_emision = datetime.now().strftime("%Y/%m/%d - %H:%M:%S")
    productos_factura = get_productos_factura()
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_margins(left=10, top=10, right=10)
    
    try:
        pdf.image('src/img/img.png', x=170, y=8, w=30)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
    
    # Encabezado fijo (siempre en primera página)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'FACTURA', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f'{info_empresa[1]}', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f'{info_empresa[2]}', 0, 1)
    pdf.cell(0, 6, f'Tel: {info_empresa[3]} | Email: {info_empresa[4]}', 0, 1)
    pdf.cell(0, 6, f'NIT: {info_empresa[0]}', 0, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'DATOS DEL CLIENTE', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f'Identificación: {cliente[0]}', 0, 1)
    pdf.cell(0, 6, f'Nombre: {cliente[1]} {cliente[2]}', 0, 1)
    pdf.cell(0, 6, f'Telefono: {cliente[4]}', 0, 1)
    pdf.cell(0, 6, f'Correo: {cliente[5]}', 0, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'INFORMACIÓN DE LA FACTURA', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    ultima_id_factura = traer_ultima_id_factura_db()
    numero_factura = int(traer_ultima_id_factura_db()[0]) + 1 if ultima_id_factura else 1
    pdf.cell(0, 6, f'Número de factura: {numero_factura}', 0, 1)
    pdf.cell(0, 6, f'Fecha de emisión: {fecha_emision}', 0, 1)
    pdf.ln(15)
    
    # Verificar espacio disponible antes de crear la tabla
    espacio_disponible = 270 - pdf.get_y()  # Altura aproximada de la página
    altura_por_fila = 8  # Altura estimada por fila de producto
    
    # Calcular si necesitamos nueva página
    if len(productos_factura) * altura_por_fila > espacio_disponible:
        pdf.add_page()
    
    # Crear tabla con control de paginación
    crear_tabla_pdf(pdf, productos_factura, numero_factura, fecha_emision, ventana)
    
    ruta_completa = os.path.join("src/Facturas", f"{numero_factura}.pdf")
    pdf.output(ruta_completa)
    abrir_pdf(ruta_completa)

# Tabla para el pdf con los productos
def crear_tabla_pdf(pdf, productos, numero_factura, fecha_emision, ventana):
    # Configurar encabezados de tabla
    pdf.set_font('Arial', 'B', 10)
    encabezados = ['Código', 'Producto', 'Cantidad', 'Precio Unit.', 'IVA', 'Total']
    anchos = [20, 60, 30, 25, 25, 30]
    
    # Dibujar encabezados
    for i, encabezado in enumerate(encabezados):
        pdf.cell(anchos[i], 8, encabezado, 1, 0, 'C')
    pdf.ln()
    
    # Dibujar filas de productos
    pdf.set_font('Arial', '', 9)
    total_factura = 0
    total_iva = 0
    contador = 0
    
    for producto in productos:
        contador+=1
        
        # Cambio de fondo para mejorar la vista de productos
        if contador % 2 != 0:
            pdf.set_fill_color(165, 165, 165)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        # Verificar si necesita nueva página
        if pdf.get_y() > 250:  # Si esta cerca del final
            pdf.add_page()
            # Redibujar encabezados en nueva página
            pdf.set_font('Arial', 'B', 10)
            for i, encabezado in enumerate(encabezados):
                pdf.cell(anchos[i], 8, encabezado, 1, 0, 'C')
            pdf.ln()
            pdf.set_font('Arial', '', 9)
        
        iva_monto = producto[5] * 0.19
        total_item = producto[5]
        
        total_factura += total_item
        total_iva += iva_monto

        pdf.cell(anchos[0], 8, str(producto[0]), 1, 0, 'L')
        pdf.cell(anchos[1], 8, str(producto[1]), 1, 0, 'L')
        pdf.cell(anchos[2], 8, str(producto[3]), 1, 0, 'C')
        pdf.cell(anchos[3], 8, f"${producto[4]:,.2f}", 1, 0, 'R')
        pdf.cell(anchos[4], 8, f"${iva_monto:,.2f}", 1, 0, 'R')
        pdf.cell(anchos[5], 8, f"${total_item:,.2f}", 1, 0, 'R')
        pdf.ln()
    
    # Agregar total general
    if pdf.get_y() > 270 - 20:  # Si no hay espacio para el total
        pdf.add_page()
    
    # Subtotal
    pdf.set_font('Arial', '', 10)
    pdf.set_fill_color(220, 220, 220)  # Gris claro para los totales
    
    pdf.cell(160, 8, 'SUBTOTAL:', 1, 0, 'R', True)
    pdf.cell(30, 8, f"${total_factura - total_iva:,.2f}", 1, 1, 'R', True)
    
    # IVA
    pdf.cell(160, 8, 'TOTAL IVA:', 1, 0, 'R', True)
    pdf.cell(30, 8, f"${total_iva:,.2f}", 1, 1, 'R', True)
    
    # Total final
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(180, 180, 180)  # Gris más oscuro
    pdf.cell(160, 10, 'TOTAL FACTURA:', 1, 0, 'R', True)
    pdf.cell(30, 10, f"${total_factura:,.2f}", 1, 1, 'R', True)
    
    crear_factura_db(numero_factura, fecha_emision, (total_factura - total_iva), total_iva, total_factura, ventana)

# Función para abrir automáticamente el pdf
def abrir_pdf(ruta):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(ruta)
        elif sistema == "Darwin":  # macOS
            subprocess.run(["open", ruta])
        else:  # Linux y otros
            subprocess.run(["xdg-open", ruta])
        
        print(f"✓ PDF abierto: {ruta}")
    except Exception as e:
        print(f"✗ No se pudo abrir el PDF: {e}")

# Función para actualizar la tabla de facturación
def actualizar_datos_facturación(tabla, frame, call = False):
    productos_factura = get_productos_factura()
    
    if not call:
        for i in range(len(productos_factura)):
            productos_factura[i].insert(5, productos_factura[i][3] * productos_factura[i][4])
        set_productos_factura(productos_factura)

    for item in tabla.get_children():
        tabla.delete(item)
    for fila in productos_factura:
        tabla.insert('', tk.END, text=str(productos_factura.index(fila)), values=fila)
    
    verificar_producto_usuario_factura(frame)

# Función para editar cantidad del producto de facturación
def editar_cantidad_factura(root, tabla, frame):
    producto_seleccionado = tabla.selection()[0]
    info_producto_seleccionado = tabla.item(producto_seleccionado, 'values')
    
    ventana_editar = tk.Toplevel(root)
    ventana_editar.title("Editar cantidad")
    ventana_editar.geometry("400x300")
    titulo_editar=ttk.Label(ventana_editar, text=f"Editar cantidad de {info_producto_seleccionado[1]}", font=("Arial", 16, "bold"))
    titulo_editar.grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    label_nueva_cantidad_producto = ttk.Label(ventana_editar, text="Nueva cantidad: ", font=("Arial", 10, "bold"))
    label_nueva_cantidad_producto.grid(row=1, column=0, padx=10, pady=5)
    input_nueva_cantidad_producto = tk.Entry(ventana_editar, width=30)
    input_nueva_cantidad_producto.grid(row=2, column=0, padx=10, pady=5)
    
    btn_actualizar = ttk.Button(ventana_editar, text="Actualizar", command=lambda: editar_lista_facturacion(info_producto_seleccionado[0], int(input_nueva_cantidad_producto.get()), ventana_editar, tabla, frame))
    btn_actualizar.grid(row=3, column=0, padx=10, pady=5)

# Funcion para actualizar lista de facturación
def editar_lista_facturacion(id, nueva_cantidad, ventana, tabla, frame):
    limite = traer_inventario_producto_id_db(id)[0]
    productos_factura = get_productos_factura()
    if nueva_cantidad >= 1:
        if nueva_cantidad <= limite:
            for producto in productos_factura:
                if int(id) == producto[0]:
                    producto[3] = nueva_cantidad
                    producto[5] = producto[3] * producto[4]
            messagebox.showinfo("Facturación", "Se actualizó la cantidad correctamente", parent=ventana)
            ventana.destroy()
            verificar_producto_usuario_factura(frame, ventana)
        else:
            messagebox.showerror("Error", f"Se excede las existencias del producto. Inventario: {limite}", parent=ventana)
    else:
        messagebox.showerror("Error", "La nueva cantidad no puede ser negativa o 0. Si desea eliminar el producto, selecciona el botón 'Eliminar'", parent=ventana)
    actualizar_datos_facturación(tabla)

# Función para verificar usuario
def verificar_usuario(id, ventana, frame):
    
    usuario = verificar_usuario_db(id)
    if usuario:
        set_cliente(usuario)
        
        messagebox.showinfo("Búsqueda", f"{usuario[1]} {usuario[2]} será asociad@ a la factura", parent=ventana)
        
        ttk.Label(frame, text=f"{usuario[1]} {usuario[2]}", anchor='center', font=("Arial", 10, "bold")).grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Label(frame, text=f"{usuario[0]}", anchor='center', font=("Arial", 10, "bold")).grid(row=14, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
        verificar_producto_usuario_factura(frame, ventana)
    else:
        messagebox.showerror("Búsqueda", "El cliente no se encuentra registrado", parent=ventana)

# Funcion para registrar usuarios
def registrar_usuario(root, tipo_usuario = None):
    info_usuario = get_usuario()
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title('Registro de Usuarios' if tipo_usuario != 'admin1' else "Registro Administrador")
    ventana_registro.geometry("400x300")
    titulo_registro=ttk.Label(ventana_registro, text="Registrar nuevo Usuario" if tipo_usuario != 'admin1' else "Registrar Administrador")
    titulo_registro.grid(row=0, column=0, padx=5, pady=20, sticky="nw")
    
    label_id_usuario = ttk.Label(ventana_registro, text="ID del Usuario:")
    label_id_usuario.grid(row=1, column=0, padx=10, pady=5)
    input_id_usuario = tk.Entry(ventana_registro, width=30)
    input_id_usuario.grid(row=1, column=1, padx=10, pady=5)

    label_nombre_usuario = ttk.Label(ventana_registro, text="Nombre del Usuario:")
    label_nombre_usuario.grid(row=2, column=0, padx=10, pady=5)
    input_nombre_usuario = tk.Entry(ventana_registro, width=30)
    input_nombre_usuario.grid(row=2, column=1, padx=10, pady=5)
    
    label_apellidos = ttk.Label(ventana_registro, text="Apellidos:")
    label_apellidos.grid(row=3, column=0, padx=10, pady=5)
    input_apellidos = tk.Entry(ventana_registro, width=30)
    input_apellidos.grid(row=3, column=1, padx=10, pady=5)
    
    label_telefono = ttk.Label(ventana_registro, text="Teléfono:")
    label_telefono.grid(row=4, column=0, padx=10, pady=5)
    input_telefono = tk.Entry(ventana_registro, width=30)
    input_telefono.grid(row=4, column=1, padx=10, pady=5)
    
    label_correo = ttk.Label(ventana_registro, text="Correo:")
    label_correo.grid(row=5, column=0, padx=10, pady=5)
    input_correo = tk.Entry(ventana_registro, width=30)
    input_correo.grid(row=5, column=1, padx=10, pady=5)    
    
    input_contrasena = tk.Entry(ventana_registro, width=30)
    
    opciones = traer_tipos()
    opcion_seleccionada = tk.StringVar()
    combo_tipo_usuario = ttk.Combobox(ventana_registro, textvariable=opcion_seleccionada, values=opciones, state='readonly')
    combo_tipo_usuario.current(2)
    
    if tipo_usuario == 'admin1' or info_usuario[6] == 0:
        
        label_contrasena = ttk.Label(ventana_registro, text="Contraseña:")
        label_contrasena.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        input_contrasena.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(ventana_registro, text="Tipo de usuario").grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        combo_tipo_usuario.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")
        actualizar_contraseña_registro(opcion_seleccionada.get()[0], [label_contrasena, input_contrasena])
        combo_tipo_usuario.bind("<<ComboboxSelected>>", lambda event: actualizar_contraseña_registro(opcion_seleccionada.get()[0], [label_contrasena, input_contrasena]))
        
        if tipo_usuario == 'admin1':
            from utils.utils import finalizar_programa
            root.withdraw()
            ttk.Label(ventana_registro, text='Primer usuario administrador').grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
            combo_tipo_usuario.current(0)
            combo_tipo_usuario.config(state='disabled')
            
            ventana_registro.protocol("WM_DELETE_WINDOW", lambda: finalizar_programa(root))
    
    btn_registrar = ttk.Button(ventana_registro, text="Registrar", command=lambda: registrar_usuario_db(root, input_id_usuario.get(), input_nombre_usuario.get(), input_apellidos.get(), input_telefono.get(), input_correo.get(), input_contrasena.get(), opcion_seleccionada.get()[0], ventana_registro))
    btn_registrar.grid(row=8, column=1, padx=5, pady=5, sticky="nsew")

# Función para verificar las entradas del registro
def verificar_entradas_registro(id, nombre, apellidos, telefono, correo, contrasena, tipo_usuario):
    return id.strip() == '' or nombre.strip() == '' or apellidos.strip() == '' or telefono.strip() == '' or correo == '' or contrasena == '' if tipo_usuario == 'admin' or tipo_usuario == 'empleado' else id.strip() == '' or nombre.strip() == '' or apellidos.strip() == '' or telefono.strip() == '' or correo == ''