# FUNCIONES PARA VENTANAS CON CONDICIONES EN CAMPOS COMBOBOX
def actualizar_contraseña_registro(seleccion, widgets_ocultar:list):
    for widget in widgets_ocultar:
        if seleccion != '2':
            widget.grid()
        else:
            widget.grid_remove()