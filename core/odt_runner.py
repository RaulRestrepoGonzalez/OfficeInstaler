import os
import subprocess
import ctypes
import ctypes.wintypes
import threading
import logging


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [ODT] %(message)s",
                    filename=os.path.join(os.path.dirname(__file__), "..", "odt_debug.log"),
                    filemode="w")


class ODTNotFoundError(FileNotFoundError):
    pass


class ODTExecutionError(Exception):
    pass


def _is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def save_configuration(xml_text: str, output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_text)
    return output_path


def find_odt(odt_exe_path: str, odt_dir: str) -> str | None:
    if os.path.isfile(odt_exe_path):
        return odt_exe_path
    candidate = os.path.join(odt_dir, "setup.exe")
    if os.path.isfile(candidate):
        return candidate
    return None


def run_odt(odt_exe_path: str, config_path: str, mode: str) -> None:
    if not os.path.exists(odt_exe_path):
        raise ODTNotFoundError(f"No se encontró setup.exe en: {odt_exe_path}")
    if not os.path.exists(config_path):
        raise ODTExecutionError(f"No se encontró el archivo de configuración: {config_path}")

    action = "/download" if mode == "download" else "/configure"
    logging.info("Ejecutando: %s %s %s", odt_exe_path, action, config_path)
    logging.info("¿Es admin? %s", _is_admin())

    if mode in ("configure", "install"):
        if _is_admin():
            logging.info("Ejecutando directamente (ya somos admin)")
            try:
                subprocess.Popen([odt_exe_path, action, config_path], shell=False)
            except Exception as e:
                logging.error("Error lanzando setup.exe: %s", e)
                raise ODTExecutionError(f"Error al ejecutar setup.exe: {e}")
        else:
            logging.info("Solicitando elevación via UAC...")
            try:
                result = ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", odt_exe_path,
                    f"{action} \"{config_path}\"",
                    os.path.dirname(odt_exe_path), 1
                )
                logging.info("ShellExecuteW devolvió: %d", result)
                if result <= 32:
                    raise ODTExecutionError(
                        "No se pudo lanzar setup.exe con permisos de administrador.\n\n"
                        "Ejecuta la aplicación como Administrador:\n"
                        "1. Cierra esta app\n"
                        "2. Haz clic derecho > 'Ejecutar como administrador'\n"
                        "3. Vuelve a intentar la instalación"
                    )
            except Exception as e:
                logging.error("Error en ShellExecuteW: %s", e)
                raise ODTExecutionError(
                    f"Error al solicitar elevación: {e}\n\n"
                    "Ejecuta la aplicación como Administrador e intenta de nuevo."
                )
    else:
        try:
            proc = subprocess.Popen(
                [odt_exe_path, action, config_path],
                shell=False, creationflags=subprocess.CREATE_NO_WINDOW
            )
            proc.wait(timeout=600)
            logging.info("Descarga completada, código %d", proc.returncode)
            if proc.returncode != 0:
                raise ODTExecutionError(
                    f"La descarga terminó con error (código {proc.returncode}).\n\n"
                    "Verifica tu conexión a internet y la configuración."
                )
        except subprocess.TimeoutExpired:
            proc.kill()
            raise ODTExecutionError("La descarga excedió el tiempo de espera (10 min).")
        except OSError as e:
            logging.error("Error en descarga: %s", e)
            raise ODTExecutionError(
                f"Error al ejecutar setup.exe: {e}\n\n"
                "Si el error es por permisos, ejecuta la app como Administrador."
            )
