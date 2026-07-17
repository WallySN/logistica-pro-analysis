import os
from pathlib import Path

# ==============================================================================
# CONFIGURACIÓN DE RUTAS BASE
# ==============================================================================

# config.py está en src/utils/config.py -> Subimos 3 niveles para llegar a la raíz
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==============================================================================
# RUTAS DE DATOS
# ==============================================================================
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# ==============================================================================
# RUTAS DE REPORTES Y SALIDAS
# ==============================================================================
OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
REPORTS_DIR = OUTPUTS_DIR / "reports"

# Rutas específicas de figuras
FIGURES_GENERALES = FIGURES_DIR / "generales"
FIGURES_PRODUCTOS = FIGURES_DIR / "productos"
FIGURES_VENTAS = FIGURES_DIR / "ventas"
FIGURES_COMPRAS = FIGURES_DIR / "compras"
FIGURES_PROVEEDORES = FIGURES_DIR / "proveedores"
FIGURES_INVENTARIO = FIGURES_DIR / "inventario"
FIGURES_INCIDENTES = FIGURES_DIR / "incidentes"
FIGURES_DEVOLUCIONES = FIGURES_DIR / "devoluciones"

# Rutas de reportes
REPORTS_PDF = REPORTS_DIR / "pdf_executives"
REPORTS_EXCEL = REPORTS_DIR / "excel_summaries"

# ==============================================================================
# CREACIÓN DE DIRECTORIOS
# ==============================================================================
DIRECTORIOS = [
    DATA_RAW, 
    DATA_PROCESSED, 
    OUTPUTS_DIR,
    FIGURES_DIR, 
    REPORTS_DIR,
    FIGURES_GENERALES, 
    FIGURES_PRODUCTOS, 
    FIGURES_VENTAS,
    FIGURES_COMPRAS, 
    FIGURES_PROVEEDORES, 
    FIGURES_INVENTARIO,
    FIGURES_INCIDENTES, 
    FIGURES_DEVOLUCIONES,
    REPORTS_PDF, 
    REPORTS_EXCEL
]

for path in DIRECTORIOS:
    path.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# DETECCIÓN DE ARCHIVOS EXCEL
# ==============================================================================

# Buscar CUALQUIER archivo .xlsx en data/raw/
archivos_excel = list(DATA_RAW.glob("*.xlsx"))

if archivos_excel:
    EXCEL_FILE = archivos_excel[0]
    print(f"📁 Archivo Excel encontrado de forma dinámica: {EXCEL_FILE.name}")
else:
    # Fallback al nombre por defecto
    EXCEL_FILE = DATA_RAW / "logistica_pro_expandido (2).xlsx"
    print(f"⚠️ No se encontró ningún Excel dinámico en data/raw/, usando fallback por defecto: {EXCEL_FILE.name}")