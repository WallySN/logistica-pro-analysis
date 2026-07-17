# src/03_visualizacion/graficas_compras.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_COMPRAS
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_compras_estado(df_compras):
    """Gráfico de compras por estado."""
    logger.info("Generando gráfico compras por estado...")
    
    df = df_compras.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    estado = df['Estado'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(estado))
    
    wedges, texts, autotexts = ax.pie(estado, labels=estado.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(estado))
    ax.set_title('Distribución de Compras por Estado', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'compras_por_estado.png', FIGURES_COMPRAS)

def grafico_compras_proveedor(df_compras):
    """Top 10 proveedores por compras."""
    logger.info("Generando top proveedores por compras...")
    
    df = df_compras.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Total USD'] = pd.to_numeric(df['Total USD'], errors='coerce')
    
    prov = df.groupby('Proveedor')['Total USD'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colores = sns.color_palette("husl", len(prov))
    barras = ax.bar(range(len(prov)), prov.values, color=colores)
    ax.set_xticks(range(len(prov)))
    ax.set_xticklabels(prov.index, rotation=45, ha='right')
    ax.set_title('Top 10 Proveedores por Compras', fontsize=14, fontweight='bold')
    ax.set_ylabel('USD')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=9, rotation=45)
    
    plt.tight_layout()
    guardar_figura(fig, 'top_proveedores_compras.png', FIGURES_COMPRAS)

def grafico_cumplimiento_entrega(df_compras):
    """Cumplimiento de entrega (cantidad recibida vs solicitada)."""
    logger.info("Generando gráfico cumplimiento...")
    
    df = df_compras.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Cantidad Solicitada'] = pd.to_numeric(df['Cantidad Solicitada'], errors='coerce')
    df['Cantidad Recibida'] = pd.to_numeric(df['Cantidad Recibida'], errors='coerce')
    df['Cumplimiento %'] = (df['Cantidad Recibida'] / df['Cantidad Solicitada'] * 100).round(2)
    
    # Categorizar cumplimiento
    condiciones = [
        (df['Cumplimiento %'] >= 100),
        (df['Cumplimiento %'] >= 90) & (df['Cumplimiento %'] < 100),
        (df['Cumplimiento %'] < 90)
    ]
    categorias = ['100% o más', '90% - 99%', 'Menos de 90%']
    df['Categoria'] = np.select(condiciones, categorias, default='N/A')
    
    cumplimiento = df['Categoria'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colores = ['#2ecc71', '#f39c12', '#e74c3c']
    barras = ax.bar(cumplimiento.index, cumplimiento.values, color=colores[:len(cumplimiento)])
    ax.set_title('Cumplimiento de Entrega por Cantidad', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cantidad de Órdenes')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    guardar_figura(fig, 'cumplimiento_entrega.png', FIGURES_COMPRAS)

def grafico_tiempos_entrega(df_compras):
    """Días de retraso en entregas."""
    logger.info("Generando tiempos de entrega...")
    
    df = df_compras.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Fecha Entrega Esperada'] = pd.to_datetime(df['Fecha Entrega Esperada'], errors='coerce')
    df['Fecha Entrega Real'] = pd.to_datetime(df['Fecha Entrega Real'], errors='coerce')
    df['Dias Retraso'] = (df['Fecha Entrega Real'] - df['Fecha Entrega Esperada']).dt.days
    
    # Filtrar valores válidos
    retrasos = df['Dias Retraso'].dropna()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(retrasos, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
    ax.axvline(retrasos.mean(), color='red', linestyle='--', linewidth=2, label=f'Promedio: {retrasos.mean():.1f} días')
    ax.set_title('Distribución de Días de Retraso en Entregas', fontsize=14, fontweight='bold')
    ax.set_xlabel('Días de Retraso (negativo = adelanto)')
    ax.set_ylabel('Frecuencia')
    ax.legend()
    
    plt.tight_layout()
    guardar_figura(fig, 'tiempos_entrega.png', FIGURES_COMPRAS)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de compras listo")