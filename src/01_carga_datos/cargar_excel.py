# src/01_carga_datos/cargar_excel.py
import pandas as pd
import sys
from pathlib import Path

# Agregar raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import EXCEL_FILE, DATA_PROCESSED
from utils.loggers import logger

def cargar_hojas_excel(ruta_archivo=None):
    """
    Carga todas las hojas del archivo Excel.
    Retorna un diccionario con DataFrames.
    """
    if ruta_archivo is None:
        ruta_archivo = EXCEL_FILE
    
    logger.info(f"Cargando archivo: {ruta_archivo}")
    
    try:
        # Cargar todas las hojas
        excel = pd.ExcelFile(ruta_archivo)
        hojas = {}
        
        for nombre_hoja in excel.sheet_names:
            logger.info(f"  → Cargando hoja: {nombre_hoja}")
            df = pd.read_excel(excel, sheet_name=nombre_hoja)
            
            # Limpiar nombres de columnas (quitar espacios extras)
            df.columns = df.columns.str.strip()
            
            # Eliminar filas duplicadas de encabezado si existen
            if len(df) > 0 and df.iloc[0].astype(str).equals(df.columns.astype(str)):
                df = df.iloc[1:].reset_index(drop=True)
            
            hojas[nombre_hoja] = df
            logger.info(f"    ✓ {len(df)} filas, {len(df.columns)} columnas")
        
        logger.info(f"✓ Carga completada: {len(hojas)} hojas")
        return hojas
        
    except FileNotFoundError:
        logger.error(f"✗ Archivo no encontrado: {ruta_archivo}")
        raise
    except Exception as e:
        logger.error(f"✗ Error al cargar Excel: {str(e)}")
        raise

def guardar_datos_procesados(hojas, carpeta_salida=None):
    """Guarda cada hoja como CSV en data/processed."""
    if carpeta_salida is None:
        carpeta_salida = DATA_PROCESSED
    
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    
    for nombre, df in hojas.items():
        ruta_csv = carpeta_salida / f"{nombre.lower().replace(' ', '_')}.csv"
        df.to_csv(ruta_csv, index=False, encoding='utf-8')
        logger.info(f"  → Guardado: {ruta_csv.name}")

def main():
    """Ejecuta la carga y guardado de datos."""
    logger.info("=" * 50)
    logger.info("INICIANDO CARGA DE DATOS")
    logger.info("=" * 50)
    
    # Cargar datos
    hojas = cargar_hojas_excel()
    
    # Guardar como CSV procesados
    guardar_datos_procesados(hojas)
    
    logger.info("=" * 50)
    logger.info("CARGA COMPLETADA")
    logger.info("=" * 50)
    
    return hojas

if __name__ == "__main__":
    main()