"""
Vista de contenido principal: tarjetas para elegir edición, canal,
opciones generales, apps a excluir y ruta del ODT. Se re-renderiza
cada vez que el usuario cambia de producto en la barra lateral.
"""

import customtkinter as ctk
from tkinter import filedialog

from config.products import PRODUCTS, LANGUAGES, EXCLUDABLE_APPS
from ui.components.card import Card
from ui import theme


def render_product_view(content_frame, state, on_preview, on_install):
    """
    Dibuja dentro de `content_frame` las tarjetas correspondientes al
    producto actualmente seleccionado en `state.current_family`.

    `state` es la instancia de OfficeInstallerApp: contiene todas las
    variables (StringVar/BooleanVar) que representan la selección actual.
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

    family = state.current_family
    data = PRODUCTS[family]

    # --- Card: selección de edición ---
    card_edition = Card(content_frame, title=f"{family} · Elige una edición")
    card_edition.pack(fill="x", pady=(0, 16))
    radio_wrap = ctk.CTkFrame(card_edition, fg_color="transparent")
    radio_wrap.pack(fill="x", padx=16, pady=(0, 8))
    for edition in data["products"]:
        ctk.CTkRadioButton(
            radio_wrap, text=edition, variable=state.edition_vars[family],
            value=edition, fg_color=theme.COLOR_BLUE, hover_color=theme.COLOR_BLUE_HOVER,
            font=theme.FONT_BODY
        ).pack(anchor="w", pady=4)

    ctk.CTkLabel(card_edition, text="Canal de actualización", font=theme.FONT_BODY,
                 text_color=theme.COLOR_TEXT_SECONDARY).pack(anchor="w", padx=16, pady=(6, 2))
    ctk.CTkOptionMenu(
        card_edition, variable=state.channel_vars[family], values=data["channels"],
        fg_color=theme.COLOR_BLUE, button_color=theme.COLOR_BLUE, button_hover_color=theme.COLOR_BLUE_HOVER,
        width=280
    ).pack(anchor="w", padx=16, pady=(0, 16))

    # --- Card: opciones generales ---
    card_options = Card(content_frame, title="Opciones generales")
    card_options.pack(fill="x", pady=(0, 16))
    opts_grid = ctk.CTkFrame(card_options, fg_color="transparent")
    opts_grid.pack(fill="x", padx=16, pady=(0, 16))

    col1 = ctk.CTkFrame(opts_grid, fg_color="transparent")
    col1.pack(side="left", anchor="n", padx=(0, 40))
    ctk.CTkLabel(col1, text="Arquitectura", font=theme.FONT_BODY,
                 text_color=theme.COLOR_TEXT_SECONDARY).pack(anchor="w")
    for arch in ("x64", "x32"):
        ctk.CTkRadioButton(col1, text=arch, variable=state.arch_var, value=arch,
                            fg_color=theme.COLOR_BLUE, hover_color=theme.COLOR_BLUE_HOVER,
                            font=theme.FONT_BODY).pack(anchor="w", pady=2)

    col2 = ctk.CTkFrame(opts_grid, fg_color="transparent")
    col2.pack(side="left", anchor="n", padx=(0, 40))
    ctk.CTkLabel(col2, text="Modo", font=theme.FONT_BODY,
                 text_color=theme.COLOR_TEXT_SECONDARY).pack(anchor="w")
    ctk.CTkRadioButton(col2, text="Instalar", variable=state.mode_var, value="install",
                        command=state.toggle_download_path, fg_color=theme.COLOR_BLUE,
                        hover_color=theme.COLOR_BLUE_HOVER, font=theme.FONT_BODY).pack(anchor="w", pady=2)
    ctk.CTkRadioButton(col2, text="Solo descargar", variable=state.mode_var, value="download",
                        command=state.toggle_download_path, fg_color=theme.COLOR_BLUE,
                        hover_color=theme.COLOR_BLUE_HOVER, font=theme.FONT_BODY).pack(anchor="w", pady=2)

    col3 = ctk.CTkFrame(opts_grid, fg_color="transparent")
    col3.pack(side="left", anchor="n")
    ctk.CTkLabel(col3, text="Idioma de instalación", font=theme.FONT_BODY,
                 text_color=theme.COLOR_TEXT_SECONDARY).pack(anchor="w")
    ctk.CTkOptionMenu(
        col3, variable=state.language_var, values=list(LANGUAGES.keys()),
        fg_color=theme.COLOR_BLUE, button_color=theme.COLOR_BLUE, button_hover_color=theme.COLOR_BLUE_HOVER,
        width=220
    ).pack(anchor="w", pady=(2, 0))

    state.download_row = ctk.CTkFrame(card_options, fg_color="transparent")
    ctk.CTkLabel(state.download_row, text="Carpeta de descarga", font=theme.FONT_BODY,
                 text_color=theme.COLOR_TEXT_SECONDARY).pack(anchor="w")
    ctk.CTkEntry(state.download_row, textvariable=state.download_path_var, width=400).pack(anchor="w", pady=(2, 0))
    state.toggle_download_path()

    # --- Card: excluir aplicaciones ---
    card_apps = Card(content_frame, title="Excluir aplicaciones (opcional)")
    card_apps.pack(fill="x", pady=(0, 16))
    apps_grid = ctk.CTkFrame(card_apps, fg_color="transparent")
    apps_grid.pack(fill="x", padx=16, pady=(0, 16))
    for i, app in enumerate(EXCLUDABLE_APPS):
        ctk.CTkCheckBox(
            apps_grid, text=app, variable=state.exclude_vars[app],
            fg_color=theme.COLOR_BLUE, hover_color=theme.COLOR_BLUE_HOVER, font=theme.FONT_BODY
        ).grid(row=i // 4, column=i % 4, sticky="w", padx=10, pady=6)

    # --- Card: ruta del ODT ---
    card_odt = Card(content_frame, title="Ubicación del Office Deployment Tool")
    card_odt.pack(fill="x", pady=(0, 16))
    odt_row = ctk.CTkFrame(card_odt, fg_color="transparent")
    odt_row.pack(fill="x", padx=16, pady=(8, 0))
    ctk.CTkEntry(odt_row, textvariable=state.odt_path_var, width=520).pack(side="left")

    def browse_odt():
        path = filedialog.askopenfilename(title="Selecciona setup.exe (ODT oficial)",
                                           filetypes=[("Ejecutable", "*.exe")])
        if path:
            state.odt_path_var.set(path)

    ctk.CTkButton(
        odt_row, text="Buscar...", width=90, fg_color=theme.COLOR_SURFACE,
        text_color=theme.COLOR_BLUE, border_width=1, border_color=theme.COLOR_BORDER,
        hover_color=theme.COLOR_SIDEBAR_HOVER, command=browse_odt
    ).pack(side="left", padx=(8, 0))

    ctk.CTkLabel(
        card_odt, text="Si no se encuentra, se descargará automáticamente al ejecutar.",
        font=theme.FONT_CAPTION, text_color=theme.COLOR_TEXT_SECONDARY, anchor="w"
    ).pack(fill="x", padx=16, pady=(2, 10))

    ctk.CTkLabel(
        content_frame,
        text="(*) Esta herramienta solo genera configuration.xml y llama al ODT oficial. "
             "No activa Office: necesitas tu propia licencia (Microsoft 365, clave de volumen, etc.).",
        font=theme.FONT_CAPTION, text_color=theme.COLOR_TEXT_SECONDARY, wraplength=800, justify="left"
    ).pack(fill="x", pady=(4, 16))

    # --- Barra de acciones ---
    actions = ctk.CTkFrame(content_frame, fg_color="transparent")
    actions.pack(fill="x", pady=(0, 20))
    ctk.CTkButton(
        actions, text="Vista previa XML", fg_color=theme.COLOR_SURFACE, text_color=theme.COLOR_BLUE,
        border_width=1, border_color=theme.COLOR_BORDER, hover_color=theme.COLOR_SIDEBAR_HOVER,
        width=160, command=on_preview
    ).pack(side="left")
    ctk.CTkButton(
        actions, text="Generar e instalar", fg_color=theme.COLOR_BLUE, hover_color=theme.COLOR_BLUE_HOVER,
        width=180, command=on_install
    ).pack(side="left", padx=10)
