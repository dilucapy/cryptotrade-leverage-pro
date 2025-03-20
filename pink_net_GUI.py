from tkinter import *

# Iniciar Tkinter
app = Tk()

# Tamaño de la ventana
app.geometry('1020x630+0+0')

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

title_label.grid(row=0, column=0)

# Panel Izquierdo
left_panel = Frame(app, bd=1, relief=FLAT)
left_panel.pack(side=LEFT)

# Menu Primario
primary_menu = Frame(left_panel, bd=1, relief=FLAT)
primary_menu.pack(side=BOTTOM)

# Botones Menu Primario
primary_buttons = ["ADD new symbol",
                   "Show MARGINS",
                   "Update MARGINS",
                   "Mostrar POSICIONES ABIERTAS",
                   "Calcular LEVERAGE",
                   "Calculate BURN PRICE",
                   "EXIT"]

row_number = 0
for button in primary_buttons:
    button = Button(primary_menu,
                    text=button.title(),
                    font=('Dosis', 12, 'bold'),
                    bd=1,
                    fg='white',
                    bg='azure4',
                    width=24,
                    relief=RAISED,
                    pady=5,
                    cursor='hand2')

    button.grid(row=row_number,
                column=0)

    row_number += 1

# Menu Assets
asset_menu = Frame(left_panel, bd=1, relief=FLAT)
asset_menu.pack(side=TOP)

# Panel Derecho
right_panel = Frame(app, bd=1, relief=FLAT)
right_panel.pack(side=RIGHT)

# Menu secundario
secondary_menu = Frame(right_panel, bd=1, relief=FLAT)
secondary_menu.pack()










# Evitar que la pantalla se cierre
app.mainloop()



