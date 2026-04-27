# Sistema de Facturación — Supermercado

Aplicación de escritorio para la facturación y administración de productos de un supermercado.  
Desarrollada en Python con interfaz gráfica en Tkinter. **Proyecto universitario en desarrollo activo.**

---

## Descripción

Sistema integral que permite gestionar el inventario, la creación de usuarios y la facturación de un negocio de tipo supermercado. Cuenta con módulos para la creación de facturas en PDF, búsqueda de productos en tiempo real y administración de diferentes tipos de usuarios con control de acceso.

---

## Funcionalidades

- Inicio de sesión con encriptación de contraseñas (bcrypt)
- Gestión de usuarios: clientes, empleados y administradores
- Revisión y administración de inventario de productos
- Búsqueda de productos en tiempo real *(en desarrollo)*
- Creación y visualización de facturas en formato PDF (FPDF2)
- Historial de facturas generadas
- Base de datos local con SQLite3

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| Tkinter | Interfaz gráfica de usuario (GUI) |
| SQLite3 | Base de datos local |
| FPDF2 | Generación de facturas en PDF |
| bcrypt | Encriptación de contraseñas |
| python-dotenv | Gestión de variables de entorno |

---

## Instalación

### Requisitos

- Python 3.12+
- Sistema operativo: Windows

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/Darkkthrax/Proyecto-Facturacion.git
cd Proyecto-Facturacion

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Configura las variables de entorno
cp .env_ejemplo .env
# Edita el archivo .env con tus valores

# 4. Ejecuta la aplicación
python main.py
```

---

## Estructura del Proyecto

Proyecto-Facturacion/
├── main.py           # Punto de entrada
├── auth/             # Lógica de autenticación
├── DBmanager/        # Gestión de base de datos
├── gui/              # Interfaces gráficas (Tkinter)
├── models/           # Modelos de datos
├── src/              # Lógica de negocio
├── utils/            # Utilidades generales
├── requirements.txt  # Dependencias
└── .env_ejemplo      # Plantilla de variables de entorno

---

## Estado del Proyecto

Este proyecto se encuentra **en desarrollo activo**. Las funcionalidades marcadas pueden estar incompletas o sujetas a cambios.

---

## Autor

**Jerónimo Orozco Urrego**  
Analista y Desarrollador de Software | Ingeniería en Sistemas  
[LinkedIn](https://www.linkedin.com/in/jeronimo-orozco-u/) · [GitHub](https://github.com/Darkkthrax)