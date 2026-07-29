import os
import sys


def _get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    try:
        __compiled__
    except NameError:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    else:
        return os.path.dirname(sys.executable)


BASE_DIR = _get_base_dir()

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

ODT_PATH_DEFAULT = os.path.join(BASE_DIR, "setup.exe")

ODT_DIR = os.path.join(BASE_DIR, "odt")
ODT_EXPECTED_PATH = os.path.join(ODT_DIR, "setup.exe")

DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ODT_DIR, exist_ok=True)
