# src/02_analisis/analisis_clientes.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos

def analizar_clientes(df_clientes):
    """
    Análisis completo de la tabla Clientes.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE CLIENTES")
    logger.info("=" * 50)
    
    df = df_clientes.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    df['Límite Crédito USD'] = pd.to_numeric(df['Límite Crédito USD'], errors='coerce')
    df['Días Crédito'] = pd.to_numeric(df['Días Crédito'], errors='coerce')
    df['Descuento %'] = pd.to_numeric(df['Descuento %'], errors='coerce')
    df['Volumen Anual Estimado'] = pd.to_numeric(df['Volumen Anual Estimado'], errors='coerce')
    df['Fecha Registro'] = pd.to_datetime(df['Fecha Registro'], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    kpis_credito = calcular_kpis_basicos(df, 'Límite Crédito USD')
    kpis_volumen = calcular_kpis_basicos(df, 'Volumen Anual Estimado')
    
    logger.info(f"Total clientes: {len(df)}")
    logger.info(f"Límite crédito promedio: ${kpis_credito['promedio']:,.2f}")
    logger.info(f"Volumen anual estimado total: {kpis_volumen['total']:,.0f}")
    logger.info(f"Descuento promedio: {df['Descuento %'].mean():.1f}%")
    
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
    
    # 5. Por Sector
    logger.info("\n--- POR SECTOR ---")
    sector = df['Sector'].value_counts()
    logger.info(f"\n{sector}")
    
    # 6. Top 10 clientes por límite de crédito
    logger.info("\n--- TOP 10 LÍMITE DE CRÉDITO ---")
    top_credito = df.nlargest(10, 'Límite Crédito USD')[['ID', 'Empresa', 'País', 'Tipo', 'Límite Crédito USD', 'Estado']]
    logger.info(f"\n{top_credito}")
    
    # 7. Clientes morosos
    logger.info("\n--- CLIENTES MOROSOS ---")
    morosos = df[df['Estado'] == 'Moroso'][['ID', 'Empresa', 'País', 'Límite Crédito USD', 'Días Crédito']]
    logger.info(f"Total morosos: {len(morosos)}")
    logger.info(f"\n{morosos}")
    
    logger.info("\n✓ Análisis de clientes completado")
    
    return {
        'total': len(df),
        'credito_promedio': kpis_credito['promedio'],
        'volumen_total': kpis_volumen['total'],
        'estado': estado,
        'por_pais': pais,
        'por_tipo': tipo,
        'por_sector': sector,
        'top_credito': top_credito,
        'morosos': morosos
    }