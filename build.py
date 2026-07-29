import os
import sys
import shutil
import subprocess

ICON_PATH = os.path.join("assets", "icons", "app.ico")
OUTPUT_NAME = "OfficeInstaller"
DIST_DIR = "dist"
BUILD_DIR = "build"

args = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--clean",
    "--noconfirm",
    f"--name={OUTPUT_NAME}",
    f"--distpath={DIST_DIR}",
    f"--workpath={BUILD_DIR}",
    f"--icon={ICON_PATH}",
    "--add-data", f"assets{os.pathsep}assets",
    "main.py",
]

print("Ejecutando PyInstaller...")
subprocess.run(args, check=True)

exe_path = os.path.join(DIST_DIR, f"{OUTPUT_NAME}.exe")
if os.path.isfile(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n--- EXE generado: {exe_path} ({size_mb:.1f} MB) ---")
    print("Es un ejecutable portable (--onefile).")
    print("Al ejecutarse crea las carpetas 'output/' y 'odt/' junto al .exe.")
else:
    print(f"\nERROR: No se encontró el exe en {exe_path}")
    sys.exit(1)
