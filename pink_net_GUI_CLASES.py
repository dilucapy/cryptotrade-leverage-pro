import tkinter as tk
from tkinter import *
import GUI_functions_module
import uuid
import json
from tkinter import Toplevel, Label, Entry, Button, Checkbutton, BooleanVar, messagebox, simpledialog
import requests

# ruta del archivo JSON
filename = 'pink_net_data_3_GUI.json'

""" Utilizar clases para gestionar el estado y la lógica de tu GUI es una práctica
 fundamental para construir aplicaciones más complejas y mantenibles:"""


class AssetManagerGUI(tk.Tk):  # Hereda de tk.Tk
    """Clase AssetManagerGUI: Toda la lógica y los widgets de tu GUI están ahora
    dentro de esta clase."""
    def __init__(self, data, filename):
        super().__init__()  # Llama al constructor de la clase padre (tk.Tk)
        self.data = data
        self.filename = filename

        # Inicializar el estado de la GUI
        self.data = GUI_functions_module.load_data('pink_net_data_3_GUI.json')
        self.data = GUI_functions_module.order_orders(self.data)

        # Configuración para la selección única de botones de activo
        self.selected_asset = tk.StringVar()  # Almacena el símbolo del activo actualmente seleccionado
        self.active_asset_button = None  # Para rastrear el botón activo
        self.default_button_bg = 'azure4'  # Color de fondo por defecto
        self.selected_button_bg = 'green'  # Color de fondo cuando está seleccionado

        self.selected_asset_data = None  # Inicialización de self.selected_asset_data
        self.new_order_data = None  # Para almacenar los datos del formulario

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
        self.title_label = Label(self.top_panel, text='Gestión de Operaciones Apalancadas', fg='azure4', font=('Dosis', 20), bg='burlywood', width=30)
        self.title_label.grid(row=0, column=0, columnspan=5, pady=5, sticky="ew")

        # Panel de Activos (para los botones de activos)
        self.asset_menu = Frame(self.top_panel, bd=1, relief=FLAT)
        self.asset_menu.grid(row=1, column=0, columnspan=5, padx=10, pady=10,
                             sticky="ew")  # Lo colocamos debajo del título
        self.create_asset_buttons()

        # Panel Izquierdo (para el menu primario)
        self.left_panel = Frame(self.master, bd=1, relief=FLAT, bg='burlywood')
        self.left_panel.pack(side=LEFT, fill=Y)

        # Menu Primario
        self.primary_menu = Frame(self.left_panel, bd=1, relief=FLAT, bg='burlywood')
        self.primary_menu.pack(side=LEFT, padx=10, pady=10)
        self.create_primary_menu_buttons()

        # Panel Derecho (para mostrar información del activo y otras funciones)
        self.right_panel = Frame(self.master, bd=1, relief=FLAT, padx=10, pady=10)
        self.right_panel.pack(side=RIGHT, fill=X, padx=10, pady=10, expand=True)

        self.create_asset_info_section()  # crea seccion de iformación del activo (símbolo, precio, margin)
        #self.create_asset_orders_section()  # crea seccion de ordenes del activo
        #self.create_secondary_menu_buttons_section()  # crea seccion de menu secundario con botones para llamar a otros metodos


    def create_primary_menu_buttons(self):
        """Método para crear los botones del menús primario.
        command en los botones:
        Para los botones del menú primario, el command ahora llama directamente
        a métodos de la clase (por ej., self.add_new_symbol_ui)."""

        primary_buttons_config = [
            {"text": "ADD new symbol", "command": self.add_new_symbol},
            {"text": "Show MARGINS", "command": self.show_margins},
            {"text": "Update MARGINS", "command": self.update_margins},
            {"text": "Mostrar POSICIONES ABIERTAS", "command": self.show_open_positions},
            {"text": "Calcular LEVERAGE", "command": self.calculate_leverage},
            {"text": "Calculate BURN PRICE", "command": self.calculate_burn_price},
            {"text": "EXIT", "command": self.quit}
        ]
        for config in primary_buttons_config:
            button = Button(self.primary_menu, text=config["text"].title(), font=('Dosis', 12, 'bold'), bd=1, fg='white', bg='azure4', width=24, relief=RAISED, pady=10, cursor='hand2', command=config["command"])
            button.pack(pady=4, fill=X)

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

        # Destruir todos los widgets hijos del right_panel excepto self.asset_info_frame
        for widget in self.right_panel.winfo_children():
            if widget != self.asset_info_frame:
                widget.destroy()

        # linea para depuracion
        print(f"Hijos del right_panel antes de crear botones secundarios: {self.right_panel.winfo_children()}")

        # Crea la sección para mostrar las órdenes del activo y los botones de creación de ordenes
        self.create_asset_orders_section()

        # Destruir todos los widgets del panel izquierdo (menú primario)
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        # Crear y mostrar los botones del menú secundario en el panel izquierdo
        self.create_left_secondary_menu_buttons()

    def add_new_symbol(self):
        """Muestra una ventana de nivel superior (encimna de la ventana princiapla)
        para agregar un nuevo símbolo de activo."""
        add_symbol_window = Toplevel(self)
        add_symbol_window.title("Agregar Nuevo Símbolo")

        symbol_label = Label(add_symbol_window, text="Nuevo Símbolo:")
        symbol_label.pack(padx=10, pady=5)

        symbol_entry = Entry(add_symbol_window)
        symbol_entry.pack(padx=10, pady=5)
        symbol_entry.focus_set()  # Enfocar el campo de entrada al abrir la ventana

        def save_new_symbol():
            new_symbol = symbol_entry.get().strip().upper()
            if new_symbol:
                if new_symbol in self.data:
                    messagebox.showerror("Error", f"El símbolo '{new_symbol}' ya existe.")
                else:
                    self.data[new_symbol] = {
                        "current_price": 0,  # O cualquier otro valor inicial
                        "margin": 0,
                        "open_orders": [],
                        "buy_limits": [],
                        "sell_limits": []
                    }
                    self.save_data()  # Guarda todos los datos, incluyendo el nuevo símbolo
                    self.create_asset_buttons()  # Actualiza los botones de activos en el 'top panel'
                    messagebox.showinfo("Éxito", f"Símbolo '{new_symbol}' agregado.")
                    add_symbol_window.destroy()  # llama al metodo para destruir la instacia de toplevel
            else:
                messagebox.showerror("Error", "Por favor, introduce un símbolo.")

        save_button = Button(add_symbol_window, text="Guardar Símbolo", command=save_new_symbol)
        save_button.pack(pady=10)

        cancel_button = Button(add_symbol_window, text="Cancelar", command=add_symbol_window.destroy)
        cancel_button.pack(pady=5)

    def show_margins(self):
        pass

    def update_margins(self):
        pass

    def show_open_positions(self):
        pass

    def calculate_leverage(self):
        pass

    def calculate_burning_price_of_all(self):
        """calcula el precio de quema de todos los activos.
        Se ejecuta desde el menu primario"""
        pass

    def update_asset_info_display(self):
        """Actualiza la información del activo seleccionado en la GUI.
        Este método actualiza el contenido de un widget
        (en este caso, un Label en el right_panel)
        con la información del activo seleccionado."""
        if self.selected_asset and self.selected_asset_data:
            # obtener precio actual del activo
            symbol = self.selected_asset.get()  # Obtiene el valor del StringVar como string
            current_price = self.get_price(symbol)

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
        self.asset_info_frame.pack(pady=2, fill=X)

        self.info_label = Label(self.asset_info_frame,  # El Label ahora va dentro del asset_info_frame
                                text="Seleccione un activo para ver su información.",
                                font=('Arial', 11, 'bold'))
        self.info_label.pack()

        self.update_asset_info_display()  # llama a este metodo que actualiza la info en el label del activo seleccionado

    def add_new_order(self, data_asset, active_symbol, order_type, order_details):
        """Agrega una nueva orden del tipo especificado a los datos del activo."""

        order = {
            'id': order_details.get('id'),
            'price': order_details.get('price'),
            'amount_usdt': order_details.get('amount_usdt'),
            'quantity': round(order_details.get('amount_usdt', 0) / order_details.get('price', 1),
                              8) if order_details.get('price', 1) != 0 else 0,
            'stop_loss': order_details.get('stop_loss'),
            'target': order_details.get('target'),
        }

        if order_type == 'open':
            order['mother_order'] = order_details.get('mother_order', False)
            if 'open_orders' not in data_asset:
                data_asset['open_orders'] = []
            data_asset['open_orders'].append(order)
            print("Orden abierta agregada!")
        elif order_type == 'pending_buy':
            if 'buy_limits' not in data_asset:
                data_asset['buy_limits'] = []
            data_asset['buy_limits'].append(order)
            print("Orden de compra pendiente agregada!")
        elif order_type == 'pending_sell':
            if 'sell_limits' not in data_asset:
                data_asset['sell_limits'] = []
            data_asset['sell_limits'].append(order)
            print("Orden de venta pendiente agregada!")
        else:
            print(f"Tipo de orden '{order_type}' no válido.")
            return data_asset

        # Actualizar los datos del activo en el objeto data y guardar
        self.save_data_asset(self.data, data_asset, active_symbol)
        return data_asset

    def save_data_asset(self, data, data_asset, active_symbol):
        """Guarda los datos actualizados del activo en el objeto data y en el archivo."""
        if active_symbol in data:
            data[active_symbol] = data_asset
            try:
                with open(self.filename, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Datos para '{active_symbol}' guardados correctamente en '{self.filename}'.")
            except Exception as e:
                print(f"Error al guardar los datos en '{self.filename}': {e}")
        else:
            print(f"Error: Activo '{active_symbol}' no encontrado en los datos.")

    def save_data(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=4)
            print("Datos guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def handle_add_new_order(self, order_type):
        """
        Toma la información de la nueva orden recopilada del formulario
        (almacenada en self.new_order_data) y la agrega a la estructura
        de datos para el activo seleccionado. Luego, actualiza la
        visualización de las órdenes.
        """
        active_symbol = self.selected_asset.get()
        if active_symbol in self.data and self.new_order_data:
            self.data[active_symbol] = self.add_new_order(self.data[active_symbol], active_symbol, order_type, self.new_order_data)
            #self.save_data_asset(self.data, self.data[active_symbol], active_symbol)  # Guardar los datos
            self.show_orders(self.open_orders_frame, "open")
            self.show_orders(self.pending_buy_orders_frame, "pending_buy")
            self.show_orders(self.pending_sell_orders_frame, "pending_sell")
            self.update_asset_info_display()
            self.new_order_data = None  # Resetear los datos del formulario
        elif not active_symbol:
            tk.messagebox.showerror("Error", "Por favor, seleccione un activo primero.")
        elif not self.new_order_data:
            tk.messagebox.showerror("Error", "No se ingresaron datos en el formulario.")

    def show_new_order_form(self, order_type):
        """Esta función es llamada cuando el usuario hace clic en uno de los botones de
        "Crear Nueva Orden".
        Crea una nueva ventana secundaria (Toplevel) que es el formulario.
        Se encarga de procesar los datos ingresados por el usuario en el formulario
        para crear una nueva orden.
        Recibe el tipo de orden ('order_type') como argumento, y los valores de los
        campos de entrada (precio, monto, stop loss, target, y si es una orden madre).
        Intenta convertir los valores de precio, monto, stop loss ytarget a números de punto flotante.
        Si la conversión es exitosa, almacena estos valores
        (junto con el booleano de 'mother_order') en el atributo 'self.new_order_data' de la clase.
        Luego, llama a la función 'self.handle_add_new_order' para que se agregue la
        orden a los datos y se actualice la interfaz.
        Finalmente, cierra la ventana del formulario.
        Si ocurre un error durante la conversión a número (por ejemplo, si el usuario ingresó texto),
        muestra un cuadro de mensaje de error al usuario pidiéndole que ingrese valores numéricos válidos."""
        form = Toplevel(self)
        form.title(f"Nueva Orden de {order_type.capitalize()}")

        price_label = Label(form, text="Precio:")
        price_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        price_entry = Entry(form)
        price_entry.grid(row=0, column=1, padx=5, pady=5)

        amount_label = Label(form, text="Monto (USDT):")
        amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        amount_entry = Entry(form)
        amount_entry.grid(row=1, column=1, padx=5, pady=5)

        sl_label = Label(form, text="Stop Loss (0 para ninguno):")
        sl_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        sl_entry = Entry(form)
        sl_entry.grid(row=2, column=1, padx=5, pady=5)

        tp_label = Label(form, text="Target (0 para ninguno):")
        tp_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tp_entry = Entry(form)
        tp_entry.grid(row=3, column=1, padx=5, pady=5)

        mother_var = BooleanVar()
        if order_type == 'open':
            mother_check = Checkbutton(form, text="¿Orden Madre?", variable=mother_var)
            mother_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        submit_button = Button(form, text="Crear Orden",
                               command=lambda: self.get_form_data(form, order_type, price_entry.get(),
                                                                  amount_entry.get(), sl_entry.get(),
                                                                  tp_entry.get(),
                                                                  mother_var.get() if order_type == 'open' else False))
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

        cancel_button = Button(form, text="Cancelar", command=form.destroy)
        cancel_button.grid(row=6, column=0, columnspan=2, pady=5)

        form.wait_window()  # Pausa la ejecución de la ventana principal hasta que el formulario se cierre.

    def get_form_data(self, form, order_type, price, amount, sl, tp, mother_order):
        """
        Recupera los datos ingresados por el usuario en el formulario de nueva orden,
        genera un 'id' único para la orden, valida los datos convirtiéndolos a sus
        tipos numéricos correspondientes, almacena todos los detalles (incluyendo el 'id')
        en el atributo self.new_order_data como un diccionario, llama a la función
        para manejar la adición de la nueva orden (self.handle_add_new_order), y
        finalmente destruye la ventana del formulario. En caso de que la conversión
        a número falle (ValueError), muestra un mensaje de error al usuario.
        """
        try:
            price_val = float(price)
            amount_val = float(amount)
            sl_val = float(sl)
            tp_val = float(tp)

            order_id = str(uuid.uuid4())  # Generar el 'id' único aquí

            self.new_order_data = {
                'id': order_id,  # Incluir el 'id' en los datos de la orden
                'price': price_val,
                'amount_usdt': amount_val,
                'stop_loss': sl_val,
                'target': tp_val,
                'mother_order': mother_order
            }
            self.handle_add_new_order(order_type)  # llama al metodo manejar la adición de la nueva orden
            form.destroy()  # destruye la ventana del formulario
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    def delete_order(self, order_id):
        """Elimina una orden del activo seleccionado basándose en su ID."""
        symbol = self.selected_asset.get()

        if symbol in self.data:
            # este bucle asegura que intentemos eliminar la orden de la lista correcta.
            for order_type_key in ['open_orders', 'buy_limits', 'sell_limits']:
                if order_type_key in self.data[symbol]:  # verifica si esa clave existe dentro del diccionario de datos del activo seleccionado
                    # guardamos la longitud original de la lista de órdenes del tipo actual.
                    # Esto nos permitirá verificar más tarde si realmente se eliminó alguna orden.
                    original_length = len(self.data[symbol][order_type_key])
                    # creando una nueva lista sin la orden que queremos borrar (order_id)
                    self.data[symbol][order_type_key] = [
                        order for order in self.data[symbol][order_type_key] if order.get('id') != order_id
                    ]
                    if len(self.data[symbol][order_type_key]) < original_length:
                        print(f"Orden con ID '{order_id}' eliminada de {order_type_key} para {symbol}.")
                        self.save_data_asset(self.data, self.data[symbol], symbol)
                        # Recargar y mostrar las órdenes actualizadas
                        self.show_orders(self.open_orders_frame, "open")
                        self.show_orders(self.pending_buy_orders_frame, "pending_buy")
                        self.show_orders(self.pending_sell_orders_frame, "pending_sell")
                        return  # Salir de la función una vez que se elimina la orden

        print(f"No se encontró ninguna orden con ID '{order_id}' para eliminar.")

    def create_asset_orders_section(self):
        """Crea la sección para mostrar los botones de creación de ordenes y las órdenes del activo."""
        # Destruir los frames de las órdenes antiguas si existen
        if hasattr(self, 'asset_orders_frame'):
            self.asset_orders_frame.destroy()
        if hasattr(self, 'open_orders_frame'):
            self.open_orders_frame.destroy()
        if hasattr(self, 'pending_buy_orders_frame'):
            self.pending_buy_orders_frame.destroy()
        if hasattr(self, 'pending_sell_orders_frame'):
            self.pending_sell_orders_frame.destroy()
        if hasattr(self, 'buttons_frame_orders'):  # Destruir el frame de los botones también si existe
            self.buttons_frame_orders.destroy()

        # Crear los nuevos frames para las órdenes
        self.asset_orders_frame = Frame(self.right_panel, bd=1, relief=SUNKEN)
        self.asset_orders_frame.pack(pady=10, fill=BOTH, expand=True)

        # Sección para los botones de creación de nuevas órdenes
        # new_order_label = Label(self.asset_orders_frame, text="Crear Nueva Orden:", font=('Dosis', 12, 'italic'))
        # new_order_label.pack(anchor='w', pady=(10, 2))

        actions = [
            {"text": "Add OPEN ORDER", "command": lambda: self.show_new_order_form('open')},
            {"text": "Add BUY LIMIT", "command": lambda: self.show_new_order_form('pending_buy')},
            {"text": "Add SELL LIMIT", "command": lambda: self.show_new_order_form('pending_sell')},
            # Agrega aquí más botones de creación si es necesario
        ]

        buttons_frame = Frame(self.asset_orders_frame)  # Frame contenedor para los botones
        buttons_frame.pack(fill=tk.X)

        for action in actions:
            button = Button(buttons_frame,
                            text=action["text"],
                            font=('Dosis', 10, 'italic', 'bold'),
                            padx=10,
                            pady=10,
                            bg=self.default_button_bg,
                            fg='white',
                            bd=1,
                            relief=RAISED,
                            cursor='hand2',
                            command=action["command"])
            button.pack(side=LEFT, padx=5, pady=2)  # Empaquetamos los botones a la izquierda

        #Label(self.asset_orders_frame, text="Órdenes del Activo", font=('Dosis', 14, 'bold')).pack(pady=5, anchor='w')

        # Sección para las listas de órdenes (abiertas, compras pendientes y ventas pendientes)
        self.open_orders_frame = Frame(self.asset_orders_frame)
        self.open_orders_frame.pack(fill=X, pady=2)
        Label(self.open_orders_frame, text="Órdenes Abiertas").pack(anchor='w')
        self.show_orders(self.open_orders_frame, "open")

        self.pending_buy_orders_frame = Frame(self.asset_orders_frame)
        self.pending_buy_orders_frame.pack(fill=X, pady=2)
        Label(self.pending_buy_orders_frame, text="Compras Pendientes").pack(anchor='w')
        self.show_orders(self.pending_buy_orders_frame, "pending_buy")

        self.pending_sell_orders_frame = Frame(self.asset_orders_frame)
        self.pending_sell_orders_frame.pack(fill=X, pady=2)
        Label(self.pending_sell_orders_frame, text="Ventas Pendientes").pack(anchor='w')
        self.show_orders(self.pending_sell_orders_frame, "pending_sell")

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

    def show_orders(self, parent_frame, order_type):
        """Llena el frame con la información de las órdenes del tipo especificado."""
        # Limpiar los widgets existentes en el parent_frame, excepto los Label
        for widget in parent_frame.winfo_children():
            if not isinstance(widget, tk.Label):
                widget.destroy()
        
        symbol = self.selected_asset.get()
        orders = self.get_orders_for_asset(symbol, order_type)

        for order in orders:
            # Crear un Frame para contener la información de la orden y el botón
            order_row_frame = Frame(parent_frame)
            order_row_frame.pack(fill=X, pady=2)  # Empaquetar el frame de la fila

            order_info = f"Price: {order.get('price', 'N/A')} ---> {order.get('amount_usdt', 'N/A')} USDT, " \
                         f"SL: {order.get('stop_loss', 'N/A')}, Target: {order.get('target', 'N/A')}, " \
                         f"Quanttity: {order.get('quantity', 'N/A')}, MO: {order.get('mother_order', False)}"

            order_label = Label(order_row_frame, text=order_info, font=('Dosis', 12, 'bold'))
            order_label.pack(side=LEFT, anchor='w')  # Empaquetar la etiqueta a la izquierda

            delete_button = Button(order_row_frame, text="Delete",
                                   command=lambda oid=order.get('id'): self.delete_order(oid))
            delete_button.pack(side=RIGHT, padx=5)  # Empaquetar el botón a la derecha

            """# Botón de Editar (opcional, pero lo coloco como ejemplo)
            edit_button = Button(order_row_frame, text="Editar",
                                 command=lambda oid=order.get('id'): self.edit_order(oid))
            edit_button.pack(side=RIGHT, padx=2)"""

    def delete_all_asset_data(self):
        """Borra todos los datos del activo seleccionado, mantiene el símbolo y actualiza la interfaz de órdenes."""
        symbol = self.selected_asset.get()

        if symbol in self.data:
            # Destruir la sección de órdenes actual para una actualización visual instantánea
            if hasattr(self, 'asset_orders_frame'):
                self.asset_orders_frame.destroy()

            self.data[symbol] = {
                "current_price": 0,
                "margin": 0,
                "open_orders": [],
                "buy_limits": [],
                "sell_limits": []
            }
            self.save_data()
            self.update_asset_info_display()
            self.create_asset_orders_section() # Volver a crear la sección de órdenes vacía
            messagebox.showinfo("Acción Exitosa", f"Los datos del activo '{symbol}' han sido restablecidos.")
        else:
            messagebox.showerror("Error", f"El símbolo '{symbol}' no existe en los datos.")

    def clear_asset_buttons(self):
        """Elimina todos los botones de activos del panel superior."""
        if hasattr(self, 'top_panel'):
            for widget in self.top_panel.winfo_children():
                widget.destroy()

    def delete_asset(self):
        """Pregunta al usuario si desea eliminar el activo seleccionado y lo elimina,
        recreando los widgets para actualizar la lista de activos."""
        symbol = self.selected_asset.get()

        if symbol:
            confirmation = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el activo '{symbol}'?")
            if confirmation:
                if symbol in self.data:
                    del self.data[symbol]
                    self.save_data()  # Guardar los cambios en el archivo JSON

                    # Destruir los widgets para actualizar la lista de activos
                    for widget in self.winfo_children():
                        widget.destroy()

                    # Limpiar el estado de selección del activo
                    self.selected_asset.set("")
                    self.selected_asset_data = None
                    self.active_asset_button = None

                    # Recrear los widgets con la lista de activos actualizada
                    self.create_widgets()

                    messagebox.showinfo("Acción Exitosa", f"El activo '{symbol}' ha sido eliminado.")
                else:
                    messagebox.showerror("Error", f"El activo '{symbol}' no existe en los datos.")
            else:
                messagebox.showinfo("Eliminación Cancelada", f"Se mantuvo el activo '{symbol}'.")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un activo para eliminar.")

    def calculate_mother_order(self):
        """Abre el formulario para calcular la orden madre."""
        symbol = self.selected_asset.get()

        if not symbol:
            messagebox.showerror("Error", "Por favor, selecciona un activo primero.")
            return
        # muestra el formulario para ingresar los datos necesarios para calcular la orden madre
        self.show_calculate_mother_order_form(symbol)

    def show_calculate_mother_order_form(self, symbol):
        """Crea y muestra el formulario para calcular la orden madre."""
        top = tk.Toplevel(self)
        top.title(f"Calcular Orden Madre para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Precio Promedio de Compra:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_average_price = tk.Entry(top)
        entry_average_price.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Monto de Posición Abierta (USDT):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_open_position = tk.Entry(top)
        entry_open_position.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top, text="Beneficio Tomado:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_profits_taken = tk.Entry(top)
        entry_profits_taken.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(top, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_quantity = tk.Entry(top)
        entry_quantity.grid(row=3, column=1, padx=5, pady=5)

        # --- Botones ---
        calculate_button = tk.Button(top, text="Calcular",
                                      command=lambda: self.perform_mother_order_calculation(
                                          symbol,
                                          entry_average_price.get(),
                                          entry_open_position.get(),
                                          entry_profits_taken.get(),
                                          entry_quantity.get(),
                                          top  # se pasa la ventana Toplevel para cerrarla
                                      ))
        calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(top, text="Cancelar", command=top.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    def perform_mother_order_calculation(self, symbol, avg_price_str, open_pos_str, profit_str, qty_str, form_window):
        """Realiza el cálculo de la orden madre y pregunta si se guarda."""
        try:
            average_purchase_price = float(avg_price_str)
            open_position_usdt = float(open_pos_str)
            profits_taken = float(profit_str)
            quantity_mother_order = float(qty_str)

            if quantity_mother_order != 0:
                price_mother_order = average_purchase_price - (profits_taken / quantity_mother_order)
                price_mother_order_rounded = round(price_mother_order, 3)

                result_message = (
                    f"AMOUNT Mother Order {symbol}: {open_position_usdt} USDT\n"
                    f"PRICE Mother Order {symbol}: {price_mother_order_rounded}\n"
                    f"QUANTITY Mother Order: {quantity_mother_order}"
                )
                messagebox.showinfo("Resultado Orden Madre", result_message)

                save_confirmation = messagebox.askyesno("Guardar Orden Madre", "¿Desea guardar esta orden madre en OPEN ORDERS?")
                if save_confirmation:
                    if symbol in self.data:
                        new_order = {
                            "id": str(uuid.uuid4()),
                            "type": "open",
                            "price": price_mother_order_rounded,
                            "amount_usdt": open_position_usdt,
                            "quantity": quantity_mother_order,
                            "stop_loss": "N/A",
                            "target": "N/A",
                            "mother_order": True
                        }
                        self.data[symbol]["open_orders"].append(new_order)
                        self.save_data()
                        self.create_asset_orders_section()
                        messagebox.showinfo("Orden Guardada", "La orden madre ha sido guardada en órdenes abiertas.")
                    else:
                        messagebox.showerror("Error", f"El símbolo '{symbol}' ya no existe en los datos.")
                form_window.destroy()  # Cerrar el formulario después del cálculo y (opcional) guardado de la orden
            else:
                messagebox.showerror("Error", "La cantidad de la orden madre no puede ser cero.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos en todos los campos.")

    def generate_pink_net(self):
        """Abre el formulario para generar la PINK NET (Ordenes de compras pendientes)"""
        symbol = self.selected_asset.get()

        if not symbol:
            messagebox.showerror("Error", "Por favor, selecciona un activo primero.")
            return

        self.show_generate_pink_net_form(symbol)

    def show_generate_pink_net_form(self, symbol):
        """Crea y muestra el formulario para generar la PINK NET."""
        top = tk.Toplevel(self)
        top.title(f"Generar PINK NET para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Cantidad de Niveles:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_levels = tk.Entry(top)
        entry_levels.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Precio del Nivel Inicial:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_initial_level = tk.Entry(top)
        entry_initial_level.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top, text="Precio del Nivel Final:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_final_level = tk.Entry(top)
        entry_final_level.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(top, text="Monto Total a Invertir (USDT):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_investment_amount = tk.Entry(top)
        entry_investment_amount.grid(row=3, column=1, padx=5, pady=5)

        # --- Botones ---
        generate_button = tk.Button(top, text="Generar",
                                       command=lambda: self.calculate_pink_net_and_ask_save(
                                           symbol,
                                           entry_levels.get(),
                                           entry_initial_level.get(),
                                           entry_final_level.get(),
                                           entry_investment_amount.get(),
                                           top  # Pasar la ventana Toplevel para cerrarla
                                       ))
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(top, text="Cancelar", command=top.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    def calculate_pink_net_and_ask_save(self, symbol, levels_str, initial_level_str, final_level_str, investment_amount_str, form_window):
        """Realiza el cálculo de la PINK NET y pregunta si se guarda."""
        try:
            levels = int(levels_str)
            initial_level = float(initial_level_str)
            final_level = float(final_level_str)
            investment_amount = float(investment_amount_str)

            if levels <= 0 or investment_amount <= 0:
                messagebox.showerror("Error", "La cantidad de niveles y el monto de inversión deben ser mayores que cero.")
                return

            pink_net = []
            price_range = initial_level - final_level
            increment = price_range / (levels - 1) if levels > 1 else 0
            amount_per_level = investment_amount / levels

            for i in range(levels):
                price = initial_level - i * increment
                quantity = amount_per_level / price if price > 0 else 0
                level_pink_net = {
                    'price': round(price, 3),
                    'amount_usdt': round(amount_per_level, 2),
                    'quantity': round(quantity, 5),
                    'stop_loss': 0,  # se puede agregar campos al formulario si se desea
                    'target': 0,  # se puede agregar campos al formulario si se desea
                }
                pink_net.append(level_pink_net)

            result_message = "PINK NET Generada:\n"
            for level in pink_net:
                result_message += f"Precio: {level['price']}, Monto: {level['amount_usdt']} USDT, Cantidad: {level['quantity']}\n"

            messagebox.showinfo("PINK NET Generada", result_message)

            save_confirmation = messagebox.askyesno("Guardar PINK NET", "¿Desea guardar estos niveles como órdenes límite de compra?")
            if save_confirmation:
                if symbol in self.data:
                    # Advertir al usuario sobre la sobreescritura
                    overwrite = messagebox.askyesno("Advertencia", "Guardar la PINK NET sobreescribirá las órdenes límite de compra existentes. ¿Continuar?")
                    if overwrite:
                        self.data[symbol]["buy_limits"] = pink_net
                        self.save_data()
                        self.create_asset_orders_section()  # Actualizar la sección de órdenes
                        messagebox.showinfo("PINK NET Guardada", "La PINK NET ha sido guardada en órdenes límite de compra.")
                else:
                    messagebox.showerror("Error", f"El símbolo '{symbol}' ya no existe en los datos.")

            form_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos en todos los campos.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "El precio del nivel no puede ser cero.")

    def get_price(self, symbol):
        """
        Obtiene el precio actual de un activo en Binance.

        Parámetros:
        symbol (str): El símbolo del activo en formato por ej. 'HBAR'

        Retorna:
        float: El precio actual del activo, o None si hay un error.
        """
        quote = 'USDT'
        full_symbol = f'{symbol}{quote}'
        try:
            response = requests.get(f'https://api.binance.com/api/v3/ticker/price', params={'symbol': full_symbol})
            response.raise_for_status()
            data = response.json()
            return float(data['price'])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de API", f"Error al obtener el precio de {symbol}: {e}")
            return None

    def calculate_burn_price(self):
        """Calcula el precio de quema del activo seleccionado, obteniendo el precio actual de Binance."""
        symbol = self.selected_asset.get()

        if not symbol:
            messagebox.showerror("Error", "Por favor, selecciona un activo primero.")
            return

        current_price = self.get_price(symbol)

        if current_price is not None:
            if symbol in self.data:
                data_asset = self.data[symbol]
                margin = data_asset.get("margin", 0)

                burn_price_message = f" BURN PRICE SUMMARY {symbol} ".center(50, '*') + "\n"
                burn_price_message += "Advertencia: tener actualizada la orden madre y el MARGIN!\n\n"
                burn_price_message += f"CURRENT PRICE: {current_price}\n"
                burn_price_message += f"MARGIN: {margin} USDT\n\n"

                quantity_mother_order = 0
                mother_order_found = False
                if 'open_orders' in data_asset:
                    for order in data_asset['open_orders']:
                        if order.get('mother_order', False):
                            quantity_mother_order = order['quantity']
                            mother_order_found = True
                            break

                if not mother_order_found:
                    burn_price_message += "No hay MOTHER ORDER!\n"
                else:
                    burn_price_message += f"Cantidad Mother Order: {quantity_mother_order}\n"

                total_amount_buy_limits = 0
                total_quantity_buy_limits = 0
                if 'buy_limits' in data_asset and data_asset['buy_limits']:
                    for order in data_asset['buy_limits']:
                        total_amount_buy_limits += order['amount_usdt']
                        total_quantity_buy_limits += order['quantity']
                    burn_price_message += f"Total cantidad buy limits: {total_quantity_buy_limits}\n"
                    burn_price_message += f"Total monto buy limits: {total_amount_buy_limits} USDT\n"
                else:
                    burn_price_message += "No hay BUY LIMITS!\n"

                total_quantity = quantity_mother_order + total_quantity_buy_limits
                if total_quantity == 0:
                    messagebox.showerror("Error",
                                         "No se puede calcular BURN PRICE porque la cantidad total de activo es CERO.")
                else:
                    burn_price = ((current_price * quantity_mother_order) + total_amount_buy_limits - margin) / total_quantity
                    burn_price_message += f"\nBURN PRICE: {round(burn_price, 3)} USDT\n"
                    messagebox.showinfo("Resultado Burn Price", burn_price_message)

            else:
                messagebox.showerror("Error", f"No se encontraron datos para el activo '{symbol}'.")
        else:
            # Manejar el caso en que no se pudo obtener el precio de la API
            pass  # El error ya se mostró en get_price()

    def generate_sales_cloud(self):
        """Abre el formulario para generar la NUBE DE VENTAS."""
        symbol = self.selected_asset.get()

        if not symbol:
            messagebox.showerror("Error", "Por favor, selecciona un activo primero.")
            return

        self.show_generate_sales_cloud_form(symbol)

    def show_generate_sales_cloud_form(self, symbol):
        """Crea y muestra el formulario para generar la NUBE DE VENTAS."""
        top = tk.Toplevel(self)
        top.title(f"Generar NUBE DE VENTAS para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Cantidad de Niveles:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_levels = tk.Entry(top)
        entry_levels.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Precio del Nivel Inicial:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        entry_initial_level = tk.Entry(top)
        entry_initial_level.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top, text="Precio del Nivel Final:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        entry_final_level = tk.Entry(top)
        entry_final_level.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(top, text="Monto Total a Reducir (USDT):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_withdrawal_amount = tk.Entry(top)
        entry_withdrawal_amount.grid(row=3, column=1, padx=5, pady=5)

        # --- Botones ---
        generate_button = tk.Button(top, text="Generar",
                                       command=lambda: self.calculate_sales_cloud_and_ask_save(
                                           symbol,
                                           entry_levels.get(),
                                           entry_initial_level.get(),
                                           entry_final_level.get(),
                                           entry_withdrawal_amount.get(),
                                           top  # Pasar la ventana Toplevel para cerrarla
                                       ))
        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(top, text="Cancelar", command=top.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    def calculate_sales_cloud_and_ask_save(self, symbol, levels_str, initial_level_str, final_level_str, withdrawal_amount_str, form_window):
        """Realiza el cálculo de la NUBE DE VENTAS y pregunta si se guarda."""
        try:
            levels = int(levels_str)
            initial_level = float(initial_level_str)
            final_level = float(final_level_str)
            withdrawal_amount = float(withdrawal_amount_str)

            if levels <= 0 or withdrawal_amount <= 0:
                messagebox.showerror("Error", "La cantidad de niveles y el monto total a reducir deben ser mayores que cero.")
                return

            sales_cloud = []
            price_range = final_level - initial_level
            increment = price_range / (levels - 1) if levels > 1 else 0
            amount_per_level = withdrawal_amount / levels

            for i in range(levels):
                price = initial_level + i * increment
                quantity = amount_per_level / price if price > 0 else 0
                level_cloud = {
                    'price': round(price, 3),
                    'amount_usdt': round(amount_per_level, 2),
                    'quantity': round(quantity, 5),
                    'stop_loss': 0,
                    'target': 0,
                }
                sales_cloud.append(level_cloud)

            result_message = "NUBE DE VENTAS Generada:\n"
            for level in sales_cloud:
                result_message += f"Precio: {level['price']}, Monto: {level['amount_usdt']} USDT, Cantidad: {level['quantity']}\n"

            messagebox.showinfo("NUBE DE VENTAS Generada", result_message)

            save_confirmation = messagebox.askyesno("Guardar NUBE DE VENTAS", "¿Desea guardar estos niveles como SELL LIMIT?")
            if save_confirmation:
                if symbol in self.data:
                    # Advertir al usuario sobre la sobreescritura
                    overwrite = messagebox.askyesno("Advertencia", "Guardar la NUBE DE VENTAS sobreescribirá las órdenes límite de venta existentes. ¿Continuar?")
                    if overwrite:
                        self.data[symbol]["sell_limits"] = sales_cloud
                        self.save_data()
                        self.create_asset_orders_section() # Actualizar la sección de órdenes
                        messagebox.showinfo("NUBE DE VENTAS Guardada", "La NUBE DE VENTAS ha sido guardada!")
                else:
                    messagebox.showerror("Error", f"El símbolo '{symbol}' ya no existe en los datos.")

            form_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos en todos los campos.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "El precio del nivel no puede ser cero.")

    def render_open_orders(self):
        pass

    def update_current_price(self):
        pass

    def return_to_primary_menu(self):
        """Destruye todos los widgets, restablece la selección del activo y muestra el menú primario."""
        # Destruir todos los widgets de la ventana principal
        for widget in self.winfo_children():
            widget.destroy()

        # Restablecer el estado de selección del activo
        self.selected_asset.set("")
        self.selected_asset_data = None
        self.active_asset_button = None

        # Volver a crear los widgets, lo que incluirá el menú primario en el panel izquierdo
        self.create_widgets()

        print("Retorno al menú primario.")

    def create_left_secondary_menu_buttons(self):
        """Crea y empaqueta los botones del menú secundario en el panel izquierdo."""
        self.secondary_menu = Frame(self.left_panel, bd=1, relief=FLAT, bg='burlywood')
        self.secondary_menu.pack(side=LEFT, padx=10, pady=10)

        buttons_config = [
            {"text": "MENU PRINCIPAL", "command": self.return_to_primary_menu},
            {"text": "Borrar Datos del Activo", "command": self.delete_all_asset_data},
            {"text": "Borrar Activo", "command": self.delete_asset},
            {"text": "Calcular Orden Madre", "command": self.calculate_mother_order},
            {"text": "Generar PINK NET", "command": self.generate_pink_net},
            {"text": "Calcular Precio de Quema", "command": self.calculate_burn_price},
            {"text": "Generar Nube de Ventas", "command": self.generate_sales_cloud},
            {"text": "Renderizar Órdenes Abiertas", "command": self.render_open_orders},
            {"text": "Actualizar Precio Actual", "command": self.update_current_price},
        ]

        for button_info in buttons_config:
            button = tk.Button(self.secondary_menu,
                               text=button_info["text"],
                               font=('Dosis', 12, 'bold'),
                               padx=10,
                               pady=10,
                               bg=self.default_button_bg,
                               fg='white',
                               bd=1,
                               relief=RAISED,
                               cursor='hand2',
                               command=button_info["command"])

            button.pack(pady=4, padx=2, fill=X)


if __name__ == "__main__":
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Crear una instancia de la clase de GUI
    gui = AssetManagerGUI(data, filename)

    # Configurar la ventana principal (tamaño, resizable, etc.)
    gui.state('zoomed')  # Maximizar la ventana
    gui.resizable(False, False)
    gui.config(bg='burlywood')

    # Iniciar el loop principal de Tkinter (mantiene la ventana abierta y responde a los eventos)
    gui.mainloop()





