# CryptoTrade Leverage Pro

---

## Herramienta para la Gestión Inteligente de Operaciones Apalancadas

¡Hola a todos!

Les presento **CryptoTrade Leverage Pro**, mi primer proyecto completo, diseñado con entusiasmo y dedicación para ofrecer una solución práctica y eficiente a la gestión de operaciones apalancadas en el mercado de criptomonedas.

Este proyecto no solo refleja mis habilidades como programador, sino también mi pasión por el trading y mi compromiso de crear herramientas que faciliten la vida de otros traders.

¡Espero que les guste y les sea de gran utilidad!

---

## Introducción

**CryptoTrade Leverage Pro** es una herramienta de escritorio desarrollada en **Python con Tkinter**, diseñada para traders de criptomonedas que buscan optimizar y gestionar sus operaciones apalancadas. En un mercado tan volátil y emocionante como el de las criptomonedas, el apalancamiento ofrece oportunidades significativas, pero también exige una gestión cuidadosa del riesgo. Esta aplicación te proporciona las funcionalidades esenciales para tomar decisiones informadas y mantener el control de tus inversiones.

El **apalancamiento**, los **márgenes** y la **liquidación** son conceptos cruciales en el trading:

* Con el **apalancamiento**, los inversores pueden operar con sumas mayores a las que realmente poseen.
* El **margen** representa el capital necesario para iniciar y sostener una operación apalancada.
* La **liquidación** ocurre cuando el margen de un trader cae por debajo de un nivel crítico, resultando en el cierre forzado de la posición para prevenir pérdidas mayores.

Los traders pueden tomar posiciones "Long" (apostando a que el precio subirá) o "Short" (apostando a que el precio bajará).

---

## Esta Herramienta Trabaja en Sinergia con:

* **TradingView**: Para el **análisis técnico avanzado**. Visualiza gráficos profesionales de velas japonesas, con opción de agregar indicadores y dibujar líneas horizontales para planificar tus órdenes.
* **Quantfury**: El **bróker donde se ejecutan las operaciones**. Quantfury es conocido por su popularidad, confiabilidad, seguridad, bajos costos y precios de mercado transparentes, derivados de la cotización de Binance en tiempo real. ¡Si aún no lo conoces, te invito a explorar sus ventajas y a registrarte!

---

## ¿A Quién Está Dirigida?

Esta herramienta está diseñada para:

* **Traders de criptomonedas**: Que buscan una forma eficiente de gestionar sus operaciones apalancadas.
    * Se recomienda especialmente a los principiantes comenzar con un apalancamiento bajo o nulo. Operar sin apalancamiento implica simplemente comprar o vender criptoactivos con el capital disponible, sin tomar prestados fondos adicionales. Por ejemplo, si tienes una cuenta de trading con 100 USDT, puedes abrir posiciones hasta 100 USDT (ej. una compra de $100 de Bitcoin). Esto minimiza el riesgo y permite a los nuevos traders familiarizarse con la dinámica del mercado antes de incursionar en operaciones más complejas.
* **Reclutadores y empresas**: Que buscan programadores con experiencia práctica en el desarrollo de aplicaciones de escritorio, manejo de GUI, integración con APIs y un enfoque proactivo en la resolución de problemas.

---

## Funcionalidades Principales

CryptoTrade Leverage Pro ofrece un conjunto de funciones, organizadas de manera intuitiva a través de una Interfaz Gráfica de Usuario (GUI):

### MENÚ PRINCIPAL:

* **Agregar nuevo criptoactivo**: Incorpora nuevos activos a tu portafolio para un seguimiento personalizado.
* **Mostrar márgenes**: Visualiza los márgenes actuales de tus posiciones abiertas.
* **Actualizar márgenes**: Ajusta tus márgenes utilizando diferentes métodos:
    * División equitativa.
    * Ponderaciones manuales.
    * Ponderaciones automáticas (basadas en la valuación de la posición abierta de cada activo).
* **Mostrar posiciones abiertas**: Visualiza tus posiciones abiertas y su valoración en tiempo real, con **gráficos de barra interactivos de Matplotlib**.
* **Medir apalancamiento**: Calcula el apalancamiento actual y simula diferentes niveles de apalancamiento en **gráficos de Matplotlib**.
* **Calcular precios de liquidación para cada activo del portafolio**: Determina los precios de liquidación para todos los activos de tu portafolio, basándote en los márgenes estimados para cada uno.
* **Donaciones**: Este botón te permite apoyar el proyecto mediante donaciones en diversas criptomonedas o pesos argentinos (ARS). Se proporciona la dirección de la wallet y un código QR para facilitar el proceso. También puedes contactarme por correo electrónico para dejar un mensaje o comentario. ¡Tu apoyo es fundamental para el crecimiento de esta herramienta de código abierto!

---

### MENÚ DE ACTIVOS:

El menú de activos, ubicado en el panel superior, te brinda acceso rápido a la información de cada activo que agregues. Al seleccionar un activo, el menú principal se reemplaza por el menú secundario, que ofrece las siguientes opciones:

### MENÚ SECUNDARIO:

* **Volver al menú principal**: Regresa al menú principal para gestionar la cartera general.
* **Abrir TradingView**: Abre el par de trading del activo seleccionado (frente a USDT, con la cotización de Binance) en una nueva pestaña del navegador predeterminado. Aquí se dibujarán las líneas horizontales de las distintas órdenes.
* **Borrar datos del activo**: Elimina todos los datos asociados al activo, pero conserva el símbolo en el menú de activos.
* **Eliminar activo**: Elimina toda la información y remueve el símbolo del activo del menú de activos.
* **Calcular orden Madre**: Calcula la "orden Madre", una orden que consolida todas las órdenes abiertas de un activo, o un subconjunto de ellas, para una gestión unificada (sirve para unificar órdenes abiertas o considerar órdenes de largo plazo).
* **Generar niveles de Buy Limits**: Crea niveles de precios, cantidades y montos para colocar órdenes Buy Limit (órdenes de compras pendientes). Esta estrategia de compra escalonada, también conocida como Dollar-Cost Averaging (DCA), minimiza el riesgo y permite a los nuevos traders familiarizarse con la dinámica del mercado antes de incursionar en operaciones más complejas.
* **Calcular precio de liquidación**: Calcula el precio de liquidación (Stop Out) específico para el activo seleccionado, basado en el margen estimado para dicho activo.
* **Generar niveles de Sell Take Profit (Ventas de toma de ganancias)**: Crea niveles de precios, cantidad de niveles y monto a reducir en USDT, para colocar órdenes Sell Take Profit.
* **Mostrar órdenes abiertas**: Visualiza las órdenes abiertas del activo en **gráficos de Matplotlib**, incluyendo:
    * Gráficos separados para la orden abierta Madre y las órdenes abiertas no Madre.
    * Información detallada de cada orden: precio de entrada, monto inicial, beneficio en USDT y porcentaje de beneficio.
    * Precio actual del activo y beneficio total (promedio de todas las órdenes abiertas), con indicación de ganancia (verde) o pérdida (rojo).
* **Promediar órdenes**: Calcula el precio de entrada promedio y el monto total de dos o más órdenes. También tienes la opción de guardar la orden promediada como una nueva orden abierta, ya sea como orden abierta Madre o como una orden abierta independiente (orden abierta no madre).

---

### PANEL SUPERIOR

El panel superior de la interfaz muestra:

* El título del software: "CryptoTrade Leverage Pro".
* Un código de invitación para Quantfury: Al usar este código (**U23853V6**) al registrarte en Quantfury, tanto tú como yo recibimos fracciones de criptoactivos de regalo. El código se puede copiar fácilmente con el botón "Copiar".
* Un botón para acceder al sitio web de Quantfury: Te dirige a la plataforma de trading de Quantfury.

---

## Otras Consideraciones Técnicas

### Características principales del software:

* Gestión integral de operaciones apalancadas de criptoactivos.
* Interfaz de usuario intuitiva y fácil de usar.
* Visualización de datos en tiempo real con gráficos interactivos.
* Cálculo preciso de márgenes, apalancamiento y precios de liquidación.
* Soporte para órdenes abiertas, Buy Limit y Sell Take Profit.
* Integración con TradingView y Quantfury.

### Arquitectura del sistema:

* Desarrollado en **Python**.
* Interfaz gráfica de usuario (GUI) creada con **Tkinter**.
* Almacenamiento de datos en archivos **JSON**.
* Gráficos generados con **Matplotlib**.
* Manejo de imágenes con **Pillow**.
* Copia al portapapeles con **Pyperclip**.

### Tecnologías utilizadas:

* Python
* Tkinter
* JSON
* Matplotlib
* Pillow
* Pyperclip
* Webbrowser
* OS
* Requests

### Manejo de errores y excepciones:

Se ha implementado un robusto manejo de errores y excepciones para garantizar la estabilidad y confiabilidad de la aplicación.

### Análisis de código:

Se ha realizado un análisis de código con **Pylint** para asegurar la calidad y el estilo del código.

### Distribución:

El proyecto se distribuirá inicialmente como un **archivo ejecutable descargable** desde las "Releases" de GitHub. En el futuro, se planea migrar a **Django** para una experiencia de usuario más fluida y segura, eliminando la necesidad de instalaciones locales.

### Seguridad y transparencia:

El proyecto es de código abierto y ha sido auditado para garantizar que no contiene malware. Para mayor tranquilidad, se recomienda escanear el ejecutable con tu antivirus preferido.

### Documentación:

Se proporcionará documentación completa para facilitar la instalación y el uso del software:

* Documentación técnica generada con **Sphinx**.
* Manual de usuario con capturas de pantalla y videos tutoriales en YouTube.
* Guía para traders y usuarios finales, con ejemplos de uso y mejores prácticas.

---

## Procedimiento de Instalación y Despliegue

### Guía paso a paso para la instalación:

1.  Descarga el archivo ejecutable desde la sección "**Releases**" de este repositorio en GitHub.
2.  Ejecuta el archivo descargado.
3.  Sigue las instrucciones del instalador.

### Configuración y puesta en marcha:

1.  Abre la aplicación CryptoTrade Leverage Pro.
2.  Explora los menús y las opciones para familiarizarte con la interfaz.
3.  Configura tus activos y parámetros de trading según tus preferencias.
4.  Utiliza las herramientas de análisis y gestión de riesgos para optimizar tus operaciones.

---

## ¡Pruébalo y Comparte Tu Opinión!

Te invito a descargar CryptoTrade Leverage Pro, a explorar sus funcionalidades y a compartir un comentario o sugerencias. Si encuentras algún error o tienes ideas para mejorar la aplicación, no dudes en contactarme o abrir un "issue" en GitHub.

¡Tu feedback es invaluable para el desarrollo continuo de este proyecto!

---

¡Un saludo cordial y buenos trades!

**Contacto:** dilucapython@gmail.com
