import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.odt_downloader import _get_download_url
from core.odt_runner import find_odt


def test_get_download_url_returns_valid_url():
    url = _get_download_url()
    assert url.endswith(".exe"), "La URL debe terminar en .exe"
    assert "download.microsoft.com" in url, "La URL debe ser de Microsoft"
    assert "officedeploymenttool" in url, "La URL debe contener officedeploymenttool"


def test_find_odt_returns_path_when_exists(tmp_path):
    (tmp_path / "setup.exe").write_text("fake")
    odt_dir = str(tmp_path)
    result = find_odt(str(tmp_path / "setup.exe"), odt_dir)
    assert result == str(tmp_path / "setup.exe")


def test_find_odt_returns_odt_dir_when_not_at_default(tmp_path):
    odt_sub = tmp_path / "odt"
    odt_sub.mkdir()
    (odt_sub / "setup.exe").write_text("fake")
    result = find_odt(str(tmp_path / "setup.exe"), str(odt_sub))
    assert result == str(odt_sub / "setup.exe")


def test_find_odt_returns_none_when_not_found(tmp_path):
    result = find_odt(str(tmp_path / "nonexistent.exe"), str(tmp_path))
    assert result is None


if __name__ == "__main__":
    test_get_download_url_returns_valid_url()
    test_find_odt_returns_path_when_exists(__import__("tempfile").mkdtemp())
    print("Tests del downloader OK")
