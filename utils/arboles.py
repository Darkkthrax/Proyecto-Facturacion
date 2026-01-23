import tkinter as tk
#! FUNCIONES PARA SELECCIONES DE ÁRBOLES
def on_tree_select(event, tabla, btn1, btn2= None, entry = None):
    producto_seleccionado = tabla.focus()
    
    if producto_seleccionado:
        if btn2 != None:
            btn2.config(state='normal')
        if entry != None:
            entry.delete(0, tk.END)
            entry.config(state='normal', fg='grey')
            entry.insert(0, tabla.item(producto_seleccionado, 'values'))
        btn1.config(state='normal')
    else:
        if btn2 != None:
            btn2.config(state='disabled')
        if entry != None:
            entry.config(state='disabled')
        btn1.config(state='disabled')

def on_mousewheel(event, treeview):
    treeview.yview_scroll(int(-1*(event.delta/120)), "units")