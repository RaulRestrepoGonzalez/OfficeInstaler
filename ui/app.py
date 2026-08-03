"""
Ventana principal de Office Installer Facilitator.
Arma la barra superior (top app bar), la navegación lateral y delega el
contenido dinámico a ui.views.product_view.
"""

import os

import customtkinter as ctk
from tkinter import messagebox

from config.products import PRODUCTS, LANGUAGES, APPS_BY_PRODUCT_ID, ALL_APPS
from config.settings import ODT_PATH_DEFAULT, ODT_DIR, DEFAULT_DOWNLOAD_DIR, OUTPUT_DIR
from core.odt_config_builder import build_configuration_xml
from core.odt_runner import save_configuration, run_odt, find_odt, ODTNotFoundError, ODTExecutionError
from core.odt_downloader import download_odt, ODTDownloadError
from ui.components.sidebar_item import SidebarItem
from ui import theme
from ui.views.product_view import render_product_view

ctk.set_appearance_mode("dark")

ICON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "icons", "app.ico"
)


class OfficeInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Office Installer Facilitator")
        self.configure(fg_color=theme.COLOR_BG)
        if os.path.isfile(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        # --- Estado de la selección actual ---
        self.current_family = list(PRODUCTS.keys())[0]
        self.edition_vars = {f: ctk.StringVar(value=list(d["products"].keys())[0])
                              for f, d in PRODUCTS.items()}
        self.channel_vars = {f: ctk.StringVar(value=d["channels"][0])
                              for f, d in PRODUCTS.items()}
        self.arch_var = ctk.StringVar(value="x64")
        self.mode_var = ctk.StringVar(value="install")
        self.language_var = ctk.StringVar(value="Español")
        self.odt_path_var = ctk.StringVar(value=ODT_PATH_DEFAULT)
        self.download_path_var = ctk.StringVar(value=DEFAULT_DOWNLOAD_DIR)
        self.include_vars = {app: ctk.BooleanVar(value=True) for app in ALL_APPS}
        self.download_row = None  # se crea dentro de product_view

        self._build_topbar()
        self._build_body()
        self.after(50, lambda: self.state("zoomed"))

    # ---------------- Top App Bar ----------------
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color=theme.COLOR_SURFACE, height=64, corner_radius=0)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        ctk.CTkLabel(
            topbar, text="Office Installer Facilitator",
            font=theme.FONT_TITLE, text_color=theme.COLOR_TEXT
        ).pack(side="left", padx=24)

        ctk.CTkLabel(
            topbar, text="Basado en el Office Deployment Tool oficial · sin activadores",
            font=theme.FONT_CAPTION, text_color=theme.COLOR_TEXT_SECONDARY
        ).pack(side="left")

        ctk.CTkFrame(self, height=1, fg_color=theme.COLOR_BORDER, corner_radius=0).pack(fill="x")

    # ---------------- Cuerpo: sidebar + contenido ----------------
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=theme.COLOR_BG)
        body.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(body, fg_color=theme.COLOR_SIDEBAR, width=260, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar, text="PRODUCTOS", font=(theme.FONT_CAPTION[0], 11, "bold"),
            text_color=theme.COLOR_TEXT_SECONDARY, anchor="w"
        ).pack(fill="x", padx=20, pady=(20, 6))

        self.sidebar_items = {}
        for family, data in PRODUCTS.items():
            item = SidebarItem(
                sidebar, label=family, badge=data["icon"],
                on_click=lambda f=family: self._select_family(f)
            )
            item.pack(fill="x", padx=8, pady=2)
            self.sidebar_items[family] = item
        self.sidebar_items[self.current_family].set_active(True)

        content_wrapper = ctk.CTkFrame(body, fg_color=theme.COLOR_BG)
        content_wrapper.pack(side="left", fill="both", expand=True, padx=24, pady=20)

        self.content = ctk.CTkScrollableFrame(content_wrapper, fg_color=theme.COLOR_BG)
        self.content.pack(fill="both", expand=True)

        self._render_content()

    def _select_family(self, family):
        self.sidebar_items[self.current_family].set_active(False)
        self.current_family = family
        self.sidebar_items[family].set_active(True)
        self._render_content()

    def _render_content(self):
        render_product_view(
            self.content, state=self,
            on_preview=self.preview_xml, on_install=self.run_install
        )

    def toggle_download_path(self):
        if self.download_row is None:
            return
        if self.mode_var.get() == "download":
            self.download_row.pack(fill="x", padx=16, pady=(0, 8))
        else:
            self.download_row.pack_forget()

    # ---------------- Selección actual -> datos para el ODT ----------------
    def _current_selection(self):
        family = self.current_family
        edition_name = self.edition_vars[family].get()
        product_id = PRODUCTS[family]["products"][edition_name]
        channel = self.channel_vars[family].get()
        language_code = LANGUAGES[self.language_var.get()]
        available_apps = APPS_BY_PRODUCT_ID[product_id]
        excluded_apps = [app for app in available_apps if not self.include_vars[app].get()]

        return {
            "product_id": product_id,
            "channel": channel,
            "language_code": language_code,
            "arch": self.arch_var.get(),
            "excluded_apps": excluded_apps,
            "mode": self.mode_var.get(),
            "download_path": self.download_path_var.get() if self.mode_var.get() == "download" else None,
        }

    def preview_xml(self):
        sel = self._current_selection()
        xml_text = build_configuration_xml(**sel)

        preview = ctk.CTkToplevel(self)
        preview.title("Vista previa de configuration.xml")
        preview.geometry("640x520")
        textbox = ctk.CTkTextbox(preview, font=("Consolas", 11))
        textbox.pack(fill="both", expand=True, padx=12, pady=12)
        textbox.insert("1.0", xml_text)

    def run_install(self):
        sel = self._current_selection()
        xml_text = build_configuration_xml(**sel)
        config_path = os.path.join(OUTPUT_DIR, "configuration.xml")
        save_configuration(xml_text, config_path)

        odt_path = find_odt(self.odt_path_var.get(), ODT_DIR)

        if odt_path is None:
            answer = messagebox.askyesno(
                "ODT no encontrado",
                "No se encontró el Office Deployment Tool (setup.exe).\n\n"
                "¿Deseas que la aplicación lo descargue automáticamente desde Microsoft?"
            )
            if not answer:
                messagebox.showerror(
                    "ODT no encontrado",
                    "Descarga el Office Deployment Tool oficial desde Microsoft\n"
                    "https://www.microsoft.com/en-us/download/details.aspx?id=49117\n\n"
                    "y coloca setup.exe en la raíz del proyecto o en la ruta indicada."
                )
                return

            progress_win = self._show_download_progress()
            try:
                def update_progress(current, total):
                    pct = min(int(current / total * 100), 99)
                    progress_win.progressbar.set(pct / 100)
                    progress_win.label.configure(text=f"Descargando ODT... {pct}%")
                    progress_win.update()

                odt_path = download_odt(ODT_DIR, progress_callback=update_progress)
            except ODTDownloadError as e:
                messagebox.showerror("Error al descargar ODT", str(e))
                return
            finally:
                if progress_win.winfo_exists():
                    progress_win.destroy()

        try:
            run_odt(odt_path, config_path, sel["mode"])
            if sel["mode"] == "install":
                messagebox.showinfo(
                    "Instalación en curso",
                    "setup.exe se está ejecutando.\n\n"
                    "Si ves un aviso de Control de Cuentas de Usuario (UAC):\n"
                    "  -> Haz clic en 'Sí' para permitir la instalación\n\n"
                    "Sigue las instrucciones del instalador de Office.\n"
                    "Puedes cerrar esta app una vez que comience la instalación."
                )
            else:
                messagebox.showinfo(
                    "Descarga en curso",
                    f"Descargando Office en:\n{sel['download_path']}\n\n"
                    "Revisa la carpeta indicada para ver el progreso."
                )
        except ODTNotFoundError as e:
            messagebox.showerror(
                "ODT no encontrado",
                f"{e}\n\nDescarga el Office Deployment Tool oficial desde Microsoft "
                "y coloca setup.exe en la ruta indicada."
            )
        except ODTExecutionError as e:
            messagebox.showerror("Error al ejecutar ODT", str(e))
        except Exception as e:
            messagebox.showerror("Error al ejecutar ODT", str(e))

    def _show_download_progress(self):
        win = ctk.CTkToplevel(self)
        win.title("Descargando Office Deployment Tool")
        win.geometry("420x140")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()

        label = ctk.CTkLabel(win, text="Descargando ODT desde Microsoft...", font=theme.FONT_CAPTION)
        label.pack(pady=(20, 10))

        progressbar = ctk.CTkProgressBar(win, width=360, mode="determinate")
        progressbar.set(0)
        progressbar.pack(pady=(0, 20))

        info = ctk.CTkLabel(win, text="Esto puede tomar unos segundos", font=theme.FONT_CAPTION)
        info.pack()

        win.progressbar = progressbar
        win.label = label
        win.update()
        return win
