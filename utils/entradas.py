import tkinter as tk

#! FUNCIONES PARA ENTRADAS
# Función para crear un placeholder
def on_focus_in(entry, placeholder, tabla = None):
    if tabla != None and tabla.selection():
        if entry.get() == tabla.item(tabla.selection()[0], 'values')[0]:
            entry.delete(0, tk.END)
            entry.config(fg='black')
            return
        
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg='black') # Color normal para texto

def on_focus_out(entry, placeholder, tabla = None):
    if tabla != None and tabla.selection():
        if entry.get() == '':
            entry.insert(0, tabla.item(tabla.selection()[0], 'values'))
            entry.config(fg='grey')
            return
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg='grey') # Color gris para el placeholder

# Funciones para habilitar botones si una entrada tiene información
def verificar_entrada(entry, placeholder, button):
    if entry.get() != "":
        button.config(state='normal')
        on_focus_out(entry, placeholder)
    else:
        button.config(state='disabled')
        on_focus_in(entry, placeholder)

# Función para borrar entradas
def borrar_entradas(entradas):
    for entrada in entradas:
        entrada.delete(0, tk.END)

# Función para restaurar placeholder
def restaurar_entradas(entradas, placeholder):
    borrar_entradas(entradas)
    for i in range(len(entradas)):
        entradas[i].insert(0, placeholder[i])
        entradas[i].config(fg='grey')