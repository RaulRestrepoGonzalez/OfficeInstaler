"""
Pruebas unitarias del generador de configuration.xml.
Ejecutar con: python -m pytest tests/
"""

import sys
import os
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.odt_config_builder import build_configuration_xml


def test_basic_install_xml_structure():
    xml_text = build_configuration_xml(
        product_id="O365ProPlusRetail",
        channel="Current",
        language_code="es-es",
        arch="x64",
        excluded_apps=["Access", "Publisher"],
        mode="install",
    )
    root = ET.fromstring(xml_text)

    add = root.find("Add")
    assert add is not None
    assert add.get("OfficeClientEdition") == "64"
    assert add.get("Channel") == "Current"

    product = add.find("Product")
    assert product.get("ID") == "O365ProPlusRetail"

    lang = product.find("Language")
    assert lang.get("ID") == "es-es"

    excluded = [e.get("ID") for e in product.findall("ExcludeApp")]
    assert excluded == ["Access", "Publisher"]

    display = root.find("Display")
    assert display.get("AcceptEULA") == "TRUE"


def test_download_mode_sets_source_path_and_updates():
    xml_text = build_configuration_xml(
        product_id="ProPlus2021Volume",
        channel="PerpetualVL2021",
        language_code="en-us",
        arch="x32",
        excluded_apps=[],
        mode="download",
        download_path="C:\\OfficeDownload",
    )
    root = ET.fromstring(xml_text)

    add = root.find("Add")
    assert add.get("OfficeClientEdition") == "32"
    assert add.get("SourcePath") == "C:\\OfficeDownload"

    updates = root.find("Updates")
    assert updates is not None
    assert updates.get("Enabled") == "TRUE"


if __name__ == "__main__":
    test_basic_install_xml_structure()
    test_download_mode_sets_source_path_and_updates()
    print("Todos los tests pasaron correctamente.")
