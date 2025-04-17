import requests
import json
import os
import matplotlib.pyplot as plt
import time
import matplotlib.gridspec as gridspec
from tkinter import messagebox
import uuid


filename = 'pink_net_data_3_GUI.json'
# filename = 'data_pruebas.json'
data = {}

permited_leverage = 3

# Estructura para guardar en acchivo json
symbol = 'BTC'

"""
Estructura data
---------------
data = {symbol: {'current_price': 94000,
                 'open_orders': [],
                 'buy_limits': [],
                 'sell_limits': []
                 }
        }

Estructura de una orden (open_order)
------------------------------------
order = {
        'price': price,
        'amount_usdt': amount_usdt,
        'quantity': quantity,
        'stop_loss': stop_loss,
        'target': target,
        'mother_order': mother_order
    }

Estructura de una orden (limit_order)
-------------------------------------
orden = {
        'price': price,
        'amount_usdt': amount_usdt,
        'quantity': quantity,
        'stop_loss': stop_loss,
        'target': target
        }
"""


def clear_console():
    """Limpia la consola dependiendo del sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause_program():
    """Pausa la ejecución del programa hasta que el usuario presione Enter.

    Es útil para dar tiempo al usuario para leer información importante
    o para separar diferentes secciones de la ejecución del programa.
    """
    input("\nPresione ENTER para continuar...")


def loading_animation(duration):
    """Muestra una animación de carga durante el tiempo especificado.
    (en mi caso la use para inicializar activos en caso de que se
    encuentren NULL, no inicializados correctamente)

    Parámetros:
    ----------
    duration : int
        Duración en segundos para mostrar la animación de carga.
    """
    end_time = time.time() + duration
    loading_chars = ['|', '/', '-', '|', '||', '|||', '||||', '|||||', '|||||', '\\']  # Caracteres para la animación
    while time.time() < end_time:
        for char in loading_chars:
            print(f'\rInicializando... {char}', end='', flush=True)
            time.sleep(0.2)  # Esperar un corto período antes de cambiar el carácter

    print('\rInicializando... Listo!')  # Mensaje final al terminar la carga


def get_price(symbol):
    """
    Obtiene el precio actual de un activo en Binance.

    Parámetros:
    symbol (str): El símbolo del activo en formato por ej. 'HBAR'

    Retorna:
    float: El precio actual del activo.
    """
    quote = 'USDT'
    # Combina el símbolo con la moneda de cotización
    full_symbol = f'{symbol}{quote}'
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price', params={'symbol': full_symbol})
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"\nError al obtener el precio por medio de la API:\n{e}")
        return None


def load_data(filename):
    """Carga los datos desde un archivo JSON."""
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            return data
    else:
        print(f"No se encontró el archivo {filename}.")
        return None


def get_current_price(symbol):
    """Obtiene el precio actual de un símbolo desde la API de Binance."""
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return float(data['price'])
    else:
        print("Error al obtener el precio actual.")
        return None


def add_open_order(data_asset, active_symbol):
    """Agrega una 'open order' a los datos del activo específico."""

    price = float(input("\nPrecio de entrada para la orden abierta: "))
    amount_usdt = float(input("Monto en dólares: "))
    response = input("¿Es esta una orden madre? (s/n, por defecto 'n'): ").strip().lower()
    mother_order = False
    # Asignar True o False basado en la respuesta
    if response == 's':
        mother_order = True
    else:
        mother_order = False  # Por defecto es False
    stop_loss = 0  # Puedes permitir que el usuario ingrese estos valores si lo deseas
    target = 0
    quantity = round(amount_usdt / price, 8)  # calcula cantindad de activo

    # Asegurarse de que la estructura exista
    if 'open_orders' not in data_asset:
        data_asset['open_orders'] = []

    # se inicializa estructura de una open orden
    orden = {
        'id': str(uuid.uuid4()),  # El 'id' es local a esta orden
        'price': price,
        'amount_usdt': amount_usdt,
        'quantity': quantity,
        'stop_loss': stop_loss,
        'target': target,
        'mother_order': mother_order
    }

    data_asset['open_orders'].append(orden)
    print("Orden abierta agregada!")


def add_buy_limit(data_asset):
    """Agrega una 'buy limit' (compra limite) a los datos del activo específico."""
    price = float(input("Precio de entrada para BUY LIMIT: "))
    amount_usdt = float(input("Monto en dólares: "))
    stop_loss = 0
    target = 0

    quantity = round(amount_usdt / price, 8)

    # Asegurarse de que la estructura exista
    if 'buy_limits' not in data_asset:
        data_asset['buy_limits'] = []

    # se inicializa estructura de una buy limit
    order = {
        'price': price,
        'amount_usdt': amount_usdt,
        'quantity': quantity,
        'stop_loss': stop_loss,
        'target': target,
    }

    data_asset['buy_limits'].append(order)
    print("BUY LIMIT agregada!")


def add_sell_limit(data_asset, active_symbol):
    """Agrega una 'sell limit' a la lista de 'sell_limits' del activo específico."""
    print(f" ADD SELL LIMIT for {active_symbol} ".center(75, '*'))
    price = float(input("\nPrecio de venta: "))
    amount_usdt = float(input("Monto en dólares: "))

    stop_loss = 0
    target = 0
    quantity = round(amount_usdt / price, 8)  # calcula cantindad de activo

    # Asegurarse de que la estructura exista
    if 'sell_limits' not in data_asset:
        data_asset['sell_limits'] = []

    # se inicializa estructura de una sell limit
    sell_order = {
        'price': price,
        'amount_usdt': amount_usdt,
        'quantity': quantity,
        'stop_loss': stop_loss,
        'target': target,
    }

    data_asset['sell_limits'].append(sell_order)
    print("SELL LIMIT agregada!")


def save_data(data, filename):
    """Guarda 'data' (todos los activos) en un archivo JSON."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def save_data_asset(data, data_asset, symbol, filename):
    """Guarda solo el activo específico en el archivo JSON."""

    # Actualizar o agregar el activo específico
    data[symbol] = data_asset

    # Guardar los datos actualizados en el archivo JSON
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def order_orders(data):
    """Ordena las órdenes abiertas y órdenes límite de activos financieros.

    Parámetros:
    ----------
    data : dict
        Un diccionario que contiene información sobre diferentes activos.
        Cada activo es una clave en el diccionario, y su valor es otro
        diccionario que incluye listas de órdenes abiertas ('open_orders')
        y órdenes límite ('limit_orders').

    Retorno:
    -------
    dict
        El mismo diccionario `data`, pero con las listas de órdenes ordenadas por precio.
    """

    for asset, data_asset in data.items():
        # Verificar si data_asset es None
        if data_asset is None:
            print(f"Advertencia: El activo '{asset}' es None. Saltando.")
            continue  # Salta a la siguiente iteración

        # Verificar si 'open_orders' y 'limit_orders' están presentes
        if 'open_orders' not in data_asset:
            print(f"Advertencia: El activo '{asset}' no tiene 'open_orders'. Saltando.")
            continue  # Salta a la siguiente iteración

        if 'buy_limits' not in data_asset:
            print(f"Advertencia: El activo '{asset}' no tiene 'buy_limits'. Saltando.")
            continue  # Salta a la siguiente iteración

        # Ordenar open_orders por precio
        """data_asset['open_orders'] = sorted(data_asset['open_orders'], key=lambda x: x['price'])"""
        # Ordenar open_orders por precio, pero mantener la orden madre en la primera posición
        data_asset['open_orders'] = sorted(data_asset['open_orders'], key=lambda x: (not x['mother_order'], x['price']))
        for order in data_asset['open_orders']:
            print(order)
        # Ordenar buy_limits por precio
        data_asset['buy_limits'] = sorted(data_asset['buy_limits'], key=lambda x: x['price'])
        print()
        for order in data_asset['buy_limits']:
            print(order)
        print(50 * '*')

    return data


def choose_current_price(active_symbol):
    """
    Permite al usuario elegir cómo establecer el valor de current_price.

    Parámetros:
    symbol (str): El símbolo del activo cuyo precio se desea obtener.
    max_price (float): El precio máximo definido anteriormente.

    Retorna:
    float: El valor elegido para current_price.
    """

    print("\nSeleccione una opción:")
    print("1 - Obtener CURRENT PRICE por medio de la API")
    print("2 - Ingresar manualmente un precio")
    print("3 - Salir\n")

    option = input("Seleccione una opción (1,2 o 3): ")

    if option == '1':
        current_price = get_price(active_symbol)
        if current_price is None:
            print("No se pudo obtener el precio actual. Saliendo...")

    elif option == '2':
        current_price = -1  # Inicializar a un valor negativo para entrar en el bucle
        while current_price <= 0:  # Continuar mientras el precio no sea positivo
            try:
                current_price = float(input("Ingrese CURRENT PRICE manualmente: "))
                if current_price <= 0:
                    print("Debe ingresar un número positivo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

    elif option == '3':
        print("Saliendo!")
        return None  # Retornar None si se desea salir

    else:
        print("Opción no válida. Saliendo...")
        return None  # Retornar None si la opción es inválida

    return current_price


def plot_open_orders(data_asset, current_price, active_symbol):
    """Grafica la orden madre con un gradico de barra en un subgrafico,
    y en otro subgrafico renderiza las operaciones abiertas no madre
    tambien con grafico de barras

    Toma los datos del activo, el precio actual,
    el symbol del activo

    Las órdenes en ganancia se muestran en color verde y las órdenes
    en pérdida se muestran en color rojo.

    Parámetros:
    ----------
    data_asset : dict
        Un diccionario que contiene información sobre un activo específico.
    current_price : float
        El precio actual del activo.
    active_symbol: str
        el símbolo del activo en cuestión
    """

    # Extraer las 'open orders'
    open_orders = data_asset['open_orders']

    if not open_orders:
        print('*' * 75)
        print(f"No hay órdenes abiertas para '{active_symbol}'.")
        pause_program()
        return

    # Filtrar órdenes madre
    mother_orders = [order for order in open_orders if order.get('mother_order', False)]

    # Verificar si hay más de una orden madre
    if len(mother_orders) > 1:
        print("Error: Hay más de una orden madre. Solo se permite una orden madre.")
        return  # Salir de la función si hay más de una orden madre

    # Filtrar órdenes NO madres
    non_mother_orders = [order for order in open_orders if not order.get('mother_order', False)]

    # Preparar datos para el gráfico de órdenes madre
    if mother_orders:
        mother_prices = [order['price'] for order in mother_orders]
        mother_amounts_usdt = [order['amount_usdt'] for order in mother_orders]
        mother_percentages = [(current_price - price) / price for price in mother_prices]
        mother_profits = [amount_usdt * percentage for amount_usdt, percentage in
                          zip(mother_amounts_usdt, mother_percentages)]
    else:
        print("No existe MOTHER ORDER!")
        mother_profits = []

    # Preparar datos para el gráfico de órdenes no madre
    if non_mother_orders:
        non_mother_prices = [order['price'] for order in non_mother_orders]
        non_mother_amounts_usdt = [order['amount_usdt'] for order in non_mother_orders]
        non_mother_percentages = [(current_price - price) / price for price in non_mother_prices]
        non_mother_profits = [amount_usdt * percentage for amount_usdt, percentage in
                              zip(non_mother_amounts_usdt, non_mother_percentages)]
    else:
        # non_mother_profits = []
        # Si no hay órdenes no madre, establecer listas vacias
        non_mother_prices = []
        non_mother_amounts_usdt = []
        non_mother_percentages = []
        non_mother_profits = []

    # Calcular profits
    total_mother_profits = round(sum(mother_profits), 2)
    total_non_mother_profits = round(sum(non_mother_profits), 2)

    # Crear un rango para el eje x basado en la cantidad de órdenes
    x1 = list(range(1, len(mother_orders) + 1))
    x2 = list(range(1, len(non_mother_orders) + 1))

    # Determinar colores según ganancia o pérdida
    colors1 = ['red' if distance <= 0 else 'forestgreen' for distance in mother_profits]
    colors2 = ['red' if distance <= 0 else 'forestgreen' for distance in non_mother_profits]

    # Crear figura y especificar la cuadrícula de subgráficos
    fig = plt.figure(figsize=(14, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])  # Ajustar las proporciones de los subgráficos

    # Subgráfico para la orden madre (más pequeño)
    ax1 = fig.add_subplot(gs[0])

    # Graficar orden madre
    bars = ax1.bar(x1, mother_profits, color=colors1)

    # Añadir etiquetas sobre cada barra con profits, porcentajes y precios
    for bar, profit, percentage, price, amount_usdt in zip(bars, mother_profits, mother_percentages, mother_prices,
                                                           mother_amounts_usdt):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval,
                 f"Price: {price}\nInitial: {amount_usdt} USDT\nProfits: {round(yval, 2)} USDT\n({round(percentage * 100, 2)}%)",
                 ha='center', va='bottom', fontsize=11)

    # Configurar los ticks del eje x
    ax1.set_xticks(x1)
    etiquetas = ['M O T H E R   O R D E R']
    ax1.set_xticklabels(etiquetas)

    # Establecer límites del eje Y centrando el 0
    if mother_profits:  # Verificar que no esté vacío
        max_profit = max(max(mother_profits), abs(min(mother_profits)))  # Valor máximo absoluto
        ax1.set_ylim(-max_profit - 150, max_profit + 150)  # Ajustar límites para centrar el 0

    # Añadir etiquetas y título
    ax1.set_ylabel('Profits USDT')
    ax1.set_title(f'MOTHER ORDER for {active_symbol}')

    # Mostrar la cuadrícula de fondo
    ax1.grid(axis='y', linestyle='--', alpha=0.7)  # Cuadrícula horizontal

    # Crear leyenda para mostrar profit de la orden madre
    ax1.axhline(y=total_mother_profits, color='red' if total_mother_profits <= 0 else 'forestgreen',
                linestyle='--',
                label=f'PROFIT: {total_mother_profits} USDT', alpha=0.7)

    # Mostrar la leyenda
    ax1.legend(loc='upper right', fontsize=12)

    # Agregar una línea horizontal en y=0 con un grosor mayor y color negrita para que se destaque
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)

    # Subgráfico para las ordenes NO madres (tamaño más grande)
    ax2 = fig.add_subplot(gs[1])

    # Añadir etiquetas y título
    ax2.set_xlabel('O P E N   O R D E R S   N O N   M O T H E R')
    ax2.set_ylabel('Profits USDT')
    ax2.set_title(f'OPEN ORDERS for {active_symbol}')

    # Verificar si no esta vacio
    if non_mother_profits:

        # Graficar ordenes NO madre
        bars2 = ax2.bar(x2, non_mother_profits, color=colors2)

        # Añadir etiquetas sobre cada barra con profits, porcentajes y precios
        for bar, profit, percentage, price, amount_usdt in zip(bars2, non_mother_profits, non_mother_percentages,
                                                               non_mother_prices,
                                                               non_mother_amounts_usdt):
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2, yval,
                     f"Price: {price}\nInitial: {amount_usdt} USDT\nProfits: {round(yval, 2)} USDT\n({round(percentage * 100, 2)}%)",
                     ha='center', va='bottom', fontsize=11)

        # Configurar los ticks del eje x
        ax2.set_xticks(x2)
        ax2.set_xticklabels(x2)

        # Agregar una línea horizontal en y=0 con un grosor mayor y color negrita para que se destaque
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)

        # Mostrar la cuadrícula de fondo
        ax2.grid(axis='y', linestyle='--', alpha=0.7)  # Cuadrícula horizontal

        # Crear leyenda para el total de profits de órdenes abiertas no madre
        ax2.axhline(y=total_non_mother_profits, color='red' if total_non_mother_profits <= 0 else 'forestgreen',
                    linestyle='--',
                    label=f'TOTAL PROFIT OPEN ORDERS: {total_non_mother_profits} USDT', alpha=0.7)

        # Mostrar la leyenda
        ax2.legend(loc='upper right', fontsize=12)

        # Establecer límites del eje Y
        if mother_profits:  # Verificar que no esté vacío
            ax2.set_ylim(min(non_mother_profits) - 50, max(non_mother_profits) + 50)

    else:
        # Si no hay datos para ordenes abiertas no madre, establecer límites del eje Y igual al subgrafico 1
        if mother_profits:  # Verificar que no esté vacío
            max_profit = max(max(mother_profits), abs(min(mother_profits)))  # Valor máximo absoluto
            ax2.set_ylim(-max_profit - 50, max_profit + 50)  # Ajustar límites para centrar el 0

        # Crear leyenda que muestre que no hay OPEN ORDERS
        ax2.text(0.5, 0.5, "No se encontraron datos", ha='center', va='center', fontsize=14, color='blue',
                 weight='bold')

        # Eliminar las marcas del eje x
        ax2.set_xticks([])

    # Añadir texto para el precio actual anclado a la figura (no al subgráfico)
    fig.text(0.22, 0.98, f'CURRENT PRICE {active_symbol}: {current_price}',
             ha='center', fontsize=12, color='blue', weight='bold')

    # Ajustar el layout para evitar superposiciones
    fig.tight_layout()

    # Mostrar gráfico maximizado
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Maximiza la ventana del gráfico en Windows
    except AttributeError:
        pass  # Si no se puede maximizar, simplemente continúa

    # Mostrar el gráfico
    plt.show()


def select_asset(data, symbol):
    """Seleccione un activo y devuelve los datos del activo."""
    # Verificar si el símbolo existe en los datos
    if symbol in data:
        asset_data = data[symbol]
        return asset_data, symbol
    else:
        messagebox.showinfo("Info", f"El símbolo '{symbol}' no se encuentra en los datos")
        return None


def show_open_orders(data_asset, active_symbol):
    # Obtener las órdenes abiertas del activo
    open_orders = data_asset['open_orders']

    if not open_orders:
        print(75 * '*')
        print(f"\nNo hay órdenes abiertas para '{active_symbol}'.\n")
        return

    print(f" OPEN ORDERS for {active_symbol} ".center(75, '*'))
    print()
    # Listas para almacenar órdenes madre y otras órdenes
    mother_orders = []
    other_orders = []

    # Recorrer las órdenes abiertas y separarlas
    for order in open_orders:
        if order['mother_order']:
            mother_orders.append(order)  # Agregar a la lista de órdenes madre
        else:
            other_orders.append(order)  # Agregar a la lista de otras órdenes

    # Concatenar las listas para que las órdenes madre aparezcan primero
    sorted_open_orders = mother_orders + other_orders

    # Mostrar las órdenes en pantalla
    for order in sorted_open_orders:
        print(f"Price: {order['price']} ---> {order['amount_usdt']} USDT, "
              f"Stop Loss: {order['stop_loss']}, Target: {order['target']}, "
              f"Quantity: {order['quantity']}, MO: {order['mother_order']}")


def show_buy_limits(data_asset, active_symbol):
    # Verificar si 'buy_limits' existe y no está vacía
    if 'buy_limits' in data_asset and data_asset['buy_limits']:
        # Obtener las compras pendientes del activo
        buy_limits = data_asset['buy_limits']

        # Ordenar las órdenes por precio de mayor a menor
        buy_limits_sorted = sorted(buy_limits, key=lambda order: order['price'], reverse=True)

        print(f" BUY LIMITS for {active_symbol} ".center(75, '*'))
        print()
        for order in buy_limits_sorted:
            # Asegurarse de que todos los campos existen antes de imprimir
            price = order.get('price', 'N/A')
            amount_usdt = order.get('amount_usdt', 'N/A')
            stop_loss = order.get('stop_loss', 'N/A')
            target = order.get('target', 'N/A')
            quantity = order.get('quantity', 'N/A')
            # Imprimir en pantalla la orden
            print(f"Price: {order['price']} ---> {order['amount_usdt']} USDT, "
                  f"Stop Loss: {order['stop_loss']}, Target: {order['target']}, "
                  f"Quantity: {order['quantity']}")
        print()
    else:
        print(75 * '*')
        print(f"\nNo hay compras pendientes para '{active_symbol}'.\n")


def show_sell_limits(data_asset, active_symbol):
    # Verificar si 'sell_limits' existe y no está vacía
    if 'sell_limits' in data_asset and data_asset['sell_limits']:
        # Obtener las ventas pendientes del activo
        sell_limits = data_asset['sell_limits']

        # Ordenar las órdenes por precio de menor a mayor
        sell_limits_sorted = sorted(sell_limits, key=lambda order: order['price'])

        print(f" SELL LIMITS for {active_symbol} ".center(75, '*'))
        print()
        for order in sell_limits_sorted:
            # Asegurarse de que todos los campos existen antes de imprimir
            price = order.get('price', 'N/A')
            amount_usdt = order.get('amount_usdt', 'N/A')
            stop_loss = order.get('stop_loss', 'N/A')
            target = order.get('target', 'N/A')
            quantity = order.get('quantity', 'N/A')
            # Imprimir en pantalla la orden
            print(f"Price: {order['price']} ---> {order['amount_usdt']} USDT, "
                  f"Stop Loss: {order['stop_loss']}, Target: {order['target']}, "
                  f"Quantity: {order['quantity']}")
        print()
    else:
        print(75 * '*')
        print(f"\nNo hay ventas pendientes para '{active_symbol}'.\n")


def select_price_open_orders(data_asset):
    """Solicita al usuario que ingrese el precio de una orden abierta
    y verifica si existe.

    Returns:
        dict or None: La orden encontrada o None si no existe.
    """
    # Preguntar por el precio
    try:
        price = float(input("Ingrese el precio de la orden: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
        return None

    # Verificar si hay órdenes abiertas
    open_orders = data_asset['open_orders']
    if not open_orders:
        print("No hay órdenes abiertas para este activo.")
        return None  # No hay órdenes abiertas

    # Verificar si existe una orden abierta con el precio especificado
    for order in open_orders:
        if order['price'] == price:
            print(f"\nOrden encontrada: Precio: {order['price']}, Monto USDT: {order['amount_usdt']}")
            return order  # Retorna la orden encontrada

    print("No existe orden abierta en ese precio!")
    return None  # No se encontró ninguna orden con ese precio


def remove_open_order(data, data_asset, active_symbol, filename):
    """Elimina una orden abierta del activo especificado
    y actualiza el archivo JSON.

    Returns:
            dict: El objeto data asset actualizado."""

    # Verificar si 'open_orders' existe y no está vacía
    if 'open_orders' not in data_asset or not data_asset['open_orders']:
        print('*' * 75)
        print("No hay órdenes abiertas disponibles para eliminar.")
        return data_asset  # Salir de la función si no hay órdenes abiertas

    print(f" REMOVE OPEN ORDER {active_symbol} ".center(75, '*'))

    # Seleccionar precio y devolver la orden abierta con dicho precio
    order = select_price_open_orders(data_asset)

    # Verificar si se encontró una orden antes de intentar eliminarla
    if order is not None:
        confirmation = input(f"¿Está seguro de que desea eliminar la orden a {order['price']}? (s/n): ").strip().lower()
        if confirmation == 's':
            try:
                data_asset['open_orders'].remove(order)
                print("OPEN ORDER eliminada!")

                # Actualizar los datos del activo en el objeto data
                save_data_asset(data, data_asset, active_symbol, filename)

            except ValueError:
                print("Error: La orden no se pudo eliminar porque no está en la lista.")
        else:
            print("Eliminación cancelada.")
    else:
        print("No se pudo eliminar la orden porque no fue encontrada.")

    return data_asset  # Devolver el objeto data_asset actualizado


def select_price_buy_limit(data_asset):
    """Solicita al usuario que ingrese el precio de una compra limite
    y verifica si existe.

    Returns:
        dict or None: La orden encontrada o None si no existe.
    """
    # Preguntar por el precio
    try:
        price = float(input("Ingrese el precio de la orden: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
        return None

    # Verificar si hay órdenes limites
    buy_limits = data_asset['buy_limits']
    if not buy_limits:
        print("No hay compras pendientes para este activo.")
        return None  # No hay compras limite

    # Verificar si existe una compra limite con el precio especificado
    for order in buy_limits:
        if order['price'] == price:
            print(f"\nOrden encontrada: Precio: {order['price']}, Monto USDT: {order['amount_usdt']}")
            return order  # Retorna la orden encontrada

    print("No existe BUY LIMIT en ese precio!")
    return None  # No se encontró ninguna orden limite de compra con ese precio


def remove_buy_limit(data, data_asset, active_symbol, filename):
    """Elimina una BUY LIMIT (orden limite de compra)
    del activo especificado y actualiza el archivo JSON.

    Returns:
            dict: El objeto data asset actualizado."""

    # Verificar si 'buy_limits' existe y no está vacía
    if 'buy_limits' not in data_asset or not data_asset['buy_limits']:
        return data_asset  # Salir de la función si no hay órdenes abiertas

    print(f" REMOVE BUY LIMIT {active_symbol} ".center(75, '*'))

    # Seleccionar precio y devolver la 'orden limite' con dicho precio
    order = select_price_buy_limit(data_asset)

    # Verificar si se encontró una orden antes de intentar eliminarla
    if order is not None:
        confirmation = input(
            f"¿Está seguro de que desea eliminar la BUY LIMIT a {order['price']}? (s/n): ").strip().lower()
        if confirmation == 's':
            try:
                data_asset['buy_limits'].remove(order)
                print("BUY LIMIT eliminada!")
                # Actualizar los datos del activo en el objeto data
                save_data_asset(data, data_asset, active_symbol, filename)

            except ValueError:
                print("Error: La orden no se pudo eliminar porque no está en la lista.")

        else:
            print("Eliminación cancelada.")
    else:
        print("No se pudo eliminar la BUY LIMIT porque no fue encontrada.")
        pause_program()
        clear_console()

    return data_asset  # Asegúrate de devolver el objeto actualizado


def select_price_sell_limit(data_asset):
    """Solicita al usuario que ingrese el precio de una venta limite
    y verifica si existe.

    Returns:
        dict or None: La orden encontrada o None si no existe.
    """
    # Preguntar por el precio
    try:
        price = float(input("Ingrese el precio de la orden: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
        return None

    # Verificar si hay órdenes limites
    sell_limits = data_asset['sell_limits']
    if not sell_limits:
        print("No hay ventas pendientes para este activo.")
        return None  # No hay compras limite

    # Verificar si existe una venta limite con el precio especificado
    for order in sell_limits:
        if order['price'] == price:
            print(f"\nOrden encontrada: Precio: {order['price']}, Monto USDT: {order['amount_usdt']}")
            return order  # Retorna la orden encontrada

    print("No existe SELL LIMIT en ese precio!")
    return None  # No se encontró ninguna venta limite de venta con ese precio


def remove_sell_limit(data, data_asset, active_symbol, filename):
    """Elimina una SELL LIMIT (orden limite de venta)
    del activo especificado y actualiza el archivo JSON.

    Returns:
            dict: El objeto data asset actualizado."""

    # Verificar si 'sell_limits' existe y no está vacía
    if 'sell_limits' not in data_asset or not data_asset['sell_limits']:
        return data_asset  # Salir de la función si no hay órdenes de ventas limites

    print(f" REMOVE SELL LIMIT {active_symbol} ".center(75, '*'))

    # Seleccionar precio y devolver la 'sell limit' con dicho precio
    order = select_price_sell_limit(data_asset)

    # Verificar si se encontró una orden antes de intentar eliminarla
    if order is not None:
        confirmation = input(
            f"¿Está seguro de que desea eliminar la SELL LIMIT a {order['price']}? (s/n): ").strip().lower()
        if confirmation == 's':
            try:
                data_asset['sell_limits'].remove(order)
                print("SELL LIMIT eliminada!")
                # Actualizar los datos del activo en el objeto data
                save_data_asset(data, data_asset, active_symbol, filename)

            except ValueError:
                print("Error: La orden no se pudo eliminar porque no está en la lista.")

        else:
            print("Eliminación cancelada.")
    else:
        print("No se pudo eliminar la SEL LIMIT porque no fue encontrada.")

    return data_asset  # Asegúrate de devolver el objeto actualizado


# original
def draw_amounts_and_calculate_total_open_amount2(data):
    # trabajando para actualizar montos mas exactos, basados en cantidad de activo (cant.activo * current_price)
    """Muestra los montos de órdenes madres abiertas,
    en un gráfico de barras y devuelve el total_open_amount"""

    # Crear encabezados
    total_open_amount = 0
    list_amount = []
    list_symbol = []

    # Filtrar órdenes madres en el data
    for symbol, data_asset in data.items():
        if data_asset['open_orders']:
            for order in data_asset['open_orders']:
                if order.get('mother_order', False):
                    list_symbol.append(symbol)
                    # Obtenemos el precio actual para el activo
                    current_price = get_price(symbol)
                    # Calculamos monto en base a la cantidad de activo de la orden madre
                    amount = round(order['quantity'] * current_price)
                    # Agregamos el monto del activo a la lista 'list_amount'
                    list_amount.append(amount)
                    total_open_amount += amount

    if not list_amount:
        print(f"\nNo hay ninguna orden madre guardada!\n")
        return

    # Ordenar símbolos y montos de menor a mayor
    sorted_data = sorted(zip(list_symbol, list_amount), key=lambda x: x[1])
    sorted_symbols, sorted_amounts = zip(*sorted_data)  # Desempaquetar

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

    # Mostrar la cuadrícula de fondo
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Cuadrícula horizontal

    # Mostrar gráfico maximizado
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Maximiza la ventana del gráfico en Windows
    except AttributeError:
        pass  # Si no se puede maximizar, simplemente continúa

    # Mostrar gráfico
    plt.show()

    return int(total_open_amount)


# modificando ok! falta probar que funcione correctamente y adaptar para un metodo de la clase GUI
def draw_amounts_and_calculate_total_open_amount(data):
    # trabajando para actualizar montos mas exactos, basados en cantidad de activo (cant.activo * current_price)
    """Muestra los montos de órdenes abiertas (orden madre + ordenes no madres),
    en un gráfico de barras y devuelve el total_open_amount"""

    total_open_amount = 0
    list_amount = []
    list_symbol = []

    # Filtrar órdenes madres en el data
    for symbol, data_asset in data.items():
        if data_asset['open_orders']:
            total_quantity = 0
            # bucle para calcular la cantidad total del activo
            for order in data_asset['open_orders']:
                quantity = order.get('quantity', 0)
                total_quantity += quantity

            # Obtenemos el precio actual para el activo
            current_price = get_price(symbol)
            # Calculamos monto total del activo en base a la cantidad total de activo
            amount = round(total_quantity * current_price, 2)
            list_amount.append(amount)
            total_open_amount += amount

    if not list_amount:
        print(f"\nNo hay ninguna orden madre guardada!\n")
        return

    # Ordenar símbolos y montos de menor a mayor
    sorted_data = sorted(zip(list_symbol, list_amount), key=lambda x: x[1])
    sorted_symbols, sorted_amounts = zip(*sorted_data)  # Desempaquetar

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

    # Mostrar la cuadrícula de fondo
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Cuadrícula horizontal

    # Mostrar gráfico maximizado
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Maximiza la ventana del gráfico en Windows
    except AttributeError:
        pass  # Si no se puede maximizar, simplemente continúa

    # Mostrar gráfico
    plt.show()

    return int(total_open_amount)


def calculate_leverage(total_open_amount):
    print(" Calculate LEVERAGE ".center(75, '*'))
    print(f"\nTotal OPEN AMOUNT: {total_open_amount} USDT")

    # Manejo de errores al ingresar la cuenta de trading
    try:
        trading_account = float(input("Trading Account: "))
        if trading_account <= 0:
            raise ValueError("La cuenta de trading debe ser mayor que cero.")
    except ValueError as e:
        print(f"Error: {e}")
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

    pause_program()

    # Crear gráfico
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(leverage_levels))

    # Gráficos de barras
    bars1 = plt.bar(x, leveraged_amounts, width=bar_width, label='Leveraged Amount', color='blue', alpha=0.6)

    bars2 = plt.bar([i + bar_width for i in x], reduce_positions, width=bar_width,
                    label='Reduce Position USDT',
                    color=['red' if reduce <= 0 else 'forestgreen' for reduce in reduce_positions], alpha=0.6)

    # Añadir etiquetas sobre cada barra
    for bar1, bar2, leverage in zip(bars1, bars2, leverage_levels):
        plt.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height(),
                 f"X {leverage}\n{bar1.get_height()} USDT",
                 ha='center', va='bottom', fontsize=11, weight='bold')

        plt.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height(),
                 f"{bar2.get_height()} USDT",
                 ha='center', va='bottom', fontsize=11, weight='bold')

    # Etiquetas y título
    plt.xlabel('Leverage')
    plt.ylabel('Amount (USDT)')
    plt.title(
        f'Leveraged Amount and Reduce Position by Leverage Level\nTOTAL OPEN AMOUNT: {total_open_amount}\nTRADING ACCOUNT: {trading_account}\nLEVERAGE: {leveragex}')
    plt.xticks([i + bar_width / 2 for i in x], leverage_levels)
    plt.legend()

    plt.tight_layout()

    # Mostrar la cuadrícula de fondo
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Cuadrícula horizontal

    # Mostrar gráfico maximizado
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Maximiza la ventana del gráfico en Windows
    except AttributeError:
        pass  # Si no se puede maximizar, simplemente continúa

    # Mostrar gráfico
    plt.show()


def show_and_update_current_price(data_asset, active_symbol):
    """Muestra el precio actual del activo especificado y
    pregunta al usuario si desea actualizarlo.

    Imprime el precio actual del activo y solicita al usuario
    si desea realizar una actualización.
    Si el usuario elige actualizar, se llama a la función `choose_current_price`
    para obtener el nuevo precio.

    Parameters:
    ----------
    data_asset : dict
        El diccionario que contiene la información del activo, incluyendo el precio actual.

    active_symbol : str
        El símbolo del activo cuyo precio se está mostrando y actualizando.

    Returns:
    -------
    dict
        Devuelve el objeto data_asset actualizado, incluyendo el nuevo precio.
    """

    # Mostrar el precio actual
    current_price = data_asset['current_price']
    print('*' * 75)
    print(f"\nCURRENT PRICE {active_symbol}: {current_price}\n")

    # Preguntar al usuario si desea actualizar el precio
    update = input("¿Desea actualizar el precio? (s/n): ").strip().lower()

    if update == 's':
        clear_console()
        try:
            # se llama a esta funcion para determinar el current price del activo
            new_price = choose_current_price(active_symbol)  # Asumiendo que esta función devuelve un nuevo precio
            # Verificar si new_price es None
            if new_price is None:
                print("No se pudo establecer un CURRENT PRICE")
                return data_asset

            # Actualizar el current_price en data_asset
            data_asset['current_price'] = new_price
            print(f"\nCURRENT PRICE {active_symbol} ha sido actualizado a {new_price}.\n")
            return data_asset  # Devolver el objeto data_asset actualizado

        except ValueError:
            print("Error: Debe introducir un número válido para el nuevo precio.")

    else:
        print('*' * 75)
        print("\nNo se ha realizado ninguna actualización\n")
        return data_asset


def remove_asset(data, active_symbol, filename):
    """Pregunta al usuario si desea eliminar el activo,
    y Elimina un activo del diccionario de data

    Parámetros:
    ----------
    data : dict
        El diccionario que contiene información sobre diferentes activos.

    active_symbol : str
        El símbolo del activo que se desea eliminar.

    filename : str
        El nombre del archivo JSON donde se guardan los datos.
    """
    print(f" {active_symbol} ".center(75, '*'))
    while True:
        response = input("\nEsta seguro que desea eliminar el activo (s/n): ").strip().lower()

        if response == 's':
            # Verificar si el símbolo existe en los datos
            if active_symbol in data:
                del data[active_symbol]  # Eliminar el activo del diccionario
                print(f"\n{active_symbol} ha sido eliminado!\n")
                print("*" * 75)

                # Guardar cambios en el archivo JSON
                save_data(data, filename)  # Asegúrate de que esta función esté definida
                break

            else:
                print(f"Error: '{active_symbol}' no existe en los datos.")

        elif response == 'n':
            print(f"Se mantuvo el activo {active_symbol}!\n")
            break

        else:
            print("Selecione un opción válida!")


def calculate_mother_order(active_symbol):
    """
    Calcula  precio mother order.

    Parámetros:
    ----------
    data_asset : dict
        Diccionario que contiene información sobre las órdenes abiertas y otros datos del activo.

    active_symbol : str
        Símbolo del activo para el cual se está calculando la orden madre.

    Retorna:
    -------
    tuple
        Una tupla que contiene:
        - open_psotion_usdt (float): Monto Inicial de la orden madre.
        - price_mother_order (float): Precio de entrada de la orden madre.
        - quantity_mother_order(float): cantidad de activo de la orden madre
    """

    print(" Calculate MOTHER ORDER ".center(75, '*'))

    average_purchase_price = float(input("Average price: "))
    open_position_usdt = float(input("Open Position USDT: "))
    profits_taken = float(input("Profit Taken: "))
    quantity_mother_order = float(input("Quantity: "))

    # Calcular el precio orden madre
    price_mother_order = average_purchase_price - (profits_taken / quantity_mother_order)
    price_mother_order_rounded = round(price_mother_order, 3)

    print(f"\nAMOUNT Mother Order {active_symbol}: {open_position_usdt} USDT")
    print(f"PRICE Mother Order {active_symbol}: {price_mother_order_rounded}")
    print(f"QUANTITY Mother Order: {quantity_mother_order}")

    return open_position_usdt, price_mother_order_rounded, quantity_mother_order


def update_and_save_mother_order(data, data_asset, amount_usdt_mother_order, price_mother_order, quantity_mother_order,
                                 active_symbol,
                                 filename):
    """Pregunta al usuario si desea actualizar y guardar mother order.

    Parámetros:
    data (dict): El diccionario que contiene los datos generales.
    data_asset (dict): El diccionario que contiene los datos a actualizar y guardar.
    active_symbol (str): El símbolo activo relacionado con la orden.
    filename (str): El nombre del archivo donde se guardan los datos.
    """

    mother_order_found = False  # Variable para rastrear si se encontró una orden madre

    if data_asset['open_orders']:
        for order in data_asset['open_orders']:
            if order.get('mother_order', False):  # Usar get para evitar KeyError
                mother_order_found = True
                print("Existencia de una MOTHER ORDER!")
                response = input("¿Deseas actualizar MOTHER ORDER? (s/n): ").strip().lower()
                if response == 's':
                    # Eliminar la orden madre vieja
                    data_asset['open_orders'].remove(order)  # Elimina la orden madre
                    break  # Salir del bucle después de encontrar y eliminar la orden madre

    if not mother_order_found:
        print("NO hay MOTHER ORDER")
        response = input("¿Deseas guardar MOTHER ORDER? (s/n): ").strip().lower()

    if response == 's':
        new_mother_order = {
            'price': price_mother_order,
            'amount_usdt': amount_usdt_mother_order,
            'quantity': quantity_mother_order,
            'stop_loss': 0,
            'target': 0,
            'mother_order': True
        }

        data_asset['open_orders'].append(new_mother_order)  # Agrega la nueva 'Mother Order' a 'Open Orders'

        # Guardar el data_asset en 'filename' (archivo JSON)
        save_data_asset(data, data_asset, active_symbol, filename)
        print("MOTHER ORDER actualizada exitosamente!")


def get_purchase_parameters():
    """Solicita al usuario los parámetros para generar niveles de compra,
    para crear la denominada 'PINK NET'

    Retorno:
    -------
    tuple
        Una tupla que contiene el número de niveles, el precio inicial del nivel,
        el precio final del nivel y el monto destinado a invertir
    """

    while True:
        try:
            levels = int(input("\nNúmero de LEVELS a generar: "))
            if levels <= 0:
                print("Por favor, introduce un número entero positivo para los niveles.")
                continue

            initial_level = float(input("Precio del nivel inicial: "))
            final_level = float(input("Precio del nivel final: "))
            investment_amount = float(input("Monto disponible a invertir: "))
            break  # Salir del bucle si todo es correcto

        except ValueError:
            print(
                "Entrada no válida. Asegúrate de introducir un número entero para los niveles y un número decimal para el nivel inicial y nivel final")

    return levels, initial_level, final_level, investment_amount


def generate_pink_net(levels, initial_level, final_level, investment_amount):
    """Genera una serie de niveles de precios para comprar un activo.
    La denominada PINK NET
    Parámetros:
    ----------
    levels : int  Cantidad de niveles a generar.

    initial_level : float  El precio del nivel inicial.

    final_level : float  El precio del nivel final.

    investment_amount : float  Monto total a invertir en los niveles.

    Retorno:
    -------
    list
        Una lista de diccionarios que representan los niveles de compra.
        La 'PINK NET'
    """

    pink_net = []  # Lista para almacenar los niveles de compra

    # Calcular el rango entre el precio inicial y el precio final
    price_range = initial_level - final_level

    # Calcular el incremento por nivel
    if levels > 1:
        increment = price_range / (levels - 1)  # Dividir el rango en partes iguales
    else:
        increment = 0  # Si solo hay un nivel, no hay incremento

    # Calcular cuánto se invertirá en cada nivel
    amount_per_level = investment_amount / levels

    # Generar los niveles
    for i in range(levels):
        price = initial_level - i * increment  # Calcular el precio del nivel

        # Calcular la cantidad de activos que se pueden comprar en este nivel
        quantity = amount_per_level / price if price > 0 else 0

        # Crear el diccionario para el nivel
        level_pink_net = {
            'price': round(price, 3),  # Redondear a dos decimales
            'amount_usdt': round(amount_per_level, 2),  # Monto a invertir en este nivel
            'quantity': round(quantity, 5),  # Redondear a cuatro decimales
            'stop_loss': 0,
            'target': 0,
        }

        pink_net.append(level_pink_net)  # Añadir el nivel a la lista

    return pink_net


# (la original era show_trading_account_and_margins) NO TIENE USO EN EL PROGRAMA!
def create_list_with_mother_order(data):
    """crea una lista de activos que tienen abierta una orden madre"""

    # verificar si existen activos
    if not data:
        print("No hay activos guardados!\n")
        pause_program()
        clear_console()

    # el total de los margenes seria trading account
    list_symbol = []
    # si existe una orden madre se agrega el symbol a la lista
    for symbol, data_asset in data.items():
        for order in data_asset['open_orders']:
            if order['mother_order']:
                list_symbol.append(symbol)

    return list_symbol

def list_of_symbols_with_open_order_or_buy_limit(data):
    """crea una lista de activos que contiene al menos
    una OPEN ORDER o BUY LIMIT"""

    # verificar si existen activos
    if not data:
        print("No hay activos guardados!\n")

    list_symbol = []

    for symbol, data_asset in data.items():
        if data_asset['open_orders'] or data_asset['buy_limits']:
            list_symbol.append(symbol)

    return list_symbol

def get_symbols_for_buttons(data):
    """crea una lista de los simbolos de los activos que se encuentran en data
    para crear los botones en el panel asset_menu"""

    list_symbol = []
    for symbol, data_asset in data.items():
        list_symbol.append(symbol)

    return list_symbol


def show_margins_and_total(data):
    # calcular total de margenes almacenados
    total_margin = 0
    for symbol, data_asset in data.items():
        margin = data_asset['margin']
        total_margin += margin

    # Crear encabezados
    print(f"{'Symbol':<15} {'MARGIN (USDT)':<15} {'Weight':<10}")
    print('-' * 40)  # Línea separadora
    # Calcular ponderacion en base al margin y cuenta de trading
    for symbol, data_asset in data.items():
        margin = data_asset['margin']
        ponderacion = round(margin / total_margin, 3)
        print(f"{symbol:<15} {data_asset['margin']:<15} {ponderacion:<10}")

    print(f"\nTOTAL MARGINS: {total_margin}")


def calculate_margins(data):
    """calcula margen de capital destinado a tolerar perdidas
     para cada activo del data, por medio de ponderacion equitativa
     o no equitativa.
     Calcula ponderaciones automaticamente, asigna 'margin' a cada activo
     y los guarda en el diccionario 'data'"""
    # verificar si existen activos
    if not data:
        print("No hay activos guardados!\n")
        pause_program()
        clear_console()

    num_assets = 0
    for symbol, data_asest in data.items():
        if symbol:
            num_assets += 1

    # Mostrar opciones
    print(" CALCULATE ASSET MARGIN ".center(75, '*'))
    print("\n1 - División Equitativa ")
    print("2 - Ponderación NO equitativa")
    print("3 - Volver al menú principal")

    while True:
        # Inicializar la variable de respuesta
        response = input("\nElige una opción (1, 2 o 3): ")

        if response not in ['1', '2', '3']:
            print("Opción no válida. Elige 1, 2 o 3.")

        elif response == '1':
            clear_console()
            print(" ASSET MARGIN - División Equitativa ".center(75, '*'))
            trading_account = float(input("Monto Cuenta de Trading: "))
            # calculo de margin de forma equitativa
            margin = round(trading_account / num_assets, 2)
            # calculo ponderacion
            ponderacion = round(margin / trading_account, 3)
            # Crear encabezados
            print(f"\n{'Symbol':<15} {'MARGIN (USDT)':<15} {'Weight':<10}")
            for symbol, data_asset in data.items():
                # Asigno el margin a cada activo
                data_asset['margin'] = margin
                print(f"{symbol:<15} {margin:<15} {ponderacion:<10}")

            # guarda data actualizado
            save_data(data, filename)

            pause_program()
            clear_console()
            break

        elif response == '2':
            clear_console()
            print(" ASSET MARGIN - Ponderacion ".center(75, '*'))

            trading_account = float(input("Trading Account: "))

            total_usdt_open_positions = 0
            list_amounts = []
            for asset, data_asset in data.items():
                amount_asset = float(input(f"Posicion abierta de {asset}: "))
                list_amounts.append(amount_asset)
                total_usdt_open_positions += amount_asset

            # Verificar que hay posiciones abiertas antes de calcular ponderaciones
            if total_usdt_open_positions > 0:
                clear_console()
                print(" ASSET MARGIN - Ponderacion ".center(75, '*'))
                # Crear encabezados
                print(f"\n{'Symbol':<15} {'MARGIN (USDT)':<15} {'Weight':<10}")
                # Recorrer los datos y calcular las ponderación
                for (symbol, data_asset), amount_asset in zip(data.items(), list_amounts):
                    weight = round(amount_asset / total_usdt_open_positions, 3)
                    margin = round(trading_account * weight)
                    data_asset['margin'] = margin
                    print(f"{symbol:<15} {margin:<15} {weight:<10}")

                # Guardar 'data'
                save_data(data, filename)
                print("\nMárgenes asignados y guardados!")
                pause_program()
                clear_console()
                break
            else:
                print("Error: No hay posiciones abiertas para calcular ponderaciones.")
                pause_program()

        elif response == '3':
            clear_console()
            break


# revisar que diferencia hay entra esta funcion y 'update burn prices'
def calculate_burn_price(active_symbol, data_asset, current_price):
    """calcula el precio de quema del activo"""
    margin = data_asset['margin']
    print(f" BURN PRICE SUMMARY {active_symbol} ".center(75, '*'))
    print("Advertencia: tener actualizada la orden madre si la hubiese y MARGIN!\n")
    print(f"CURRENT PRICE: {current_price}")
    print(f"MARGIN: {margin} USDT")

    quantity_mother_order = 0
    mother_order_found = False
    # Verificamos si existe la orden madre
    for key, value in data_asset.items():
        if key == 'open_orders':
            for order in value:
                if order.get('mother_order', False):  # Usamos get para evitar errores si 'mother_order' no existe
                    quantity_mother_order = order['quantity']
                    mother_order_found = True  # Marcamos que encontramos una orden madre
                    break  # Salimos del bucle si encontramos una orden madre

        if mother_order_found:  # Si encontramos una orden madre, salimos del bucle externo también
            break

    # Verificamos si no se encontró ninguna orden madre
    if not mother_order_found:
        print("No hay MOTHER ORDER!")

    total_amount_buy_limits = 0
    total_quantity_buy_limits = 0

    # verificamos si existen ordenes buy limits
    if data_asset['buy_limits']:
        # obtenemos el monto total y cantidad total  de todas las orden limites
        for order in data_asset['buy_limits']:
            amount = order['amount_usdt']
            total_amount_buy_limits += amount
            quantity = order['quantity']
            total_quantity_buy_limits += quantity
    else:
        print("No hay BUY LIMITS!")

    print(f"total quantity buy limits: {total_quantity_buy_limits}")
    print(f"total amounts buy limits: {total_amount_buy_limits}")

    # Calculamos total de activo (de mother order y buy limits)
    total_quantity = quantity_mother_order + total_quantity_buy_limits
    # asegurarse de que el total quantity no sea igual a 0
    if total_quantity == 0:
        print("No se puede calcular BURN PRICE porque la cantidad de activo es CERO")

    else:
        # Calculamos BURN PRICE
        burn_price = ((current_price * quantity_mother_order) + total_amount_buy_limits - margin) / total_quantity
        print(f"\nBURN PRICE: {round(burn_price, 3)} USDT\n")


def get_sales_parameters():
    """Solicita al usuario los parámetros para generar niveles de ventas,
    para crear la denominada 'SALE CLOUD' (nube de ventas)

    Retorno:
    -------
    tuple
        Una tupla que contiene el número de niveles, el precio inicial del nivel de venta,
        el precio final del nivel de venta y el monto total a reducir posiciones
    """

    while True:
        try:
            print(" Generate SALES CLOUD ".center(75, '*'))
            levels = int(input("\nNúmero de LEVELS a generar: "))
            if levels <= 0:
                print("Por favor, introduce un número entero positivo para los niveles.")
                continue

            initial_level = float(input("Precio del nivel inicial: "))
            final_level = float(input("Precio del nivel final: "))
            withdrawal_amount = float(input("Monto a reducir: "))
            break  # Salir del bucle si todo es correcto

        except ValueError:
            print(
                "Entrada no válida. Asegúrate de introducir un número entero para los niveles y un número decimal para el nivel inicial y nivel final")

    return levels, initial_level, final_level, withdrawal_amount


def generate_sales_cloud(levels, initial_level, final_level, withdrawal_amount):
    """Genera una serie de niveles de precios para vender un activo.
    La denominada 'NUBE DE VENTAS'.
    Parámetros:
    ----------
    levels : int  Cantidad de niveles a generar.

    initial_level : float  El precio del nivel inicial (primer nivel de venta)

    final_level : float  El precio del nivel final (ultimo nivel de venta)

    withdrawal_amount : float  Monto total a reducir (en dolares)

    Retorno:
    -------
    list
        Una lista de diccionarios que representan los niveles de venta.
    """

    sales_cloud = []  # Lista para almacenar los niveles de venta 'NUBE DE VENTAS'

    # Calcular el rango entre el precio inicial y el precio final
    price_range = final_level - initial_level

    # Calcular el incremento por nivel
    if levels > 1:
        increment = price_range / (levels - 1)  # Dividir el rango en partes iguales
    else:
        increment = 0  # Si solo hay un nivel, no hay incremento

    # Calcular cuánto se invertirá en cada nivel
    amount_per_level = withdrawal_amount / levels

    # Generar los niveles
    for i in range(levels):
        price = initial_level + i * increment  # Calcular el precio del nivel

        # Calcular la cantidad de activos que se pueden vender en este nivel
        quantity = amount_per_level / price if price > 0 else 0

        # Crear el diccionario para el nivel
        level_cloud = {
            'price': round(price, 3),  # Redondear a dos decimales
            'amount_usdt': round(amount_per_level, 2),  # Monto a invertir en este nivel
            'quantity': round(quantity, 5),  # Redondear a cuatro decimales
            'stop_loss': 0,
            'target': 0,
        }

        sales_cloud.append(level_cloud)  # Añadir el nivel a la lista

    return sales_cloud


def update_burn_prices(data, list_symbol):
    """toma la lista de simbolos que tienen operaciones abiertas
    o compras limites y sobre esos activos se calcula el
    burn_price respectivo"""

    for symbol, data_asset in data.items():
        if symbol in list_symbol:
            current_price = get_price(symbol)
            calculate_burn_price(symbol, data_asset, current_price)


def calculate_and_show_all_burning_prices():
    """calcula y muestra el precio de quema de todos los activos.
    Se ejecuta desde el menu primario"""
    while True:
        response = input("\nHas actualizado los MARGINS? (s/n):").strip().lower()
        if response == 's':
            list_symbol = list_of_symbols_with_open_order_or_buy_limit(data)
            update_burn_prices(data, list_symbol)
            pause_program()
            break

        elif response == 'n':
            print("Debes actualizar los MARGINS!")
            pause_program()
            break
        else:
            print("No es una opción valida!")


data = load_data(filename)
data = order_orders(data)



def main():  # Función principal para ejecutar el flujo del programa
    global data  # Declarar que vamos a usar la variable global data

    while True:
        # Mostrar activos disponibles o agregar uno nuevo
        print(" Seleccione un Activo o Agrege uno nuevo ".center(75, '*'))
        for symbol in data.keys():
            print(f"{symbol}")

        print("1:  ADD new symbol")
        print("2:  Show MARGINS")
        print("3:  Update MARGINS")
        print("4:  Mostrar POSICIONES ABIERTAS")
        print("5:  Calcular LEVERAGE")
        print("6:  Calculate BURN PRICE")
        print("7:  EXIT\n")

        active_symbol = input("Selecciona un activo o una opción (1-6): ").strip().upper()

        if active_symbol == '1':
            clear_console()
            print(" NEW ASSET ".center(75, '*'))
            new_symbol = input("\nIntroduce el nuevo símbolo: ").strip().upper()
            # Lógica para asegurarte de que el símbolo no exista ya en tus datos
            if new_symbol in data:
                print(f"El símbolo '{new_symbol}' ya existe.")
                continue
            # Agregar el nuevo símbolo e inicializar su diccionario
            else:
                clear_console()  # limpiar pantalla
                data[new_symbol] = {
                    "current_price": 0,  # O cualquier otro valor inicial que necesites
                    "margin": 0,
                    "open_orders": [],
                    "buy_limits": [],
                    "sell_limits": []}

                # Se asigna la inicializacion del nuevo diccionario a 'data_asset'
                # data_asset = data[new_symbol]

                # Guardar el nuevo asset
                save_data_asset(data, data[new_symbol], new_symbol, filename)
                print('*' * 75)
                print(f"\nSímbolo '{new_symbol}' agregado.\n")
                continue

        elif active_symbol == '2':
            clear_console()
            show_margins_and_total(data)
            pause_program()

        elif active_symbol == '3':
            clear_console()
            calculate_margins(data)

        elif active_symbol == '4':
            clear_console()
            total_open_amount = draw_amounts_and_calculate_total_open_amount(data)

        elif active_symbol == '5':
            clear_console()
            total_open_amount = draw_amounts_and_calculate_total_open_amount(data)
            calculate_leverage(total_open_amount)

        elif active_symbol == '6':
            clear_console()
            while True:
                response = input("\nHas actualizado los MARGINS? (s/n):").strip().lower()
                if response == 's':
                    list_symbol = list_of_symbols_with_open_order_or_buy_limit(data)
                    update_burn_prices(data, list_symbol)
                    pause_program()
                    break

                elif response == 'n':
                    print("Debes actualizar los MARGINS!")
                    pause_program()
                    break
                else:
                    print("No es una opción valida!")

        elif active_symbol == '7':
            print("...Saliendo del programa!")
            break

        elif active_symbol not in data:
            clear_console()
            print('*' * 75)
            print("\nOpción no válida. Intenta de nuevo.\n")
            continue  # Volver al inicio del bucle

        else:
            # Obtener los datos del activo seleccionado
            data_asset = data[active_symbol]
            # Verificar si data_asset es None
            if data_asset is None:
                print(f"Advertencia: '{active_symbol}' NO está inicializado! (NULL)\n")
                loading_animation(5)

                # Inicializar el activo
                data[active_symbol] = {
                    "current_price": 0,
                    "margin": 0,
                    "open_orders": [],
                    "buy_limits": [],
                    "sell_limits": []
                }

                # Guardar los cambios en el archivo JSON si es necesario
                save_data_asset(data, data[active_symbol], active_symbol, filename)

                continue  # Volver al inicio del bucle
            clear_console()

            while True:
                # Muestra el menú de opciones al usuario
                print(f" {active_symbol} ".center(75, '*'))
                print("\n1. Add OPEN ORDER")
                print("2. Add BUY LIMIT")
                print("3. Add SELL LIMIT")
                print("4. Show OPEN ORDERS")
                print("5. Show BUY LIMITS")
                print("6. Show SELL LIMITS ")
                print("7. Delete OPEN ORDER")
                print("8. Delete BUY LIMIT")
                print("9. Delete SELL LIMIT")
                print("10. Delete ASSET")
                print("11. Calculate MOTHER ORDER")
                print("12. Generate PINK NET")
                print("13. Calculate BURN PRICE")
                print("14. Generate SALES CLOUD")
                print("15. Render OPEN ORDERS")
                print("16. Update CURRENT PRICE")
                print("17. Volver")
                opcion = input("Selecciona una opción (1-17): ")

                if opcion == '1':
                    clear_console()
                    add_open_order(data_asset, active_symbol)
                    save_data_asset(data, data_asset, active_symbol,
                                    filename)  # Guardar cambios después de cada adición"""

                elif opcion == '2':
                    clear_console()
                    add_buy_limit(data_asset)
                    save_data_asset(data, data_asset, active_symbol,
                                    filename)  # Guardar cambios después de cada adición"""

                elif opcion == '3':
                    clear_console()
                    add_sell_limit(data_asset, active_symbol)
                    save_data_asset(data, data_asset, active_symbol, filename)

                elif opcion == '4':
                    clear_console()
                    show_open_orders(data_asset, active_symbol)
                    pause_program()

                elif opcion == '5':
                    clear_console()
                    show_buy_limits(data_asset, active_symbol)
                    pause_program()
                    clear_console()

                elif opcion == '6':
                    clear_console()
                    show_sell_limits(data_asset, active_symbol)
                    pause_program()

                elif opcion == '7':
                    clear_console()
                    show_open_orders(data_asset, active_symbol)
                    data_asset = remove_open_order(data, data_asset, active_symbol, filename)
                    pause_program()

                elif opcion == '8':
                    clear_console()
                    show_buy_limits(data_asset, active_symbol)
                    data_asset = remove_buy_limit(data, data_asset, active_symbol, filename)
                    pause_program()

                elif opcion == '9':
                    clear_console()
                    show_sell_limits(data_asset, active_symbol)
                    data_asset = remove_sell_limit(data, data_asset, active_symbol, filename)
                    pause_program()
                    clear_console()

                elif opcion == '10':
                    clear_console()
                    remove_asset(data, active_symbol, filename)
                    pause_program()
                    clear_console()
                    print("...Volviendo al menú principal")
                    break

                elif opcion == '11':
                    clear_console()
                    amount_usdt_mother_order, price_mother_order, quantity_mother_order = calculate_mother_order(
                        active_symbol)
                    update_and_save_mother_order(data, data_asset, amount_usdt_mother_order, price_mother_order,
                                                 quantity_mother_order, active_symbol, filename)

                elif opcion == '12':
                    clear_console()
                    print(" CREATE PINK NET ".center(75, '*'))
                    levels, initial_level, final_level, investment_amount = get_purchase_parameters()
                    pink_net = generate_pink_net(levels, initial_level, final_level, investment_amount)
                    for level in pink_net:
                        print(level)

                    # Preguntar al usuario si desea guardar los niveles de compra
                    save_choice = input("¿Deseas guardar los niveles de compra? (s/n): ").strip().lower()

                    if save_choice == 's':
                        """RECORDATORIO: Cuando se crea una Pink Net nueva y se decide guardarla,
                         si existian BUY LIMITS, las sobreescribe!"""
                        # Actualizar la 'buy limits' del 'data_asset'con las 'purchase_levels'
                        data_asset['buy_limits'] = pink_net
                        save_data_asset(data, data_asset, active_symbol, filename)
                        print("\nLa 'PINK NET' se ha guardado en BUY LIMITS!")

                    elif save_choice == 'n':
                        print("No se guardaron los niveles de compra.")
                    else:
                        print("Opción no válida. Por favor, introduce 's' o 'n'")

                elif opcion == '13':
                    clear_console()
                    current_price = get_price(active_symbol)
                    if current_price:
                        calculate_burn_price(active_symbol, data_asset, current_price)
                    elif current_price == None:
                        current_price = -1  # Inicializar a un valor negativo para entrar en el bucle
                        while current_price <= 0:  # Continuar mientras el precio no sea positivo
                            try:
                                current_price = float(input("Ingrese CURRENT PRICE manualmente: "))
                                if current_price <= 0:
                                    print("Debe ingresar un número positivo.")

                            except ValueError:
                                print("Entrada no válida. Por favor, ingrese un número.")

                        calculate_burn_price(active_symbol, data_asset, current_price)

                    pause_program()

                elif opcion == '14':
                    clear_console()
                    levels, initial_level, final_level, withdrawal_amount = get_sales_parameters()
                    sales_cloud = generate_sales_cloud(levels, initial_level, final_level, withdrawal_amount)
                    for sell_level in sales_cloud:
                        print(sell_level)

                    # Preguntar al usuario si desea guardar los niveles de venta
                    save_choice = input("¿Deseas guardar los niveles de venta? (s/n): ").strip().lower()

                    if save_choice == 's':
                        """RECORDATORIO: Cuando se crea una SALES CLOUD nueva y se decide guardarla,
                         si existian SELL LIMITS, las sobreescribe!"""
                        # Actualizar la 'sell limits' del 'data_asset'con las 'sales_cloud' (lista de ventas limites)
                        data_asset['sell_limits'] = sales_cloud
                        save_data_asset(data, data_asset, active_symbol, filename)
                        print("\nLa 'SALES CLOUD' se ha guardado en SELL LIMITS!")

                    elif save_choice == 'n':
                        print("No se guardaron los niveles de ventas.")
                    else:
                        print("Opción no válida. Por favor, introduce 's' o 'n'")

                elif opcion == '15':
                    clear_console()
                    current_price = get_price(active_symbol)
                    if current_price:
                        plot_open_orders(data_asset, current_price, active_symbol)
                    elif current_price == None:
                        current_price = data_asset['current_price']
                        # Verificar si el precio actual es cero
                        if current_price == 0:
                            print(f" {active_symbol} ".center(75, '*'))
                            print("\nCURRENT PRICE no está establecido (valor en cero)\n")
                            # Llamar a la función para establecer el precio
                            current_price = choose_current_price(active_symbol)

                            # Verificar si el nuevo precio es válido
                            if current_price <= 0:
                                print("El precio debe ser un número positivo. No se puede continuar.")
                                return  # Salir de la opción sin graficar
                            else:
                                data_asset['current_price'] = current_price
                                plot_open_orders(data_asset, current_price, active_symbol)
                                # Actualiza y guarda data_asset con el nuevo valor de current price
                                save_data_asset(data, data_asset, active_symbol, filename)
                                print(
                                    f"\nCURRENT PRICE {active_symbol}: {round(current_price, 3)} USDT ...actualizado y guardado!\n")
                                pause_program()
                                clear_console()
                        else:
                            print("Existe Current price almacenado (No actualizado!)")
                            print(f"CURRENT PRICE for {active_symbol}: {current_price} USDT")
                            pause_program()
                            plot_open_orders(data_asset, current_price, active_symbol)

                elif opcion == '16':
                    clear_console()
                    data_asset = show_and_update_current_price(data_asset, active_symbol)
                    save_data_asset(data, data_asset, active_symbol, filename)
                    pause_program()

                elif opcion == '17':
                    clear_console()
                    print("...Volviendo al menú principal")
                    break

                else:
                    print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()