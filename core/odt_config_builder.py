"""
Generación del configuration.xml que consume el Office Deployment Tool (ODT)
oficial de Microsoft. Módulo sin dependencias de UI: puede probarse de forma
aislada (ver tests/test_odt_config_builder.py).
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom


def build_configuration_xml(product_id: str, channel: str, language_code: str,
                             arch: str, excluded_apps: list[str], mode: str,
                             download_path: str | None = None) -> str:
    """
    Construye el XML de configuración del ODT.

    Args:
        product_id: ID de producto Click-to-Run (ej. "O365ProPlusRetail").
        channel: canal de actualización (ej. "Current", "PerpetualVL2021").
        language_code: código de idioma ODT (ej. "es-es").
        arch: "x64" o "x32".
        excluded_apps: lista de IDs de apps a excluir (ej. ["Access", "Publisher"]).
        mode: "install" o "download".
        download_path: carpeta local usada como SourcePath cuando mode == "download".

    Returns:
        XML formateado como string, listo para escribirse a disco.
    """
    configuration = ET.Element("Configuration")

    add = ET.SubElement(configuration, "Add")
    add.set("OfficeClientEdition", "64" if arch == "x64" else "32")
    add.set("Channel", channel)
    if mode == "download" and download_path:
        add.set("SourcePath", download_path)

    product = ET.SubElement(add, "Product")
    product.set("ID", product_id)

    lang = ET.SubElement(product, "Language")
    lang.set("ID", language_code)

    for app in excluded_apps:
        exclude = ET.SubElement(product, "ExcludeApp")
        exclude.set("ID", app)

    display = ET.SubElement(configuration, "Display")
    display.set("Level", "Full")
    display.set("AcceptEULA", "TRUE")

    if mode == "download":
        updates = ET.SubElement(configuration, "Updates")
        updates.set("Enabled", "TRUE")

    rough = ET.tostring(configuration, encoding="utf-8")
    return minidom.parseString(rough).toprettyxml(indent="  ")
