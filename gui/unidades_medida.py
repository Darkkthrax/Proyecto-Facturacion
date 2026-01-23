import tkinter as tk                    # Librería de interfaz gráfica
from tkinter import ttk, messagebox
from utils.entradas import *
from utils.arboles import on_tree_select, actualizar_tabla
from DBmanager.DBunidades_medida import traer_unidades_medida, crear_unidad_medida_db, traer_unidad_medida_nombre, editar_unidad_medida_db

def crear_admin_unidades_medida(ventana):
    ventana_unidades_medida = tk.Toplevel(ventana)
    ventana_unidades_medida.title("Unidades de Medida")
    
    titulo_admin_unidades = ttk.Label(ventana_unidades_medida, text="Unidades de Medida", font=("Arial", 16, "bold"))
    titulo_admin_unidades.grid(row=0, column=0, padx=5, pady=10, sticky='nsew')
    
    frame_opciones = ttk.Frame(ventana_unidades_medida)
    frame_opciones.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
    
    tabla_unidades = ttk.Treeview(ventana_unidades_medida, columns='#1')
    tabla_unidades.grid(row=1, column=0,  padx=10, pady=5, sticky='nsew')
    
    tabla_unidades.heading('#0', text='ID')
    tabla_unidades.column('#0', width=50)
    tabla_unidades.heading('#1', text='Unidades de medida')
    tabla_unidades.column('#1', minwidth=70)

    entrada_nueva_unidad = tk.Entry(frame_opciones)
    entrada_nueva_unidad.bind('<KeyRelease>', lambda event: verificar_entrada(entrada_nueva_unidad, 'Nueva unidad', btn_agregar_unidad))
    entrada_nueva_unidad.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_agregar_unidad = tk.Button(frame_opciones, text='Agregar Unidad', bg="lightgreen", state='disabled', command=lambda: agregar_unidad_medida(ventana_unidades_medida, entrada_nueva_unidad.get()))
    btn_agregar_unidad.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    
    entrada_editar_unidad = tk.Entry(frame_opciones, state='disabled')
    entrada_editar_unidad.bind('<KeyRelease>', lambda event: verificar_entrada(entrada_editar_unidad, 'Editar Unidad', btn_editar_unidad))
    entrada_editar_unidad.bind("<FocusIn>", lambda event: on_focus_in(entrada_editar_unidad, 'Editar Unidad', tabla=tabla_unidades))
    entrada_editar_unidad.bind("<FocusOut>", lambda event: on_focus_out(entrada_editar_unidad, 'Editar Unidad', tabla=tabla_unidades))
    entrada_editar_unidad.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_editar_unidad = tk.Button(frame_opciones, text="Editar Unidad", state='disabled', command=lambda: editar_unidad_medida(ventana_unidades_medida, tabla_unidades, entrada_editar_unidad.get(), entrada_editar_unidad))
    btn_editar_unidad.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_eliminar_unidad = tk.Button(frame_opciones, text='Eliminar Unidad', state='disabled')
    btn_eliminar_unidad.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_volver = tk.Button(frame_opciones, text='Cerrar')
    btn_volver.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
    
    unidades = traer_unidades_medida()
    for unidad in unidades:
        tabla_unidades.insert('', tk.END, text=str(unidades.index(unidad)), values=unidad)
    
    tabla_unidades.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tabla_unidades, btn_editar_unidad, btn_eliminar_unidad, entrada_editar_unidad))

def agregar_unidad_medida(ventana, nombre):
    if nombre.strip() == '':
        messagebox.showerror("Error", "Agregue un nombre a la unidad de medida", parent=ventana)
        return
    if traer_unidad_medida_nombre(nombre.strip().capitalize()) != None:
        messagebox.showerror("Error", "Ya existe esta unidad de medida", parent=ventana)
        return
    crear_unidad_medida_db(ventana, nombre.strip().capitalize())

def editar_unidad_medida(ventana, tabla, nuevo_nombre, entrada):
    unidad_seleccionada = tabla.item(tabla.selection()[0], 'values')[0]

    if nuevo_nombre.strip() == '':
        messagebox.showerror("Error", "El nuevo nombre no puede estar vacío", parent=ventana)
        return
    
    if traer_unidad_medida_nombre(nuevo_nombre.strip().capitalize()) != None:
        messagebox.showerror("Error", "Ya existe esta unidad de medida", parent=ventana)
        return
    
    if messagebox.askyesno("Editar Unidad", "¿Está seguro que quiere cambiar el nombre de esta unidad?\nTodo producto con esta unidad de medida será cambiado por la nueva unidad de medida",parent=ventana):
        editar_unidad_medida_db(ventana, unidad_seleccionada, nuevo_nombre)
        entrada.delete(0, tk.END)
        actualizar_tabla(tabla, traer_unidades_medida())
        return