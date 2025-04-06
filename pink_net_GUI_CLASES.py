import tkinter as tk
from tkinter import *
import GUI_functions_module
from functools import partial

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

        # Configuración para la selección única de botones de activo
        self.selected_asset = tk.StringVar()  # Almacena el símbolo del activo actualmente seleccionado
        self.active_asset_button = None  # Para rastrear el botón activo
        self.default_button_bg = 'azure4'  # Color de fondo por defecto
        self.selected_button_bg = 'green'  # Color de fondo cuando está seleccionado

        self.selected_asset_data = None  # Inicialización de self.selected_asset_data

        # Crear los widgets de la GUI
        self.create_widgets()


        self.selected_asset = tk.StringVar()
        self.active_asset_button = None  # Para rastrear el botón activo
        self.default_button_bg = 'azure4'  # Color de fondo por defecto
        self.selected_button_bg = 'green'  # Color de fondo cuando está seleccionado



    def create_widgets(self):
        """Este método crea todos los widgets de tu GUI
        (paneles, etiquetas, menús, botones) y los organiza utilizando .pack()"""
        # Panel Superior (para etiqueta de titulo y Panel de activos)
        self.top_panel = Frame(self.master, bd=1, relief=FLAT, bg='burlywood')
        self.top_panel.pack(side=TOP, fill=X)
        self.title_label = Label(self.top_panel, text='Gestión de Operaciones Apalancadas', fg='azure4', font=('Dosis', 30), bg='burlywood', width=30)
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="ew")

        # Panel de Activos (para los botones de activos)
        self.asset_menu = Frame(self.top_panel, bd=1, relief=FLAT)
        self.asset_menu.grid(row=1, column=0, columnspan=5, padx=10, pady=10,
                             sticky="ew")  # Lo colocamos debajo del título
        self.create_asset_buttons()

        # Panel Izquierdo (para el menu primario)
        self.left_panel = Frame(self.master, bd=1, relief=FLAT)
        self.left_panel.pack(side=LEFT, fill=Y)

        # Menu Primario
        self.primary_menu = Frame(self.left_panel, bd=1, relief=FLAT)
        self.primary_menu.pack(side=TOP, padx=10, pady=10)
        self.create_primary_menu_buttons()

        # Panel Derecho (para mostrar información del activo y otras funciones)
        self.right_panel = Frame(self.master, bd=1, relief=FLAT)
        self.right_panel.pack(side=RIGHT, fill=X, padx=10, pady=10, expand=True)
        self.info_label = Label(self.right_panel,
                                text="Seleccione un activo para ver su información.",
                                font=('Arial', 12, 'bold'))
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

    # en un principio habia creado botones para los activos, pero luego implemente radio buttons
    """def create_asset_buttons(self):
        Métodos para crear los botones de los activos.
        Para los botones de los activos, el command utiliza lambda para llamar
        al método self.select_asset_handler(symbol).
        Aquí, symbol se pasa como argumento al método de la clase.

        list_symbols = GUI_functions_module.get_symbols_for_buttons(self.data)
        num_columns = 6  # Define el número máximo de botones por fila (ajusta según tu preferencia)
        row = 1
        column = 0

        for symbol in list_symbols:
            button = Button(self.top_panel,
                            text=symbol, font=('Dosis', 12, 'bold'),
                            bd=1, fg='white', bg='azure4', width=24,
                            relief=RAISED, pady=2, cursor='hand2',
                            command=lambda s=symbol: self.select_asset_handler(s))
            button.grid(row=row, column=column, padx=2, pady=2,
                        sticky="ew")  # sticky="ew" hace que el botón se expanda horizontalmente

            column += 1
            if column >= num_columns:
                column = 0
                row += 1
"""

    """def select_asset_handler(self, symbol):
        esta función se encarga de manejar la selección de un activo.
        self.selected_asset.set(symbol)  # se establece el valor de la variable de control self.selected_asset con el symbol del activo que el usuario acaba de seleccionar al hacer clic en su Radiobutton
        print(f"Activo seleccionado: {self.selected_asset.get()}")
        # Aquí podrías habilitar o mostrar el menú secundario"""


    """def create_asset_radiobutton(self):
        list_symbols = GUI_functions_module.get_symbols_for_buttons(self.data)
        row = 1
        column = 0
        num_columns = 5
        for symbol in list_symbols:
            rb = tk.Radiobutton(self.top_panel,
                                text=symbol,
                                variable=self.selected_asset,
                                value=symbol,
                                font=('Dosis', 16, 'bold'),
                                padx=10,
                                pady=5,
                                command=lambda s=symbol: self.select_asset_handler(s))
            rb.grid(row=row, column=column, padx=5, pady=5, sticky="w")
            column += 1
            if column >= num_columns:
                column = 0
                row += 1

        print(f"Valor inicial de self.selected_asset: '{self.selected_asset.get()}'")"""

    def create_asset_buttons(self):
        list_symbols = GUI_functions_module.get_symbols_for_buttons(self.data)
        row = 1
        column = 0
        num_columns = 5
        for symbol in list_symbols:
            button = Button(self.top_panel,
                            text=symbol,
                            font=('Dosis', 16, 'bold'),
                            padx=10,
                            pady=5,
                            bg=self.default_button_bg,
                            fg='white',
                            bd=1,
                            relief=RAISED,
                            cursor='hand2')
            #button.config(command=partial(self.select_asset, symbol, button))
            button.config(command=lambda s=symbol, btn=button: self.select_asset(s, btn))
            button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
            column += 1
            if column >= num_columns:
                column = 0
                row += 1

    def select_asset(self, symbol, button):
        """esta función se encarga de manejar la selección de un activo"""
        self.selected_asset.set(symbol)  # Se actualiza la variable de control con el símbolo del activo seleccionado.
        print(f"Activo seleccionado: {self.selected_asset.get()}")

        # Se maneja la apariencia visual de los botones (deseleccionando el anterior y seleccionando el actual).
        if self.active_asset_button and self.active_asset_button != button:
            self.active_asset_button.config(bg=self.default_button_bg)

        # Seleccionar el botón actual
        self.active_asset_button = button
        button.config(bg=self.selected_button_bg)

        # Buscar y asignar la información del activo seleccionado
        if symbol in self.data:
            self.selected_asset_data = self.data[symbol]
        else:
            self.selected_asset_data = None  # O podrías mostrar un mensaje de error

        # se llama a este metodo para mostrar informacion del activo
        self.update_asset_info_display()
        #self.show_asset_orders()  # metodo para mostrar las ordenes relacionas con el activo
        """crear la funcion show_asset_order """

    # (El resto de tus métodos: create_asset_info_section, create_asset_actions_section,
    # update_asset_info_display, show_asset_orders, y los métodos de acción del activo
    # permanecen similares, pero ahora se basan en self.selected_asset.get())

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

    """def select_asset_handler(self, symbol):
        Maneja la selección de un activo.
        Este método se encarga de:
        Llamar a GUI_functions_module.select_asset(self.data, symbol)
        para obtener la información del activo.
        Actualizar el estado de la GUI (almacena la información del activo seleccionado
        en self.selected_asset_data y self.selected_symbol
        Llamar a self.update_asset_info_display() para mostrar la información del activo
        en la interfaz (en este ejemplo, en la self.info_label del right_panel).
        asset_info = GUI_functions_module.select_asset(self.data, symbol)
        if asset_info:
            self.selected_asset_data, self.selected_symbol = asset_info
            print(f"Activo seleccionado: {self.selected_symbol}")
            print(f"Datos del activo: {self.selected_asset_data}")
            self.update_asset_info_display()
        else:
            print(f"Error al seleccionar el activo '{symbol}'.")"""

    def update_asset_info_display(self):
        """Actualiza la información del activo seleccionado en la GUI.
        Este método actualiza el contenido de un widget
        (en este caso, un Label en el right_panel)
        con la información del activo seleccionado."""
        if self.selected_asset and self.selected_asset_data:
            # obtener precio actual del activo
            symbol = self.selected_asset.get()  # Obtiene el valor del StringVar como string
            current_price = GUI_functions_module.get_price(symbol)
            info_text = f"Símbolo: {symbol}\n"

            if current_price is None:
                tk.messagebox.showerror("Error al obtener precio",
                                        f"No se pudo obtener el precio actual para el activo: {symbol}")
                print("No se pudo obtener el precio actual.")
                self.info_label.config(text="Error al obtener el precio.")  # Informar del error en la GUI
                return  # Salir de la función para no mostrar información incompleta
            else:
                info_text += f"Precio actual: {current_price}\n"

            if 'margin' in self.selected_asset_data:
                margin = self.selected_asset_data['margin']
                info_text += f"Margin: {margin}\n"
            else:
                info_text += "Margin: No disponible\n"

            self.info_label.config(text=info_text)

        else:
            self.info_label.config(text="Seleccione un activo para ver su información.")


if __name__ == "__main__":
    # Iniciar Tkinter creando la ventana principal
    app = tk.Tk()

    # Crear una instancia de la clase de GUI,pasándole la ventana principal (app) como el 'master'
    gui = AssetManagerGUI(app)

    # Configurar la ventana principal (tamaño, resizable, etc.)
    app.state('zoomed')  # Maximizar la ventana
    app.resizable(False, False)
    app.config(bg='burlywood')

    # Iniciar el bucle principal de Tkinter,que mantiene la ventana abierta y responde a los eventos
    app.mainloop()

