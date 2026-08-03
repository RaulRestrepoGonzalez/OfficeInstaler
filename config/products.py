"""
Catálogo de productos, canales de actualización e idiomas soportados
por el Office Deployment Tool (ODT) oficial de Microsoft.

Referencia oficial de IDs de producto y canales:
https://learn.microsoft.com/en-us/microsoft-365-apps/deploy/overview-office-deployment-tool
"""

# ProductId reales usados por el ODT (Click-to-Run).
PRODUCTS = {
    "Microsoft 365 Apps": {
        "products": {
            "Microsoft 365 Apps for enterprise": "O365ProPlusRetail",
            "Microsoft 365 Apps for business": "O365BusinessRetail",
        },
        "channels": ["Current", "MonthlyEnterprise", "SemiAnnual", "SemiAnnualPreview"],
        "icon": "365",
    },
    "Office LTSC 2024": {
        "products": {
            "Professional Plus 2024": "ProPlus2024Volume",
            "Standard 2024": "Standard2024Volume",
        },
        "channels": ["PerpetualVL2024"],
        "icon": "24",
    },
    "Office LTSC 2021": {
        "products": {
            "Professional Plus 2021": "ProPlus2021Volume",
            "Standard 2021": "Standard2021Volume",
        },
        "channels": ["PerpetualVL2021"],
        "icon": "21",
    },
    "Office 2019": {
        "products": {
            "Professional Plus 2019": "ProPlus2019Volume",
            "Standard 2019": "Standard2019Volume",
        },
        "channels": ["PerpetualVL2019"],
        "icon": "19",
    },
    "Office 2016": {
        "products": {
            "Professional Plus 2016": "ProPlus2016Volume",
            "Standard 2016": "Standard2016Volume",
        },
        "channels": ["PerpetualVL2016"],
        "icon": "16",
    },
}

# Aplicaciones individuales disponibles por producto (ID ODT : lista de apps).
# Teams solo viene incluido en Microsoft 365 Apps; las ediciones de volumen
# (LTSC/2019/2016) no lo incluyen. Access/Publisher solo en ProPlus y O365 Pro.
APPS_BY_PRODUCT_ID = {
    "O365ProPlusRetail": [
        "Access", "Excel", "OneNote", "Outlook", "PowerPoint", "Publisher",
        "Word", "Teams", "OneDrive", "Groove", "Lync",
    ],
    "O365BusinessRetail": [
        "Excel", "OneNote", "Outlook", "PowerPoint", "Word",
        "Teams", "OneDrive", "Lync",
    ],
    "ProPlus2024Volume": [
        "Access", "Excel", "OneNote", "Outlook", "PowerPoint", "Publisher",
        "Word", "OneDrive", "Groove", "Lync",
    ],
    "Standard2024Volume": [
        "Excel", "OneNote", "Outlook", "PowerPoint", "Word", "OneDrive", "Lync",
    ],
    "ProPlus2021Volume": [
        "Access", "Excel", "OneNote", "Outlook", "PowerPoint", "Publisher",
        "Word", "OneDrive", "Groove", "Lync",
    ],
    "Standard2021Volume": [
        "Excel", "OneNote", "Outlook", "PowerPoint", "Word", "OneDrive", "Lync",
    ],
    "ProPlus2019Volume": [
        "Access", "Excel", "OneNote", "Outlook", "PowerPoint", "Publisher",
        "Word", "OneDrive", "Groove", "Lync",
    ],
    "Standard2019Volume": [
        "Excel", "OneNote", "Outlook", "PowerPoint", "Word", "OneDrive", "Lync",
    ],
    "ProPlus2016Volume": [
        "Access", "Excel", "OneNote", "Outlook", "PowerPoint", "Publisher",
        "Word", "OneDrive", "Groove", "Lync",
    ],
    "Standard2016Volume": [
        "Excel", "OneNote", "Outlook", "PowerPoint", "Word", "OneDrive", "Lync",
    ],
}

# Todas las apps del catálogo (unión) para inicializar el estado de la UI.
ALL_APPS = sorted({app for apps in APPS_BY_PRODUCT_ID.values() for app in apps})

# Idiomas de instalación disponibles (código ODT : nombre visible).
LANGUAGES = {
    "Español": "es-es",
    "Inglés": "en-us",
    "Portugués (Brasil)": "pt-br",
    "Francés": "fr-fr",
    "Alemán": "de-de",
    "Italiano": "it-it",
    "Coreano": "ko-kr",
    "Japonés": "ja-jp",
    "Chino (Simplificado)": "zh-cn",
    "Vietnamita": "vi-vn",
    "Hindi": "hi-in",
}
