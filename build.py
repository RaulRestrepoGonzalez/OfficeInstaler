import os
import sys
import shutil
import subprocess

ICON_PATH = os.path.join("assets", "icons", "app.ico")
OUTPUT_NAME = "OfficeInstaller"
DIST_DIR = "dist"

# --- Limpiar outputs anteriores ---
if os.path.isdir(DIST_DIR):
    for entry in os.listdir(DIST_DIR):
        path = os.path.join(DIST_DIR, entry)
        if entry.endswith(".build") or entry.endswith(".dist") or entry.endswith(".onefile-build"):
            shutil.rmtree(path, ignore_errors=True)

args = [
    sys.executable, "-m", "nuitka",
    "--onefile",
    "--plugin-enable=tk-inter",
    "--windows-console-mode=disable",
    f"--windows-icon-from-ico={ICON_PATH}",
    f"--output-dir={DIST_DIR}",
    f"--output-filename={OUTPUT_NAME}.exe",
    f"--file-description=Office Installer Facilitator",
    f"--file-version=1.0.0.0",
    f"--product-version=1.0.0.0",
    f"--product-name=Office Installer Facilitator",
    f"--company-name=Office Installer Facilitator",
    "--copyright=Freeware",
    "--include-data-dir=assets=assets",
    "--zig",
    "--assume-yes-for-downloads",
    "main.py",
]

print("=== Nuitka Build (onefile) ===")
print("Compilando Office Installer Facilitator a código nativo...")
print()

subprocess.run(args, check=True)

exe_path = os.path.join(DIST_DIR, f"{OUTPUT_NAME}.exe")
if os.path.isfile(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n--- EXE nativo generado: {exe_path} ({size_mb:.1f} MB) ---")
    print("Un solo archivo portátil (onefile) - sin dependencias")
else:
    print(f"\nERROR: No se encontró el exe en {exe_path}")
    sys.exit(1)
