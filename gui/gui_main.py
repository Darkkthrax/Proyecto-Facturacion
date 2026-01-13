import tkinter as tk
from tkinter import ttk
from .facturacion import facturar_productos
from .facturas import administrar_facturas_realizadas
from .productos import crear_admin_productos

# Función para crear el menú principal
def crear_interfaz_principal(root):
    #* TÍTULO PRINCIPAL
    titulo_principal = ttk.Label(root, text="Bienvenido", font=("Arial", 16, "bold"))
    titulo_principal.grid(row=0, column=1, padx=5, pady=20, sticky="n")

    logo_image = tk.PhotoImage(file="src/img/img.png")
    logo_image = logo_image.subsample(10, 10)
    logo_label = ttk.Label(root, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=2, column=1, padx=5, pady=10, sticky="n")

    #* BOTONES
    #? Administrar productos
    boton_productos = ttk.Button(root, text="Administrar productos", command=lambda: crear_admin_productos(root))
    boton_productos.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

    #? Administrar facturas
    boton_facturas = ttk.Button(root, text="Administrar facturas", command=lambda: administrar_facturas_realizadas(root))
    boton_facturas.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    #? Facturar
    boton_facturar = ttk.Button(root, text="Facturar", command=lambda: facturar_productos(root))
    boton_facturar.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")