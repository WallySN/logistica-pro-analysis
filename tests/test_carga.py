# tests/test_carga.py
import sys
from pathlib import Path
import importlib.util

# Agregar raíz del proyecto al path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.config import EXCEL_FILE


def cargar_modulo(ruta_relativa, nombre_modulo):
    """Carga un módulo dinámicamente."""
    ruta = PROJECT_ROOT / "src" / ruta_relativa
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre_modulo] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_archivo_existe():
    """Verifica que el archivo Excel existe."""
    assert EXCEL_FILE.exists(), f"Archivo no encontrado: {EXCEL_FILE}"
    print(f"✓ Archivo existe: {EXCEL_FILE}")


def test_cargar_hojas():
    """Prueba la carga de hojas del Excel."""
    mod_carga = cargar_modulo("01_carga_datos/cargar_excel.py", "test_cargar_excel")
    hojas = mod_carga.cargar_hojas_excel()
    
    assert len(hojas) > 0, "No se cargaron hojas"
    assert 'Productos' in hojas, "Falta hoja Productos"
    assert 'Ventas' in hojas, "Falta hoja Ventas"
    
    print(f"✓ Hojas cargadas: {list(hojas.keys())}")
    print(f"✓ Productos: {len(hojas['Productos'])} filas")
    print(f"✓ Ventas: {len(hojas['Ventas'])} filas")


if __name__ == "__main__":
    test_archivo_existe()
    test_cargar_hojas()
    print("\n✓ Todos los tests de carga pasaron")