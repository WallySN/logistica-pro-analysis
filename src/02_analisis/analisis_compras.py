# src/02_analisis/analisis_compras.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos, resumen_categorias

def analizar_compras(df_compras):
    """
    Análisis completo de la tabla Compras.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE COMPRAS")
    logger.info("=" * 50)
    
    df = df_compras.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    cols_num = ['Cantidad Solicitada', 'Cantidad Recibida', 'Costo Unitario USD',
                'Costo Total USD', 'Descuento %', 'Impuesto USD', 'Total USD']
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fechas
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Fecha Entrega Esperada'] = pd.to_datetime(df['Fecha Entrega Esperada'], errors='coerce')
    df['Fecha Entrega Real'] = pd.to_datetime(df['Fecha Entrega Real'], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    kpis_total = calcular_kpis_basicos(df, 'Total USD')
    kpis_costo = calcular_kpis_basicos(df, 'Costo Total USD')
    
    logger.info(f"Total órdenes: {len(df)}")
    logger.info(f"Compras totales USD: ${kpis_total['total']:,.2f}")
    logger.info(f"Costo promedio: ${kpis_costo['promedio']:,.2f}")
    
    # 2. Por Estado
    logger.info("\n--- POR ESTADO ---")
    estado = df['Estado'].value_counts()
    logger.info(f"\n{estado}")
    
    # 3. Por Proveedor
    logger.info("\n--- TOP 10 PROVEEDORES ---")
    prov = resumen_categorias(df, 'Proveedor', 'Total USD').head(10)
    logger.info(f"\n{prov}")
    
    # 4. Por Almacén Destino
    logger.info("\n--- POR ALMACÉN DESTINO ---")
    alm = resumen_categorias(df, 'Almacén Destino', 'Total USD')
    logger.info(f"\n{alm}")
    
    # 5. Tasa de cumplimiento (cantidad recibida vs solicitada)
    logger.info("\n--- CUMPLIMIENTO DE ENTREGA ---")
    df['Cumplimiento %'] = (df['Cantidad Recibida'] / df['Cantidad Solicitada'] * 100).round(2)
    cumplimiento = df['Cumplimiento %'].describe()
    logger.info(f"\n{cumplimiento}")
    
    # 6. Diferencia de días (entrega real vs esperada)
    logger.info("\n--- TIEMPOS DE ENTREGA ---")
    df['Dias Retraso'] = (df['Fecha Entrega Real'] - df['Fecha Entrega Esperada']).dt.days
    tiempos = df['Dias Retraso'].describe()
    logger.info(f"\n{tiempos}")
    
    # 7. Por Moneda
    logger.info("\n--- POR MONEDA ---")
    moneda = df['Moneda'].value_counts()
    logger.info(f"\n{moneda}")
    
    logger.info("\n✓ Análisis de compras completado")
    
    return {
        'kpis_total': kpis_total,
        'kpis_costo': kpis_costo,
        'estado': estado,
        'por_proveedor': prov,
        'por_almacen': alm,
        'cumplimiento': cumplimiento,
        'tiempos': tiempos,
        'moneda': moneda
    }