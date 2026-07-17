# src/02_analisis/analisis_ventas.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos, resumen_categorias

def analizar_ventas(df_ventas):
    """
    Análisis completo de la tabla Ventas.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE VENTAS")
    logger.info("=" * 50)
    
    df = df_ventas.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir columnas numéricas
    cols_num = ['Cantidad', 'Precio Unitario USD', 'Subtotal USD', 
                'Descuento %', 'Impuesto USD', 'Total USD']
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convertir fechas
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Fecha Envío'] = pd.to_datetime(df['Fecha Envío'], errors='coerce')
    df['Fecha Entrega'] = pd.to_datetime(df['Fecha Entrega'], errors='coerce')
    
    # 1. KPIs Generales
    logger.info("\n--- KPIs GENERALES ---")
    kpis_total = calcular_kpis_basicos(df, 'Total USD')
    kpis_cantidad = calcular_kpis_basicos(df, 'Cantidad')
    
    logger.info(f"Total ventas: {len(df)}")
    logger.info(f"Ventas totales USD: ${kpis_total['total']:,.2f}")
    logger.info(f"Ticket promedio: ${kpis_total['promedio']:,.2f}")
    logger.info(f"Cantidad promedio: {kpis_cantidad['promedio']:.1f}")
    
    # 2. Ventas por Estado
    logger.info("\n--- POR ESTADO ---")
    estado_counts = df['Estado'].value_counts()
    logger.info(f"\n{estado_counts}")
    
    # 3. Ventas por Canal
    logger.info("\n--- POR CANAL ---")
    canal = resumen_categorias(df, 'Canal de Venta', 'Total USD')
    logger.info(f"\n{canal}")
    
    # 4. Ventas por Método de Pago
    logger.info("\n--- POR MÉTODO DE PAGO ---")
    pago = resumen_categorias(df, 'Método de Pago', 'Total USD')
    logger.info(f"\n{pago}")
    
    # 5. Top 10 Clientes
    logger.info("\n--- TOP 10 CLIENTES ---")
    top_clientes = df.groupby('Cliente')['Total USD'].sum().sort_values(ascending=False).head(10)
    logger.info(f"\n{top_clientes}")
    
    # 6. Ventas por mes
    logger.info("\n--- VENTAS POR MES ---")
    df['Año-Mes'] = df['Fecha'].dt.to_period('M')
    ventas_mes = df.groupby('Año-Mes')['Total USD'].sum().sort_index()
    logger.info(f"\n{ventas_mes}")
    
    # 7. Productos más vendidos
    logger.info("\n--- TOP 10 SKU MÁS VENDIDOS ---")
    top_skus = df.groupby('SKU')['Cantidad'].sum().sort_values(ascending=False).head(10)
    logger.info(f"\n{top_skus}")
    
    logger.info("\n✓ Análisis de ventas completado")
    
    return {
        'kpis_total': kpis_total,
        'kpis_cantidad': kpis_cantidad,
        'estado_counts': estado_counts,
        'por_canal': canal,
        'por_pago': pago,
        'top_clientes': top_clientes,
        'ventas_mes': ventas_mes,
        'top_skus': top_skus
    }