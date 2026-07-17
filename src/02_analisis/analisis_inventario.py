# src/02_analisis/analisis_inventario.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos

def analizar_inventario(df_inventario):
    """
    Análisis completo de la tabla Inventario.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE INVENTARIO")
    logger.info("=" * 50)
    
    df = df_inventario.copy()
    
    # Limpiar encabezado duplicado
    if df.iloc[0]['ID Línea'] == 'ID Línea':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    cols_num = ['Stock Físico', 'Reservado', 'Disponible', 'Stock Mínimo',
                'Stock Máximo', 'Punto Reorden', 'Costo Unitario USD', 
                'Valor Inventario USD', 'Rotación Anual']
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 1. KPIs
    logger.info("\n--- KPIs GENERALES ---")
    kpis_stock = calcular_kpis_basicos(df, 'Stock Físico')
    kpis_valor = calcular_kpis_basicos(df, 'Valor Inventario USD')
    
    logger.info(f"Total líneas de inventario: {len(df)}")
    logger.info(f"Stock físico total: {kpis_stock['total']:,.0f} unidades")
    logger.info(f"Valor total inventario: ${kpis_valor['total']:,.2f}")
    logger.info(f"Valor promedio por línea: ${kpis_valor['promedio']:,.2f}")
    
    # 2. Por Estado
    logger.info("\n--- POR ESTADO ---")
    estado = df['Estado'].value_counts()
    logger.info(f"\n{estado}")
    
    # 3. Por Almacén
    logger.info("\n--- POR ALMACÉN ---")
    almacen = df.groupby('Almacén')['Valor Inventario USD'].sum().sort_values(ascending=False)
    logger.info(f"\n{almacen}")
    
    # 4. Productos con stock bajo (Disponible < Stock Mínimo)
    logger.info("\n--- STOCK BAJO (Disponible < Mínimo) ---")
    stock_bajo = df[df['Disponible'] < df['Stock Mínimo']][['SKU', 'Almacén', 'Disponible', 'Stock Mínimo', 'Estado']]
    logger.info(f"Total: {len(stock_bajo)} líneas")
    logger.info(f"\n{stock_bajo.head(10)}")
    
    # 5. Productos con sobre-stock (Disponible > Stock Máximo)
    logger.info("\n--- SOBRE-STOCK (Disponible > Máximo) ---")
    sobre_stock = df[df['Disponible'] > df['Stock Máximo']][['SKU', 'Almacén', 'Disponible', 'Stock Máximo']]
    logger.info(f"Total: {len(sobre_stock)} líneas")
    logger.info(f"\n{sobre_stock.head(10)}")
    
    # 6. Rotación anual
    logger.info("\n--- ROTACIÓN ANUAL ---")
    rotacion = df['Rotación Anual'].describe()
    logger.info(f"\n{rotacion}")
    
    # 7. Top 10 valor de inventario
    logger.info("\n--- TOP 10 VALOR DE INVENTARIO ---")
    top_valor = df.nlargest(10, 'Valor Inventario USD')[['SKU', 'Almacén', 'Stock Físico', 'Costo Unitario USD', 'Valor Inventario USD']]
    logger.info(f"\n{top_valor}")
    
    logger.info("\n✓ Análisis de inventario completado")
    
    return {
        'total_lineas': len(df),
        'stock_total': kpis_stock['total'],
        'valor_total': kpis_valor['total'],
        'estado': estado,
        'por_almacen': almacen,
        'stock_bajo': stock_bajo,
        'sobre_stock': sobre_stock,
        'rotacion': rotacion,
        'top_valor': top_valor
    }