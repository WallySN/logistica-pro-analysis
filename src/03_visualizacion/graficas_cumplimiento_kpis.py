# src/03_visualizacion/graficas_cumplimiento_kpis.py
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

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_kpis_generales(resultados_productos, resultados_ventas, resultados_compras, 
                           resultados_inventario, resultados_proveedores, resultados_incidentes):
    """Dashboard de KPIs generales del proyecto."""
    logger.info("Generando dashboard de KPIs generales...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    fig.suptitle('Dashboard de KPIs - Logística Pro', fontsize=18, fontweight='bold', y=0.98)
    
    # 1. Total Productos
    ax1 = fig.add_subplot(gs[0, 0])
    total_prod = resultados_productos.get('kpis_precio', {}).get('total', 0)
    ax1.text(0.5, 0.5, f'{total_prod:,.0f}', fontsize=28, ha='center', va='center', 
             fontweight='bold', color='#2ecc71')
    ax1.text(0.5, 0.2, 'Productos', fontsize=14, ha='center', va='center')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#2ecc71', linewidth=3))
    
    # 2. Total Ventas
    ax2 = fig.add_subplot(gs[0, 1])
    total_ventas = resultados_ventas.get('kpis_total', {}).get('total', 0)
    ax2.text(0.5, 0.5, f'${total_ventas:,.0f}', fontsize=22, ha='center', va='center',
             fontweight='bold', color='#3498db')
    ax2.text(0.5, 0.2, 'Ventas Totales', fontsize=14, ha='center', va='center')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#3498db', linewidth=3))
    
    # 3. Total Compras
    ax3 = fig.add_subplot(gs[0, 2])
    total_compras = resultados_compras.get('kpis_total', {}).get('total', 0)
    ax3.text(0.5, 0.5, f'${total_compras:,.0f}', fontsize=22, ha='center', va='center',
             fontweight='bold', color='#e74c3c')
    ax3.text(0.5, 0.2, 'Compras Totales', fontsize=14, ha='center', va='center')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#e74c3c', linewidth=3))
    
    # 4. Margen Promedio
    ax4 = fig.add_subplot(gs[1, 0])
    margen = resultados_productos.get('kpis_margen', {}).get('promedio', 0)
    ax4.text(0.5, 0.5, f'{margen:.1f}%', fontsize=28, ha='center', va='center',
             fontweight='bold', color='#9b59b6')
    ax4.text(0.5, 0.2, 'Margen Promedio', fontsize=14, ha='center', va='center')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#9b59b6', linewidth=3))
    
    # 5. Valor Inventario
    ax5 = fig.add_subplot(gs[1, 1])
    valor_inv = resultados_inventario.get('valor_total', 0)
    ax5.text(0.5, 0.5, f'${valor_inv:,.0f}', fontsize=22, ha='center', va='center',
             fontweight='bold', color='#f39c12')
    ax5.text(0.5, 0.2, 'Valor Inventario', fontsize=14, ha='center', va='center')
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    ax5.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#f39c12', linewidth=3))
    
    # 6. Calificación Proveedores
    ax6 = fig.add_subplot(gs[1, 2])
    calif = resultados_proveedores.get('calificacion_promedio', 0)
    ax6.text(0.5, 0.5, f'{calif:.2f}', fontsize=28, ha='center', va='center',
             fontweight='bold', color='#1abc9c')
    ax6.text(0.5, 0.2, 'Calif. Proveedores', fontsize=14, ha='center', va='center')
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    ax6.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#1abc9c', linewidth=3))
    
    # 7. Costo Incidentes
    ax7 = fig.add_subplot(gs[2, 0])
    costo_inc = resultados_incidentes.get('costo_total', 0)
    ax7.text(0.5, 0.5, f'${costo_inc:,.0f}', fontsize=22, ha='center', va='center',
             fontweight='bold', color='#e74c3c')
    ax7.text(0.5, 0.2, 'Costo Incidentes', fontsize=14, ha='center', va='center')
    ax7.set_xlim(0, 1)
    ax7.set_ylim(0, 1)
    ax7.axis('off')
    ax7.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#e74c3c', linewidth=3))
    
    # 8. Ticket Promedio
    ax8 = fig.add_subplot(gs[2, 1])
    ticket = resultados_ventas.get('kpis_total', {}).get('promedio', 0)
    ax8.text(0.5, 0.5, f'${ticket:,.2f}', fontsize=22, ha='center', va='center',
             fontweight='bold', color='#3498db')
    ax8.text(0.5, 0.2, 'Ticket Promedio', fontsize=14, ha='center', va='center')
    ax8.set_xlim(0, 1)
    ax8.set_ylim(0, 1)
    ax8.axis('off')
    ax8.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#3498db', linewidth=3))
    
    # 9. Total Proveedores
    ax9 = fig.add_subplot(gs[2, 2])
    total_prov = resultados_proveedores.get('total', 0)
    ax9.text(0.5, 0.5, f'{total_prov}', fontsize=28, ha='center', va='center',
             fontweight='bold', color='#2ecc71')
    ax9.text(0.5, 0.2, 'Proveedores', fontsize=14, ha='center', va='center')
    ax9.set_xlim(0, 1)
    ax9.set_ylim(0, 1)
    ax9.axis('off')
    ax9.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='#2ecc71', linewidth=3))
    
    guardar_figura(fig, 'kpis_generales_dashboard.png', FIGURES_GENERALES)
    logger.info("✓ Dashboard de KPIs guardado")

def grafico_cumplimiento_vs_meta(df_ventas, meta_ventas=500000, df_compras=None, meta_compras=300000):
    """Gauge chart de cumplimiento vs metas."""
    logger.info("Generando cumplimiento vs metas...")
    
    ventas = df_ventas.copy()
    if ventas.iloc[0]['ID'] == 'ID':
        ventas = ventas.iloc[1:].reset_index(drop=True)
    ventas['Total USD'] = pd.to_numeric(ventas['Total USD'], errors='coerce')
    total_ventas = ventas['Total USD'].sum()
    
    cumplimiento_ventas = min((total_ventas / meta_ventas) * 100, 150)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gauge Ventas
    ax1 = axes[0]
    theta = np.linspace(0, np.pi, 100)
    r = 1.0
    
    # Arco de fondo
    ax1.fill_between(np.cos(theta), np.sin(theta), 0, alpha=0.1, color='gray')
    
    # Arco de progreso
    progress_theta = theta[:int(cumplimiento_ventas)]
    ax1.fill_between(np.cos(progress_theta), np.sin(progress_theta), 0, 
                     alpha=0.6, color='#2ecc71' if cumplimiento_ventas >= 100 else '#f39c12')
    
    ax1.text(0, 0.3, f'{cumplimiento_ventas:.1f}%', fontsize=36, ha='center', va='center', fontweight='bold')
    ax1.text(0, -0.1, f'${total_ventas:,.0f} / ${meta_ventas:,.0f}', fontsize=12, ha='center', va='center')
    ax1.text(0, -0.3, 'Meta Ventas', fontsize=14, ha='center', va='center')
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-0.5, 1.2)
    ax1.axis('off')
    
    # Gauge Compras
    if df_compras is not None:
        compras = df_compras.copy()
        if compras.iloc[0]['ID'] == 'ID':
            compras = compras.iloc[1:].reset_index(drop=True)
        compras['Total USD'] = pd.to_numeric(compras['Total USD'], errors='coerce')
        total_compras = compras['Total USD'].sum()
        cumplimiento_compras = min((total_compras / meta_compras) * 100, 150)
        
        ax2 = axes[1]
        ax2.fill_between(np.cos(theta), np.sin(theta), 0, alpha=0.1, color='gray')
        progress_theta2 = theta[:int(cumplimiento_compras)]
        ax2.fill_between(np.cos(progress_theta2), np.sin(progress_theta2), 0,
                         alpha=0.6, color='#2ecc71' if cumplimiento_compras >= 100 else '#f39c12')
        
        ax2.text(0, 0.3, f'{cumplimiento_compras:.1f}%', fontsize=36, ha='center', va='center', fontweight='bold')
        ax2.text(0, -0.1, f'${total_compras:,.0f} / ${meta_compras:,.0f}', fontsize=12, ha='center', va='center')
        ax2.text(0, -0.3, 'Meta Compras', fontsize=14, ha='center', va='center')
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-0.5, 1.2)
        ax2.axis('off')
    
    guardar_figura(fig, 'cumplimiento_vs_metas.png', FIGURES_GENERALES)
    logger.info("✓ Cumplimiento vs metas guardado")

if __name__ == "__main__":
    logger.info("Módulo de gráficas de cumplimiento KPIs listo")