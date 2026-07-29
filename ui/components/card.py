"""
Tarjeta plana estilo Material Design: fondo blanco, borde sutil,
esquinas redondeadas. Usada como contenedor de cada sección del formulario.
"""

import customtkinter as ctk
from ui import theme


class Card(ctk.CTkFrame):
    def __init__(self, master, title: str | None = None, **kwargs):
        super().__init__(master, fg_color=theme.COLOR_SURFACE, corner_radius=12,
                          border_width=1, border_color=theme.COLOR_BORDER, **kwargs)
        if title:
            ctk.CTkLabel(
                self, text=title, font=theme.FONT_SECTION,
                text_color=theme.COLOR_TEXT, anchor="w"
            ).pack(fill="x", padx=16, pady=(14, 4))
