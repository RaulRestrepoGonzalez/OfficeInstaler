"""
Punto de entrada de Office Installer Facilitator.

Ejecutar con:
    python main.py
"""

from ui.app import OfficeInstallerApp


def main():
    app = OfficeInstallerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
