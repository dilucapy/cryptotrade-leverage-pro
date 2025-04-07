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
        self.right_panel = Frame(self.master, bd=1, relief=FLAT, padx=10, pady=10)
        self.right_panel.pack(side=RIGHT, fill=X, padx=10, pady=10, expand=True)

        self.create_asset_info_section()  # crea seccion de iformación del activo (símbolo, precio, margi)
        self.create_asset_orders_section()  # crea seccion de ordenes del activo
        #self.create_secondary_menu_buttons_section()  # crea seccion de menu secundario con botones para llamar a otros metodos


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

    def create_asset_info_section(self):
        # asset_info_frame (contiene nformación del activo como símbolo, precio y margin)
        self.asset_info_frame = Frame(self.right_panel)  # Empaquetar este frame en right_panel
        self.asset_info_frame.pack(pady=5, fill=X)

        self.info_label = Label(self.asset_info_frame,  # El Label ahora va dentro del asset_info_frame
                                text="Seleccione un activo para ver su información.",
                                font=('Arial', 12, 'bold'))
        self.info_label.pack()

        self.update_asset_info_display()  # llama a este metodo que actualiza la info en el label del activo seleccionado

    def populate_orders(self, parent_frame, order_type):
        """Llena el frame con la información de las órdenes del tipo especificado."""
        # Aquí iría la lógica para obtener las órdenes del activo seleccionado
        # (usando self.selected_asset.get()) y crear Labels y Buttons
        # dentro del parent_frame.

        symbol = self.selected_asset.get()
        # **TODO: Implementar la lógica para obtener las órdenes de self.data
        #        filtrando por el símbolo y el tipo de orden (order_type).**
        orders = self.get_orders_for_asset(symbol, order_type)  # Ejemplo de llamada a una función que debes implementar

        for order in orders:
            order_info = f"ID: {order['id']}, Precio: {order['price']}, Cantidad: {order['quantity']}"
            order_label = Label(parent_frame, text=order_info)
            order_label.pack(anchor='w')

            edit_button = Button(parent_frame, text="Editar", command=lambda oid=order['id']: self.edit_order(oid))
            edit_button.pack(side=LEFT, padx=2)

            delete_button = Button(parent_frame, text="Borrar", command=lambda oid=order['id']: self.delete_order(oid))
            delete_button.pack(side=LEFT, padx=2)

    def add_open_order(self):
        pass

    def add_pending_buy(self):
        pass

    def add_pending_sell(self):
        pass

    def create_asset_orders_section(self):
        """Crea la sección para mostrar las órdenes del activo y los botones de creación."""
        self.asset_orders_frame = Frame(self.right_panel, bd=1, relief=SUNKEN)
        self.asset_orders_frame.pack(pady=10, fill=BOTH, expand=True)

        Label(self.asset_orders_frame, text="Órdenes del Activo", font=('Dosis', 14, 'bold')).pack(pady=5, anchor='w')

        # Sección para las listas de órdenes (abiertas, compras pendientes y ventas pendientes)
        self.open_orders_frame = Frame(self.asset_orders_frame)
        self.open_orders_frame.pack(fill=X, pady=2)
        Label(self.open_orders_frame, text="Órdenes Abiertas").pack(anchor='w')
        self.populate_orders(self.open_orders_frame, "open")

        self.pending_buy_orders_frame = Frame(self.asset_orders_frame)
        self.pending_buy_orders_frame.pack(fill=X, pady=2)
        Label(self.pending_buy_orders_frame, text="Compras Pendientes").pack(anchor='w')
        self.populate_orders(self.pending_buy_orders_frame, "pending_buy")

        self.pending_sell_orders_frame = Frame(self.asset_orders_frame)
        self.pending_sell_orders_frame.pack(fill=X, pady=2)
        Label(self.pending_sell_orders_frame, text="Ventas Pendientes").pack(anchor='w')
        self.populate_orders(self.pending_sell_orders_frame, "pending_sell")

        # Sección para los botones de creación de nuevas órdenes
        new_order_label = Label(self.asset_orders_frame, text="Crear Nueva Orden:", font=('Dosis', 12, 'italic'))
        new_order_label.pack(anchor='w', pady=(10, 2))

        actions = [
            {"text": "Orden Abierta", "command": self.add_open_order},
            {"text": "Compra Pendiente", "command": self.add_pending_buy},
            {"text": "Venta Pendiente", "command": self.add_pending_sell},
            # Agrega aquí más botones de creación si es necesario
        ]

        for action in actions:
            button = Button(self.asset_orders_frame, text=action["text"], command=action["command"])
            button.pack(fill=X, pady=2)


    def get_orders_for_asset(self, symbol, order_type):
        """Obtiene las órdenes del activo seleccionado y del tipo especificado."""
        if symbol in self.data:
            if order_type == "open":
                return self.data[symbol].get('open_orders', [])
            elif order_type == "pending_buy":
                return self.data[symbol].get('buy_limits', [])
            elif order_type == "pending_sell":
                return self.data[symbol].get('sell_limits', [])
        return []

    def populate_orders(self, parent_frame, order_type):
        """Llena el frame con la información de las órdenes del tipo especificado."""
        symbol = self.selected_asset.get()
        orders = self.get_orders_for_asset(symbol, order_type)

        for order in orders:
            order_info = f"Precio: {order.get('price', 'N/A')} ---> {order.get('amount_usdt', 'N/A')} USDT, " \
                         f"SL: {order.get('stop_loss', 'N/A')}, TP: {order.get('target', 'N/A')}, " \
                         f"Cant: {order.get('quantity', 'N/A')}, MO: {order.get('mother_order', False)}"
            order_label = Label(parent_frame, text=order_info)
            order_label.pack(anchor='w')

            delete_button = Button(parent_frame, text="Borrar",
                                   command=lambda oid=order.get('id'): self.delete_order(oid))
            delete_button.pack(side=LEFT, padx=2)




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

