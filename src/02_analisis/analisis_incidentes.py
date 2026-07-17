# src/02_analisis/analisis_incidentes.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos

def analizar_incidentes(df_incidentes):
    """
    Análisis completo de la tabla Incidentes_Transporte.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE INCIDENTES DE TRANSPORTE")
    logger.info("=" * 50)
    
    df = df_incidentes.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID_Incidente'] == 'ID_Incidente':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    df['Costo_Incidente_USD'] = pd.to_numeric(df['Costo_Incidente_USD'], errors='coerce')
    df['Horas_Retraso'] = pd.to_numeric(df['Horas_Retraso'], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    kpis_costo = calcular_kpis_basicos(df, 'Costo_Incidente_USD')
    kpis_retraso = calcular_kpis_basicos(df, 'Horas_Retraso')
    
    logger.info(f"Total incidentes: {len(df)}")
    logger.info(f"Costo total incidentes: ${kpis_costo['total']:,.2f}")
    logger.info(f"Costo promedio por incidente: ${kpis_costo['promedio']:,.2f}")
    logger.info(f"Retraso total: {kpis_retraso['total']:,.0f} horas")
    logger.info(f"Retraso promedio: {kpis_retraso['promedio']:.1f} horas")
    
    # 2. Por Tipo de Incidente
    logger.info("\n--- POR TIPO DE INCIDENTE ---")
    tipo = df['Tipo_Incidente'].value_counts()
    logger.info(f"\n{tipo}")
    
    # 3. Costo por tipo
    logger.info("\n--- COSTO POR TIPO ---")
    costo_tipo = df.groupby('Tipo_Incidente')['Costo_Incidente_USD'].agg(['count', 'sum', 'mean']).sort_values('sum', ascending=False)
    logger.info(f"\n{costo_tipo}")
    
    # 4. Top 10 incidentes más costosos
    logger.info("\n--- TOP 10 MÁS COSTOSOS ---")
    top_costo = df.nlargest(10, 'Costo_Incidente_USD')[['ID_Incidente', 'ID_Venta', 'Tipo_Incidente', 'Costo_Incidente_USD', 'Horas_Retraso']]
    logger.info(f"\n{top_costo}")
    
    # 5. Top 10 mayores retrasos
    logger.info("\n--- TOP 10 MAYORES RETRASOS ---")
    top_retraso = df.nlargest(10, 'Horas_Retraso')[['ID_Incidente', 'ID_Venta', 'Tipo_Incidente', 'Horas_Retraso', 'Costo_Incidente_USD']]
    logger.info(f"\n{top_retraso}")
    
    # 6. Correlación costo vs retraso
    logger.info("\n--- CORRELACIÓN ---")
    corr = df['Costo_Incidente_USD'].corr(df['Horas_Retraso'])
    logger.info(f"Correlación Costo vs Retraso: {corr:.3f}")
    
    logger.info("\n✓ Análisis de incidentes completado")
    
    return {
        'total_incidentes': len(df),
        'costo_total': kpis_costo['total'],
        'costo_promedio': kpis_costo['promedio'],
        'retraso_total': kpis_retraso['total'],
        'retraso_promedio': kpis_retraso['promedio'],
        'por_tipo': tipo,
        'costo_por_tipo': costo_tipo,
        'top_costo': top_costo,
        'top_retraso': top_retraso,
        'correlacion': corr
    }