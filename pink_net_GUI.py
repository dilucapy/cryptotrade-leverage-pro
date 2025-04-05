from tkinter import messagebox
import tkinter as tk
from tkinter import *
import GUI_functions_module


# Archivo JSON (se encuentra en el directorio: C:\DFX -C\PYTHON - UDEMY\PROYECTOS PROPIOS\PINK NET)
filename = 'pink_net_data_3_GUI.json'

data = GUI_functions_module.load_data(filename)
data = GUI_functions_module.order_orders(data)


def add_new_symbol(asset_symbols, data, filename):
    """Crea elementos para agregar un nuevo símbolo en la GUI.
    (Crear los elementos de la interfaz necesarios para que el usuario
    introduzca el nuevo símbolo (etiqueta y campo de entrada)"""

    Label(asset_menu, text="Nuevo Símbolo:", font=('Dosis', 12)).pack(pady=2)
    entry_symbol = Entry(asset_menu, font=('Dosis', 12, 'bold'), bd=1, width=15)
    entry_symbol.pack(pady=2)

    def obtener_y_validar():
        """Función anidada para obtener y validar el nuevo símbolo."""
        new_symbol = entry_symbol.get().strip().upper()
        if not new_symbol:
            messagebox.showerror("Error", "Por favor introduce un símbolo.")

            return
        if new_symbol in data:
            messagebox.showerror("Error", f"El símbolo '{new_symbol}' ya existe.")
            return

        # Lógica para agregar el símbolo a 'data'
        data[new_symbol] = {
            "current_price": 0,
            "margin": 0,
            "open_orders": [],
            "buy_limits": [],
            "sell_limits": []
        }

        # Guardamos el nuevo símbolo inicializado en el archivo JSON
        GUI_functions_module.save_data_asset(data, data[new_symbol], new_symbol, filename)
        messagebox.showinfo("Éxito", f"Símbolo '{new_symbol}' agregado!")
        entry_symbol.delete(0, tk.END)  # Limpiar el Entry

        # Agregamos el botón del nuevo símbolo en el contenedor asset_symbols
        new_symbol_button = Button(asset_menu,
                                   text=f"{new_symbol}",
                                   font=('Dosis', 12),
                                   bd=1,
                                   fg='white',
                                   bg='azure4',
                                   width=24,
                                   relief=RAISED,
                                   pady=1,
                                   cursor='hand2',
                                   command=lambda: GUI_functions_module.select_asset(data, new_symbol))

        new_symbol_button.pack(side=BOTTOM, pady=10)

    agregar_button = Button(asset_menu, text="Agregar", font=('Dosis', 12), command=obtener_y_validar)
    agregar_button.pack(pady=2)


# Iniciar Tkinter
app = Tk()

"""# Tamaño de la ventana
app.geometry('1020x630+0+0')"""

# Maximizar la ventana
app.state('zoomed')

# Evitar maximizar la ventana
app.resizable(False, False)

# Color de fondo de la ventana
app.config(bg='burlywood')

# Panel Superior
top_panel = Frame(app, bd=1, relief=FLAT)
top_panel.pack(side=TOP)

# Etiqueta titulo
title_label = Label(top_panel,
                    text='Gestión de Operaciones Apalancadas',
                    fg='azure4',
                    font=('Dosis', 30),
                    bg='burlywood',
                    width=30)

title_label.pack()

# Panel Izquierdo
left_panel = Frame(app, bd=1, relief=FLAT)
left_panel.pack(side=LEFT)

# Menu Primario (en panel izquierdo)
primary_menu = Frame(left_panel, bd=1, relief=FLAT)
primary_menu.pack(side=BOTTOM)

# Panel Central
center_panel = Frame(app, bd=1, relief=FLAT)
center_panel.pack(side=LEFT)

# Panel de activos (en panel central)
asset_menu = Frame(center_panel, bd=1, relief=FLAT)
asset_menu.pack(side=LEFT)

# Panel Derecho
right_panel = Frame(app, bd=1, relief=FLAT)
right_panel.pack(side=RIGHT)

# Menu secundario
secondary_menu = Frame(right_panel, bd=1, relief=FLAT)
secondary_menu.pack(side=TOP)

# Botones Menu Primario
primary_buttons_config = [
    {"text": "ADD new symbol", "command": lambda: add_new_symbol(right_panel, data, filename)},
    {"text": "Show MARGINS", "command": None},
    {"text": "Update MARGINS", "command": None},
    {"text": "Mostrar POSICIONES ABIERTAS", "command": None},
    {"text": "Calcular LEVERAGE", "command": None},
    {"text": "Calculate BURN PRICE", "command": None},
    {"text": "EXIT", "command": app.quit}
]

# bucle para creacion de botones del menu primario
for config in primary_buttons_config:
    button = Button(primary_menu,
                    text=config["text"].title(),
                    font=('Dosis', 12, 'bold'),
                    bd=1,
                    fg='white',
                    bg='azure4',
                    width=24,
                    relief=RAISED,
                    pady=5,
                    cursor='hand2',
                    command=config["command"])  # Asignar el comando desde la configuración

    button.pack(pady=2) # Usar pack para una disposición vertical simple


# Creacion de Botones para los activos presentes en data
list_symbols = GUI_functions_module.get_symbols_for_buttons(data)
for symbol in list_symbols:
    button = Button(asset_menu,
                    text=symbol,
                    font=('Dosis', 12, 'bold'),
                    bd=1,
                    fg='white',
                    bg='azure4',
                    width=24,
                    relief=RAISED,
                    pady=2,
                    cursor='hand2',
                    command=lambda s=symbol: GUI_functions_module.select_asset(data, s))

    button.pack(pady=2)  # Usar pack para una disposición vertical simple



# Evitar que la pantalla se cierre
app.mainloop()



