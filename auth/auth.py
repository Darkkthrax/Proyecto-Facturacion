import tkinter as tk
from tkinter import messagebox, ttk
from utils.utils import finalizar_programa
from utils.entradas import borrar_entradas
from gui.gui_main import *
from models.models import set_usuario

#! FUNCIONES PARA INICIAR SESIÓN
def iniciar_sesion(root):
    root.withdraw()
    ventana_inicio = tk.Toplevel(root)
    ventana_inicio.title("Iniciar Sesión")
    ventana_inicio.resizable(False, False)
    ventana_inicio.protocol("WM_DELETE_WINDOW", lambda: finalizar_programa(root))
    
    ttk.Label(ventana_inicio, text="Inicio de sesión", font=("Arial", 16, "bold")).grid(row=0, column=1, padx=5, pady=20, sticky="nsew")
    
    ttk.Label(ventana_inicio, text='Identificador de usuario:').grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    input_usuario = tk.Entry(ventana_inicio, width=30)
    input_usuario.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    ttk.Label(ventana_inicio, text='Contraseña:').grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    input_contrasena = ttk.Entry(ventana_inicio, width=30, show="*")
    input_contrasena.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    
    btn_iniciar_sesion = ttk.Button(ventana_inicio, text="Iniciar sesión", command=lambda: verificar_inicio_sesion(root, input_usuario.get(), input_contrasena.get(), [input_usuario, input_contrasena], ventana_inicio))
    btn_iniciar_sesion.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    
    btn_cerrar = ttk.Button(ventana_inicio, text="Cerrar", command=lambda: finalizar_programa(root))
    btn_cerrar.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

def verificar_inicio_sesion(root, id, contrasena, entradas, ventana):
    from DBmanager.DBusuarios import verificar_usuario_db
    usuario_db = verificar_usuario_db(id)
    #TODO: Configurar inicio de sesión con nueva base de datos y contraseñas
    if not usuario_db:
        return mostrar_error(entradas, 1)
    
    if not (usuario_db[6] == 0 or usuario_db[6] == 1):
        return mostrar_error(entradas, 2)
    
    if not contrasena in usuario_db:
        return mostrar_error(entradas, 3)
    else:
        messagebox.showinfo("Inicio de sesión", "Acceso concedido")
        set_usuario(usuario_db, True)
        root.deiconify()
        crear_interfaz_principal(root)
        ventana.destroy()

#! FUNCIÓN DE MENSAJES DE ERROR

def mostrar_error(entradas, codigo):
    borrar_entradas(entradas)
    match codigo:
        case 1:
            mensaje = "Usuario inexistente."
        case 2:
            mensaje = "Usuario sin acceso autorizado."
        case 3:
            mensaje = "Usuario o contraseña incorrectas."
        case _:
            mensaje = "Ocurrió un error inesperado."
    return messagebox.showerror("Inicio de sesión", mensaje)