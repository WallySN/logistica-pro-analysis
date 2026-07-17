# src/02_analisis/analisis_financiero_inventario.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger

def analizar_financiero_inventario(df_inventario, df_productos):
    """
    Análisis financiero cruzando inventario con productos.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS FINANCIERO DE INVENTARIO")
    logger.info("=" * 50)
    
    # Limpiar datos
    inv = df_inventario.copy()
    prod = df_productos.copy()
    
    if inv.iloc[0]['ID Línea'] == 'ID Línea':
        inv = inv.iloc[1:].reset_index(drop=True)
    if prod.iloc[0]['SKU'] == 'SKU':
        prod = prod.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    inv['Valor Inventario USD'] = pd.to_numeric(inv['Valor Inventario USD'], errors='coerce')
    inv['Stock Físico'] = pd.to_numeric(inv['Stock Físico'], errors='coerce')
    inv['Disponible'] = pd.to_numeric(inv['Disponible'], errors='coerce')
    prod['Costo USD'] = pd.to_numeric(prod['Costo USD'], errors='coerce')
    prod['Precio USD'] = pd.to_numeric(prod['Precio USD'], errors='coerce')
    prod['Margen %'] = pd.to_numeric(prod['Margen %'], errors='coerce')
    
    # Merge inventario con productos
    df = inv.merge(prod[['SKU', 'Categoría', 'Gama', 'Marca', 'Costo USD', 'Precio USD', 'Margen %']], 
                   on='SKU', how='left')
    
    # 1. Valor total por categoría
    logger.info("\n--- VALOR POR CATEGORÍA ---")
    valor_cat = df.groupby('Categoría')['Valor Inventario USD'].sum().sort_values(ascending=False)
    logger.info(f"\n{valor_cat}")
    
    # 2. Valor por gama
    logger.info("\n--- VALOR POR GAMA ---")
    valor_gama = df.groupby('Gama')['Valor Inventario USD'].sum().sort_values(ascending=False)
    logger.info(f"\n{valor_gama}")
    
    # 3. ROI potencial (si todo se vendiera)
    logger.info("\n--- ROI POTENCIAL ---")
    df['Valor Venta Potencial'] = df['Disponible'] * df['Precio USD']
    df['Ganancia Potencial'] = df['Valor Venta Potencial'] - (df['Disponible'] * df['Costo USD'])
    
    roi_total = df['Ganancia Potencial'].sum()
    venta_potencial = df['Valor Venta Potencial'].sum()
    logger.info(f"Valor venta potencial: ${venta_potencial:,.2f}")
    logger.info(f"Ganancia potencial: ${roi_total:,.2f}")
    logger.info(f"Margen potencial: {(roi_total/venta_potencial)*100:.1f}%")
    
    # 4. Productos con mayor valor congelado
    logger.info("\n--- TOP 10 VALOR CONGELADO ---")
    top_congelado = df.nlargest(10, 'Valor Inventario USD')[['SKU', 'Categoría', 'Gama', 'Stock Físico', 'Valor Inventario USD']]
    logger.info(f"\n{top_congelado}")
    
    # 5. Eficiencia de inventario (rotación vs valor)
    logger.info("\n--- EFICIENCIA ---")
    df['Rotación Anual'] = pd.to_numeric(df['Rotación Anual'], errors='coerce')
    eficiencia = df.groupby('Categoría').agg({
        'Valor Inventario USD': 'sum',
        'Rotación Anual': 'mean'
    }).sort_values('Valor Inventario USD', ascending=False)
    logger.info(f"\n{eficiencia}")
    
    logger.info("\n✓ Análisis financiero de inventario completado")
    
    return {
        'valor_por_categoria': valor_cat,
        'valor_por_gama': valor_gama,
        'roi_total': roi_total,
        'venta_potencial': venta_potencial,
        'top_congelado': top_congelado,
        'eficiencia': eficiencia
    }