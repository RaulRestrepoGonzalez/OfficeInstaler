import os
import json
import urllib.request
import urllib.error
import subprocess
import tempfile
import shutil
import ssl


ODT_DOWNLOAD_PAGE = "https://www.microsoft.com/en-us/download/details.aspx?id=49117"


class ODTDownloadError(Exception):
    pass


def _get_download_url() -> str:
    context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(ODT_DOWNLOAD_PAGE, timeout=30, context=context) as resp:
            html = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise ODTDownloadError(f"No se pudo acceder a la página de descarga: {e}")

    start_marker = "__DLCDetails__"
    start_idx = html.find(start_marker)
    if start_idx == -1:
        raise ODTDownloadError("No se encontró la información de descarga en la página")

    json_start = html.index("{", start_idx)

    depth = 0
    json_end = json_start
    for i in range(json_start, len(html)):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                json_end = i + 1
                break

    json_str = html[json_start:json_end]

    try:
        data = json.loads(json_str)
        files = data.get("dlcDetailsView", {}).get("downloadFile", [])
        if not files:
            raise ODTDownloadError("No se encontraron archivos de descarga")
        url = files[0].get("url", "")
        if not url:
            raise ODTDownloadError("URL de descarga vacía")
        return url
    except (KeyError, json.JSONDecodeError, IndexError) as e:
        raise ODTDownloadError(f"Error al parsear la información de descarga: {e}")


def _reporthook(progress_callback):
    def inner(block_count, block_size, total_size):
        if progress_callback and total_size > 0:
            progress_callback(block_count * block_size, total_size)
    return inner


def _find_setup(target_dir: str) -> str | None:
    for root, _dirs, files in os.walk(target_dir):
        for f in files:
            if f.lower() == "setup.exe":
                return os.path.join(root, f)
    return None


def _extract_cab(cab_path: str, target_dir: str) -> bool:
    try:
        result = subprocess.run(
            ["expand.exe", "-R", cab_path, "-F:*", target_dir],
            capture_output=True, timeout=120
        )
        return result.returncode == 0 and os.path.isfile(os.path.join(target_dir, "setup.exe"))
    except (subprocess.TimeoutExpired, OSError):
        return False


def download_odt(target_dir: str, progress_callback=None) -> str:
    url = _get_download_url()
    filename = os.path.basename(url)

    with tempfile.TemporaryDirectory(prefix="odt_download_") as tmpdir:
        download_path = os.path.join(tmpdir, filename)

        try:
            urllib.request.urlretrieve(
                url, download_path,
                reporthook=_reporthook(progress_callback)
            )
        except Exception as e:
            raise ODTDownloadError(f"Error al descargar ODT: {e}")

        os.makedirs(target_dir, exist_ok=True)

        with open(download_path, "rb") as f:
            data = f.read()

        cab_start = data.find(b"MSCF")
        if cab_start < 0:
            raise ODTDownloadError(
                "El archivo descargado no contiene un formato válido. "
                "Descarga manualmente desde:\n"
                "https://www.microsoft.com/en-us/download/details.aspx?id=49117"
            )

        cab_path = os.path.join(tmpdir, "odt.cab")
        with open(cab_path, "wb") as f:
            f.write(data[cab_start:])

        if not _extract_cab(cab_path, target_dir):
            raise ODTDownloadError(
                "No se pudo extraer setup.exe del paquete ODT. "
                "Descarga manualmente el Office Deployment Tool desde:\n"
                "https://www.microsoft.com/en-us/download/details.aspx?id=49117\n"
                "y coloca setup.exe en la raíz del proyecto."
            )

        setup_exe = os.path.join(target_dir, "setup.exe")
        if not os.path.isfile(setup_exe):
            found = _find_setup(target_dir)
            if found:
                shutil.copy2(found, setup_exe)
            else:
                raise ODTDownloadError("No se encontró setup.exe después de la extracción")

        return setup_exe
