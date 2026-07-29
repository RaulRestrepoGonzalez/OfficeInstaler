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
- **Ejecutable portable** (generado con PyInstaller, sin dependencias)

## Captura

Tema oscuro unificado con acentos violeta (`#7C3AED`).

## Estructura del proyecto

```
office_installer/
├── main.py                        # Punto de entrada
├── build.py                       # Genera el .exe portable con PyInstaller
├── requirements.txt
├── .gitignore
├── README.md
│
├── config/
│   ├── products.py                # Catálogo de productos, canales e idiomas
│   └── settings.py                # Rutas (compatible con PyInstaller)
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
├── dist/                          # .exe generado (ignorado por git)
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

## Generar el .exe portable

```bash
pip install pyinstaller
python build.py
```

El ejecutable se genera en `dist\OfficeInstaller.exe`. Es un solo archivo
portátil que no requiere Python ni dependencias.

## Tests

```bash
python -m pytest tests/
```

## Antivirus y falsos positivos

Al empaquetar con PyInstaller, algunos antivirus pueden detectar el `.exe`
como falso positivo. Esto es común en ejecutables creados con empaquetadores
de Python.

**Para evitarlo:**

1. **Firma el ejecutable** (recomendado) – Un certificado de firma de código
   (code signing) elimina los falsos positivos. Costo aprox. $200-300/año.
2. **Reporta el falso positivo** a Microsoft:
   https://www.microsoft.com/en-us/wdsi/filesubmission
3. **Añade una exclusión** en Windows Defender por el momento.

El ejecutable ya incluye metadatos de versión (compañía, descripción, versión)
para reducir detecciones heurísticas.

## Tecnologías

- Python 3.14+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) (interfaz gráfica)
- [PyInstaller](https://pyinstaller.org/) (empaquetado)
- Office Deployment Tool oficial de Microsoft
