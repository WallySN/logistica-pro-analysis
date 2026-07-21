# src/04_reportes/dashboard.py
import sys
from pathlib import Path
import importlib.util

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from utils.loggers import logger
from utils.config import FIGURES_GENERALES

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def generar_dashboard_ejecutivo(df_ventas, df_compras, df_inventario, df_productos, df_proveedores):
    """
    Genera un dashboard ejecutivo consolidado con KPIs clave.
    """
    logger.info("Generando dashboard ejecutivo...")
    
    # Preparar datos
    for df in [df_ventas, df_compras, df_inventario, df_productos]:
        if df.iloc[0].astype(str).equals(df.columns.astype(str)):
            df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir numéricas
    df_ventas['Total USD'] = pd.to_numeric(df_ventas['Total USD'], errors='coerce')
    df_compras['Total USD'] = pd.to_numeric(df_compras['Total USD'], errors='coerce')
    df_inventario['Valor Inventario USD'] = pd.to_numeric(df_inventario['Valor Inventario USD'], errors='coerce')
    df_productos['Precio USD'] = pd.to_numeric(df_productos['Precio USD'], errors='coerce')
    df_productos['Margen %'] = pd.to_numeric(df_productos['Margen %'], errors='coerce')
    
    # Crear figura grande
    fig = plt.figure(figsize=(20, 14))
    gs = fig.add_gridspec(3, 4, hspace=0.35, wspace=0.35)
    
    fig.suptitle('DASHBOARD EJECUTIVO - LOGÍSTICA PRO', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. Total Ventas (tarjeta)
    ax1 = fig.add_subplot(gs[0, 0])
    total_ventas = df_ventas['Total USD'].sum()
    ax1.text(0.5, 0.6, f'${total_ventas:,.0f}', fontsize=24, ha='center', va='center', fontweight='bold', color='#2ecc71')
    ax1.text(0.5, 0.2, 'Ventas Totales', fontsize=12, ha='center', va='center')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#2ecc71', linewidth=3, boxstyle='round,pad=0.02'))
    
    # 2. Total Compras (tarjeta)
    ax2 = fig.add_subplot(gs[0, 1])
    total_compras = df_compras['Total USD'].sum()
    ax2.text(0.5, 0.6, f'${total_compras:,.0f}', fontsize=24, ha='center', va='center', fontweight='bold', color='#e74c3c')
    ax2.text(0.5, 0.2, 'Compras Totales', fontsize=12, ha='center', va='center')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#e74c3c', linewidth=3, boxstyle='round,pad=0.02'))
    
    # 3. Valor Inventario (tarjeta)
    ax3 = fig.add_subplot(gs[0, 2])
    total_inv = df_inventario['Valor Inventario USD'].sum()
    ax3.text(0.5, 0.6, f'${total_inv:,.0f}', fontsize=24, ha='center', va='center', fontweight='bold', color='#3498db')
    ax3.text(0.5, 0.2, 'Valor Inventario', fontsize=12, ha='center', va='center')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#3498db', linewidth=3, boxstyle='round,pad=0.02'))
    
    # 4. Margen Promedio (tarjeta)
    ax4 = fig.add_subplot(gs[0, 3])
    margen = df_productos['Margen %'].mean()
    ax4.text(0.5, 0.6, f'{margen:.1f}%', fontsize=24, ha='center', va='center', fontweight='bold', color='#9b59b6')
    ax4.text(0.5, 0.2, 'Margen Promedio', fontsize=12, ha='center', va='center')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#9b59b6', linewidth=3, boxstyle='round,pad=0.02'))
    
    # 5. Ventas por mes (línea)
    ax5 = fig.add_subplot(gs[1, :2])
    df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'], errors='coerce')
    df_ventas['Año-Mes'] = df_ventas['Fecha'].dt.to_period('M')
    ventas_mes = df_ventas.groupby('Año-Mes')['Total USD'].sum()
    ventas_mes.plot(ax=ax5, marker='o', linewidth=2, color='#2ecc71')
    ax5.set_title('Ventas por Mes', fontweight='bold')
    ax5.set_ylabel('USD')
    ax5.grid(True, alpha=0.3)
    
    # 6. Top 10 productos (barras)
    ax6 = fig.add_subplot(gs[1, 2:])
    top_prod = df_ventas.groupby('SKU')['Cantidad'].sum().sort_values(ascending=False).head(10)
    ax6.barh(range(len(top_prod)), top_prod.values, color=sns.color_palette("husl", len(top_prod)))
    ax6.set_yticks(range(len(top_prod)))
    ax6.set_yticklabels(top_prod.index)
    ax6.set_title('Top 10 SKU Más Vendidos', fontweight='bold')
    ax6.set_xlabel('Cantidad')
    
    # 7. Productos por categoría (pastel)
    ax7 = fig.add_subplot(gs[2, :2])
    cat_counts = df_productos['Categoría'].value_counts()
    ax7.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)
    ax7.set_title('Productos por Categoría', fontweight='bold')
    
    # 8. Proveedores por país (barras)
    ax8 = fig.add_subplot(gs[2, 2:])
    pais_counts = df_proveedores['País'].value_counts().head(8)
    ax8.bar(pais_counts.index, pais_counts.values, color=sns.color_palette("husl", len(pais_counts)))
    ax8.set_title('Proveedores por País (Top 8)', fontweight='bold')
    ax8.tick_params(axis='x', rotation=45)
    
    # Guardar
    from utils.helpers import guardar_figura
    guardar_figura(fig, 'dashboard_ejecutivo.png', FIGURES_GENERALES)
    logger.info("✓ Dashboard ejecutivo guardado")


if __name__ == "__main__":
    logger.info("Módulo dashboard listo")