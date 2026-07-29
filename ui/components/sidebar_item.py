import customtkinter as ctk
from ui import theme


class SidebarItem(ctk.CTkFrame):
    def __init__(self, master, label: str, badge: str, on_click, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=8, **kwargs)
        self.on_click = on_click
        self.active = False

        self.badge_lbl = ctk.CTkLabel(
            self, text=badge, width=32, height=32, corner_radius=16,
            fg_color=theme.COLOR_BLUE, text_color="white",
            font=(theme.FONT_FAMILY, 11, "bold")
        )
        self.badge_lbl.pack(side="left", padx=(10, 8), pady=8)

        self.text_lbl = ctk.CTkLabel(
            self, text=label, font=(theme.FONT_FAMILY, 13),
            text_color=theme.COLOR_TEXT, anchor="w"
        )
        self.text_lbl.pack(side="left", fill="x", expand=True, pady=8)

        for widget in (self, self.badge_lbl, self.text_lbl):
            widget.bind("<Button-1>", lambda e: self.on_click())
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        if not self.active:
            self.configure(fg_color=theme.COLOR_SIDEBAR_HOVER)

    def _on_leave(self, _event):
        if not self.active:
            self.configure(fg_color="transparent")

    def set_active(self, active: bool):
        self.active = active
        self.configure(fg_color=theme.COLOR_SIDEBAR_ACTIVE if active else "transparent")
        self.text_lbl.configure(font=(theme.FONT_FAMILY, 13, "bold" if active else "normal"))
