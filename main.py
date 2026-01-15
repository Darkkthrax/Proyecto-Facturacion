import tkinter as tk
from DBmanager.database import verificar_db
from utils.utils import finalizar_programa

if __name__ == '__main__':
    #* Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Facturación de supermercado")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", finalizar_programa(root))

    verificar_db(root) # Verificación de base de datos

    #* Ejecución de la interfaz gráfica
    root.mainloop()