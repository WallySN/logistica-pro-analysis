# src/02_analisis/analisis_transporte.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos

def analizar_transporte(df_transporte):
    """
    Análisis completo de la tabla Transporte.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE TRANSPORTE")
    logger.info("=" * 50)
    
    df = df_transporte.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    cols_num = ['Costo Base USD', 'Costo por kg USD', 'Costo por m3 USD',
                'Tiempo Estimado Días', 'Capacidad Máx kg']
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    kpis_base = calcular_kpis_basicos(df, 'Costo Base USD')
    kpis_kg = calcular_kpis_basicos(df, 'Costo por kg USD')
    kpis_tiempo = calcular_kpis_basicos(df, 'Tiempo Estimado Días')
    
    logger.info(f"Total rutas: {len(df)}")
    logger.info(f"Costo base promedio: ${kpis_base['promedio']:,.2f}")
    logger.info(f"Costo por kg promedio: ${kpis_kg['promedio']:,.2f}")
    logger.info(f"Tiempo estimado promedio: {kpis_tiempo['promedio']:.1f} días")
    
    # 2. Por Tipo
    logger.info("\n--- POR TIPO ---")
    tipo = df['Tipo'].value_counts()
    logger.info(f"\n{tipo}")
    
    # 3. Por Modalidad
    logger.info("\n--- POR MODALIDAD ---")
    modalidad = df['Modalidad'].value_counts()
    logger.info(f"\n{modalidad}")
    
    # 4. Por Empresa
    logger.info("\n--- POR EMPRESA ---")
    empresa = df.groupby('Empresa')['Costo Base USD'].agg(['count', 'mean']).sort_values('count', ascending=False)
    logger.info(f"\n{empresa}")
    
    # 5. Por Estado
    logger.info("\n--- POR ESTADO ---")
    estado = df['Estado'].value_counts()
    logger.info(f"\n{estado}")
    
    # 6. Rutas más caras
    logger.info("\n--- TOP 10 RUTAS MÁS CARAS ---")
    top_costo = df.nlargest(10, 'Costo Base USD')[['ID', 'Nombre Ruta', 'Tipo', 'Empresa', 'Origen', 'Destino', 'Costo Base USD']]
    logger.info(f"\n{top_costo}")
    
    # 7. Rutas más rápidas
    logger.info("\n--- TOP 10 RUTAS MÁS RÁPIDAS ---")
    top_rapido = df.nsmallest(10, 'Tiempo Estimado Días')[['ID', 'Nombre Ruta', 'Tipo', 'Origen', 'Destino', 'Tiempo Estimado Días']]
    logger.info(f"\n{top_rapido}")
    
    # 8. Seguro y Tracking
    logger.info("\n--- COBERTURA ---")
    logger.info(f"Con seguro: {df['Seguro Incluido'].value_counts().get('Sí', 0)}")
    logger.info(f"Con tracking: {df['Tracking Disponible'].value_counts().get('Sí', 0)}")
    
    logger.info("\n✓ Análisis de transporte completado")
    
    return {
        'total_rutas': len(df),
        'costo_base_promedio': kpis_base['promedio'],
        'tiempo_promedio': kpis_tiempo['promedio'],
        'por_tipo': tipo,
        'por_modalidad': modalidad,
        'por_empresa': empresa,
        'estado': estado,
        'top_costo': top_costo,
        'top_rapido': top_rapido
    }