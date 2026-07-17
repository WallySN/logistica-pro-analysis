# src/02_analisis/analisis_proveedores.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos

def analizar_proveedores(df_proveedores):
    """
    Análisis completo de la tabla Proveedores.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE PROVEEDORES")
    logger.info("=" * 50)
    
    df = df_proveedores.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    df['Lead Time Días'] = pd.to_numeric(df['Lead Time Días'], errors='coerce')
    df['MOQ (Cantidad Mínima)'] = pd.to_numeric(df['MOQ (Cantidad Mínima)'], errors='coerce')
    df['Calificación'] = pd.to_numeric(df['Calificación'], errors='coerce')
    df['Años de Relación'] = pd.to_numeric(df['Años de Relación'], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    logger.info(f"Total proveedores: {len(df)}")
    logger.info(f"Lead Time promedio: {df['Lead Time Días'].mean():.1f} días")
    logger.info(f"MOQ promedio: {df['MOQ (Cantidad Mínima)'].mean():.0f}")
    logger.info(f"Calificación promedio: {df['Calificación'].mean():.2f}")
    logger.info(f"Años de relación promedio: {df['Años de Relación'].mean():.1f}")
    
    # 2. Por Estado
    logger.info("\n--- POR ESTADO ---")
    estado = df['Estado'].value_counts()
    logger.info(f"\n{estado}")
    
    # 3. Por País
    logger.info("\n--- POR PAÍS ---")
    pais = df['País'].value_counts()
    logger.info(f"\n{pais}")
    
    # 4. Por Tipo
    logger.info("\n--- POR TIPO ---")
    tipo = df['Tipo'].value_counts()
    logger.info(f"\n{tipo}")
    
    # 5. Top 10 calificaciones
    logger.info("\n--- TOP 10 CALIFICACIONES ---")
    top_calif = df.nlargest(10, 'Calificación')[['ID', 'Nombre', 'País', 'Calificación', 'Años de Relación']]
    logger.info(f"\n{top_calif}")
    
    # 6. Por condición de pago
    logger.info("\n--- CONDICIÓN DE PAGO ---")
    pago = df['Condición de Pago'].value_counts()
    logger.info(f"\n{pago}")
    
    # 7. Proveedores con menor lead time
    logger.info("\n--- TOP 10 MENOR LEAD TIME ---")
    top_lead = df.nsmallest(10, 'Lead Time Días')[['ID', 'Nombre', 'País', 'Lead Time Días', 'Calificación']]
    logger.info(f"\n{top_lead}")
    
    logger.info("\n✓ Análisis de proveedores completado")
    
    return {
        'total': len(df),
        'lead_time_promedio': df['Lead Time Días'].mean(),
        'calificacion_promedio': df['Calificación'].mean(),
        'estado': estado,
        'por_pais': pais,
        'por_tipo': tipo,
        'top_calificaciones': top_calif,
        'condicion_pago': pago,
        'top_lead_time': top_lead
    }