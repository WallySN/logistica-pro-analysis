# src/02_analisis/analisis_devoluciones.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger

def analizar_devoluciones(df_devoluciones):
    """
    Análisis completo de la tabla Devoluciones.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE DEVOLUCIONES")
    logger.info("=" * 50)
    
    df = df_devoluciones.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID_Devolución'] == 'ID_Devolución':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir fecha (intentar formato normal primero, luego Excel serial)
    try:
        df['Fecha_Devolución'] = pd.to_datetime(df['Fecha_Devolución'], errors='coerce')
    except:
        try:
            df['Fecha_Devolución'] = pd.to_datetime(df['Fecha_Devolución'], errors='coerce', unit='D', origin='1899-12-30')
        except:
            df['Fecha_Devolución'] = pd.to_datetime(df['Fecha_Devolución'], errors='coerce', format='%Y-%m-%d')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    logger.info(f"Total devoluciones: {len(df)}")
    
    # 2. Por Motivo
    logger.info("\n--- POR MOTIVO ---")
    motivo = df['Motivo'].value_counts()
    logger.info(f"\n{motivo}")
    
    # 3. Por Estado del Producto
    logger.info("\n--- POR ESTADO DEL PRODUCTO ---")
    estado = df['Estado_Producto'].value_counts()
    logger.info(f"\n{estado}")
    
    # 4. Porcentajes
    logger.info("\n--- DISTRIBUCIÓN PORCENTUAL ---")
    pct_motivo = df['Motivo'].value_counts(normalize=True) * 100
    logger.info("\nMotivo:")
    logger.info(f"\n{pct_motivo.round(1)}")
    
    pct_estado = df['Estado_Producto'].value_counts(normalize=True) * 100
    logger.info("\nEstado Producto:")
    logger.info(f"\n{pct_estado.round(1)}")
    
    # 5. Cruzar motivo vs estado
    logger.info("\n--- CRUCE MOTIVO vs ESTADO ---")
    cruce = pd.crosstab(df['Motivo'], df['Estado_Producto'])
    logger.info(f"\n{cruce}")
    
    # 6. Devoluciones por mes
    logger.info("\n--- DEVOLUCIONES POR MES ---")
    df['Año-Mes'] = df['Fecha_Devolución'].dt.to_period('M')
    mes = df['Año-Mes'].value_counts().sort_index()
    logger.info(f"\n{mes}")
    
    logger.info("\n✓ Análisis de devoluciones completado")
    
    return {
        'total': len(df),
        'por_motivo': motivo,
        'por_estado': estado,
        'pct_motivo': pct_motivo,
        'pct_estado': pct_estado,
        'cruce_motivo_estado': cruce,
        'por_mes': mes
    }