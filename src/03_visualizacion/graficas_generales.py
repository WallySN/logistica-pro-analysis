# src/03_visualizacion/graficas_generales.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_GENERALES
from utils.helpers import guardar_figura
from utils.loggers import logger

# Configuración de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_resumen_empresa(df_ventas, df_compras, df_inventario, df_productos):
    """
    Dashboard general de la empresa: ventas vs compras vs inventario.
    """
    logger.info("Generando gráfico resumen de empresa...")
    
    # Preparar datos
    ventas = df_ventas.copy()
    compras = df_compras.copy()
    inventario = df_inventario.copy()
    productos = df_productos.copy()
    
    # Limpiar encabezados
    for df in [ventas, compras, inventario, productos]:
        if df.iloc[0].astype(str).equals(df.columns.astype(str)):
            df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    ventas['Total USD'] = pd.to_numeric(ventas['Total USD'], errors='coerce')
    compras['Total USD'] = pd.to_numeric(compras['Total USD'], errors='coerce')
    inventario['Valor Inventario USD'] = pd.to_numeric(inventario['Valor Inventario USD'], errors='coerce')
    
    # Crear figura
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Dashboard General - Logística Pro', fontsize=16, fontweight='bold')
    
    # 1. Ventas vs Compras (totales)
    ax1 = axes[0, 0]
    total_ventas = ventas['Total USD'].sum()
    total_compras = compras['Total USD'].sum()
    total_inventario = inventario['Valor Inventario USD'].sum()
    
    barras = ax1.bar(['Ventas', 'Compras', 'Inventario'], 
                     [total_ventas, total_compras, total_inventario],
                     color=['#2ecc71', '#e74c3c', '#3498db'])
    ax1.set_title('Totales USD', fontweight='bold')
    ax1.set_ylabel('USD')
    
    # Formatear valores en las barras
    for bar in barras:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    # 2. Distribución de productos por categoría
    ax2 = axes[0, 1]
    cat_counts = productos['Categoría'].value_counts()
    colores = sns.color_palette("husl", len(cat_counts))
    wedges, texts, autotexts = ax2.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%',
                                        colors=colores, startangle=90)
    ax2.set_title('Productos por Categoría', fontweight='bold')
    
    # 3. Estado de órdenes
    ax3 = axes[1, 0]
    estado_ventas = ventas['Estado'].value_counts()
    estado_compras = compras['Estado'].value_counts()
    
    x = np.arange(len(estado_ventas))
    width = 0.35
    
    ax3.bar(x - width/2, estado_ventas.values, width, label='Ventas', color='#2ecc71')
    ax3.bar(x + width/2, [estado_compras.get(e, 0) for e in estado_ventas.index], 
            width, label='Compras', color='#e74c3c')
    ax3.set_title('Estado de Órdenes', fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(estado_ventas.index, rotation=45)
    ax3.legend()
    
    # 4. KPIs numéricos
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    kpis = [
        f"Total Productos: {len(productos)}",
        f"Total Ventas: {len(ventas)}",
        f"Total Compras: {len(compras)}",
        f"Total Clientes: {ventas['Cliente'].nunique()}",
        f"Ticket Promedio: ${ventas['Total USD'].mean():,.2f}",
        f"Margen Promedio: {pd.to_numeric(productos['Margen %'], errors='coerce').mean():.1f}%"
    ]
    
    for i, kpi in enumerate(kpis):
        ax4.text(0.1, 0.9 - i*0.15, kpi, fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.tight_layout()
    guardar_figura(fig, 'dashboard_general.png', FIGURES_GENERALES)
    logger.info("✓ Dashboard general guardado")

def grafico_tendencias_mensuales(df_ventas, df_compras):
    """
    Tendencias mensuales de ventas y compras.
    """
    logger.info("Generando tendencias mensuales...")
    
    ventas = df_ventas.copy()
    compras = df_compras.copy()
    
    for df in [ventas, compras]:
        if df.iloc[0].astype(str).equals(df.columns.astype(str)):
            df = df.iloc[1:].reset_index(drop=True)
    
    ventas['Fecha'] = pd.to_datetime(ventas['Fecha'], errors='coerce')
    ventas['Total USD'] = pd.to_numeric(ventas['Total USD'], errors='coerce')
    compras['Fecha'] = pd.to_datetime(compras['Fecha'], errors='coerce')
    compras['Total USD'] = pd.to_numeric(compras['Total USD'], errors='coerce')
    
    ventas['Año-Mes'] = ventas['Fecha'].dt.to_period('M')
    compras['Año-Mes'] = compras['Fecha'].dt.to_period('M')
    
    v_mensual = ventas.groupby('Año-Mes')['Total USD'].sum()
    c_mensual = compras.groupby('Año-Mes')['Total USD'].sum()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    v_mensual.plot(ax=ax, marker='o', linewidth=2, label='Ventas', color='#2ecc71')
    c_mensual.plot(ax=ax, marker='s', linewidth=2, label='Compras', color='#e74c3c')
    
    ax.set_title('Tendencias Mensuales: Ventas vs Compras', fontsize=14, fontweight='bold')
    ax.set_xlabel('Mes')
    ax.set_ylabel('USD')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    guardar_figura(fig, 'tendencias_mensuales.png', FIGURES_GENERALES)
    logger.info("✓ Tendencias mensuales guardadas")

if __name__ == "__main__":
    logger.info("Módulo de gráficas generales listo")