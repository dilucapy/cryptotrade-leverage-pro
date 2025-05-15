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
import webbrowser
import os
from PIL import Image, ImageTk  # Importa Pillow para manejar imágenes
import pyperclip # Importa la librería pyperclip para el portapapeles
import smtplib  # Para enviar correos electrónicos
from email.mime.text import MIMEText



# ruta del archivo JSON
filename = 'assets_data.json'

""" Utilizar clases para gestionar el estado y la lógica de tu GUI es una práctica
 fundamental para construir aplicaciones más complejas y mantenibles:"""

# Colores para usar
mandarina_atomica = '#FEB285'
azul_palido = '#AACCEE'
burlywood = 'burlywood'
persian_pink = '#E887C5'


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

        self.message_label = tk.Label(self, text=message, font=("Arial", 12, "bold"), padx=30, pady=30)
        self.message_label.pack()

        self.ok_button = tk.Button(self,
                                   text="Aceptar",
                                   cursor='hand2',
                                   font=("Segoe UI", 12),
                                   padx=10, pady=5,
                                   command=self.destroy)
        self.ok_button.pack(pady=20)

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

        # Centrar la ventana después de que se haya creado el layout
        self.update_idletasks()  # Forzar la actualización del layout para obtener el tamaño real
        width = self.winfo_width()  # Obtener el ancho real de la ventana
        height = self.winfo_height()  # Obtener la altura real de la ventana
        screen_width = self.winfo_screenwidth()  # Obtener el ancho de la pantalla
        screen_height = self.winfo_screenheight()  # Obtener la altura de la pantalla
        x = (screen_width - width) // 2  # Calcular la coordenada x para centrar
        y = (screen_height - height) // 2   # Calcular la coordenada y para centrar
        self.geometry(f'+{x}+{y}')  # Establecer la posición de la ventana

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

        tk.Label(self, text=prompt, font=("Arial", 12, 'bold'), padx=40, pady=20).pack()

        self.entry = tk.Entry(self, font=("Arial", 12, 'bold'))
        if initialvalue is not None:
            self.entry.insert(0, initialvalue)
        self.entry.pack(padx=20, pady=5)
        self.entry.focus_set()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cancelar", cursor="hand2", font=("Segoe UI", 12), command=self.cancel, padx=10,
                  pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Aceptar", cursor="hand2", font=("Segoe UI", 12), command=self.ok, padx=10, pady=5).pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def ok(self):
        try:
            self.result = float(self.entry.get())
            self.destroy()
        except ValueError:
            self.master.show_error_messagebox(self.master, "Por favor, ingrese un número válido.")
            self.entry.focus_set()

    def cancel(self):
        self.destroy()


class CustomConfirmationDialogWithMotherOrder(tk.Toplevel):
    """Crea una ventana de diálogo de confirmación personalizada que pregunta
        al usuario con un mensaje y ofrece opciones de "Sí" y "No".
        Además, incluye una casilla de verificación para preguntar si la acción
        deseada debe guardarse como una "Orden Madre", devolviendo el estado
        de esta casilla.

        Hereda de tk.Toplevel.

        Atributos:
            result (bool o None): Almacena el resultado de la interacción del
                usuario (True para "Sí", False para "No", None si la ventana
                se cierra sin elegir).
            is_mother_order (tk.BooleanVar): Variable de Tkinter que almacena el
                estado de la casilla de verificación "Guardar como Orden Madre"
                (True si está marcada, False en caso contrario)."""
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.is_mother_order = tk.BooleanVar()  # Variable para la casilla de verificación

        # Casilla de verificación para orden madre
        style = ttk.Style()
        style.configure("Bold14.TCheckbutton", font=("Arial", 14, "bold"))
        check_madre = ttk.Checkbutton(self, text="Es Orden Madre?", style="Bold14.TCheckbutton", variable=self.is_mother_order)
        check_madre.pack(pady=5)

        # Mensaje del cuadro de dialogo
        tk.Label(self, text=message, font=("Arial", 14, "bold")).pack(padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Sí", cursor='hand2', width=15, font=("Segoe UI", 12), command=self.on_yes)
        yes_button.pack(side=tk.LEFT, padx=5)

        no_button = tk.Button(button_frame, text="No", cursor='hand2', width=15, font=("Segoe UI", 12), command=self.on_no)
        no_button.pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()

    def get_is_mother_order(self):
        return self.is_mother_order.get()


class PromediarOrdenesForm(tk.Toplevel):
    """Crea una ventana Toplevel para permitir al usuario ingresar múltiples
        órdenes (precio y monto) y calcular su precio promedio.
        Ofrece la opción de guardar el resultado como una nueva Orden Abierta,
        incluyendo la posibilidad de marcarla como orden madre."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Promediar Órdenes")
        self.geometry("460x260")  # Tamaño inicial
        self.resizable(False, False)
        self.parent = parent

        self.ordenes_data = []  # Lista para almacenar diccionarios de {'precio': Entry, 'monto': Entry}
        self.row_counter = 0

        # --- Botones del formulario ---
        add_button = tk.Button(self, text="+ Añadir Orden",
                               pady=5,
                               font=parent.button_font,  # estilos de botones del parent
                               cursor="hand2",
                               width=14,
                               command=self.add_new_order_row)
        add_button.grid(row=self.row_counter, column=0, pady=10, padx=5)

        promediar_button = tk.Button(self, text="Promediar",
                                     pady=5,
                                     font=parent.button_font,
                                     cursor="hand2",
                                     width=14,
                                     command=self.promediar_ordenes)
        promediar_button.grid(row=self.row_counter, column=1, pady=10, padx=5)

        cancelar_button = tk.Button(self, text="Cancelar",
                                    pady=5,
                                    font=parent.button_font,
                                    cursor="hand2",
                                    width=14,
                                    command=self.destroy)
        cancelar_button.grid(row=self.row_counter, column=2, pady=10, padx=5)
        self.row_counter += 1

        # --- Agregar etiquetas y campos de entradas para 2 ordenes
        self.add_order_row("Orden 1")
        self.add_order_row("Orden 2")

        self.transient(parent)  # Establece esta ventana como dependiente de la ventana parent, minimizándose o cerrándose con ella.
        self.grab_set()  # Captura todos los eventos de la aplicación, impidiendo la interacción con otras ventanas hasta que esta se cierre.
        parent.wait_window(self)  # Pausa la ejecución del código en la ventana parent hasta que esta ventana (self) sea cerrada.

    def add_order_row(self, label_text="Orden"):
        """Este metodo agrega una orden"""
        label = tk.Label(self, text=label_text,
                         font=("Arial", 12, "bold"))
        label.grid(row=self.row_counter, column=0, padx=5, pady=2, sticky="nsew")

        precio_label = tk.Label(self, text="Precio:",
                    font=("Arial", 12, "bold"))
        precio_label.grid(row=self.row_counter, column=1, padx=5, pady=2, sticky="w")
        precio_entry = tk.Entry(self, width=12, font=("Arial", 12, "bold"))
        precio_entry.grid(row=self.row_counter, column=2, padx=5, pady=2)

        monto_label = tk.Label(self, text="Monto USDT:",
                            font=("Arial", 12, "bold"))
        monto_label.grid(row=self.row_counter + 1, column=1, padx=5, pady=2, sticky="w")
        monto_entry = tk.Entry(self, width=12, font=("Arial", 12, "bold"))
        monto_entry.grid(row=self.row_counter + 1, column=2, padx=5, pady=2)

        self.ordenes_data.append({'precio': precio_entry, 'monto': monto_entry})
        self.row_counter += 2

    def add_new_order_row(self):
        order_number = len(self.ordenes_data) + 1
        self.add_order_row(f"Orden {order_number}")

        # Ajustar el tamaño de la ventana si es necesario
        self.geometry(f"460x{260 + (len(self.ordenes_data) - 2) * 50}")  # Ajuste aproximado

    def promediar_ordenes(self):
        order_values = []
        for data in self.ordenes_data:
            precio_str = data['precio'].get()
            monto_str = data['monto'].get()
            try:
                precio = float(precio_str)
                if precio < 0:
                    self.parent.show_error_messagebox(self.parent,  "El precio NO puede ser negativo!")
                    return
                monto_usdt = float(monto_str)
                if monto_usdt < 0:
                    self.parent.show_error_messagebox(self.parent,  "El monto NO puede ser negativo!")
                    return
                order_values.append({'precio': precio, 'monto_usdt': monto_usdt})
            except ValueError:
                self.parent.show_error_messagebox(self.parent, "Por favor, ingrese valores numéricos válidos para todos los precios y montos.")
                return

        if not order_values:
            return

        total_usdt = sum(order['monto_usdt'] for order in order_values)
        print(f"Total usdt {total_usdt}")

        # Calculamos cantidad total de activo
        cantidad_total_activo = 0
        for order in order_values:
            if order['precio'] != 0:
                cantidad_total_activo += order['monto_usdt'] / order['precio']
            else:
                self.parent.show_error_messagebox(self.parent,
                                                  "El precio de una de las órdenes es cero,\nno se puede calcular la cantidad.")
                return

        # Calculamos precio promedio
        precio_promedio = 0
        if cantidad_total_activo != 0:
            precio_promedio = round(total_usdt / cantidad_total_activo, 5)
        else:
            self.parent.show_error_messagebox(self.parent, "La cantidad total de activo es cero,\n no se puede calcular el precio promedio.")
            return

        print(f"Precio Promedio: {precio_promedio}")

        active_symbol = self.parent.selected_asset.get()  # Asegúrate de que 'selected_asset' esté accesible
        if active_symbol == "BTC":
            cantidad_promedio = round(cantidad_total_activo, 8)
        else:
            cantidad_promedio = round(cantidad_total_activo, 4)

        # llamamos a nuestro metodo personalizado de dialogo de confirmacion con casilla de verificacion
        guardar, is_mother_order = self.parent.show_confirmation_dialog_with_mother_order(self.parent, "Guardar Orden Promedio",
            f"Precio Promedio: {precio_promedio:.5f}\nMonto: {total_usdt:.2f} USDT\nCantidad: {cantidad_promedio}\n\n¿Desea guardarla en Ordenes Abierta?")

        if guardar:
            active_symbol = self.parent.selected_asset.get()
            if active_symbol in self.parent.data and is_mother_order:
                ordenes_actualizadas = []
                if "open_orders" in self.parent.data[active_symbol]:
                    for order in self.parent.data[active_symbol]["open_orders"]:
                        if order.get("mother_order"):
                            self.parent.show_info_messagebox(self.parent, "Advertencia",
                                                f"Se sobreescribirá la orden madre existente para {active_symbol}")
                        else:
                            ordenes_actualizadas.append(order)
                    self.parent.data[active_symbol]["open_orders"] = ordenes_actualizadas

            if active_symbol in self.parent.data:
                new_order = {
                    "id": str(uuid.uuid4()),
                    "type": "open",
                    "price": precio_promedio,
                    "amount_usdt": total_usdt,
                    "quantity": cantidad_promedio,
                    "stop_loss": None,
                    "target": None,
                    "mother_order": is_mother_order
                }
                if "open_orders" not in self.parent.data[active_symbol]:
                    self.parent.data[active_symbol]["open_orders"] = []
                self.parent.data[active_symbol]["open_orders"].append(new_order)
                self.parent.save_data_asset(self.parent.data, self.parent.data[active_symbol], active_symbol)
                self.parent.create_asset_orders_section()
                # Informa con un cuadro de dialogo
                self.parent.show_info_messagebox(self.parent, "Orden Guardada", "La orden promedio ha sido guardada en órdenes abiertas.")

            else:
                self.parent.show_error_messagebox(self.parent, f"No se encontraron datos para el activo: {active_symbol}")

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
        self.config(bg='#D5A572')  # Establece el color de background.


        # Configuración para la selección única de botones de activo
        self.selected_asset = tk.StringVar()  # Almacena el símbolo del activo actualmente seleccionado
        self.active_asset_button = None  # Para rastrear el botón activo
        self.default_button_bg = 'azure4'  # Color de fondo por defecto
        self.selected_button_bg = '#0CCE6B'  # Color de fondo cuando está seleccionado (esmeralada, tonalidad de verde)

        self.selected_asset_data = None  # Inicialización de self.selected_asset_data
        self.new_order_data = None  # Para almacenar los datos del formulario

        # Crear los widgets de la GUI
        self.create_widgets()

        # Estilos de apariencia para toplevel y button
        self.toplevel_bgcolor = "#AED5CB"  # (Tonalidad celeste) Color de fondo predeterminado para las ventanas emergentes (Toplevel)
        self.button_font = ("Segoe UI", 12)  # Fuente predeterminada para el texto de los botones (familia, tamaño)
        self.button_bgcolor = "lightgreen"  # Color de fondo predeterminado para los botones
        self.button_relief = tk.FLAT  # Estilo de relieve predeterminado para los botones (sin efecto 3D)

        # Diccionario para almacenar direcciones y rutas de QR
        self.crypto_info = {
            "Bitcoin (BTC)": {"address": "34G4JhdkiP9zKo5fbKS96YJSkLc7bXY5dH", "qr_path": "images/qr_btc.png"},
            "Ethereum (ETH)": {"address": "0xa19deb3582c3e99f06637b0aad47c8034ada0874", "qr_path": "images/qr_eth.png"},
            "USDT (Tether)": {"address": "0x3c332e33e0399aea38c3e393781ecff04226e8bf", "qr_path": "images/qr_usdt.png"},
            "Litecoin (LTC)": {"address": "MSbwoT48KJDoA1JQaaAVerXDJdXps6f6Nj", "qr_path": "images/qr_ltc.png"},
            "Solana (SOL)": {"address": "3ezjYS8M5ySPixm2N46qFPbTM9BuJi1w1rWpvXz28QDJ", "qr_path": "images/qr_sol.png"},
            "Argentine Peso (ARS)": {"address": "gustavo.dilu", "qr_path": None}
        }
        self.developer_email = "dilucapython@gmail.com"  # correo del desarrollador
        self.qr_image_tk = None  # Para evitar que la imagen sea garbage collected

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
            self.show_error_messagebox(self, f"El archivo {filename} no tiene un formato JSON válido.")
            return {}
        except Exception as e:
            self.show_error_messagebox(self, f"Ocurrió un error al cargar {filename}: {e}")
            return {}

    def order_orders(self, data):
        """Ordena todas las órdenes, en base a su precio"""
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

            # Ordenar Ventas Take Profit
            data_asset['sell_take_profit'] = sorted(data_asset['sell_take_profit'], key=lambda x: x['price'])

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

    def show_confirmation_dialog_with_mother_order(self, parent, titulo, mensaje):
        """Este metodo llama a la clase que personaliza la ventana de confirmacion
        con la opcion de guardar como orden madre y devuelve una tupla con
        (decision_si_no, es_orden_madre)"""
        dialog = CustomConfirmationDialogWithMotherOrder(parent, titulo, mensaje)
        return dialog.result, dialog.get_is_mother_order()

    def create_widgets(self):
        """Este método crea todos los widgets de la GUI
        (paneles, etiquetas, menús, botones) y los organiza utilizando .pack()"""
        # Panel Superior (para etiqueta de titulo y Panel de activos)
        self.top_panel = Frame(self.master, bd=1, relief=FLAT, bg='burlywood')
        self.top_panel.pack(side=TOP, fill=X)

        # Panel fila superior (dentro de top panel)
        self.top_row_frame = Frame(self.top_panel, bd=0, bg='burlywood')
        self.top_row_frame.grid(row=0, column=0, columnspan=1, sticky="ew")

        self.title_label = Label(self.top_row_frame, text='Herramienta de Gestión de Operaciones Apalancadas de Criptomonedas', fg='#333333', font=('Dosis', 16, 'bold'), bg='burlywood', width=59)
        self.title_label.grid(row=0, column=0, columnspan=5, pady=5, sticky="w")
        # label Codigo de invitacion de quantfury
        label_invitacion= tk.Label(self.top_row_frame, text="Código Invitacion Quantfury:", font=('Dosis', 12, 'bold'), anchor='w',
                                   bg='#000a1d', fg='#00cdc3')
        label_invitacion.grid(row=0, column=5, columnspan=3, sticky="wns", pady=15, padx=(1, 0))

        # Codigo de Invitacion en un Entry (copiable)
        invitacion_entry = tk.Entry(self.top_row_frame)
        invitacion_entry.insert(0, "U23853V6")
        invitacion_entry.config(state='readonly', font=('Dosis', 12, 'bold'), width=10)
        invitacion_entry.grid(row=0, column=8, sticky="ns", pady=15)

        # Botón para Copiar codigo de invitacion
        #self.copiar_icono = None  # Placeholder para el icono
        def copiar_al_portapapeles(widget_entry):
            codigo_invitacion = widget_entry.get()
            self.clipboard_clear()
            self.clipboard_append(codigo_invitacion)
            self.update()  # Es necesario para que el portapapeles se actualice inmediatamente
            print("Código de invitación copiado al portapapeles!")

            # animacion del boton copiar
            original_text = self.boton_copiar.cget("text")
            original_fg = self.boton_copiar.cget("fg")  # Guarda el color de texto original
            original_bg = self.boton_copiar.cget("bg")  # Guarda el color de bg original
            self.boton_copiar.config(text="Ok", state="disabled", fg="red", bg='white')
            self.after(1000, lambda: self.boton_copiar.config(state="normal",
                                                              text=original_text,
                                                              fg=original_fg,
                                                              bg=original_bg))

        self.boton_copiar = tk.Button(self.top_row_frame,
                                      text="Copiar",
                                      font=('Dosis', 12, 'bold'),
                                      padx=3,
                                      pady=3,
                                      width=6,
                                      bg='#000a1d',
                                      fg='#00cdc3',
                                      bd=1,
                                      relief=RAISED,
                                      cursor='hand2',
                                      command=lambda: copiar_al_portapapeles(invitacion_entry))

        self.boton_copiar.grid(row=0, column=9, sticky="w")

        # Boton quantfury (con imagen), dirige a la web
        try:
            self.quantfury_imagen = tk.PhotoImage(file='images/image_quantfury.png')
            self.boton_quantfury = tk.Button(self.top_row_frame,
                                             image=self.quantfury_imagen,
                                             padx=3,
                                             pady=3,
                                             bg=self.default_button_bg,
                                             bd=1,
                                             relief=tk.RAISED,
                                             cursor='hand2',
                                             command=self.open_quantfury)
            self.boton_quantfury.grid(row=0, column=10, sticky="w", padx=(16, 0))
        except tk.TclError as e:
            print(f"Error al cargar la imagen: {e}")
            # Si la imagen no se carga, puedes mostrar un texto alternativo
            self.boton_quantfury = tk.Button(self.top_row_frame,
                                             text="Ir a Quantfury",
                                             font=('Dosis', 12, 'bold'),
                                             padx=5,
                                             pady=5,
                                             width=10,
                                             bg=self.default_button_bg,
                                             fg='white',
                                             bd=1,
                                             relief=tk.RAISED,
                                             cursor='hand2',
                                             command=self.open_quantfury)
            self.boton_quantfury.grid(row=0, column=10, sticky="ew", padx=(20, 0))

        # Panel de menu de Activos (para los botones de activos, dentro de top panel)
        self.asset_menu_frame = Frame(self.top_panel, bd=1, relief=FLAT, bg='burlywood')
        self.asset_menu_frame.grid(row=1, column=0, columnspan=1, padx=10, pady=10,
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
            {"text": "+ Nuevo Símbolo ", "command": self.add_new_symbol},
            {"text": "Mostrar MARGENES", "command": self.show_margins},
            {"text": "Actualizar MARGENES", "command": self.update_margins},
            {"text": "Ver Posiciones Abiertas", "command": self.show_open_positions},
            {"text": "Apalancamiento", "command": self.calculate_leverage},
            {"text": "Precios de Liquidación", "command": self.calculate_and_show_all_burning_prices},
            {"text": "Donación al Proyecto", "command": self.open_donation_window},
            {"text": "Salir", "command": self.quit}
        ]
        for config in primary_buttons_config:
            button = Button(self.primary_menu, text=config["text"], font=('Dosis', 12, 'bold'), bd=1, fg='white', bg='azure4', width=24, relief=RAISED, pady=10, cursor='hand2', command=config["command"])
            button.pack(pady=4, fill=X)

    def get_symbols_for_buttons(self):
        """Crea una lista de los símbolos de los activos que se encuentran en self.data
        para crear los botones en el panel asset_menu."""
        list_symbol = list(self.data.keys())
        return list_symbol

    def create_asset_buttons(self):
        """Crea los botones de los activos en el top_panel."""
        list_symbols = self.get_symbols_for_buttons()
        row = 1
        column = 0
        num_columns = 10
        for symbol in list_symbols:
            button = Button(self.asset_menu_frame,
                            text=symbol,
                            font=('Dosis', 16, 'bold'),
                            padx=5,
                            pady=5,
                            width=8,
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
        add_symbol_window.config(bg=self.toplevel_bgcolor)
        add_symbol_window.geometry('340x200')
        add_symbol_window.title("Agregar Nuevo Símbolo")

        symbol_label = Label(add_symbol_window, text="Nuevo Símbolo:",
                             bg=self.toplevel_bgcolor,
                             font=("Arial", 12, "bold"))

        symbol_label.pack(padx=10, pady=5)

        symbol_entry = Entry(add_symbol_window, font=("Arial", 12, "bold"), width=10)
        symbol_entry.pack(padx=10, pady=5)
        symbol_entry.focus_set()  # Enfocar el campo de entrada al abrir la ventana

        def save_new_symbol():
            new_symbol = symbol_entry.get().strip().upper()
            if new_symbol:
                if new_symbol in self.data:
                    self.show_error_messagebox(self, f"El símbolo '{new_symbol}' ya existe.")

                else:
                    self.data[new_symbol] = {
                        "margin": 0,
                        "open_orders": [],
                        "buy_limits": [],
                        "sell_take_profit": []
                    }
                    self.save_data()  # Guarda todos los datos, incluyendo el nuevo símbolo
                    self.create_asset_buttons()  # Actualiza los botones de activos en el 'top panel'
                    self.show_info_messagebox(self, "Éxito", f"Símbolo '{new_symbol}' agregado.")
                    add_symbol_window.destroy()  # llama al metodo para destruir la instacia de toplevel
            else:
                self.show_error_messagebox(self, "Por favor, introduce un símbolo.")


        save_button = Button(add_symbol_window, text="Guardar Símbolo",
                             pady=5,
                             font=self.button_font,
                             cursor="hand2",
                             command=save_new_symbol)
        save_button.pack(pady=10)

        cancel_button = Button(add_symbol_window, text="Cancelar",
                               pady=5,
                               font=self.button_font,
                               cursor="hand2",
                               command=add_symbol_window.destroy)
        cancel_button.pack(pady=5)

    def show_margins(self):
        """Muestra los márgenes individuales de cada activo y el total en un cuadro de diálogo,
        ordenados por margen de mayor a menor."""
        total_margin = 0
        asset_margins = []
        margins_report = "  SIMBOLO         MARGEN (USDT)   PONDERACION\n"
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

            margins_report += f"{symbol:<17}      {margin:<18.2f}          {ponderacion:<10}\n"

        margins_report += f"\n\n  MARGEN TOTAL: {int(total_margin)} USDT"

        self.show_info_messagebox(self, "Margen por activo y Margen Total", margins_report)

    def ask_trading_account(self, parent):
        """Método que muestra la ventana de diálogo personalizado
        para pedir al usuario que ingrese el monto de cuenta de trading."""
        dialog = CustomAskFloatDialog(parent,
                                      title="Monto Cuenta de Trading",
                                      prompt="Ingrese Monto Cuenta de Trading:")
        if dialog.result is None:
            return
        elif dialog.result == 0:
            self.show_error_messagebox(self, "El monto de la cuenta de trading debe ser mayor que cero.")
        elif dialog.result < 0:
            self.show_error_messagebox(self, "Monto de Cuenta de Trading, no puede ser negativo!")
            return
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

    def calculate_weighted_margin_form(self):
        """Muestra un formulario para ingresar los montos de posición abierta
        de cada activo y calcula los márgenes ponderados."""

        top_weighted_form = tk.Toplevel(self)
        top_weighted_form.title("Ponderación Manual")
        top_weighted_form.config(bg=self.toplevel_bgcolor)
        top_weighted_form.geometry('500x370')

        row = 0
        # Frame para etiqueta de sugerencia
        suggestion_frame = tk.Frame(top_weighted_form)
        suggestion_frame.grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        # etiqueta de sugerencia
        label = tk.Label(suggestion_frame,
                         text="Sugerencia:\nCalcular Ponderaciones en base a la posicion abierta de cada activo",
                         bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "italic"), justify="left", pady=5)
        label.grid()


        # Etiqueta para el monto total de la cuenta de trading
        label = tk.Label(top_weighted_form,
                         text="Monto Cuenta de Trading (USDT):",
                         bg=self.toplevel_bgcolor,
                         font=("Arial", 11, "bold"))
        label.grid(row=row, column=0, padx=5, pady=10, sticky="e")

        entry_trading_account = tk.Entry(top_weighted_form, font=("Arial", 12, "bold"))
        entry_trading_account.grid(row=row, column=1, padx=(5, 140), pady=(5, 20), sticky="ew")
        row += 1

        # Etiquetas y campos de entrada para cada activo
        entry_amounts = {}
        for symbol in self.data:
            label_asset = tk.Label(top_weighted_form,
                                   text=f"{symbol}:",
                                   bg=self.toplevel_bgcolor,
                                   font=("Arial", 11, "bold"))
            label_asset.grid(row=row, column=0, padx=5, pady=10, sticky="e")
            entry = tk.Entry(top_weighted_form, font=("Arial", 12, "bold"))
            entry.grid(row=row, column=1, padx=(5, 140), pady=10, sticky="ew")
            entry_amounts[symbol] = entry
            row += 1

        def calculate_and_show():
            trading_account_str = entry_trading_account.get()
            try:
                trading_account = float(trading_account_str)  # Intenta convertir a float
            except ValueError:
                self.show_error_messagebox(self, "Por favor, ingrese un número válido para la Cuenta de Trading.")
                top_weighted_form.destroy()
                return  # Sale de la función si la conversión falla

            if trading_account is None:
                return  # El usuario canceló, no hay nada que calcular ni mostrar
            elif trading_account == 0:
                self.show_error_messagebox(self, "La cuenta de Trading debe ser mayor a cero!")
                top_weighted_form.destroy()
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
                    self.show_error_messagebox(self, f"Por favor, ingrese un número válido para la posición abierta de {symbol}.")
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
                self.show_error_messagebox(self, "El total de las posiciones abiertas debe ser mayor que cero.")

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
        calculate_button.pack(side=tk.LEFT, padx=10, pady=20)

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

    def calculate_weighted_automatic_margin_form(self):
        trading_account = self.ask_trading_account(self)

        if trading_account is not None and trading_account > 0:

            total_open_amount, list_symbol, list_amount = self.calculate_total_open_amount()

            if not list_amount:
                self.show_info_messagebox(self, "Información",
                                          "No hay órdenes abiertas guardadas para mostrar los montos.")
                return 0  # Devuelve 0 si no hay datos

            report = "  Symbol        MARGIN (USDT)   Weight Automatic\n"
            report += "  " + "-" * 80 + "\n"

            for symbol, amount in zip(list_symbol, list_amount):
                weight_automatic = round(amount / total_open_amount, 3)
                margin_automatic = round(trading_account * weight_automatic)

                self.data[symbol]['margin'] = margin_automatic
                report += f"  {symbol:<13}      {margin_automatic:<19.2f}         {weight_automatic:<10}\n"

            self.show_info_messagebox(self, "Márgenes Actualizados (Ponderacion Automática)", report)
            self.save_data()

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

    def _calculate_weighted_automatic_form_and_destroy_window(self, selection_window):
        self.calculate_weighted_automatic_margin_form()
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
        top.geometry('420x300')
        top.title("Actualizar Márgenes de Activos")

        # Se crea un widget Label de Tkinter para mostrar texto al usuario.
        label = tk.Label(top, text="Elige una opción para calcular los márgenes:",
                         bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold"))
        label.pack(pady=20, padx=10)

        equitable_button = tk.Button(top,
                                     text="Margenes Equitativo",
                                     pady=5,
                                     font=self.button_font,
                                     cursor="hand2",
                                     command=lambda: self._calculate_equitable_and_destroy_window(top))
        equitable_button.pack(fill='x', pady=5, padx=60)

        weighted_button = tk.Button(top,
                                    text="Margenes Ponderación manual",
                                    pady=5,
                                    font=self.button_font,
                                    cursor="hand2",
                                    command=lambda: self._calculate_weighted_form_and_destroy_window(top))
        weighted_button.pack(fill='x', pady=5, padx=60)

        automatic_weighting_button = tk.Button(top,
                                    text="Margenes Ponderación Automática",
                                    pady=5,
                                    font=self.button_font,
                                    cursor="hand2",
                                    command=lambda: self._calculate_weighted_automatic_form_and_destroy_window(top))
        automatic_weighting_button.pack(fill='x', pady=5, padx=60)

        label = tk.Label(top, text="(RECOMENDADO)",
                         bg=self.toplevel_bgcolor,
                         font=("Arial", 9, "italic"))
        label.pack()

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
        """Muestra los montos totales por activo de todas
        las órdenes abiertas en un gráfico de barras."""

        total_open_amount, list_symbol, list_amount = self.calculate_total_open_amount()

        if not list_amount:
            self.show_info_messagebox(self, "Información", "No hay órdenes abiertas guardadas para mostrar los montos.")
            return 0  # Devuelve 0 si no hay datos

        # Se crea una lista, con tuplas creadas con zip (symbol, monto), por el segundo elemento (monto), de menor a mayor.
        sorted_data = sorted(zip(list_symbol, list_amount), key=lambda x: x[1])
        sorted_symbols, sorted_amounts = zip(*sorted_data)  # el asterisco que precede a sorted_data tiene la función de desempaquetar la lista

        # Crear gráfico
        plt.figure(figsize=(10, 6))
        bar_width = 0.35
        x = range(len(sorted_amounts))

        # Gráficos de barras
        bars_amounts = plt.bar(x, sorted_amounts, width=bar_width, label='Monto por Activo (USDT)', color='orange', alpha=0.7)

        # Añadir etiquetas sobre cada barra
        for bar in bars_amounts:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     f"{bar.get_height()} USDT",
                     ha='center', va='bottom', fontsize=11, weight='bold')

        # Etiquetas y título
        plt.xlabel('A C T I V O S')
        plt.ylabel('U S D T')
        plt.title(f'MONTO TOTAL ABIERTO: {total_open_amount} USDT', ha='center', weight='bold')

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

        if trading_account is None:
            return  # El usuario canceló la entrada

        top = tk.Toplevel(self)
        top.title("Calcular Apalancamiento")

        label = tk.Label(top, text="Monto apalancado y reducción de posición por nivel de apalancamiento",
                         font=('Arial', 12, 'bold'))
        label.pack(pady=5)

        if trading_account <= 0:
            self.show_error_messagebox(self, "La cuenta de trading debe ser mayor que cero.")
            return

        leveragex = round(total_open_amount / trading_account, 2)  # Se calcula el apalancamiento actual

        # Cálculo de montos apalancados y reducción de posición
        leverage_levels = [2, 3, 4, 5, 6, 7, 8, 9, 10]
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
        bars1 = ax.bar(x, leveraged_amounts, width=bar_width, label='Monto apalancado', color='blue', alpha=0.6)

        bars2 = ax.bar([i + bar_width for i in x], reduce_positions, width=bar_width,
                       label='Reducir posición USDT',
                       color=['red' if reduce <= 0 else 'forestgreen' for reduce in reduce_positions], alpha=0.6)

        # Añadir etiquetas sobre cada barra
        for bar1, bar2, leverage in zip(bars1, bars2, leverage_levels):
            ax.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(),
                    f"X {leverage}\n{bar1.get_height()} USDT",
                    ha='center', va='bottom', fontsize=9, weight='bold')

            ax.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(),
                    f"{bar2.get_height()} USDT",
                    ha='center', va='bottom', fontsize=9, weight='bold')

        # Añadir línea vertical para el apalancamiento actual
        ax.axvline(x=leveragex - 2, color='orange', linestyle='-', linewidth=2,
                   label=f'Apalancamiento Actual: {leveragex:.2f} X')  # Ajusta la posición x

        # Etiquetas y título
        ax.set_xlabel('N I V E L   D E   A P A L A N C A M I E N T O')
        ax.set_ylabel('M O N T O  (USDT)')
        ax.set_title(
            f'MONT0 TOTAL ABIERTO: {int(total_open_amount)} USDT\nCUENTA DE TRADING: {int(trading_account)} USDT\nAPALANCAMIENTO: {leveragex:.2f}  X')
        ax.set_xticks([i + bar_width / 2 for i in x])
        ax.set_xticklabels(leverage_levels)
        # Añadir un elemento de leyenda personalizado
        ax.plot([], [], color='forestgreen', marker='_', markersize=3,
                label='Monto disponible', linewidth=6, alpha=0.6)
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
        """Crea y devuelve una lista de símbolos de activos que tienen al menos
        una OPEN ORDER o una BUY LIMIT en sus datos (self.data)."""
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

                # Eliminar la tabla anterior si existe
                for widget in self.burn_price_table_frame.winfo_children():
                    widget.destroy()

                # Crear un label para el título de la tabla (de precios de quema)
                self.table_title = Label(self.burn_price_table_frame,
                                        text="P R E C I O S    D E    L I Q U I D A C I O N",
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
                tree.heading("Current Price", text="Precio Actual (USDT)")
                tree.heading("Margin", text="Margen (USDT)")
                tree.heading("Open Orders Qty", text="Total Cantidad (Open Orders)")
                tree.heading("Buy Limits Qty", text="Total Cantidad (Buy Limits)")
                tree.heading("Burn Price", text="Precio Liquidación (USDT)")

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

            info_text = f"Símbolo: {symbol}"

            if current_price is None:
                print(f"No se pudo obtener el precio actual de '{symbol}'")
                self.info_label.config(text="Error al obtener el precio.")  # Informar del error en la GUI
                return  # Salir de la función
            else:
                info_text += f"           Precio actual: {current_price}"

            if 'margin' in self.selected_asset_data:
                margin = self.selected_asset_data['margin']
                info_text += f"           Margin: {margin}"
            else:
                info_text += "           Margin: No disponible"

            # Calcular cantidad total de activo en pocisiones abiertas
            total_quantity = 0
            for order in self.selected_asset_data['open_orders']:
                quantity = order.get('quantity', 0)
                total_quantity += quantity

            # Redondear cantidad segun sea el activo seleccionado
            if symbol == 'BTC':
                total_quantity_rounded = round(total_quantity, 8)
            else:
                total_quantity_rounded = round(total_quantity, 4)

            info_text += f"           Cantidad: {total_quantity_rounded}"
            info_text += f"           Posicion Abierta: {int(total_quantity * current_price)} USDT"

            self.info_label.config(text=info_text, bg='#0CCE6B', pady=10)
            self.asset_info_frame.config(bg='#0CCE6B')  # establecemos bg (verde emeralda) al asset_info_label_frame

        else:
            self.info_label.config(text="Seleccione un activo para ver su información.")

    def create_asset_info_section(self):
        """Crea y configura la sección de la GUI donde se muestra la información detallada de un activo seleccionado.

        Esta sección se compone de un frame contenedor (`self.asset_info_frame`)
        y una etiqueta de texto (`self.info_label`) que se actualiza
        dinámicamente para mostrar el símbolo, precio, margen y otra información relevante del activo

        El frame se empaqueta dentro del panel derecho (`self.right_panel`) y se expande horizontalmente
        para ocupar todo el ancho disponible.
        Inicialmente, la etiqueta muestra un mensaje informativo indicando al usuario que seleccione un activo.

        Finalmente, se llama al método `self.update_asset_info_display()` para poblar la etiqueta
        con la información del activo actualmente seleccionado (si hay alguno).
        """
        # asset_info_frame (contiene información del activo como símbolo, precio y margin)
        self.asset_info_frame = Frame(self.right_panel)  # Empaquetar este frame en right_panel
        self.asset_info_frame.pack(pady=5, fill=X)

        self.info_label = Label(self.asset_info_frame,  # Etiqueta que se actualiza dinamicamente
                                text="Seleccione un activo para ver su información.",
                                font=('Arial', 12, 'bold'), anchor="center", pady=5)
        self.info_label.pack()

        self.update_asset_info_display()  # llama a este metodo que actualiza la info en el label del activo seleccionado

    def add_new_order(self, data_asset, active_symbol, order_type, order_details):
        """Agrega una nueva orden del tipo especificado a los datos del activo."""

        # Redondear cantidad segun sea el activo seleccionado
        if active_symbol == 'BTC':
            quantity_rounded = round(order_details.get('amount_usdt', 0) / order_details.get('price', 1),
                              8) if order_details.get('price', 1) != 0 else 0
        else:
            quantity_rounded = round(order_details.get('amount_usdt', 0) / order_details.get('price', 1),
                              4) if order_details.get('price', 1) != 0 else 0

        order = {
            'id': order_details.get('id'),
            'price': round(order_details.get('price'), 4),
            'amount_usdt': round(order_details.get('amount_usdt'), 2),
            'quantity': quantity_rounded
        }

        if order_type == 'open':
            is_mother = order_details.get('mother_order', False)
            order['mother_order'] = is_mother
            order['stop_loss'] = order_details.get('stop_loss')
            order['target'] = order_details.get('target')
            if 'open_orders' not in data_asset:
                data_asset['open_orders'] = []

            if is_mother:
                # verificar si existe una 'orden madre' en 'open_orders'
                existing_mother_order = None
                for existing_order in data_asset['open_orders']:
                    if existing_order.get('mother_order', False):
                        existing_mother_order = existing_order
                        break

                # si existe una 'orden madre', mostrar un dialogo de confirmacion para avisar y confirmar sobreescritura
                if existing_mother_order:
                    response = self.show_confirmation_dialog(self, "Confirmación", "Ya existe una orden madre\n¿Desea sobreescribirla?")
                    if response:
                        # Eliminar la orden madre existente
                        data_asset['open_orders'] = [
                            o for o in data_asset['open_orders'] if not o.get('mother_order', False)
                        ]
                        print("Orden madre existente sobreescrita y nueva orden abierta agregada!")
                    else:
                        print("Nueva orden madre no agregada.")

                else:
                    print("Nueva orden madre agregada!")
            else:
                print("Nueva orden abierta agregada!")

            data_asset['open_orders'].append(order)
            print("Orden abierta agregada!")
            # Ordenar ordenes abiertas por precio
            data_asset['open_orders'] = sorted(data_asset['open_orders'], key=lambda x: x['price'])

        elif order_type == 'pending_buy':
            order['stop_loss'] = order_details.get('stop_loss')
            order['target'] = order_details.get('target')
            if 'buy_limits' not in data_asset:
                data_asset['buy_limits'] = []
            data_asset['buy_limits'].append(order)
            print("Orden de compra pendiente agregada!")
            # Ordenar compras pendientes por precio
            data_asset['buy_limits'] = sorted(data_asset['buy_limits'], key=lambda x: x['price'])

        elif order_type == 'sell_take_profit':
            if 'sell_take_profit' not in data_asset:
                data_asset['sell_take_profit'] = []
            data_asset['sell_take_profit'].append(order)
            print("Orden de venta de toma de ganancia agregada!")
            # Ordenar Ventas Take Profit
            data_asset['sell_take_profit'] = sorted(data_asset['sell_take_profit'], key=lambda x: x['price'])

        else:
            print(f"Tipo de orden '{order_type}' no válido.")
            return data_asset  # # Devuelve data_asset sin modificar si el tipo no es válido

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
        """Toma la información de la nueva orden recopilada del formulario
        (almacenada en self.new_order_data) y la agrega a la estructura
        de datos para el activo seleccionado. Luego, actualiza la
        visualización de las órdenes."""
        # Obtiene el símbolo del activo que actualmente está seleccionado en la interfaz.
        active_symbol = self.selected_asset.get()

        # Verifica si hay un símbolo de activo seleccionado en 'self.selected_asset'
        # y si se han recopilado datos de la nueva orden en el atributo 'self.new_order_data'.
        if active_symbol in self.data and self.new_order_data:
            # Si ambas condiciones son verdaderas, procede a agregar la nueva orden.
            # Llama al método 'self.add_new_order', pasando:
            #   - Los datos actuales del activo seleccionado ('self.data[active_symbol]').
            #   - El símbolo del activo activo ('active_symbol').
            #   - El tipo de orden ('order_type').
            #   - Los datos de la nueva orden recopilados del formulario ('self.new_order_data').
            # El resultado (la estructura de datos del activo actualizada) se guarda
            # nuevamente en 'self.data[active_symbol]'.
            self.data[active_symbol] = self.add_new_order(self.data[active_symbol], active_symbol, order_type, self.new_order_data)
            self.show_orders(self.open_orders_frame, "open")
            self.show_orders(self.pending_buy_orders_frame, "pending_buy")
            self.show_orders(self.sell_take_profit_frame, "sell_take_profit")
            self.update_asset_info_display()
            self.new_order_data = None  # Resetear los datos del formulario
        elif not active_symbol:
            self.show_error_messagebox(self, "Por favor, seleccione un activo primero.")

        elif not self.new_order_data:
            self.show_error_messagebox(self, "No se ingresaron datos en el formulario.")

    def show_new_order_form(self, order_type):
        """Esta función es llamada cuando el usuario hace clic en uno de los botones de
        "Crear Nueva Orden".
        Crea una nueva ventana secundaria (Toplevel) que es el formulario.
        Se encarga de procesar los datos ingresados por el usuario en el formulario
        para crear una nueva orden.
        Recibe el tipo de orden ('order_type') como argumento, y los valores de los
        campos de entrada correspondientes segun el order_type
        (precio, monto, stop loss, target, si es una orden madre).
        Intenta convertir los valores de precio, monto, stop loss y target a números de punto flotante.
        Si la conversión es exitosa, almacena estos valores
        (junto con el booleano de 'mother_order') en el atributo 'self.new_order_data' de la clase.
        Luego, llama a la función 'self.handle_add_new_order' para que se agregue la
        orden a los datos y se actualice la interfaz.
        Finalmente, cierra la ventana del formulario.
        Si ocurre un error durante la conversión a número (por ejemplo, si el usuario ingresó texto),
        muestra un cuadro de mensaje de error al usuario pidiéndole que ingrese valores numéricos válidos."""
        form = Toplevel(self)
        form.config(bg=self.toplevel_bgcolor)
        titulo = ''
        if order_type == 'open':
            form.geometry('400x320')
            titulo = 'OPEN'
        elif order_type == 'pending_buy':
            form.geometry('400x300')
            titulo = 'BUY LIMIT'
        elif order_type == 'sell_take_profit':
            form.geometry('400x260')
            titulo = 'SELL TAKE PROFIT'

        form.title(f"Nueva Orden: {titulo}")

        row_num = 0

        price_label = Label(form, text="Precio:", bg=self.toplevel_bgcolor,
                            font=("Arial", 12, "bold"))
        price_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="e")
        price_entry = Entry(form, font=("Arial", 12, "bold"), width=12)
        price_entry.grid(row=row_num, column=1, padx=5, pady=5)
        row_num += 1

        amount_label = Label(form, text="Monto (USDT):", bg=self.toplevel_bgcolor,
                             font=("Arial", 12, "bold"))
        amount_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="e")
        amount_entry = Entry(form, font=("Arial", 12, "bold"), width=12)
        amount_entry.grid(row=row_num, column=1, padx=5, pady=5)
        row_num += 1

        stoploss_label = None
        stoploss_entry = None
        take_profit_label = None
        take_profit_entry = None

        if order_type != 'sell_take_profit':
            stoploss_label = Label(form, text="Stop Loss (opcional):", bg=self.toplevel_bgcolor,
                                   font=("Arial", 12, "bold"))
            stoploss_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="e")
            stoploss_entry = Entry(form, font=("Arial", 12, "bold"), width=12)
            stoploss_entry.grid(row=row_num, column=1, padx=5, pady=5)
            row_num += 1

            take_profit_label = Label(form, text="Target (opcional):", bg=self.toplevel_bgcolor,
                                      font=("Arial", 12, "bold"))
            take_profit_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="e")
            take_profit_entry = Entry(form, font=("Arial", 12, "bold"), width=12)
            take_profit_entry.grid(row=row_num, column=1, padx=5, pady=5)
            row_num += 1

        if order_type == 'open':
            mother_var = BooleanVar()
            mother_check = Checkbutton(form, text="¿Es Orden Madre?",
                                       bg=self.toplevel_bgcolor, font=("Arial", 12, "bold"), variable=mother_var)
            mother_check.grid(row=row_num, column=0, columnspan=2, padx=5, pady=5, sticky="e")
            row_num += 1
        else:
            row_num += 1  # Incrementar row_num para los botones

        submit_button = Button(form, text="Crear Orden",
                               pady=5,
                               padx=5,
                               width=15,
                               font=self.button_font,
                               cursor="hand2",
                               command=lambda: self.get_form_data(  # llama a este metodo de la clase de GUI
                                   form,
                                   order_type,
                                   price_entry.get(),  # Obtiene el precio del campo de entrada
                                   amount_entry.get(),  # Obtiene el monto del campo de entrada
                                   stoploss_entry.get() if stoploss_entry else None,  # Obtiene el Stop Loss o None si no existe
                                   take_profit_entry.get() if take_profit_entry else None,  # Obtiene el Take Profit  o None si no existe
                                   mother_var.get() if order_type == 'open' else False  # Obtiene el estado de orden madre si es 'open'
                               ))
        submit_button.grid(row=row_num, column=1, columnspan=2, pady=10)
        row_num += 1

        cancel_button = Button(form, text="Cancelar",
                               pady=5,
                               padx=5,
                               width=15,
                               font=self.button_font,
                               cursor="hand2",
                               command=form.destroy)
        cancel_button.grid(row=row_num, column=1, columnspan=2, pady=10)

        form.wait_window()  # Pausa la ejecución de la ventana principal hasta que el formulario se cierre.

    def get_form_data(self, form, order_type, price, amount, sl, tp, mother_order):
        """Recupera los datos ingresados por el usuario en el formulario de nueva orden,
        genera un 'id' único para la orden, valida los datos convirtiéndolos a sus
        tipos numéricos correspondientes, almacena todos los detalles (incluyendo el 'id')
        en el atributo self.new_order_data como un diccionario, llama a la función
        para manejar la adición de la nueva orden (self.handle_add_new_order), y
        finalmente destruye la ventana del formulario. En caso de que la conversión
        a número falle (ValueError), muestra un mensaje de error al usuario."""
        order_data = {}
        try:
            price_val = float(price)
            amount_val = float(amount)

            order_id = str(uuid.uuid4())  # Generar el 'id' único aquí
            order_data['id'] = order_id
            order_data['price'] = price_val
            order_data['amount_usdt'] = amount_val

            if order_type == 'open':
                order_data['mother_order'] = mother_order
                order_data['stop_loss'] = float(sl) if sl else None
                order_data['target'] = float(tp) if tp else None
            elif order_type == 'pending_buy':
                order_data['stop_loss'] = float(sl) if sl else None
                order_data['target'] = float(tp) if tp else None
            elif order_type == 'sell_take_profit':
                # No se agregan stop_loss ni target para sell_take_profit
                pass

            self.new_order_data = order_data  # almacena la nueva orden en el atributo 'new_order_data'
            self.handle_add_new_order(order_type)  # llama al metodo manejar la adición de la nueva orden
            form.destroy()  # destruye la ventana del formulario
        except ValueError:
            self.show_error_messagebox(self, "Por favor, ingrese valores numéricos válidos.")

    def delete_order(self, order_id):
        """Pide Confirmacion al usuario para eliminar una orden del activo seleccionado basándose en su ID."""
        if not self.show_confirmation_dialog(self, "Confirmar Eliminación", "¿Está seguro de que desea eliminar esta orden?"):
            return  # Si el usuario hace clic en "No", salimos de la función sin eliminar nada
        symbol = self.selected_asset.get()

        if symbol in self.data:
            # este bucle asegura que intentemos eliminar la orden de la lista correcta.
            for order_type_key in ['open_orders', 'buy_limits', 'sell_take_profit']:
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
                        self.show_orders(self.sell_take_profit_frame, "sell_take_profit")
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
        if hasattr(self, 'sell_take_profit_frame'):
            self.sell_take_profit_frame.destroy()
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
            {"text": "Add SELL TAKE PROFIT", "command": lambda: self.show_new_order_form('sell_take_profit')},
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

        self.sell_take_profit_frame = Frame(self.asset_orders_frame)
        self.sell_take_profit_frame.pack(fill=X, pady=2)
        Label(self.sell_take_profit_frame, text="Ventas Take Profit").pack(anchor='w')
        self.show_orders(self.sell_take_profit_frame, "sell_take_profit")

    def get_orders_for_asset(self, symbol, order_type):
        """Obtiene las órdenes del activo seleccionado y del tipo especificado."""
        #print(f"get_orders_for_asset - Symbol: '{symbol}', Data for symbol: '{self.data.get(symbol)}'")  # Linea par depurar error
        #print(f"Order type: {order_type}")  # Linea par depurar error
        if symbol in self.data:
            if order_type == "open":
                return self.data[symbol].get('open_orders', [])
            elif order_type == "pending_buy":
                return self.data[symbol].get('buy_limits', [])
            elif order_type == "sell_take_profit":
                return self.data[symbol].get('sell_take_profit', [])
        return []

    def show_orders(self, parent_frame, order_type):
        """Llena el frame con la información de las órdenes del tipo especificado (con precio copiable)."""
        # Limpiar los widgets existentes en el parent_frame, excepto los Label y Button
        for widget in parent_frame.winfo_children():
            if not isinstance(widget, tk.Label) and not isinstance(widget, tk.Button):
                widget.destroy()

        symbol = self.selected_asset.get()
        orders = self.get_orders_for_asset(symbol, order_type)

        for order in orders:
            # Crear un Frame para contener la información de la orden y el botón 'delete'
            order_row_frame = Frame(parent_frame, bg='lightgray')
            order_row_frame.pack(fill=X, pady=2)  # Empaquetar el frame de la fila

            # Label "Precio:"
            price_label_text = tk.Label(order_row_frame, text="Precio:", font=('Dosis', 10, 'bold'), anchor='w', bg='lightgray')
            price_label_text.pack(side=LEFT)

            # Precio (copiable)
            price_entry = tk.Entry(order_row_frame)
            price_rounded = round(order.get('price', 'N/A'), 4)
            price_entry.insert(0, price_rounded)
            price_entry.config(state='readonly', font=('Dosis', 10, 'bold'), width=11)
            price_entry.pack(side=LEFT, padx=(5, 5))  # Empaquetar el widget para que se muestre

            # Label "Quantity:"
            quantity_label_text = tk.Label(order_row_frame, text="Quantity:", font=('Dosis', 10, 'bold'), anchor='w', bg='lightgray')
            quantity_label_text.pack(side=LEFT)

            # Cantidad (copiable)
            quantity = order.get('quantity', 'N/A')
            symbol = self.selected_asset.get()  # Obtener el activo seleccionado
            # bloque para redondear 'quantity' segun sea el simbolo seleccionado
            if symbol == 'BTC':
                rounded_quantity = f"{float(quantity):.8f}" if isinstance(quantity, (int, float)) else quantity
            else:
                rounded_quantity = f"{float(quantity):.4f}" if isinstance(quantity, (int, float)) else quantity

            quantity_entry = tk.Entry(order_row_frame)
            quantity_entry.insert(0, rounded_quantity)
            quantity_entry.config(state='readonly', font=('Dosis', 10, 'bold'), width=14)
            quantity_entry.pack(side=LEFT, padx=(5, 5))

            # Label "Amount:"
            amount_label_text = tk.Label(order_row_frame, text="Amount (USDT):", font=('Dosis', 10, 'bold'), anchor='w', bg='lightgray')
            amount_label_text.pack(side=LEFT)

            # Amount (copiable)
            amount_entry = tk.Entry(order_row_frame)
            amount_entry.insert(0, order.get('amount_usdt', 'N/A'))
            amount_entry.config(state='readonly', font=('Dosis', 10, 'bold'), width=14)
            amount_entry.pack(side=LEFT, padx=(5, 5))

            if order_type == 'open':
                mo_label = tk.Label(order_row_frame, text=f"MO: {order.get('mother_order', False)}", font=('Dosis', 10, 'bold'),
                                    anchor='w', bg='lightgray')
                mo_label.pack(side=LEFT)

            if order_type != 'sell_take_profit':
                sl_label = tk.Label(order_row_frame, text=f"SL: {order.get('stop_loss', 'N/A')}", font=('Dosis', 10, 'bold'),
                                    anchor='w', bg='lightgray')
                sl_label.pack(side=LEFT, padx=5)
                tp_label = tk.Label(order_row_frame, text=f"TP: {order.get('target', 'N/A')}", font=('Dosis', 10, 'bold'),
                                    anchor='w', bg='lightgray')
                tp_label.pack(side=LEFT)

            delete_button = Button(order_row_frame, text="X", fg='white', bg='#C21E29', padx=5,
                                   font=("Segoe UI", 10, 'bold'),
                                   cursor="hand2",
                                   command=lambda oid=order.get('id'): self.delete_order(oid))
            delete_button.pack(side=RIGHT)  # Empaquetar el botón a la derecha

    def delete_all_asset_data(self):
        """Borra todos los datos del activo seleccionado, con confirmación previa."""
        symbol = self.selected_asset.get()

        if symbol in self.data:
            # Mostrar diálogo de confirmación
            confirm = self.show_confirmation_dialog(self, "Confirmar Borrado",
                                                    f"¿Estás seguro de que deseas borrar todos los datos del activo '{symbol}'?")

            if confirm:  # Si el usuario hace clic en "Sí" o confirma
                # Destruir la sección de órdenes actual para una actualización visual instantánea
                if hasattr(self, 'asset_orders_frame'):
                    self.asset_orders_frame.destroy()

                self.data[symbol] = {
                    "margin": 0,
                    "open_orders": [],
                    "buy_limits": [],
                    "sell_take_profit": []
                }
                self.save_data()
                self.update_asset_info_display()
                self.create_asset_orders_section()  # Volver a crear la sección de órdenes vacía
            else:
                pass

        else:
            self.show_error_messagebox(self, f"El símbolo '{symbol}' no existe en los datos.")

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
            confirmation = self.show_confirmation_dialog(self, "Confirmar Eliminación", f"¿Está seguro de que desea eliminar el activo '{symbol}'?")
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

                    #self.show_info_messagebox(self, "Acción Exitosa", f"El activo '{symbol}' ha sido eliminado.")

                else:
                    self.show_error_messagebox(self, f"El activo '{symbol}' no existe en los datos.")

            else:
                pass
                #self.show_info_messagebox(self, "Eliminación Cancelada", f"Se mantuvo el activo '{symbol}'.")

        else:
            self.show_error_messagebox(self, "Por favor, seleccione un activo para eliminar.")

    def calculate_mother_order(self):
        """Abre el formulario para calcular la orden madre."""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            return
        # muestra el formulario para ingresar los datos necesarios para calcular la orden madre
        self.show_calculate_mother_order_form(symbol)

    def show_calculate_mother_order_form(self, symbol):
        """Crea y muestra el formulario para calcular la orden madre."""
        top = tk.Toplevel(self)
        top.config(bg=self.toplevel_bgcolor)
        top.geometry('460x280')
        top.title(f"Calcular Orden Madre para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Precio Promedio de Compra:", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_average_price = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_average_price.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(top, text="Monto de Posición Abierta (USDT):", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_open_position = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_open_position.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(top, text="Beneficio Tomado:", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_profits_taken = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_profits_taken.grid(row=2, column=1, padx=5, pady=10)

        tk.Label(top, text="Cantidad:", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entry_quantity = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_quantity.grid(row=3, column=1, padx=5, pady=10)

        # --- Botones ---
        calculate_button = tk.Button(top, text="Calcular",
                                     pady=5,
                                     padx=5,
                                     width=15,
                                     font=self.button_font,
                                     cursor="hand2",
                                     command=lambda: self.perform_mother_order_calculation(
                                          symbol,
                                          entry_average_price.get(),
                                          entry_open_position.get(),
                                          entry_profits_taken.get(),
                                          entry_quantity.get(),
                                          top  # se pasa la ventana Toplevel para cerrarla
                                      ))
        calculate_button.grid(row=4, column=1, pady=30)

        cancel_button = tk.Button(top, text="Cancelar",
                                  pady=5,
                                  padx=5,
                                  width=15,
                                  font=self.button_font,
                                  cursor="hand2",
                                  command=top.destroy)
        cancel_button.grid(row=4, column=0, pady=30)

    def perform_mother_order_calculation(self, symbol, avg_price_str, open_pos_str, profit_str, qty_str, form_window):
        """Realiza validaciones, el cálculo de la orden madre y pregunta si se guarda."""
        try:
            average_purchase_price = float(avg_price_str)
            open_position_usdt = float(open_pos_str)
            profits_taken = float(profit_str)
            quantity_mother_order = float(qty_str)

            if average_purchase_price == 0 or average_purchase_price < 0:
                self.show_error_messagebox(self, "Precio promedio de compra debe ser mayor a cero.")
                form_window.destroy()
                return

            if open_position_usdt == 0 or open_position_usdt < 0:
                self.show_error_messagebox(self, "Monto de Posición Abierta debe ser mayor a cero.")
                form_window.destroy()
                return

            if quantity_mother_order != 0:
                price_mother_order = average_purchase_price - (profits_taken / quantity_mother_order)
                price_mother_order_rounded = round(price_mother_order, 4)

                result_message = (
                    f"---------- Mother Order {symbol} ----------\n\n"
                    f"Amount: {open_position_usdt} USDT\n"
                    f"Price: {price_mother_order_rounded}\n"
                    f"Quantity: {quantity_mother_order}"
                )
                self.show_info_messagebox(self, "Resultado Orden Madre", result_message)

                save_confirmation = self.show_confirmation_dialog(self, "Guardar Orden Madre", "¿Desea guardar esta orden madre en OPEN ORDERS?")
                if save_confirmation:
                    if symbol in self.data:
                        existing_mother_order = None
                        if "open_orders" in self.data[symbol]:
                            for order in self.data[symbol]["open_orders"]:
                                if order.get("mother_order"):
                                    existing_mother_order = order
                                    break

                        if existing_mother_order:
                            confirm_overwrite = self.show_confirmation_dialog(self, "Advertencia", f"Ya existe una orden madre para {symbol}.\n ¿Desea sobreescribirla?")
                            if confirm_overwrite:
                                # Eliminar la orden madre existente
                                self.data[symbol]["open_orders"] = [
                                    order for order in self.data[symbol]["open_orders"] if not order.get("mother_order")
                                ]
                                new_order = {
                                    "id": str(uuid.uuid4()),
                                    "price": price_mother_order_rounded,
                                    "amount_usdt": open_position_usdt,
                                    "quantity": quantity_mother_order,
                                    "stop_loss": None,
                                    "target": None,
                                    "mother_order": True
                                }
                                self.data[symbol]["open_orders"].append(new_order)
                                self.save_data()
                                self.create_asset_orders_section()
                                self.show_info_messagebox(self, "Orden Guardada",
                                                          "La orden madre se ha sobreescrito!")
                            else:
                                pass
                                #self.show_info_messagebox(self, "Operación Cancelada", "La nueva orden madre no ha sido guardada.")
                        else:
                            new_order = {
                                "id": str(uuid.uuid4()),
                                "price": price_mother_order_rounded,
                                "amount_usdt": open_position_usdt,
                                "quantity": quantity_mother_order,
                                "stop_loss": None,
                                "target": None,
                                "mother_order": True
                            }
                            self.data[symbol]["open_orders"].append(new_order)
                            self.save_data()
                            self.create_asset_orders_section()
                            self.show_info_messagebox(self, "Orden Guardada",
                                                      "La orden madre ha sido guardada en órdenes abiertas.")
                    else:
                        self.show_error_messagebox(self, "Por favor, seleccione un activo primero.")

                form_window.destroy()  # Cerrar el formulario después del cálculo y (opcional) guardado de la orden
            else:
                self.show_error_messagebox(self, "La cantidad de la orden madre no puede ser cero.")
                form_window.destroy()
        except ValueError:
            self.show_error_messagebox(self, "Por favor, introduce valores numéricos válidos en todos los campos.")
            form_window.destroy()

    def generate_pink_net(self):
        """Abre el formulario para generar Buy Limits (niveles de ordenes de compras pendientes,
        inicialmente la llamaba con el nombre ficticio Pink Net, por eso ese nombre!)"""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            return

        self.show_generate_pink_net_form(symbol)

    def show_generate_pink_net_form(self, symbol):
        """Crea y muestra el formulario para generar la PINK NET (niveles de compras pendientes).
        (son BUY LIMITS)"""
        top = tk.Toplevel(self)
        top.geometry('400x320')
        top.title(f"Generar BUY LIMITS para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Precio (Nivel Inicial):",
                         font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_initial_level = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_initial_level.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(top, text="Precio (Nivel Final):",
                         font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_final_level = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_final_level.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(top, text="Cantidad de Niveles:",
                 font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_levels = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_levels.grid(row=2, column=1, padx=5, pady=10)

        tk.Label(top, text="Monto Total a Invertir (USDT):",
                         font=("Arial", 12, "bold")).grid(row=3, column=0, padx=(20, 5), pady=5, sticky="e")
        entry_investment_amount = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_investment_amount.grid(row=3, column=1, padx=5, pady=10)

        # --- Botones ---
        generate_button = tk.Button(top, text="Generar",
                                    pady=5,
                                    width=15,
                                    font=self.button_font,
                                    cursor="hand2",
                                    command=lambda: self.calculate_pink_net_and_ask_save(
                                        symbol,
                                        entry_levels.get(),
                                        entry_initial_level.get(),
                                        entry_final_level.get(),
                                        entry_investment_amount.get(),
                                        top  # Pasar la ventana Toplevel para cerrarla
                                   ))

        generate_button.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(top, text="Cancelar",
                                  pady=5,
                                  width=15,
                                  font=self.button_font,
                                  cursor="hand2",
                                  command=top.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    def calculate_pink_net_and_ask_save(self, symbol, levels_str, initial_level_str, final_level_str, investment_amount_str, form_window):
        """Realiza el cálculo de la PINK NET y pregunta si se guarda."""
        try:
            levels = int(levels_str)
            initial_level = float(initial_level_str)
            final_level = float(final_level_str)
            investment_amount = float(investment_amount_str)

            if levels <= 0 or investment_amount <= 0:
                self.show_error_messagebox(self, "La cantidad de niveles y el monto de inversión deben ser mayores que cero.")
                form_window.destroy()
                return

            current_price = self.get_price(symbol)
            if initial_level > current_price or final_level > current_price:
                self.show_error_messagebox(self,
                                           "Los niveles de precios deben ser menor al precio actual!")
                form_window.destroy()
                return

            pink_net = []
            price_range = initial_level - final_level
            increment = price_range / (levels - 1) if levels > 1 else 0
            amount_per_level = investment_amount / levels

            for i in range(levels):
                price = initial_level - i * increment
                quantity = amount_per_level / price if price > 0 else 0
                level_pink_net = {
                    'id': str(uuid.uuid4()),  # Generar el 'id' único aquí
                    'price': round(price, 3),
                    'amount_usdt': round(amount_per_level, 2),
                    'quantity': round(quantity, 5),
                    'stop_loss': 0,  # se puede agregar campos al formulario si se desea
                    'target': 0,  # se puede agregar campos al formulario si se desea
                }
                pink_net.append(level_pink_net)

            result_message = "Niveles BUY LIMITS Generados:\n\n"
            for level in pink_net:
                result_message += f"Precio: {level['price']}, Monto: {level['amount_usdt']} USDT, Cantidad: {level['quantity']}\n"

            self.show_info_messagebox(self, "Niveles BUY LIMITS Generados!", result_message )

            save_confirmation = self.show_confirmation_dialog(self, "Guardar niveles BUY LIMITS", "¿Desea guardar estos niveles como órdenes límite de compra?")

            if save_confirmation:
                if symbol in self.data:
                    # Advertir al usuario sobre la sobreescritura
                    overwrite = self.show_confirmation_dialog(self, "Advertencia", "Guardar las BUY LIMITS sobreescribirá las órdenes límite de compra existentes. ¿Continuar?")

                    if overwrite:
                        self.data[symbol]["buy_limits"] = pink_net
                        self.save_data()
                        self.create_asset_orders_section()  # Actualizar la sección de órdenes
                        self.show_info_messagebox(self, "Niveles BUY LIMITS Guardados", "Los niveles de compras pendientes han sido guardado en órdenes BUY LIMITS.")

                else:
                    self.show_error_messagebox(self, f"El símbolo '{symbol}' ya no existe en los datos.")

            form_window.destroy()

        except ValueError:
            self.show_error_messagebox(self, "Por favor, introduce valores numéricos válidos en todos los campos.")

        except ZeroDivisionError:
            self.show_error_messagebox(self, "El precio del nivel no puede ser cero.")

    def get_price(self, symbol):
        """Obtiene el precio actual de un activo en Binance.
        Parámetros:
            symbol (str): El símbolo del activo en formato por ej. 'HBAR'

            Retorna:
            float: El precio actual del activo, o None si hay un error."""

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
            data = response.json()  #  toma la respuesta que recibiste de la API y la convierte en una estructura de datos de Python (generalmente un diccionario o una lista de diccionarios)
            return float(data['price'])
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                error_message = f"El símbolo '{symbol}' no existe o no es un par válido en Binance."
            else:
                error_message = f"Error al obtener el precio de {symbol}:\n{e}"
            self.show_error_messagebox(self, error_message)
            return None  # O algún otro valor que indique que no se pudo obtener el precio
        except requests.exceptions.RequestException as e:
            self.show_error_messagebox(self, f"Error de conexión a la API: {e}")
            return None
        except Exception as e:
            self.show_error_messagebox(self, f"Error inesperado al obtener el precio: {e}")
            return None

    def calculate_burn_price(self):
        """Calcula el precio de quema del activo seleccionado, obteniendo el precio actual de Binance.
        El cambio que hicimos con esta funcion es que ahora obtiene la cantidad total del activo en vez
        de calcular la cantidad de activo de la orden madre (ahora la orden madre no se considera la
        resultante de todas las ordenes abiertas.
        Las ordenes NO madres, ahora pueden no estar incluidas en la orden madre y ser independientes.)"""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            return

        current_price = self.get_price(symbol)

        if current_price is not None:
            if symbol in self.data:
                data_asset = self.data[symbol]
                margin = data_asset.get("margin", 0)

                if margin == 0:
                    self.show_info_messagebox(self, "Información", "No se puede calcular Precio de Liquidación\nMargin = 0\nActualizar Margin!")

                else:
                    burn_price_message = f"  PRECIO LIQUIDACION: {symbol}  ".center(70, '*') + "\n\n"
                    burn_price_message += "Advertencia: tener actualizada las OPEN ORDERS y el MARGIN!\n\n"
                    burn_price_message += f"CURRENT PRICE: {current_price}\n"
                    burn_price_message += f"MARGIN: {margin} USDT\n\n"

                    # bucle calcula cantidad total de activo, en ordenes abiertas
                    quantity_open_orders = 0
                    if 'open_orders' in data_asset:
                        for order in data_asset['open_orders']:
                            quantity_open_orders += order['quantity']

                    # Para redondear la cantidad segun sea el simbolo
                    if symbol == 'BTC':
                        quantity_open_orders = round(quantity_open_orders, 8)
                    else:
                        quantity_open_orders = round(quantity_open_orders, 3)

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

                    else:
                        burn_price_message += "No hay BUY LIMITS!\n"

                    total_quantity = quantity_open_orders + total_quantity_buy_limits
                    if total_quantity == 0:
                        self.show_error_messagebox(self, "No se puede calcular PRECIO DE LIQUIDACION\n No existen OPEN ORDERS ni BUY LIMITS")

                    else:
                        burn_price = ((current_price * quantity_open_orders) + total_amount_buy_limits - margin) / total_quantity
                        burn_price_message += f"\nBURN PRICE: {round(burn_price, 3)} USDT\n\n"
                        burn_price_message += "".center(82, '*')
                        self.show_info_messagebox(self, "Resultado Burn Price", burn_price_message)  # se llama al metodo que encapsula la clase personalizada 'CustomInfoDialog'

            else:
                self.show_error_messagebox(self, f"No esta ingresado '{symbol}' en el data.")

        else:
            # Manejar el caso en que no se pudo obtener el precio de la API
            pass  # El error ya se mostró en get_price()

    def generate_sales_cloud(self):
        """Abre el formulario para generar la NUBE DE VENTAS
        (genera los Niveles de Venta de Toma de Ganancia)"""
        symbol = self.selected_asset.get()

        if not symbol:
            self.show_error_messagebox(self, "Por favor, selecciona un activo primero.")
            return

        self.show_generate_sales_cloud_form(symbol)

    def show_generate_sales_cloud_form(self, symbol):
        """Crea y muestra el formulario para generar la NUBE DE VENTAS.
        genera ordenes de ventas de toma de ganacia"""
        top = tk.Toplevel(self)
        top.config(bg=self.toplevel_bgcolor, padx=50, pady=20)
        #top.geometry('420x280')
        top.title(f"Generar Niveles de Ventas para {symbol}")

        # --- Etiquetas y campos de entrada ---
        tk.Label(top, text="Precio (Nivel Inicial):", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        entry_initial_level = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_initial_level.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top, text="Precio (Nivel Final):", bg=self.toplevel_bgcolor,
                         font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        entry_final_level = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_final_level.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(top, text="Niveles:", bg=self.toplevel_bgcolor,
                 font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        entry_levels = tk.Entry(top, font=("Arial", 12, "bold"), width=12)
        entry_levels.grid(row=2, column=1, padx=5, pady=5)

        # --- Botones ---
        generate_button = tk.Button(top, text="Generar",
                                    pady=5,
                                    padx=5,
                                    width=15,
                                    font=self.button_font,
                                    cursor="hand2",
                                    command=lambda: self.calculate_sales_cloud_and_ask_save(
                                        symbol,
                                        entry_levels.get(),
                                        entry_initial_level.get(),
                                        entry_final_level.get(),
                                        top  # Pasar la ventana Toplevel para cerrarla
                                    ))
        generate_button.grid(row=4, column=0, columnspan=2, pady=10, sticky='we')

        cancel_button = tk.Button(top, text="Cancelar",
                                  pady=5,
                                  padx=5,
                                  width=15,
                                  font=self.button_font,
                                  cursor="hand2",
                                  command=top.destroy)
        cancel_button.grid(row=5, column=0, columnspan=2, pady=5, sticky='we')

    def calculate_total_open_quantity(self):
        """Calcula cantidad total de activo de todas las operaciones abiertas
        y devuelte el resultado"""

        if self.selected_asset_data.get('open_orders'):
            total_quantity = 0
            for order in self.selected_asset_data['open_orders']:
                quantity = order.get('quantity', 0)
                total_quantity += quantity

            return total_quantity

    def calculate_sales_cloud_and_ask_save(self, symbol, levels_str, initial_level_str, final_level_str, form_window):
        """Realiza el cálculo de los niveles de ventas y pregunta si se guarda."""
        try:
            levels = int(levels_str)
            initial_level = float(initial_level_str)
            final_level = float(final_level_str)
            current_price = self.get_price(symbol)
            total_quantity = self.calculate_total_open_quantity()

            if initial_level < current_price:
                self.show_info_messagebox(self, "Advertencia", "\nEl Nivel Inicial debe ser mayor al Precio Actual")
                form_window.destroy()  # cierra la ventana
                return

            if initial_level > final_level:
                self.show_info_messagebox(self, "Advertencia", "\nEl Nivel Inicial debe ser menor al Nivel Final")
                form_window.destroy()  # cierra la ventana
                return

            if levels <= 0:
                self.show_error_messagebox(self, "La cantidad de niveles debe ser mayor que cero.")
                form_window.destroy()  # cierra la ventana
                return

            sales_cloud = []
            price_range = final_level - initial_level
            increment = price_range / (levels - 1) if levels > 1 else 0

            for i in range(levels):
                price_per_level = initial_level + i * increment
                quantity_per_level = total_quantity / levels
                amount_per_level = quantity_per_level * price_per_level
                rounded_amount = round(amount_per_level / 10) * 10  # Para redondear a los 10 dólares más cercanos
                level_cloud = {
                    'id': str(uuid.uuid4()),  # Generar 'id' único para cada orden de venta
                    'price': round(price_per_level, 3),
                    'amount_usdt': rounded_amount,
                    'quantity': round(quantity_per_level, 5)}

                sales_cloud.append(level_cloud)

            result_message = "Niveles de Ventas:\n\n"
            for level in sales_cloud:
                result_message += f"Precio: {level['price']}, Monto: {level['amount_usdt']} USDT, Cantidad: {level['quantity']}\n"

            self.show_info_messagebox(self, "VENTAS de Toma de Ganancia Generada", result_message)

            save_confirmation = self.show_confirmation_dialog(self, "Guardar Niveles de VENTAS",
                                                              "¿Desea guardar estos niveles como SELL TAKE PROFIT?")
            if save_confirmation:
                if symbol in self.data:
                    # Advertir al usuario sobre la sobreescritura
                    overwrite = self.show_confirmation_dialog(self, "Advertencia",
                                                              "Guardar la Niveles de Toma de Ganancias, sobreescribirá \n las órdenes existentes en SELL TAKE PROFIT. ¿Continuar?")
                    if overwrite:
                        self.data[symbol]["sell_take_profit"] = sales_cloud
                        self.save_data()
                        self.create_asset_orders_section()  # Actualizar la sección de órdenes
                        self.show_info_messagebox(self, "Niveles VENTAS de Toma de Ganancias Guardada",
                                                  "Los Niveles de VENTAS han sido guardado!")

                else:
                    self.show_error_messagebox(self, f"El símbolo '{symbol}' ya no existe en los datos.")

            form_window.destroy()

        except ValueError:
            self.show_error_messagebox(self, "Por favor, introduce valores numéricos válidos en todos los campos.")

        except ZeroDivisionError:
            self.show_error_messagebox(self, "El precio del nivel no puede ser cero.")

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
            self.show_error_messagebox(self, "Hay más de una orden madre!\nSolo se permite una.")
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
            mother_quantity = mother_order['quantity']
            mother_profit = (current_price - mother_price) * mother_quantity

        # --- DATOS ordenes NO madre ---
        non_mother_profits = []
        non_mother_prices = []
        non_mother_amounts_usdt = []
        non_mother_percentages = []
        non_mother_quantity = []
        if non_mother_orders:
            non_mother_prices = [order['price'] for order in non_mother_orders]
            non_mother_amounts_usdt = [order['amount_usdt'] for order in non_mother_orders]
            non_mother_percentages = [(current_price - price) / price for price in non_mother_prices]
            non_mother_quantity = [order['quantity'] for order in non_mother_orders]
            non_mother_profits = [(current_price - price) * quantity for price, quantity in zip(non_mother_prices, non_mother_quantity)]
            """non_mother_profits = [amount_usdt * percentage for amount_usdt, percentage in
                                  zip(non_mother_amounts_usdt, non_mother_percentages)]"""

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
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
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

        # --- Configuraciones comunes a todos los casos para ax2 ---
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)

        # Crear y mostrar la leyenda
        handles = []
        labels = []
        # Leyenda de abreviaturas
        legend_labels = {'P': 'Precio', 'I': 'Monto Inicial (USDT)', 'Pf': 'Beneficios (USDT)',
                         '%': 'Porcentaje'}
        for key, value in legend_labels.items():
            handle = plt.Rectangle((0, 0), 1, 1, color='black', ec='black')
            label = f"{key}: {value}"
            handles.append(handle)
            labels.append(label)
        ax2.legend(handles, labels, loc='upper right', fontsize=10)

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
                         ha='center', va='bottom', fontsize=10, fontweight='bold')
            ax2.set_xticks(x2)
            ax2.set_xticklabels(x2)

            ax2.axhline(y=total_non_mother_profits, color='red' if total_non_mother_profits <= 0 else 'forestgreen',
                        linestyle='--', label=f'TOTAL PROFIT OPEN ORDERS: {total_non_mother_profits} USDT',
                        alpha=0.7)

            # Handle y label para el total profit
            total_profit_color = 'red' if total_non_mother_profits <= 0 else 'forestgreen'
            profit_handle = plt.Line2D([0], [0], color=total_profit_color, linestyle='--')
            profit_label = f'TOTAL NON MOTHER PFOFIT: {total_non_mother_profits} USDT'
            handles.append(profit_handle)
            labels.append(profit_label)

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
            ax2.text(0.5, 0.8, "No Open Orders (Non-Mother)", ha='center', va='center', fontsize=14, color='blue',
                     weight='bold')

        # Añade un texto con el precio actual y el beneficio total a la figura.
        text_color = '#e90400' if round(mother_profit + total_non_mother_profits, 2) <= 0 else '#088304'
        fig.text(0.22, 0.98, f'     PRECIO ACTUAL {active_symbol}: {current_price}      BENEFICIO TOTAL: {round(mother_profit + total_non_mother_profits, 2)} USDT',
                 ha='center', fontsize=12, color=text_color,
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

        # Bloque para intentar cargar la imagen del logo de Trading View
        try:
            self.tradingview_logo = tk.PhotoImage(file='images/image_tradingview.png')

        except tk.TclError as e:
            print(f"Error al cargar el icono de TradingView: {e}")
            self.tradingview_logo = None

        buttons_config = [
            {"text": "<<     Volver", "command": self.return_to_primary_menu},
            {"text": "Trading View", "command": self.open_tradingview},
            {"text": "Borrar Datos del Activo", "command": self.delete_all_asset_data},
            {"text": "Eliminar Activo", "command": self.delete_asset},
            {"text": "Calcular Orden Madre", "command": self.calculate_mother_order},
            {"text": "Generar Buy Limits", "command": self.generate_pink_net},
            {"text": "Calcular Precio de Liquidación", "command": self.calculate_burn_price},
            {"text": "Generar Niveles de Ventas", "command": self.generate_sales_cloud},
            {"text": "Ver Ordenes Abiertas", "command": self.render_open_orders},
            {"text": "Promediar Ordenes", "command": self.mostrar_promediar_ordenes_form}
        ]

        for i, button_info in enumerate(buttons_config):
            config = {
                "text": button_info["text"],
                "font": ('Dosis', 12, 'bold'),
                "padx": 10,
                "pady": 10,
                "bg": self.default_button_bg,
                "fg": 'white',
                "bd": 1,
                "relief": RAISED,
                "cursor": 'hand2',
                "command": button_info["command"]
            }

            # Carga la imagen del logo de Trading View
            if i == 1 and self.tradingview_logo:  # Si es el segundo botón y el logo se cargó
                config["image"] = self.tradingview_logo
                config["text"] = ""  # No muestra texto si hay imagen

            elif i == 1 and not self.tradingview_logo:  # Si es el segundo botón y el logo no se cargó
                pass  # Usar el texto predeterminado

            # Crea los botones con sus configuraciones
            button = tk.Button(self.secondary_menu, **config)
            button.pack(pady=4, padx=2, fill=X)

    def mostrar_promediar_ordenes_form(self):
        """Crea una instancia de la ventana de formulario 'PromediarOrdenesForm'
    (una nueva ventana Toplevel para ingresar y promediar órdenes).
    La instancia se crea pasando 'self' (la ventana principal de la aplicación)
    como el 'parent'. Esto establece a la ventana principal como la ventana
    padre de este nuevo formulario Toplevel, haciéndolo dependiente de la
    ventana principal en su comportamiento (por ejemplo, al minimizar)."""
        PromediarOrdenesForm(self)

    def open_quantfury(self):
        """Abre la plataforma de trading Quantfury en una nueva pestaña
        del navegador web predeterminado del usuario.
        Utiliza la biblioteca `webbrowser` para abrir la URL"""
        url = "https://trading.quantfury.com/"
        webbrowser.open_new_tab(url)

    def copiar_al_portapapeles(self):
        """Copia el código de invitación al portapapeles del sistema."""
        codigo_invitacion = "U23853V6"
        self.master.clipboard_clear()
        self.master.clipboard_append(codigo_invitacion)
        self.master.update()  # Es necesario para que el portapapeles se actualice inmediatamente

    def open_tradingview(self):
        """Abre el gráfico del activo seleccionado en TradingView.
        Este método obtiene el símbolo del activo a través de la variable self.selected_asset.
        Luego, construye la URL para el gráfico de ese activo en el exchange (BINANCE) emparejado con USDT.
        Finalmente, utiliza el módulo webbrowser para abrir esta URL en una nueva pestaña
        del navegador web predeterminado del usuario."""
        active_symbol = self.selected_asset.get()
        ticker = f"{active_symbol}USDT"  # Le agregamos USDT al símbolo
        exchange = "BINANCE"
        url = f"https://es.tradingview.com/chart/?symbol={exchange}:{ticker}"  # Estructura básica de la URL
        webbrowser.open_new_tab(url)

    def open_donation_window(self):
        """Abre una ventana Toplevel para las donaciones."""
        self.donation_window = tk.Toplevel(self)
        self.donation_window.title("Apoyar el Proyecto")
        # Establecer el tamaño fijo de la ventana (en píxeles)
        ancho = 660
        alto = 660
        self.donation_window.geometry(f"{ancho}x{alto}")

        # Deshabilitar la capacidad de redimensionar la ventana (ancho y alto)
        self.donation_window.resizable(False, False)

        self.create_donation_widgets(self.donation_window)

    def update_donation_info(self, event):
        """Actualiza la información mostrada en la sección de donaciones
            basándose en la criptomoneda o la opción seleccionada por el usuario
            en el desplegable (Combobox).

            Este método se activa cuando el usuario selecciona un nuevo elemento
            en el Combobox de opciones de donación. Su función principal es:
                - Obtener la criptomoneda o la opción seleccionada.
                - Buscar la información correspondiente (dirección/alias y ruta del QR)
                  en el diccionario `self.crypto_info`(en el construtor de la clase principal)
                - Actualizar el campo de texto (`self.address_entry`) con la dirección
                  de la billetera de la criptomoneda seleccionada o el alias de
                  Mercado Pago para el Peso Argentino.
                - Manejar la visualización del código QR:
                    - Si se selecciona Peso Argentino, se limpia la etiqueta del QR
                      y se muestra un mensaje indicando que se debe copiar el alias.
                    - Si hay una ruta de archivo QR válida para la criptomoneda
                      seleccionada, intenta abrir la imagen, redimensionarla y
                      mostrarla en la etiqueta `self.qr_label`. Si ocurre un error
                      al cargar la imagen, se muestra un mensaje de error.
                    - Si no hay una ruta de archivo QR válida, se muestra un mensaje
                      indicando que el QR no está disponible.
                - En caso de que la selección no se encuentre en `self.crypto_info`,
                  se limpia el campo de la dirección y la etiqueta del QR."""
        selected_crypto = self.selected_crypto.get()
        info = self.crypto_info.get(selected_crypto)
        if info:
            self.address_entry.config(state='normal')
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, info["address"])
            self.address_entry.config(state='readonly')

            qr_path = info["qr_path"]

            if selected_crypto == "Argentine Peso (ARS)":
                self.qr_label.config(image='')
                self.qr_label.config(
                    text="Para donar en Pesos Argentinos\nCopiar ALIAS!", font=('Dosis', 12, 'italic', 'bold'), pady=30)

            elif qr_path and os.path.exists(qr_path):
                try:
                    img = Image.open(qr_path)
                    img = img.resize((150, 150))
                    self.qr_image_tk = ImageTk.PhotoImage(img)
                    self.qr_label.config(image=self.qr_image_tk)
                    self.qr_label.config(text="")  # Limpiar cualquier texto anterior
                except Exception as e:
                    self.qr_label.config(image='')
                    self.qr_label.config(text=f"Error al cargar QR: {e}")
            else:
                self.qr_label.config(image='')
                self.qr_label.config(text="QR no disponible")
        else:
            self.address_entry.config(state='normal')
            self.address_entry.delete(0, tk.END)
            self.address_entry.config(state='readonly')
            self.qr_label.config(image='')
            self.qr_label.config(text="")

    def animate_copy_button(self, button):
        """Anima el botón de copiar cambiando el texto y el color.
        Lo use en el toplevel de donaciones"""
        original_text = button.cget("text")
        original_fg = button.cget("fg")  # Guarda el color de texto original
        original_bg = button.cget("bg")  # Guarda el colo de bg original
        button.config(text="¡Copiado!", state="disabled", fg="red", bg='white')
        self.after(1000, lambda: button.config(text=original_text, state="normal",
                                               fg=original_fg,
                                               bg=original_bg))  # Restaura el texto, estado y color original

    def copy_address_to_clipboard(self):
        """Copia la dirección de la billetera al portapapeles."""
        address_to_copy = self.address_entry.get()
        pyperclip.copy(address_to_copy)
        self.animate_copy_button(self.copy_address_button)

    def copy_email_to_clipboard(self):
        """Copia el correo del desarrollador al portapapeles."""
        pyperclip.copy(self.developer_email)
        self.animate_copy_button(self.copy_email_button)

    def create_donation_widgets(self, parent_window):
        """Crea y configura los widgets necesarios para la ventana de donaciones.

            Este método se encarga de construir la interfaz de usuario dentro de la ventana
            proporcionada como `parent_window`, permitiendo a los usuarios apoyar el proyecto
            a través de diversas opciones de criptomonedas o mediante Mercado Pago.

            Los widgets creados incluyen:
                - Una sección de narrativa profesional que agradece al usuario por su apoyo
                  y explica la importancia de las contribuciones.
                - Un desplegable (Combobox) que permite al usuario seleccionar la criptomoneda
                  o la opción de Peso Argentino para su donación.
                - Una sección para mostrar la dirección de la billetera de la criptomoneda
                  seleccionada o el alias de Mercado Pago, junto con un botón para copiar
                  esta información al portapapeles.
                - Un área para mostrar el código QR correspondiente a la criptomoneda
                  seleccionada (oculto si se selecciona Peso Argentino).
                - Una sección que muestra la información de contacto del desarrollador
                  (su correo electrónico) con un botón para copiarlo al portapapeles.

            La información mostrada (dirección/alias y código QR) se actualiza dinámicamente
            cuando el usuario selecciona una opción diferente en el Combobox, gracias a la
            vinculación con el método `self.update_donation_info`.
            """
        # --- Narrativa Profesional ---
        saludo_label = tk.Label(parent_window, text="¡Gracias por ser parte de este proyecto!", font=('Dosis', 14, 'bold'))
        saludo_label.pack(pady=(10, 5), padx=10, anchor='w')

        narrativa_text = tk.Label(
            parent_window,
            text=(
                "Este proyecto se desarrolla con dedicación y esfuerzo continuo\npara brindarte las mejores herramientas.\n"
                "Si encuentras valor en esta aplicación, deseas apoyar su crecimiento\ny la incorporación de nuevas funcionalidades,\n"
                "te invitamos a realizar una contribución, por pequeña que sea.\nTu apoyo nos impulsa a seguir mejorando."
            ),
            justify='left', font=('Dosis', 14))
        narrativa_text.pack(pady=5, padx=(10, 40), anchor='w')

        contribucion_minima_label = tk.Label(parent_window, text="Contribución mínima sugerida: ¡Lo que sientas!", font=('Dosis', 12, 'italic'))
        contribucion_minima_label.pack(pady=20, padx=10, anchor='w')

        # --- Opción de Criptomoneda ---
        crypto_label = tk.Label(parent_window, text="Elige una opcion para realizar tu donación:", font=('Dosis', 12, 'bold'))
        crypto_label.pack(pady=(10, 5), padx=10, anchor='w')

        crypto_options = list(self.crypto_info.keys())
        self.selected_crypto = tk.StringVar(parent_window)
        self.selected_crypto.set(crypto_options[0])

        crypto_dropdown = ttk.Combobox(parent_window, textvariable=self.selected_crypto, values=crypto_options, state='readonly', font=('Dosis', 13, 'bold'))
        crypto_dropdown.pack(pady=5, padx=10, fill='x')
        crypto_dropdown.bind("<<ComboboxSelected>>", self.update_donation_info)

        # --- Dirección para Copiar y Botón Copiar ---
        address_frame = tk.Frame(parent_window)  # Nuevo frame para alinear Entry y Button
        address_frame.pack(pady=(10, 5), padx=10, fill='x')

        address_label = tk.Label(address_frame, text="Dirección:", font=('Dosis', 12, 'bold'), anchor='w')
        address_label.pack(side=tk.LEFT, padx=(0, 10))

        self.address_entry = tk.Entry(address_frame, state='readonly', font=('Consolas', 13))
        self.address_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.address_entry.insert(0, self.crypto_info[self.selected_crypto.get()]["address"])

        self.copy_address_button = tk.Button(address_frame, text="Copiar",
                                font=('Dosis', 12, 'bold'),
                                padx=5,
                                pady=5,
                                width=10,
                                bg=self.default_button_bg,
                                fg='white',
                                bd=1,
                                relief=RAISED,
                                cursor='hand2',
                                command=self.copy_address_to_clipboard)

        self.copy_address_button.pack(side=tk.RIGHT, padx=(5, 0))

        # --- Imagen del Código QR ---
        qr_label_title = tk.Label(parent_window, text="Código QR:", font=('Dosis', 12, 'bold'))
        qr_label_title.pack(pady=(10, 5), padx=10, anchor='w')

        self.qr_label = tk.Label(parent_window)
        self.qr_label.pack(pady=5, padx=10)
        self.update_donation_info(None)

        # --- Contacto del Desarrollador ---
        contact_dev_frame = tk.Frame(parent_window)
        contact_dev_frame.pack(pady=(15, 20), padx=10, fill='x')

        contact_dev_label = tk.Label(contact_dev_frame, text="Contacto del Desarrollador: ", font=('Dosis', 13, 'bold'),
                                     anchor='w')
        contact_dev_label.pack(side=tk.LEFT)

        dev_email_label = tk.Label(contact_dev_frame, text=self.developer_email, anchor='w', font=('Dosis', 13, 'italic'))
        dev_email_label.pack(side=tk.LEFT, padx=(5, 20))

        self.copy_email_button = tk.Button(contact_dev_frame, text="Copiar Correo",
                                      font=('Dosis', 12, 'bold'),
                                      padx=5,
                                      pady=5,
                                      width=10,
                                      bg=self.default_button_bg,
                                      fg='white',
                                      bd=1,
                                      relief=RAISED,
                                      cursor='hand2',
                                      command=self.copy_email_to_clipboard)

        self.copy_email_button.pack(side=tk.RIGHT)


if __name__ == "__main__":
    # Crear una instancia de la clase de GUI
    gui = AssetManagerGUI(filename)

    # Iniciar el loop principal de Tkinter (mantiene la ventana abierta y responde a los eventos)
    gui.mainloop()
