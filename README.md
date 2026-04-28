# Billing System — Supermarket

Desktop application for billing and product management for supermarkets.
Developed using Python with Tkinter for GUI. **University project, currently in active development.**

---

## Description

Comprehensive system to manage inventory, create users and handle billing for a supermarket business. It has modules to create PDF invoices, real-time product search and different types of user management using access control.

---

## Features

- Login with password encryption (bcrypt)
- User management: customers, employees and administrators
- Product inventory review and management
- Real-time product search *(WIP)*
- Invoice creation and viewing in PDF format (FPDF2)
- Invoice history
- Local database using SQLite3

---

## Technologies

| Technology | Use |
|---|---|
| Python 3.12 | Main language |
| Tkinter | Graphical User Interface (GUI) |
| SQLite3 | Local database |
| FPDF2 | PDF invoice generation |
| bcrypt | Password encryption |
| python-dotenv | Environment variable management |

---

## How to Install

### Requirements

- Python 3.12+
- Operating System (OS): Windows

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Darkkthrax/Proyecto-Facturacion.git
cd Proyecto-Facturacion

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up the environment variables
cp .env_ejemplo .env
# Edit the .env file with your values

# 4. Run the application
python main.py
```

---

## Project Structure

```text
Proyecto-Facturacion/
├── main.py           # Entry point
├── auth/             # Authentication logic
├── DBmanager/        # Database management
├── gui/              # Graphical interfaces (Tkinter)
├── models/           # Data models
├── src/              # Business logic (resources, images, PDF)
├── utils/            # General utilities
├── requirements.txt  # Dependencies
└── .env_ejemplo      # Environment variables template
```

---

## Project Status

Currently, this project is in **active development**. Features marked as WIP may be incomplete or subject to change.

---

## Author

**Jerónimo Orozco Urrego**
Software Analyst and Developer | Systems Engineering
[LinkedIn](https://www.linkedin.com/in/jeronimo-orozco-u/) · [GitHub](https://github.com/Darkkthrax)
