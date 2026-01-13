#! Parámetros globales
# Parámetros de sesión
sesion_iniciada = False
info_usuario = ()

# Lista Global de facturación
productos_factura = []
cliente = ()
info_empresa = ['987652342-1', 'Supermercado Lola', 'Cll 34A # 21 - 23 | Medellín', '5896545', 'soporte@lola.com']
impuesto = 0.19

def set_usuario(datos, sesion):
    global info_usuario
    global sesion_iniciada
    info_usuario = datos
    sesion_iniciada = sesion
    sesion_iniciada = True
    print(f"Usuario establecido: {info_usuario}")

def get_usuario():
    print(f"Usuario obtenido: {info_usuario}")
    return info_usuario

def get_sesion():
    print(f"Sesion: {sesion_iniciada}")
    return sesion_iniciada

def set_cliente(datos):
    global cliente
    cliente = datos
    print(f"cliente establecido: {cliente}")

def get_cliente():
    print(f"cliente obtenido: {cliente}")
    return cliente

def set_productos_factura(datos):
    global productos_factura
    productos_factura = datos
    print(f"productos_factura establecido: {productos_factura}")

def get_productos_factura():
    print(f"productos_factura obtenido: {productos_factura}")
    return productos_factura