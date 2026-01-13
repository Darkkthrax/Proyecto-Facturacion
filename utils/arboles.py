#! FUNCIONES PARA SELECCIONES DE ÁRBOLES
def on_tree_select(event, tabla, btn1, btn2= None):
    producto_seleccionado = tabla.focus()
    
    if producto_seleccionado:
        if btn2 != None:
            btn2.config(state='normal')
        btn1.config(state='normal')
    else:
        if btn2 != None:
            btn2.config(state='disabled')
        btn1.config(state='disabled')

def on_mousewheel(event, treeview):
    treeview.yview_scroll(int(-1*(event.delta/120)), "units")