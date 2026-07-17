# src/03_visualizacion/graficas_ventas.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_VENTAS
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_ventas_estado(df_ventas):
    """Gráfico de torta de ventas por estado."""
    logger.info("Generando gráfico ventas por estado...")
    
    df = df_ventas.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    estado = df['Estado'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(estado))
    
    wedges, texts, autotexts = ax.pie(estado, labels=estado.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(estado))
    ax.set_title('Distribución de Ventas por Estado', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'ventas_por_estado.png', FIGURES_VENTAS)

def grafico_ventas_canal(df_ventas):
    """Ventas por canal de venta."""
    logger.info("Generando ventas por canal...")
    
    df = df_ventas.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Total USD'] = pd.to_numeric(df['Total USD'], errors='coerce')
    
    canal = df.groupby('Canal de Venta')['Total USD'].sum().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.barh(canal.index, canal.values, color=sns.color_palette("husl", len(canal)))
    ax.set_title('Ventas Totales por Canal', fontsize=14, fontweight='bold')
    ax.set_xlabel('USD')
    
    for bar in barras:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width:,.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'ventas_por_canal.png', FIGURES_VENTAS)

def grafico_top_clientes(df_ventas):
    """Top 10 clientes por ventas."""
    logger.info("Generando top clientes...")
    
    df = df_ventas.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Total USD'] = pd.to_numeric(df['Total USD'], errors='coerce')
    
    top = df.groupby('Cliente')['Total USD'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colores = sns.color_palette("husl", len(top))
    barras = ax.bar(range(len(top)), top.values, color=colores)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels(top.index, rotation=45, ha='right')
    ax.set_title('Top 10 Clientes por Ventas', fontsize=14, fontweight='bold')
    ax.set_ylabel('USD')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=9, rotation=45)
    
    plt.tight_layout()
    guardar_figura(fig, 'top_clientes_ventas.png', FIGURES_VENTAS)

def grafico_ventas_metodo_pago(df_ventas):
    """Ventas por método de pago."""
    logger.info("Generando ventas por método de pago...")
    
    df = df_ventas.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Total USD'] = pd.to_numeric(df['Total USD'], errors='coerce')
    
    pago = df.groupby('Método de Pago')['Total USD'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    barras = ax.bar(pago.index, pago.values, color=sns.color_palette("husl", len(pago)))
    ax.set_title('Ventas por Método de Pago', fontsize=14, fontweight='bold')
    ax.set_ylabel('USD')
    ax.set_xticklabels(pago.index, rotation=45, ha='right')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'ventas_por_metodo_pago.png', FIGURES_VENTAS)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de ventas listo")