# src/02_analisis/analisis_productos.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.loggers import logger
from utils.helpers import calcular_kpis_basicos, resumen_categorias

def analizar_productos(df_productos):
    """
    Análisis completo de la tabla Productos.
    """
    logger.info("=" * 50)
    logger.info("ANÁLISIS DE PRODUCTOS")
    logger.info("=" * 50)
    
    # Limpiar datos
    df = df_productos.copy()
    
    # Eliminar fila de encabezado duplicado si existe
    if df.iloc[0]['SKU'] == 'SKU':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir columnas numéricas
    cols_numericas = ['Costo USD', 'Precio USD', 'Margen %', 
                      'Peso kg', 'Volumen m3', 'Stock Min', 
                      'Stock Máx', 'Punto Reorden', 'Garantía Meses']
    
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 1. KPIs Generales
    logger.info("\n--- KPIs GENERALES ---")
    kpis_precio = calcular_kpis_basicos(df, 'Precio USD')
    kpis_costo = calcular_kpis_basicos(df, 'Costo USD')
    kpis_margen = calcular_kpis_basicos(df, 'Margen %')
    
    logger.info(f"Total productos: {len(df)}")
    logger.info(f"Precio promedio: ${kpis_precio['promedio']:,.2f}")
    logger.info(f"Costo promedio: ${kpis_costo['promedio']:,.2f}")
    logger.info(f"Margen promedio: {kpis_margen['promedio']:.1f}%")
    
    # 2. Análisis por Categoría
    logger.info("\n--- POR CATEGORÍA ---")
    resumen_cat = resumen_categorias(df, 'Categoría', 'Precio USD')
    logger.info(f"\n{resumen_cat}")
    
    # 3. Análisis por Gama
    logger.info("\n--- POR GAMA ---")
    resumen_gama = resumen_categorias(df, 'Gama', 'Precio USD')
    logger.info(f"\n{resumen_gama}")
    
    # 4. Análisis por Marca
    logger.info("\n--- TOP 10 MARCAS ---")
    resumen_marca = resumen_categorias(df, 'Marca', 'Precio USD').head(10)
    logger.info(f"\n{resumen_marca}")
    
    # 5. Productos con mayor margen
    logger.info("\n--- TOP 10 MARGENES ---")
    top_margen = df.nlargest(10, 'Margen %')[['SKU', 'Nombre', 'Marca', 'Gama', 'Margen %', 'Precio USD']]
    logger.info(f"\n{top_margen}")
    
    # 6. Productos por condición
    logger.info("\n--- POR CONDICIÓN ---")
    condicion_counts = df['Condición'].value_counts()
    logger.info(f"\n{condicion_counts}")
    
    # 7. Productos por estado
    logger.info("\n--- POR ESTADO ---")
    estado_counts = df['Estado'].value_counts()
    logger.info(f"\n{estado_counts}")
    
    logger.info("\n✓ Análisis de productos completado")
    
    return {
        'kpis_precio': kpis_precio,
        'kpis_costo': kpis_costo,
        'kpis_margen': kpis_margen,
        'resumen_categoria': resumen_cat,
        'resumen_gama': resumen_gama,
        'resumen_marca': resumen_marca,
        'top_margen': top_margen,
        'condicion_counts': condicion_counts,
        'estado_counts': estado_counts
    }

# BLOQUE DE PRUEBA ELIMINADO - se ejecuta desde main.py