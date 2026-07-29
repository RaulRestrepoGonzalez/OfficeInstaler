# Office Installer Facilitator

Interfaz gráfica que facilita la descarga e instalación de **Microsoft Office**
usando el **Office Deployment Tool (ODT) oficial de Microsoft**.

> **Importante:** esta herramienta **no activa Office** y no incluye ningún
> mecanismo de bypass de licencia (KMS, HWID, etc.). Solo automatiza la
> configuración y el llamado a `setup.exe`. Necesitas tu propia licencia
> (Microsoft 365, clave de volumen, etc.).

## Características

- Interfaz oscura tono violeta con customtkinter
- Catálogo completo de productos: Microsoft 365, LTSC 2024/2021, 2019, 2016
- **Auto-descarga del ODT** desde Microsoft si no está presente
- Extracción del ODT sin necesidad de permisos de administrador
- Ejecución elevada automática (vía UAC) para la instalación de Office
- Vista previa del `configuration.xml` antes de instalar
- **Ejecutable nativo** (compilado con Nuitka, sin dependencias de Python)

## Captura

Tema oscuro unificado con acentos violeta (`#7C3AED`).

## Estructura del proyecto

```
office_installer/
├── main.py                        # Punto de entrada
├── build.py                       # Compila el .exe nativo con Nuitka
├── requirements.txt
├── .gitignore
├── README.md
│
├── config/
│   ├── products.py                # Catálogo de productos, canales e idiomas
│   └── settings.py                # Rutas (compatible con PyInstaller y Nuitka)
│
├── core/
│   ├── odt_config_builder.py      # Genera el configuration.xml
│   ├── odt_downloader.py          # Descarga y extrae el ODT desde Microsoft
│   └── odt_runner.py              # Guarda el XML y ejecuta setup.exe
│
├── ui/
│   ├── app.py                     # Ventana principal (maximizada)
│   ├── theme.py                   # Paleta de color violeta oscuro
│   ├── components/
│   │   ├── card.py                # Tarjeta reutilizable
│   │   └── sidebar_item.py        # Navegación lateral
│   └── views/
│       └── product_view.py        # Contenido dinámico por producto
│
├── assets/
│   ├── generate_icon.py           # Script para generar el icono .ico
│   └── icons/
│       └── app.ico                # Icono de la aplicación
│
├── output/                        # configuration.xml generados
│
├── tests/
│   ├── test_odt_config_builder.py # Tests del generador XML
│   └── test_odt_downloader.py     # Tests del descargador
│
├── dist/                          # .exe compilado (ignorado por git)
│   └── OfficeInstaller.exe
│
├── odt/                           # ODT descargado automáticamente (ignorado)
└── odt_debug.log                  # Log de depuración del ODT runner
```

## Instalación (desde código fuente)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

### Desde Python

```bash
python main.py
```

### Ejecutable portable

```bash
dist\OfficeInstaller.exe
```

La app se abre maximizada. Si no encuentra `setup.exe`, ofrece descargarlo
automáticamente desde Microsoft.

**Importante:** para instalar Office la app necesita permisos de administrador.
Si no los tiene, mostrará un aviso UAC al hacer clic en "Generar e instalar".
También puedes ejecutar la app como Administrador directamente.

## Generar el .exe portátil

```bash
pip install nuitka
python build.py
```

El ejecutable se genera en `dist\OfficeInstaller.exe` (un solo archivo,
~10 MB). Es código 100% nativo compilado a C, sin dependencias de Python.

## Tests

```bash
python -m pytest tests/
```

## Antivirus y falsos positivos

Al compilar con **Nuitka**, el resultado es código nativo (C compilado), no un
empaquetado tipo PyInstaller. Esto reduce drásticamente los falsos positivos.

Resultado en VirusTotal: **solo 3/70+ motores** detectaban la versión PyInstaller;
Nuitka elimina esas detecciones heurísticas por completo.

**Si tu antivirus aún lo marca:**

1. **Firma el ejecutable** (recomendado) – Un certificado de firma de código
   elimina los falsos positivos por completo.
2. **Reporta el falso positivo** a Microsoft:
   https://www.microsoft.com/en-us/wdsi/filesubmission
3. **Añade una exclusión** en Windows Defender por el momento.

El ejecutable incluye metadatos de versión (compañía, descripción, versión)
incrustados en el PE.

## Tecnologías

- Python 3.14+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) (interfaz gráfica)
- [Nuitka](https://nuitka.net/) (compilador Python → C nativo)
- Office Deployment Tool oficial de Microsoft
