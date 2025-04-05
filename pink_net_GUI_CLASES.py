import tkinter as tk
from tkinter import *
import GUI_functions_module

""" Utilizar clases para gestionar el estado y la lógica de tu GUI es una práctica
 fundamental para construir aplicaciones más complejas y mantenibles:"""


class AssetManagerGUI:
    """Clase AssetManagerGUI: Toda la lógica y los widgets de tu GUI están ahora
    dentro de esta clase."""
    def __init__(self, master):
        """Este es el constructor de la clase. Recibe la ventana principal (master).
        Inicializa el estado de la GUI
        (carga los datos, inicializa variables para el activo seleccionado).
        Llama a self.create_widgets() para construir la interfaz."""
        self.master = master
        master.title("Gestión de Operaciones Apalancadas")

        # Inicializar el estado de la GUI
        self.data = GUI_functions_module.load_data('pink_net_data_3_GUI.json')
        self.data = GUI_functions_module.order_orders(self.data)
        self.selected_asset_data = None
        self.selected_symbol = None

        # Crear los widgets de la GUI
        self.create_widgets()

    def create_widgets(self):
        """Este método crea todos los widgets de tu GUI
        (paneles, etiquetas, menús, botones) y los organiza utilizando .pack()"""
        # Panel Superior
        self.top_panel = Frame(self.master, bd=1, relief=FLAT, bg='burlywood')
        self.top_panel.pack(side=TOP, fill=X)
        self.title_label = Label(self.top_panel, text='Gestión de Operaciones Apalancadas', fg='azure4', font=('Dosis', 30), bg='burlywood', width=30)
        self.title_label.pack(pady=10)

        # Panel Izquierdo
        self.left_panel = Frame(self.master, bd=1, relief=FLAT)
        self.left_panel.pack(side=LEFT, fill=Y)

        # Menu Primario
        self.primary_menu = Frame(self.left_panel, bd=1, relief=FLAT)
        self.primary_menu.pack(side=TOP, padx=10, pady=10)
        self.create_primary_menu_buttons()

        # Panel de Activos
        self.asset_menu = Frame(self.left_panel, bd=1, relief=FLAT)
        self.asset_menu.pack(side=BOTTOM, padx=10, pady=10)
        self.create_asset_buttons()

        # Panel Derecho (para mostrar información del activo, etc.)
        self.right_panel = Frame(self.master, bd=1, relief=FLAT)
        self.right_panel.pack(side=RIGHT, fill=Y, padx=10, pady=10)
        self.info_label = Label(self.right_panel, text="Seleccione un activo para ver su información.")
        self.info_label.pack(pady=10)

    def create_primary_menu_buttons(self):
        """Método para crear los botones del menús primario.
        command en los botones:
        Para los botones del menú primario, el command ahora llama directamente
        a métodos de la clase (por ej., self.add_new_symbol_ui)."""

        primary_buttons_config = [
            {"text": "ADD new symbol", "command": self.add_new_symbol_ui},
            {"text": "Show MARGINS", "command": self.show_margins},
            {"text": "Update MARGINS", "command": self.update_margins},
            {"text": "Mostrar POSICIONES ABIERTAS", "command": self.show_open_positions},
            {"text": "Calcular LEVERAGE", "command": self.calculate_leverage},
            {"text": "Calculate BURN PRICE", "command": self.calculate_burn_price},
            {"text": "EXIT", "command": self.master.quit}
        ]
        for config in primary_buttons_config:
            button = Button(self.primary_menu, text=config["text"].title(), font=('Dosis', 12, 'bold'), bd=1, fg='white', bg='azure4', width=24, relief=RAISED, pady=5, cursor='hand2', command=config["command"])
            button.pack(pady=2, fill=X)

    def create_asset_buttons(self):
        """Métodos para crear los botones de los activos.
        Para los botones de los activos, el command utiliza lambda para llamar
        al método self.select_asset_handler(symbol).
        Aquí, symbol se pasa como argumento al método de la clase."""

        list_symbols = GUI_functions_module.get_symbols_for_buttons(self.data)
        for symbol in list_symbols:
            button = Button(self.asset_menu,
                            text=symbol, font=('Dosis', 12, 'bold'),
                            bd=1, fg='white', bg='azure4', width=24,
                            relief=RAISED, pady=2, cursor='hand2',
                            command=lambda s=symbol: self.select_asset_handler(s))
            button.pack(pady=2, fill=X)

    def add_new_symbol_ui(self):
        # Implementa la lógica para mostrar la interfaz de agregar nuevo símbolo aquí
        pass

    def show_margins(self):
        pass

    def update_margins(self):
        pass

    def show_open_positions(self):
        pass

    def calculate_leverage(self):
        pass

    def calculate_burn_price(self):
        pass

    def select_asset_handler(self, symbol):
        """Maneja la selección de un activo.
        Este método se encarga de:
        Llamar a GUI_functions_module.select_asset(self.data, symbol)
        para obtener la información del activo.
        Actualizar el estado de la GUI (almacena la información del activo seleccionado
        en self.selected_asset_data y self.selected_symbol
        Llamar a self.update_asset_info_display() para mostrar la información del activo
        en la interfaz (en este ejemplo, en la self.info_label del right_panel)."""
        asset_info = GUI_functions_module.select_asset(self.data, symbol)
        if asset_info:
            self.selected_asset_data, self.selected_symbol = asset_info
            print(f"Activo seleccionado: {self.selected_symbol}")
            print(f"Datos del activo: {self.selected_asset_data}")
            self.update_asset_info_display()
        else:
            print(f"Error al seleccionar el activo '{symbol}'.")

    def update_asset_info_display(self):
        """Actualiza la información del activo seleccionado en la GUI.
        Este método actualiza el contenido de un widget (en este caso, un Label en el right_panel)
        con la información del activo seleccionado."""
        if self.selected_symbol and self.selected_asset_data:
            info_text = f"Símbolo: {self.selected_symbol}\n"
            for key, value in self.selected_asset_data.items():
                info_text += f"{key}: {value}\n"
            self.info_label.config(text=info_text)
        else:
            self.info_label.config(text="Seleccione un activo para ver su información.")


if __name__ == "__main__":
    app = tk.Tk()
    gui = AssetManagerGUI(app)
    app.geometry('1020x630+0+0')
    app.resizable(False, False)
    app.config(bg='burlywood')
    app.mainloop()