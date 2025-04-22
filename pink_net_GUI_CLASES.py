import tkinter as tk
from tkinter import *
import uuid
import json
from tkinter import Toplevel, Label, Entry, Button, Checkbutton, BooleanVar, messagebox, simpledialog, ttk
import requests
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# ruta del archivo JSON
filename = 'pink_net_data_3_GUI.json'

""" Utilizar clases para gestionar el estado y la lógica de tu GUI es una práctica
 fundamental para construir aplicaciones más complejas y mantenibles:"""

# Colores para usar
mandarina_atomica = '#FEB285'
azul_palido = '#AACCEE'
burlywood = 'burlywood'


class CustomInfoDialog(tk.Toplevel):
    """Una ventana de diálogo personalizada para mostrar mensajes informativos al usuario.
        Esta clase hereda de tk.Toplevel y proporciona una alternativa a los messagebox.showinfo()
        estándar, permitiendo un mayor control sobre la apariencia del diálogo, incluyendo la
        fuente del mensaje.

        Atributos:
            parent (tk.Tk o tk.Toplevel): La ventana padre de este diálogo.
            title (str): El título de la ventana del diálogo (por defecto: "Información").
            message (str): El mensaje de texto que se mostrará en el diálogo (por defecto: "").
            message_label (tk.Label): El widget Label que contiene el mensaje.
            ok_button (tk.Button): El botón "Aceptar" para cerrar el diálogo.

        Métodos:
            __init__(self, parent, title="Información", message=""):
                Inicializa una nueva instancia de CustomInfoDialog. Configura la ventana,
                crea y empaqueta el Label del mensaje y el botón "Aceptar". También
                establece la modalidad y centra la ventana sobre su padre (opcional).
        """
    def __init__(self, parent, title="Información", message=""):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)

        self.message_label = tk.Label(self, text=message, font=("Arial", 12, "bold"), padx=20, pady=20)
        self.message_label.pack()

        self.ok_button = tk.Button(self,
                                   text="Aceptar",
                                   cursor='hand2',
                                   font=("Segoe UI", 12),
                                   command=self.destroy, padx=10, pady=5)
        self.ok_button.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)


class CustomErrorDialog(tk.Toplevel):
    """Una ventana de diálogo personalizada para mostrar mensajes de error al usuario.
       Hereda de tk.Toplevel y presenta un título y un mensaje de error,
       junto con un botón "Aceptar" para cerrar la ventana."""
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Error")
        self.resizable(False, False)

        self.message_label = tk.Label(self, text=message, fg="red", font=("Arial", 14, "bold"), padx=20, pady=20)
        self.message_label.pack()

        self.ok_button = tk.Button(self,
                                   text="Aceptar",
                                   cursor='hand2',
                                   font=("Segoe UI", 12),
                                   padx=10, pady=5,
                                   command=self.destroy)
        self.ok_button.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

        try:
            pass
            # self.error_icon = tk.PhotoImage(file="ruta/al/icono_error.png") # Reemplaza con tu ruta
            # self.iconphoto(False, self.error_icon)
        except tk.TclError as e:
            print(f"Error al cargar el icono: {e}")


class CustomConfirmationDialog(tk.Toplevel):
    """Una ventana de diálogo personalizada para obtener una respuesta booleana (Sí/No)
    del usuario.
    Hereda de tk.Toplevel y presenta un mensaje con botones "Sí" y "No",
    almacenando la elección del usuario en el atributo `result`."""
    def __init__(self, parent, title="Confirmación", message=""):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None  # almacena la respuesta

        tk.Label(self, text=message, font=("Arial", 14, "bold"), padx=20, pady=20).pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Sí", cursor='hand2', font=("Segoe UI", 12), command=lambda: self.set_result(True), padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="No", cursor='hand2', font=("Segoe UI", 12), command=lambda: self.set_result(False), padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def set_result(self, value):
        self.result = value
        self.destroy()


class CustomAskFloatDialog(tk.Toplevel):
    """Una ventana de diálogo personalizada para solicitar un valor float al usuario.
    Hereda de tk.Toplevel y proporciona un control adicional sobre el diálogo."""
    def __init__(self, parent, title="Ingrese un valor", prompt="Por favor, ingrese un número:", initialvalue=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None

        tk.Label(self, text=prompt, font=("Arial", 12), padx=20, pady=10).pack()

        self.entry = tk.Entry(self, font=("Arial", 12))
        if initialvalue is not None:
            self.entry.insert(0, initialvalue)
        self.entry.pack(padx=20, pady=5)
        self.entry.focus_set()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Aceptar", cursor="hand2", font=("Segoe UI", 12), command=self.ok, padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", cursor="hand2", font=("Segoe UI", 12), command=self.cancel, padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def ok(self):
        try:
            self.result = float(self.entry.get())
            self.destroy()
        except ValueError:
            tk.messagebox.showerror("Error", "Por favor, ingrese un número válido.")
            self.entry.focus_set()

    def cancel(self):
        self.destroy()


class AssetManagerGUI(tk.Tk):  # Hereda de tk.Tk
    """Clase AssetManagerGUI: Toda la lógica y los widgets de tu GUI están ahora
    dentro de esta clase."""
    def __init__(self, filename):
        super().__init__()  # Llama al constructor de la clase padre (tk.Tk)

        self.filename = filename  # Archivo de datos
        self.data = self.load_data(self.filename)  # Carga los datos iniciales desde el archivo
        # Ordenar las órdenes si se cargaron los datos correctamente.
        if self.data:
            self.order_orders(self.data)

        # Configurar la ventana principal
        self.state('zoomed')  # Maximizar la ventana
        self.resizable(False, False)  # Impide el redimensionamiento de la ventana.
        self.config(bg=azul_palido)  # Establece el color de background.


        # Configuración para la selección única de botones de activo
        self.selected_asset = tk.StringVar()  # Almacena el símbolo del activo actualmente seleccionado
        self.active_asset_button = None  # Para rastrear el botón activo
        self.default_button_bg = 'azure4'  # Color de fondo por defecto
        self.selected_button_bg = 'green'  # Color de fondo cuando está seleccionado

        self.selected_asset_data = None  # Inicialización de self.selected_asset_data
        self.new_order_data = None  # Para almacenar los datos del formulario

        # Crear los widgets de la GUI
        self.create_widgets()

        # Estilos de apariencia para toplevel y button
        self.toplevel_bgcolor = "orange"  # Color de fondo predeterminado para las ventanas emergentes (Toplevel)
        self.button_font = ("Segoe UI", 12)  # Fuente predeterminada para el texto de los botones (familia, tamaño)
        self.button_bgcolor = "lightgreen"  # Color de fondo predeterminado para los botones
        self.button_relief = tk.FLAT  # Estilo de relieve predeterminado para los botones (sin efecto 3D)

    def load_data(self, filename):
        """Carga los datos desde un archivo JSON. Devuelve un diccionario,
        incluso si el archivo no se encuentra (diccionario vacío)
        o muestra un error al usuario si falla la carga."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            self.show_info_messagebox("Información", f"No se encontró el archivo: {filename}. Iniciando con datos vacíos.")
            return {}
        except json.JSONDecodeError:
            self.show_error_messagebox("Error de Formato", f"El archivo {filename} no tiene un formato JSON válido.")
            return {}
        except Exception as e:
            self.show_error_messagebox("Error Inesperado", f"Ocurrió un error al cargar {filename}: {e}")
            return {}

    def order_orders(self, data):
        """Ordena las órdenes abiertas y órdenes límite de activos financieros."""
        for asset, data_asset in data.items():
            # Verificar si data_asset es None
            if data_asset is None:
                print(f"Advertencia: El activo '{asset}' es None")
                continue

            # Verificar si 'open_orders' y 'limit_orders' están presentes
            if 'open_orders' not in data_asset:
                print(f"Advertencia: El activo '{asset}' no tiene 'open_orders'.")
                continue
            if 'buy_limits' not in data_asset:
                print(f"Advertencia: El activo '{asset}' no tiene 'buy_limits'.")
                continue

            # Ordenar open_orders por precio, pero mantener la orden madre en la primera posición
            data_asset['open_orders'] = sorted(data_asset['open_orders'],
                                               key=lambda x: (not x['mother_order'], x['price']))

            # Ordenar buy_limits por precio
            data_asset['buy_limits'] = sorted(data_asset['buy_limits'], key=lambda x: x['price'])
        return data

    def show_info_messagebox(self, parent, titulo, mensaje):
        """Este metodo es una alternativa a 'messagebox.showinfo'
        se llama a la clase que personaliza la ventana de informacion"""
        CustomInfoDialog(parent, titulo, mensaje)

    def show_error_messagebox(self, parent, mensaje):
        """Este metodo es una alternativa a 'messagebox.showerror'
        llama a la clase que personaliza la ventana de error"""
        CustomErrorDialog(parent, mensaje)

    def show_confirmation_dialog(self, parent, titulo, mensaje):
        """Este metodo es una alternativa a 'messagebox.askyesno'
        llama a la clase que personaliza la ventana de confirmacion"""
        dialog = CustomConfirmationDialog(parent, titulo, mensaje)
        return dialog.result

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

        # Panel Derecho (para mostrar información del activo y otras funciones)
        self.right_panel = Frame(self.master, bd=1, relief=FLAT, padx=10, pady=10)
        self.right_panel.pack(side=RIGHT, fill=X, padx=10, pady=10, expand=True)

        # Frame para la tabla de precios de quema
        self.burn_price_table_frame = tk.Frame(self.right_panel)
        self.burn_price_table_frame.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo (para el menu primario)
        self.left_panel = Frame(self.master, bd=1, relief=FLAT, bg='burlywood')
        self.left_panel.pack(side=LEFT, fill=Y)

        # Menu Primario
        self.primary_menu = Frame(self.left_panel, bd=1, relief=FLAT, bg='burlywood')
        self.primary_menu.pack(side=LEFT, padx=10, pady=10)
        self.create_primary_menu_buttons()

        # crea seccion de iformación del activo (símbolo, precio, margin)
        self.create_asset_info_section()
        #self.create_asset_orders_section()  # crea seccion de ordenes del activo
        #self.create_secondary_menu_buttons_section()  # crea seccion de menu secundario con botones para llamar a otros metodos

    def create_primary_menu_buttons(self):
        """Método para crear los botones del menú primario.
        command en los botones: llama directamente
        a métodos de la clase (por ej., self.add_new_symbol)."""

        primary_buttons_config = [
            {"text": "ADD new symbol", "command": self.add_new_symbol},
            {"text": "Show MARGINS", "command": self.show_margins},
            {"text": "Update MARGINS", "command": self.update_margins},
            {"text": "Mostrar POSICIONES ABIERTAS", "command": self.show_open_positions},
            {"text": "Calcular LEVERAGE", "command": self.calculate_leverage},
            {"text": "Calculate BURN PRICES", "command": self.calculate_and_show_all_burning_prices},
            {"text": "EXIT", "command": self.quit}
        ]
        for config in primary_buttons_config:
            button = Button(self.primary_menu, text=config["text"].title(), font=('Dosis', 12, 'bold'), bd=1, fg='white', bg='azure4', width=24, relief=RAISED, pady=10, cursor='hand2', command=config["command"])
            button.pack(pady=4, fill=X)

    def get_symbols_for_buttons(self):
        """Crea una lista de los símbolos de los activos que se encuentran en self.data
        para crear los botones en el panel asset_menu."""
        list_symbol = list(self.data.keys())
        return list_symbol

    def create_asset_buttons(self):
        """Crea los botones de los activos en el top_panel."""
        list_symbols = self.get_symbols_for_buttons()  # llama al método como self.metodo()
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

        # Si la sección de información del activo existe, la hace visible nuevamente
        if hasattr(self, 'asset_info_frame'):
            self.asset_info_frame.pack(pady=2, fill=X)

        # Destruir todos los widgets hijos del right_panel excepto self.asset_info_frame
        for widget in self.right_panel.winfo_children():
            if widget != self.asset_info_frame:
                widget.destroy()

        # Se maneja la apariencia visual de los botones
        # Deseleccionar el botón anterior
        if self.active_asset_button and self.active_asset_button != button:
            self.active_asset_button.config(bg=self.default_button_bg)

        # Seleccionar el botón actual
        self.active_asset_button = button
        button.config(bg=self.selected_button_bg)

        # Buscar y asignar la información del activo seleccionado
        if symbol in self.data:
            self.selected_asset_data = self.data[symbol]
        else:
            self.selected_asset_data = None

        # se llama a este metodo para mostrar informacion del activo
        self.update_asset_info_display()

        # linea para depuracion
        #print(f"Hijos del right_panel antes de crear botones secundarios: {self.right_panel.winfo_children()}")

        # Crea la sección para mostrar las órdenes del activo y los botones de creación de ordenes
        self.create_asset_orders_section()

        # Destruir todos los widgets del panel izquierdo (menú primario)
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        # Crear y mostrar los botones del menú secundario en el panel izquierdo
        self.create_left_secondary_menu_buttons()

    def add_new_symbol(self):
        """Muestra una ventana de nivel superior (encimna de la ventana principal)
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
        """Muestra los márgenes individuales de cada activo y el total en un cuadro de diálogo,
        ordenados por margen de mayor a menor."""
        total_margin = 0
        asset_margins = []
        margins_report = "  Symbol        MARGIN (USDT)   Weight\n"
        margins_report += "  " + "-" * 80 + "\n"

        # Primer bucle: Se itera sobre todos los activos para calcular la suma total de los márgenes y almacenar los márgenes con sus símbolos
        for symbol, data_asset in self.data.items():
            margin = data_asset.get('margin', 0)  # Usamos .get() para evitar errores si la clave no existe (con valor predeterminado de '0')
            total_margin += margin
            asset_margins.append({'symbol': symbol, 'margin': margin})

        # Ordenar la lista de activos por margen de mayor a menor
        asset_margins_ordenados = sorted(asset_margins, key=lambda item: item['margin'], reverse=True)

        # Muestra un error si el margen total es cero.
        if total_margin == 0:
            self.show_error_messagebox(self, "Total Margin = 0\nDebes Actualizar Margenes!")
            return  # Salir de la función si no hay márgenes para mostrar

        # Segundo bucle: se itera sobre los márgenes ordenados para calcular la ponderación y construir el reporte
        for asset in asset_margins_ordenados:
            symbol = asset['symbol']
            margin = asset['margin']
            if total_margin > 0:
                ponderacion = round(margin / total_margin, 3)
            else:
                ponderacion = 0.0

            margins_report += f"  {symbol:<13}      {margin:<17.2f}         {ponderacion:<10}\n"

        margins_report += f"\n\n  TOTAL MARGINS: {int(total_margin)} USDT"

        self.show_info_messagebox(self, "Márgenes y Total", margins_report)

    def ask_trading_account(self, parent):
        """Método que muestra la ventana de diálogo personalizado
        para pedir al usuario que ingrese el monto de cuenta de trading."""
        dialog = CustomAskFloatDialog(parent,
                                      title="Monto Cuenta de Trading",
                                      prompt="Ingrese el monto total de la cuenta de trading:")
        return dialog.result

    def calculate_equitable_margin(self):
        """Divide el monto total de la cuenta de trading equitativamente
        entre los activos y actualiza sus márgenes."""
        trading_account = self.ask_trading_account(self)

        if trading_account is not None and trading_account > 0:
            num_assets = len(self.data)
            if num_assets > 0:
                margin = round(trading_account / num_assets, 2)
                ponderacion = round(margin / trading_account, 3) if trading_account > 0 else 0.0
                report = "  Symbol        MARGIN (USDT)    Weight\n"
                report += "  " + "-" * 80 + "\n"
                for symbol, data_asset in self.data.items():
                    data_asset['margin'] = margin
                    report += f"  {symbol:<13}      {margin:<17.2f}         {ponderacion:<10}\n"

                self.show_info_messagebox(self, "Márgenes Actualizados (Equitativo)", report)
                self.save_data()

            else:
                self.show_error_messagebox(self, "No hay activos para calcular el margen.")

        elif trading_account is not None:
            self.show_error_messagebox(self, "El monto de la cuenta de trading debe ser mayor que cero.")

    def calculate_weighted_margin_form(self):
        """Muestra un formulario para ingresar los montos de posición abierta
        de cada activo y calcula los márgenes ponderados."""

        top_weighted_form = tk.Toplevel(self)
        top_weighted_form.title("Ponderación NO Equitativa")
        top_weighted_form.config(bg=self.toplevel_bgcolor)
        top_weighted_form.geometry('400x350')

        row = 0

        # Etiqueta para el monto total de la cuenta de trading
        label = tk.Label(top_weighted_form,
                         text="Monto Total de la Cuenta de Trading (USDT):",
                         bg=self.toplevel_bgcolor,
                         font=("Arial", 10, "bold"))
        label.grid(row=row, column=0, padx=5, pady=5, sticky="w")

        entry_trading_account = tk.Entry(top_weighted_form, font=("Arial", 12, "bold"))
        entry_trading_account.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        row += 1

        # Etiquetas y campos de entrada para cada activo
        entry_amounts = {}
        for symbol in self.data:
            label_asset = tk.Label(top_weighted_form,
                                   text=f"Posición Abierta en USDT para {symbol}:",
                                   bg=self.toplevel_bgcolor,
                                   font=("Arial", 10, "bold"))
            label_asset.grid(row=row, column=0, padx=5, pady=10, sticky="w")
            entry = tk.Entry(top_weighted_form, font=("Arial", 12, "bold"))
            entry.grid(row=row, column=1, padx=5, pady=10, sticky="ew")
            entry_amounts[symbol] = entry
            row += 1

        def calculate_and_show():
            trading_account_str = entry_trading_account.get()
            try:
                trading_account = float(trading_account_str)
                if trading_account <= 0:
                    self.show_error_messagebox("El monto de la cuenta de trading debe ser mayor que cero.")
                    return
            except ValueError:
                self.show_error_messagebox("Por favor, ingrese un número válido para el monto de la cuenta de trading.")
                return

            total_usdt_open_positions = 0
            current_amounts = {}
            for symbol, entry in entry_amounts.items():
                amount_str = entry.get()
                try:
                    amount_asset = float(amount_str)
                    current_amounts[symbol] = amount_asset
                    total_usdt_open_positions += amount_asset
                except ValueError:
                    self.show_error_messagebox(f"Por favor, ingrese un número válido para la posición abierta de {symbol}.")
                    return

            if total_usdt_open_positions > 0:
                report = "  Symbol        MARGIN (USDT)   Weight\n"
                report += "  " + "-" * 80 + "\n"
                for symbol, data_asset in self.data.items():
                    amount_asset = current_amounts.get(symbol, 0)
                    weight = round(amount_asset / total_usdt_open_positions, 3)
                    margin = round(trading_account * weight)
                    data_asset['margin'] = margin
                    report += f"  {symbol:<13}      {margin:<17.2f}         {weight:<10}\n"

                self.show_info_messagebox(self, "Márgenes Actualizados (Ponderado)", report)
                self.save_data()
                top_weighted_form.destroy()  # Cerrar el formulario después de calcular
            else:
                self.show_error_messagebox("El total de las posiciones abiertas debe ser mayor que cero.")

        # Frame para los botones
        button_frame = tk.Frame(top_weighted_form, bg=self.toplevel_bgcolor)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)

        # Botón Calcular
        calculate_button = tk.Button(button_frame,
                                     text="Calcular",
                                     cursor="hand2",
                                     font=self.button_font,
                                     pady=5,
                                     padx=20,
                                     command=calculate_and_show)
        calculate_button.pack(side=tk.LEFT, padx=10)

        # Botón Cancelar
        cancel_button = tk.Button(button_frame,
                                  text="Cancelar",
                                  cursor="hand2",
                                  font=self.button_font,
                                  pady=5,
                                  padx=20,
                                  command=top_weighted_form.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

        top_weighted_form.grid_columnconfigure(1, weight=1)  # Hacer que la columna de entrada se expanda

    def _calculate_equitable_and_destroy_window(self, selection_window):
        """(Metodo interno en update_margins)
        Calcula márgenes equitativos y cierra la ventana de selección.
        selection_window es la ventana Toplevel que se crea en el método update_margins
        y presenta las opciones al usuario."""
        self.calculate_equitable_margin()
        selection_window.destroy()

    def _calculate_weighted_form_and_destroy_window(self, selection_window):
        """(Metodo interno para el metodo update_margins)
        Muestra el formulario ponderado y cierra la ventana de selección.
        selection_window es la ventana Toplevel que se crea en el método update_margins
        y presenta las opciones al usuario"""

        self.calculate_weighted_margin_form()
        selection_window.destroy()

    def update_margins(self):
        """Permite al usuario actualizar los márgenes de los activos
        mediante división equitativa o ponderación."""
        if not self.data:
            self.show_info_messagebox(self, "Información", "No hay activos guardados!")
            return

        # Si 'self.data' no está vacío, se crea una nueva ventana Toplevel
        top = tk.Toplevel(self)
        top.config(bg=self.toplevel_bgcolor)
        top.geometry('400x260')
        top.title("Actualizar Márgenes de Activos")

        # Se crea un widget Label de Tkinter para mostrar texto al usuario.
        label = tk.Label(top, text="Elige una opción para calcular los márgenes:", bg=self.toplevel_bgcolor, font=("Arial", 12, "bold"))
        label.pack(pady=10)

        equitable_button = tk.Button(top,
                                     text="División Equitativa",
                                     pady=5,
                                     font=self.button_font,
                                     cursor="hand2",
                                     command=lambda: self._calculate_equitable_and_destroy_window(top))
        equitable_button.pack(fill='x', pady=5, padx=60)

        weighted_button = tk.Button(top,
                                    text="Ponderación NO Equitativa",
                                    pady=5,
                                    font=self.button_font,
                                    cursor="hand2",
                                    command=lambda: self._calculate_weighted_form_and_destroy_window(top))
        weighted_button.pack(fill='x', pady=5, padx=60)

        cancel_button = tk.Button(top,
                                  text="Cancel",
                                  pady=5,
                                  font=self.button_font,
                                  cursor="hand2",
                                  command=top.destroy)
        cancel_button.pack(fill='x', pady=30, padx=100)

    def calculate_total_open_amount(self):
        """Calcula el monto total de todas las operaciones abiertas por activo
        y devuelve el total general, la lista de símbolos y la lista de montos."""

        total_open_amount = 0
        list_amount = []
        list_symbol = []

        for symbol, data_asset in self.data.items():
            if data_asset.get('open_orders'):
                total_quantity = 0
                for order in data_asset['open_orders']:
                    quantity = order.get('quantity', 0)
                    total_quantity += quantity

                # Obtenemos el precio actual para el activo
                current_price = self.get_price(symbol)

                if current_price is not None:
                    amount = int(total_quantity * current_price)  # redondeamos a entero
                    list_amount.append(amount)
                    list_symbol.append(symbol)
                    total_open_amount += amount
                else:
                    print(f"No se pudo obtener el precio para {symbol}.")
                    # Si no se pudo obtener el precio (con la API), se agrega el monto de apertura total de todas las ordenes abiertas
                    sum_amount = 0
                    for order in data_asset['open_orders']:
                        amount = order['amount_usdt']
                        sum_amount += amount

                    list_amount.append(int(sum_amount))
                    total_open_amount += sum_amount
                    list_symbol.append(symbol)

        return total_open_amount, list_symbol, list_amount

    def show_open_positions(self):
        """Muestra los montos totales por activo de todas las órdenes abiertas
                en un gráfico de barras."""

        total_open_amount, list_symbol, list_amount = self.calculate_total_open_amount()

        if not list_amount:
            messagebox.showinfo("Información", "No hay órdenes abiertas guardadas para mostrar los montos.")
            return 0  # Devuelve 0 si no hay datos

        # Se crea una lista, con tuplas creadas con zip (symbol, monto), por el segundo elemento (monto), de menor a mayor.
        sorted_data = sorted(zip(list_symbol, list_amount), key=lambda x: x[1])
        sorted_symbols, sorted_amounts = zip(*sorted_data)  # el asterisco que precede a sorted_data tiene la función de desempaquetar la lista

        # Crear gráfico
        plt.figure(figsize=(10, 6))
        bar_width = 0.35
        x = range(len(sorted_amounts))

        # Gráficos de barras
        bars_amounts = plt.bar(x, sorted_amounts, width=bar_width, label='Amount', color='orange', alpha=0.7)

        # Añadir etiquetas sobre cada barra
        for bar in bars_amounts:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     f"{bar.get_height()} USDT",
                     ha='center', va='bottom', fontsize=11, weight='bold')

        # Etiquetas y título
        plt.xlabel('ASSETS')
        plt.ylabel('Amount (USDT)')
        plt.title(f'TOTAL OPEN AMOUNT: {total_open_amount} USDT', ha='center', weight='bold')

        # Configurar marcas en el eje x con los símbolos
        plt.xticks(x, sorted_symbols, weight='bold', rotation=45)

        plt.legend()
        plt.tight_layout()

        # Mostrar gráfico maximizado (si es lo deseado)
        mng = plt.get_current_fig_manager()
        try:
            mng.window.state('zoomed')
        except AttributeError:
            pass

        plt.show()

        return total_open_amount  # Devuelve el total

    def calculate_leverage(self):
        """Calcula y muestra el apalancamiento y el monto a reducir por nivel de apalancamiento."""

        total_open_amount, _, _ = self.calculate_total_open_amount()

        # ventana de dialogo para preguntar al usuario por el monto de Trading Account
        trading_account = self.ask_trading_account(self)

        top = tk.Toplevel(self)
        top.title("Calcular Apalancamiento")

        label = tk.Label(top, text="Leveraged Amount and Reduce Position by Leverage Level",
                         font=('Arial', 12, 'bold'))
        label.pack(pady=5)

        if trading_account is None:
            return  # El usuario canceló la entrada

        if trading_account <= 0:
            self.show_error_messagebox("La cuenta de trading debe ser mayor que cero.")
            return

        leveragex = round(total_open_amount / trading_account, 2)  # Se calcula el apalancamiento actual

        # Cálculo de montos apalancados y reducción de posición
        leverage_levels = [2, 3, 4, 5, 6, 7, 8]
        leveraged_amounts = []
        reduce_positions = []

        for leverage in leverage_levels:
            amount = int(trading_account * leverage)
            leveraged_amounts.append(amount)
            reduce_usdt = int(amount - total_open_amount)
            reduce_positions.append(reduce_usdt)

        # Crear figura de Matplotlib y embeberla en Tkinter
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35
        x = range(len(leverage_levels))

        # Gráficos de barras
        bars1 = ax.bar(x, leveraged_amounts, width=bar_width, label='Leveraged Amount', color='blue', alpha=0.6)

        bars2 = ax.bar([i + bar_width for i in x], reduce_positions, width=bar_width,
                       label='Reduce Position USDT',
                       color=['red' if reduce <= 0 else 'forestgreen' for reduce in reduce_positions], alpha=0.6)

        # Añadir etiquetas sobre cada barra
        for bar1, bar2, leverage in zip(bars1, bars2, leverage_levels):
            ax.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(),
                    f"X {leverage}\n{bar1.get_height()} USDT",
                    ha='center', va='bottom', fontsize=9, weight='bold')

            ax.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(),
                    f"{bar2.get_height()} USDT",
                    ha='center', va='bottom', fontsize=9, weight='bold')

        # Etiquetas y título
        ax.set_xlabel('Leverage')
        ax.set_ylabel('Amount (USDT)')
        ax.set_title(
            f'TOTAL OPEN AMOUNT ---> {int(total_open_amount)} USDT\nTRADING ACCOUNT ---> {int(trading_account)} USDT\nLEVERAGE ---> {leveragex:.2f}  X')
        ax.set_xticks([i + bar_width / 2 for i in x])
        ax.set_xticklabels(leverage_levels)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        fig.tight_layout()

        # Toma la figura de Matplotlib (fig) y la "integra" en un widget de Tkinter (FigureCanvasTkAgg)
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        top.state('zoomed')  # Maximizar la ventana del gráfico

    def list_of_symbols_with_open_order_or_buy_limit(self):
        """
        Crea y devuelve una lista de símbolos de activos que tienen al menos
        una OPEN ORDER o una BUY LIMIT en sus datos (self.data).
        """
        list_symbol = []
        if not self.data:
            print("No hay activos guardados en la GUI!\n")
            return list_symbol  # Devuelve una lista vacía

        for symbol, data_asset in self.data.items():
            if 'open_orders' in data_asset and data_asset['open_orders'] or \
                    'buy_limits' in data_asset and data_asset['buy_limits']:
                list_symbol.append(symbol)
        return list_symbol

    def calculate_and_show_all_burning_prices(self):
        """Calcula y muestra el precio de quema de todos los activos
        (que contengan al mneos una OPNEN ORDER o BUY LIMIT)
        en un widget Treeview dentro del self.right_panel, con confirmación Sí/No."""

        def calculate_and_display():
            confirmed = self.show_confirmation_dialog(self, "Confirmación", "¿Has actualizado los MARGINS?")
            if confirmed:
                list_symbol = self.list_of_symbols_with_open_order_or_buy_limit()
                if not list_symbol:
                    self.show_info_messagebox(self, "Info",
                                              "No hay activos con órdenes para calcular el Burn Price.")
                    return

                # oculta un widget que ha sido gestionado por el layout manager 'pack'(en nuestro caso un frame)
                if hasattr(self, 'asset_info_frame'):
                    self.asset_info_frame.pack_forget()  # Si usas pack

                # Crear un label para el título de la tabla (de precios de quema)
                self.table_title = Label(self.burn_price_table_frame,
                                        text="B U R N   P R I C E S",
                                        font=('Arial', 18, 'bold'))
                self.table_title.pack()

                # Crear objeto de fuente con tamaño aumentado
                table_font = tkFont.Font(family="Arial", size=18, weight="bold")

                # crea una instancia de la clase Style del módulo tkinter.ttk
                style = ttk.Style()
                #style.theme_use('default')  # usar un tema para aplicar estilos('clam', 'alt', 'default', 'classic', etc)
                # Configurar un estilo personalizado para el widget 'Treeview'
                style.configure("Custom.Treeview", font=table_font, borderwidth=1, relief="solid", background="lightgray", bordercolor="green")  # "Custom.Treeview" es simplemente un nombre que elegimos para nuestro estilo personalizado

                tree = ttk.Treeview(self.burn_price_table_frame, columns=(
                    "Symbol", "Current Price", "Margin", "Open Orders Qty", "Buy Limits Qty", "Burn Price"),
                                    show="headings", style="Custom.Treeview")

                # Definir encabezados de las columnas
                tree.heading("Symbol", text="Símbolo")
                tree.heading("Current Price", text="Precio Actual")
                tree.heading("Margin", text="Margen (USDT)")
                tree.heading("Open Orders Qty", text="Cant. Órdenes Abiertas")
                tree.heading("Buy Limits Qty", text="Cant. Buy Limits")
                tree.heading("Burn Price", text="Precio de Quema (USDT)")

                # Ajustar el ancho de las columnas (opcional)
                tree.column("Symbol", width=80)
                tree.column("Current Price", width=120)
                tree.column("Margin", width=120)
                tree.column("Open Orders Qty", width=150)
                tree.column("Buy Limits Qty", width=150)
                tree.column("Burn Price", width=150)

                for symbol in list_symbol:
                    if symbol in self.data:
                        data_asset = self.data[symbol]
                        current_price = round(self.get_price(symbol), 3)
                        if current_price is not None:
                            margin = data_asset.get("margin", 0)
                            quantity_open_orders = sum(
                                order['quantity'] for order in data_asset.get('open_orders', []))
                            total_amount_buy_limits = sum(
                                order['amount_usdt'] for order in data_asset.get('buy_limits', []))
                            total_quantity_buy_limits = sum(
                                order['quantity'] for order in data_asset.get('buy_limits', []))
                            total_quantity = quantity_open_orders + total_quantity_buy_limits
                            burn_price = None

                            if total_quantity > 0:
                                burn_price = round(((
                                                            current_price * quantity_open_orders) + total_amount_buy_limits - margin) / total_quantity,
                                                   3)
                                # Redondear en cantidad de decimales, segun valor de total_quantity
                                if total_quantity < 1:
                                    quantity_open_orders = round(quantity_open_orders, 8)
                                    total_quantity_buy_limits = round(total_quantity_buy_limits, 8)
                                else:
                                    quantity_open_orders = round(quantity_open_orders, 3)
                                    total_quantity_buy_limits = round(total_quantity_buy_limits, 3)

                            tree.insert("", tk.END, values=(
                                symbol, current_price, margin, quantity_open_orders, total_quantity_buy_limits,
                                burn_price if burn_price is not None else "N/A"))
                        else:
                            tree.insert("", tk.END, values=(symbol, "N/A", "N/A", "N/A", "N/A", "N/A"))
                    else:
                        tree.insert("", tk.END, values=(symbol, "N/A", "N/A", "N/A", "N/A", "N/A"))

                tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        calculate_and_display()  # Llama directamente a la función interna

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
        """Calcula el precio de quema del activo seleccionado, obteniendo el precio actual de Binance.
        El cambio que hicimos con esta funcion es que ahora obtiene la cantidad total del activo en vez
        de calcular la cantidad de activo de la orden madre (ahora la orden madre no se considera la
        resultante de todas las ordenes abiertas sino las que el usuario desee unificar.
        Las ordenes NO madres, ahora no van a estar incluidas en la orden madre.)"""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            messagebox.showerror("Error", "Por favor, selecciona un activo primero.")
            return

        current_price = self.get_price(symbol)

        if current_price is not None:
            if symbol in self.data:
                data_asset = self.data[symbol]
                margin = data_asset.get("margin", 0)

                burn_price_message = f" BURN PRICE {symbol} ".center(60, '*') + "\n"
                burn_price_message += "Advertencia: tener actualizada las OPEN ORDERS y el MARGIN!\n\n"
                burn_price_message += f"CURRENT PRICE: {current_price}\n"
                burn_price_message += f"MARGIN: {margin} USDT\n\n"

                # bucle calcula cantidad total de activo, en ordenes abiertas
                quantity_open_orders = 0
                if 'open_orders' in data_asset:
                    for order in data_asset['open_orders']:
                        quantity_open_orders += order['quantity']

                if quantity_open_orders == 0:
                    burn_price_message += "No hay Ordenes Abiertas!\n"
                else:
                    burn_price_message += f"Cantidad OPEN ORDERS: {quantity_open_orders}\n"

                # bucle calcula cant.total y monto total de ordenes BUY LIMITS
                total_amount_buy_limits = 0
                total_quantity_buy_limits = 0
                if 'buy_limits' in data_asset and data_asset['buy_limits']:
                    for order in data_asset['buy_limits']:
                        total_amount_buy_limits += order['amount_usdt']
                        total_quantity_buy_limits += order['quantity']
                    burn_price_message += f"Total cantidad buy limits: {total_quantity_buy_limits}\n"
                    #burn_price_message += f"Total monto buy limits: {total_amount_buy_limits} USDT\n"
                else:
                    burn_price_message += "No hay BUY LIMITS!\n"

                total_quantity = quantity_open_orders + total_quantity_buy_limits
                if total_quantity == 0:
                    self.show_error_messagebox(self, "No se puede calcular BURN PRICE\n No existen OPEN ORDERS ni BUY LIMITS")

                else:
                    burn_price = ((current_price * quantity_open_orders) + total_amount_buy_limits - margin) / total_quantity
                    burn_price_message += f"\nBURN PRICE: {round(burn_price, 3)} USDT\n"
                    self.show_info_messagebox(self, "Resultado Burn Price", burn_price_message)  # se llama al metodo que encapsula la clase personalizada 'CustomInfoDialog'
                    #messagebox.showinfo("Resultado Burn Price", burn_price_message)

            else:
                self.show_error_messagebox(self, f"No se pudo obtener el precio actual de '{symbol}'.")
                #messagebox.showerror("Error", f"No se encontraron datos para el activo '{symbol}'.")
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

    def plot_open_orders_window(self, data_asset, current_price, active_symbol):
        """Genera y muestra el gráfico de órdenes abiertas para el activo seleccionado
        en una ventana Toplevel maximizada."""

        open_orders = data_asset.get('open_orders', [])

        if not open_orders:
            self.show_info_messagebox(self, "Información", f"No hay órdenes abiertas para '{active_symbol}'.")
            return

        mother_orders = [order for order in open_orders if order.get('mother_order', False)]  # Filtra las órdenes madre.
        non_mother_orders = [order for order in open_orders if not order.get('mother_order', False)]  # # Filtra las órdenes no madre.

        if len(mother_orders) > 1:
            self.show_error_messagebox(self, "Hay más de una orden madre. Solo se permite una.")
            return

        # --- DATOS orden madre --- (Inicializar en caso de que no haya órdenes madre)
        mother_order = None
        mother_profit = 0.0  # Inicializar a 0.0 para el cálculo del total profit
        mother_price = None
        mother_amount_usdt = None
        mother_percentage = None

        if mother_orders:
            mother_order = mother_orders[0]  # Acceder directamente al primer (y único) elemento

            # Accedemos directamente a las claves 'price' y 'amount_usdt'
            mother_price = mother_order['price']
            mother_amount_usdt = mother_order['amount_usdt']
            mother_percentage = (current_price - mother_price) / mother_price
            mother_profit = mother_amount_usdt * mother_percentage

        # --- DATOS ordenes NO madre ---
        non_mother_profits = []
        non_mother_prices = []
        non_mother_amounts_usdt = []
        non_mother_percentages = []
        if non_mother_orders:
            non_mother_prices = [order['price'] for order in non_mother_orders]
            non_mother_amounts_usdt = [order['amount_usdt'] for order in non_mother_orders]
            non_mother_percentages = [(current_price - price) / price for price in non_mother_prices]
            non_mother_profits = [amount_usdt * percentage for amount_usdt, percentage in
                                  zip(non_mother_amounts_usdt, non_mother_percentages)]

        total_non_mother_profits = round(sum(non_mother_profits), 2)

        # -- Figura Principal
        fig = plt.figure(figsize=(14, 6))  # Crea la figura principal para los subgráficos.
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])  # Define la estructura de la cuadrícula de subgráficos (1 fila, 2 columnas, ratios de ancho).
        ax1 = fig.add_subplot(gs[0])  # Añade el primer subgráfico (para la orden madre).
        ax2 = fig.add_subplot(gs[1])  # Añade el segundo subgráfico (para las órdenes no madre).

        # --- Subgráfico de la orden madre ---
        # Configuraciones comunes a ambos casos (haya o no mother_profit)
        ax1.set_xticks([1])
        ax1.set_xticklabels(['MOTHER ORDER'])
        ax1.set_ylabel('Profits USDT')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
        # ax1.set_title(f'MOTHER ORDER for {active_symbol}')

        # Establecer límites del eje X para centrar la marca
        ax1.set_xlim(0, 2)  # Asegura que la marca en x=1 esté centrada

        if mother_orders:  # Verificamos si existe al menos una orden madre para dibujar
            # Dibujamos una única barra. La posición en el eje x es [1] (ya que solo hay una orden madre)
            ax1.bar([1], [mother_profit], color=['red' if mother_profit <= 0 else 'forestgreen'])
            # Texto de la etiqueta
            ax1.text(1, mother_profit,
                     f"P: {mother_price}\nI: {mother_amount_usdt}\nPf: {round(mother_profit, 2)}\n{round(mother_percentage * 100, 2)}%",
                     ha='center', va='bottom', fontsize=10)
            # Límites del eje Y (de Mother Order)
            margen_porcentual = 0.6  # 60% de margen
            y_max = abs(mother_profit) * (1 + margen_porcentual)
            y_min = -y_max
            #print(f"y_min MO: {y_min}")
            #print(f"y_max MO: {y_max}")
            ax1.set_ylim(y_min, y_max)

            # Línea horizontal del beneficio (con etiqueta)
            ax1.axhline(y=round(mother_profit, 2), color='red' if mother_profit <= 0 else 'forestgreen',
                        linestyle='--', label=f'PROFIT: {round(mother_profit, 2)} USDT', alpha=0.7)
            ax1.legend(loc='upper right',
                       fontsize=10)  # <--- Llamada a la leyenda después de dibujar el elemento con etiqueta

        else:
            ax1.set_ylim(-50, 50)  # Valores predeterminados si no hay orden madre

        # --- Subgráfico de las órdenes NO madre ---
        ax2.set_xlabel('ORDERS NON MOTHER')
        ax2.set_ylabel('Profits USDT')

        # Configuraciones comunes a todos los casos para ax2
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)

        # --- Lógica para diferentes escenarios de órdenes no madre ---
        if non_mother_profits:
            # Genera una lista de números enteros que representan las posiciones de cada barra de las órdenes no madre en el eje x.
            x2 = list(range(1, len(non_mother_orders) + 1))
            ancho_barra = 0.8  # ajustar valor de (0 a 1)
            # Cada elemento de colors2 corresponde al color de la barra respectiva
            colors2 = ['red' if distance <= 0 else 'forestgreen' for distance in non_mother_profits]
            bars2 = ax2.bar(x2, non_mother_profits, color=colors2, width=ancho_barra)

            for bar, profit, percentage, price, amount_usdt in zip(bars2, non_mother_profits,
                                                                   non_mother_percentages,
                                                                   non_mother_prices, non_mother_amounts_usdt):
                yval = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2, yval,
                         f"P: {price}\nI: {int(amount_usdt)}\nPf: {round(yval, 2)}\n{round(percentage * 100, 2)}%",
                         ha='center', va='bottom', fontsize=10)
            ax2.set_xticks(x2)
            ax2.set_xticklabels(x2)

            ax2.axhline(y=total_non_mother_profits, color='red' if total_non_mother_profits <= 0 else 'forestgreen',
                        linestyle='--', label=f'TOTAL PROFIT OPEN ORDERS: {total_non_mother_profits} USDT',
                        alpha=0.7)

            # --- Crear y mostrar la leyenda ---
            handles = []
            labels = []
            # Handle y label para el total profit
            total_profit_color = 'red' if total_non_mother_profits <= 0 else 'forestgreen'
            profit_handle = plt.Line2D([0], [0], color=total_profit_color, linestyle='--')
            profit_label = f'TOTAL NON MOTHER PFOFIT: {total_non_mother_profits} USDT'
            handles.append(profit_handle)
            labels.append(profit_label)
            # Leyenda de abreviaturas
            legend_labels = {'P': 'Precio', 'I': 'Monto Inicial (USDT)', 'Pf': 'Beneficios (USDT)',
                             '%': 'Porcentaje'}
            for key, value in legend_labels.items():
                handle = plt.Rectangle((0, 0), 1, 1, color='black', ec='black')
                label = f"{key}: {value}"
                handles.append(handle)
                labels.append(label)
            ax2.legend(handles, labels, loc='upper right', fontsize=10)

            # Limites del eje Y para ordenes no-madre
            margen_porcentual_nmo = 0.1
            min_profit_non_mother = min(non_mother_profits)
            max_profit_non_mother = max(non_mother_profits)
            max_abs_profit_non_mother = max(abs(min_profit_non_mother), abs(max_profit_non_mother),
                                            abs(total_non_mother_profits))
            limite_superior_nm = max_abs_profit_non_mother * (1 + margen_porcentual_nmo)
            limite_inferior_nm = -limite_superior_nm
            ax2.set_ylim(limite_inferior_nm, limite_superior_nm)

        else:
            ax2.set_xticks([])
            ax2.set_ylim(-50, 50)  # Valores predeterminados si no hay órdenes no madre
            ax2.text(0.5, 0.5, "No Open Orders (Non-Mother)", ha='center', va='center', fontsize=14, color='blue',
                     weight='bold')

        # Añade un texto con el precio actual y el beneficio total a la figura.
        fig.text(0.22, 0.98, f'CURRENT PRICE {active_symbol}: {current_price}      TOTAL PROFIT: {round(mother_profit + total_non_mother_profits, 2)} USDT',
                 ha='center', fontsize=12, color='blue',
                 weight='bold')
        fig.tight_layout()

        top_level = tk.Toplevel(self)  # Crea una nueva ventana Toplevel (independiente) para el gráfico.
        top_level.title(f"Gráfico de Órdenes Abiertas para {active_symbol}")
        canvas = FigureCanvasTkAgg(fig, master=top_level)  # Integra la figura de Matplotlib en la ventana Tkinter.
        canvas_widget = canvas.get_tk_widget()  # Obtiene el widget de Tkinter que contiene el gráfico.
        canvas_widget.pack(fill=tk.BOTH, expand=True)  # Organiza el widget del gráfico para que se expanda y rellene la ventana.
        canvas.draw()  # Dibuja el gráfico en el canvas.
        top_level.state('zoomed')  # Maximiza la ventana Toplevel.

    def render_open_orders(self):
        """Obtiene los datos necesarios y llama a la función para mostrar el gráfico
        de ordenes abiertas del activo seleccionado, en una ventana maximizada."""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            return

        if symbol in self.data:
            data_asset = self.data[symbol]
            current_price = self.get_price(symbol)
            self.plot_open_orders_window(data_asset, current_price, symbol)
        else:
            self.show_error_messagebox(self, f"No se encontraron datos para el activo '{symbol}'.")

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
    # Crear una instancia de la clase de GUI
    gui = AssetManagerGUI(filename)

    # Iniciar el loop principal de Tkinter (mantiene la ventana abierta y responde a los eventos)
    gui.mainloop()





