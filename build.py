import os
import sys
import subprocess

ICON_PATH = os.path.join("assets", "icons", "app.ico")
VERSION_FILE = "version_info.rc"
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
    f"--version-file={VERSION_FILE}",
    "--add-data", f"assets{os.pathsep}assets",
    "main.py",
]

print("Ejecutando PyInstaller...")
subprocess.run(args, check=True)

exe_path = os.path.join(DIST_DIR, f"{OUTPUT_NAME}.exe")
if os.path.isfile(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n--- EXE generado: {exe_path} ({size_mb:.1f} MB) ---")
    print("Portable (--onefile) con metadatos de versión.")

    print("\n--- NOTA sobre antivirus ---")
    print("Si Windows Defender u otros antivirus detectan el .exe como")
    print("falso positivo, puedes:")
    print("1. Reportarlo en https://www.microsoft.com/en-us/wdsi/filesubmission")
    print("2. Firmar el ejecutable con un certificado de código (recomendado)")
    print("3. O añadirlo a exclusiones de Windows Defender")
else:
    print(f"\nERROR: No se encontró el exe en {exe_path}")
    sys.exit(1)
