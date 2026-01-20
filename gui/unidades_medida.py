import tkinter as tk                    # Librería de interfaz gráfica
from tkinter import ttk, messagebox
from DBmanager.DBunidades_medida import traer_unidades_medida, crear_unidad_medida_db, traer_unidad_medida_nombre

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
    
    btn_agregar_unidad = tk.Button(frame_opciones, text='Agregar Unidad', bg="lightgreen")
    btn_agregar_unidad.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_editar_unidad = tk.Button(frame_opciones, text="Editar Unidad", state='disabled')
    btn_editar_unidad.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_eliminar_unidad = tk.Button(frame_opciones, text='Eliminar Unidad', state='disabled')
    btn_eliminar_unidad.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
    
    btn_volver = tk.Button(frame_opciones, text='Cerrar')
    btn_volver.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
    
    unidades = traer_unidades_medida()
    for unidad in unidades:
        tabla_unidades.insert('', tk.END, text=str(unidades.index(unidad)), values=unidad)