from tkinter import *
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from modulos.ventas.ventas_moderna import VentasModerna as Ventas
from modulos.inventario.inventario_simple import InventarioSimple as Inventario

from modulos.informacion.informacion_moderna import InformacionModerna as Informacion
from modulos.utils.estilos_modernos import estilos
from PIL import Image, ImageTk
import sys
import os

# Configurar CustomTkinter
ctk.set_appearance_mode("light")  # Modo claro
ctk.set_default_color_theme("blue")  # Tema azul

# Tamano logico de la "pagina" donde los modulos dibujan su contenido.
# Los modulos usan coordenadas absolutas, por eso mantenemos un lienzo fijo
# y permitimos desplazarse cuando la ventana es mas pequena que esta pagina.
PAGE_WIDTH = 1400
PAGE_HEIGHT = 830
NAVBAR_HEIGHT = 70


class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador

        # Configurar el frame principal con estilos modernos
        self.configure(bg=estilos.COLORS['bg_primary'])
        self.pack(fill=BOTH, expand=True)

        # Inicializar antes de widgets_modernos() porque los botones necesitan estos atributos
        self.frames = {}
        self.buttons = []
        self.active_button = None  # Boton activo actual
        self.button_map = {}  # Mapeo de modulos a botones

        self.widgets_modernos()

        # Crear los frames de los modulos con estilos modernos dentro del area scrollable
        for i in (Ventas, Inventario, Informacion):
            frame = i(self.inner_frame)
            self.frames[i] = frame
            frame.config(bg=estilos.COLORS['bg_primary'])
            frame.place(x=0, y=0, width=PAGE_WIDTH, height=PAGE_HEIGHT)

        # Habilitar scroll con la rueda del mouse
        self.activar_rueda_mouse()

        self.show_frames(Ventas)

    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

        # Refrescar datos al entrar a Ventas para ver productos recien agregados
        if container is Ventas and hasattr(frame, 'recargar_datos'):
            frame.recargar_datos(mostrar_mensaje=False)

        # Actualizar el color del boton activo
        self.actualizar_boton_activo(container)

    def Ventas(self):
        self.show_frames(Ventas)

    def Inventario(self):
        self.show_frames(Inventario)

    def Informacion(self):
        self.show_frames(Informacion)

    def actualizar_boton_activo(self, container):
        """Actualizar el color del boton activo y restaurar los demas"""
        # Restaurar todos los botones a su color normal
        for btn in self.buttons:
            btn.configure(fg_color=estilos.COLORS['primary_light'])

        # Cambiar el color del boton activo
        if container in self.button_map:
            active_btn = self.button_map[container]
            active_btn.configure(fg_color=estilos.COLORS['secondary'])  # Color diferente para activo
            self.active_button = active_btn

    def widgets_modernos(self):
        """Crear la barra de navegacion y el area de contenido scrollable"""
        # Navbar principal (siempre visible arriba)
        navbar_frame = tk.Frame(self, bg=estilos.COLORS['primary'], height=NAVBAR_HEIGHT)
        navbar_frame.pack(side=TOP, fill=X)
        navbar_frame.pack_propagate(False)

        # Titulo de la aplicacion
        title_label = tk.Label(navbar_frame, text="🏪 El Goloso - Sistema de Ventas",
                              bg=estilos.COLORS['primary'], fg=estilos.COLORS['white'],
                              font=('Segoe UI', 18, 'bold'))
        title_label.pack(side=LEFT, padx=20)

        # Contenedor de botones de navegacion (alineado a la derecha)
        buttons_frame = tk.Frame(navbar_frame, bg=estilos.COLORS['primary'])
        buttons_frame.pack(side=RIGHT, padx=20)

        # Configuracion de botones modernos
        button_configs = [
            {"text": "💰 Ventas", "command": self.Ventas, "icon": "venta_icon.png", "module": Ventas},
            {"text": "📦 Inventario", "command": self.Inventario, "icon": "inventario_icon.png", "module": Inventario},
            {"text": "ℹ️ Info", "command": self.Informacion, "icon": "informacion_icon.png", "module": Informacion}
        ]

        self.buttons = []

        for config in button_configs:
            # Crear boton moderno
            btn = self.crear_boton_navbar(buttons_frame, config["text"], config["command"])
            self.buttons.append(btn)
            # Mapear el modulo al boton
            self.button_map[config["module"]] = btn

        # Area de contenido scrollable (debajo de la navbar)
        content = tk.Frame(self, bg=estilos.COLORS['bg_primary'])
        content.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas = tk.Canvas(content, bg=estilos.COLORS['bg_primary'],
                                highlightthickness=0, bd=0)
        self.vbar = ttk.Scrollbar(content, orient='vertical', command=self.canvas.yview)
        self.hbar = ttk.Scrollbar(content, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set)

        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.vbar.grid(row=0, column=1, sticky='ns')
        self.hbar.grid(row=1, column=0, sticky='ew')

        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        # Frame interno que representa la pagina logica de los modulos
        self.inner_frame = tk.Frame(self.canvas, bg=estilos.COLORS['bg_primary'],
                                    width=PAGE_WIDTH, height=PAGE_HEIGHT)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor='nw',
            width=PAGE_WIDTH, height=PAGE_HEIGHT)
        self.canvas.configure(scrollregion=(0, 0, PAGE_WIDTH, PAGE_HEIGHT))

        # Centrar la pagina cuando la ventana es mas grande que el contenido
        self.canvas.bind('<Configure>', self._ajustar_pagina)

        # Actualizar el boton activo inicial (Ventas)
        if Ventas in self.button_map:
            self.actualizar_boton_activo(Ventas)

    def _ajustar_pagina(self, event):
        """Mantener la pagina centrada si el area visible es mas grande."""
        ancho_visible = event.width
        offset_x = max(0, (ancho_visible - PAGE_WIDTH) // 2)
        self.canvas.coords(self.canvas_window, offset_x, 0)
        self.canvas.configure(scrollregion=(0, 0,
                                            max(PAGE_WIDTH, ancho_visible),
                                            PAGE_HEIGHT))

    def activar_rueda_mouse(self):
        """Permitir desplazamiento con la rueda del mouse sobre el contenido."""
        self.winfo_toplevel().bind('<MouseWheel>', self._on_mousewheel)

    def _on_mousewheel(self, event):
        # No interferir con ventanas emergentes
        if event.widget.winfo_toplevel() is not self.winfo_toplevel():
            return

        # Dejar que los widgets con scroll propio (tablas, textos, listas,
        # canvases internos) manejen la rueda por si mismos.
        clase = event.widget.winfo_class()
        if clase in ('Treeview', 'Text', 'Listbox', 'Canvas', 'Scrollbar', 'TScrollbar'):
            return

        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def crear_boton_navbar(self, parent, text, command):
        """Crear un boton moderno con CustomTkinter (esquinas redondeadas)"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            width=130,
            height=40,
            corner_radius=15,  # Esquinas muy redondeadas
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            fg_color=estilos.COLORS['primary_light'],  # Color normal
            hover_color=estilos.COLORS['secondary'],   # Color hover
            text_color=estilos.COLORS['white'],        # Color del texto
            border_width=0,                            # Sin borde
            cursor="hand2"                             # Cursor de mano
        )
        btn.pack(side=LEFT, padx=6, pady=5)
        return btn
