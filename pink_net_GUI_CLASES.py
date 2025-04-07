import tkinter as tk
from tkinter import *
import GUI_functions_module
import uuid
import json


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
        #self.create_asset_orders_section()  # crea seccion de ordenes del activo
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
        self.create_asset_orders_section()
        #self.show_orders()  # metodo para mostrar las ordenes relacionas con el activo


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
            self.save_data_asset(self.data, self.data[active_symbol], active_symbol)  # Guardar los datos
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

    def show_orders(self, parent_frame, order_type):
        # ... (tu código para mostrar las órdenes) ...
        pass

    def delete_order(self, order_id):
        # ... (tu código para eliminar la orden) ...
        pass


    def add_open_order(self):
        pass

    def add_pending_buy(self):
        pass

    def add_pending_sell(self):
        pass

    def create_asset_orders_section(self):
        """Crea la sección para mostrar las órdenes del activo y los botones de creación."""
        # Si ya existe el frame de las órdenes, lo destruimos
        if hasattr(self, 'asset_orders_frame'):  # verifica si la instancia actual de la clase AssetManagerGUI (self) tiene un atributo llamado 'asset_orders_frame'
            self.asset_orders_frame.destroy()

        # Destruir los frames de las órdenes antiguas si existen
        if hasattr(self, 'open_orders_frame'):
            self.open_orders_frame.destroy()
        if hasattr(self, 'pending_buy_orders_frame'):
            self.pending_buy_orders_frame.destroy()
        if hasattr(self, 'pending_sell_orders_frame'):
            self.pending_sell_orders_frame.destroy()

        # Crear los nuevos frames para las órdenes
        self.asset_orders_frame = Frame(self.right_panel, bd=1, relief=SUNKEN)
        self.asset_orders_frame.pack(pady=10, fill=BOTH, expand=True)

        Label(self.asset_orders_frame, text="Órdenes del Activo", font=('Dosis', 14, 'bold')).pack(pady=5, anchor='w')

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

        # Sección para los botones de creación de nuevas órdenes
        new_order_label = Label(self.asset_orders_frame, text="Crear Nueva Orden:", font=('Dosis', 12, 'italic'))
        new_order_label.pack(anchor='w', pady=(10, 2))

        actions = [
            {"text": "Orden Abierta", "command": lambda: self.show_new_order_form('open')},
            {"text": "Compra Pendiente", "command": lambda: self.show_new_order_form('pending_buy')},
            {"text": "Venta Pendiente", "command": lambda: self.show_new_order_form('pending_sell')},
            # Agrega aquí más botones de creación si es necesario
        ]

        buttons_frame = Frame(self.asset_orders_frame)  # Frame contenedor para los botones
        buttons_frame.pack(fill=tk.X)

        for action in actions:
            button = Button(buttons_frame, text=action["text"], command=action["command"])
            button.pack(side=LEFT, padx=5, pady=2)  # Empaquetamos los botones a la izquierda


    def delete_order(self):
        # funcion para eliminar una orden
        pass

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
        symbol = self.selected_asset.get()
        orders = self.get_orders_for_asset(symbol, order_type)
        print(orders)
        print(type(orders))

        for order in orders:
            order_info = f"Price: {order.get('price', 'N/A')} ---> {order.get('amount_usdt', 'N/A')} USDT, " \
                         f"SL: {order.get('stop_loss', 'N/A')}, Target: {order.get('target', 'N/A')}, " \
                         f"Quanttity: {order.get('quantity', 'N/A')}, MO: {order.get('mother_order', False)}"

            order_label = Label(parent_frame, text=order_info, font=('Dosis', 12, 'bold'))
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

