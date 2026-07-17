# src/03_visualizacion/graficas_productos.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_PRODUCTOS
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_productos_categoria(df_productos):
    """Gráfico de barras de productos por categoría."""
    logger.info("Generando gráfico productos por categoría...")
    
    df = df_productos.copy()
    if df.iloc[0]['SKU'] == 'SKU':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Precio USD'] = pd.to_numeric(df['Precio USD'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    cat_data = df.groupby('Categoría')['Precio USD'].agg(['count', 'mean']).sort_values('count', ascending=True)
    
    barras = ax.barh(cat_data.index, cat_data['count'], color=sns.color_palette("husl", len(cat_data)))
    ax.set_title('Cantidad de Productos por Categoría', fontsize=14, fontweight='bold')
    ax.set_xlabel('Cantidad de Productos')
    
    # Añadir valores
    for i, bar in enumerate(barras):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'productos_por_categoria.png', FIGURES_PRODUCTOS)

def grafico_margen_gama(df_productos):
    """Boxplot de margen por gama."""
    logger.info("Generando boxplot margen por gama...")
    
    df = df_productos.copy()
    if df.iloc[0]['SKU'] == 'SKU':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Margen %'] = pd.to_numeric(df['Margen %'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    orden_gama = ['Baja', 'Media', 'Alta', 'Premium']
    df['Gama'] = pd.Categorical(df['Gama'], categories=orden_gama, ordered=True)
    
    sns.boxplot(data=df, x='Gama', y='Margen %', ax=ax, palette='husl')
    ax.set_title('Distribución de Margen % por Gama', fontsize=14, fontweight='bold')
    ax.set_ylabel('Margen %')
    
    plt.tight_layout()
    guardar_figura(fig, 'margen_por_gama.png', FIGURES_PRODUCTOS)

def grafico_top_marcas(df_productos):
    """Top 10 marcas por valor total."""
    logger.info("Generando top marcas...")
    
    df = df_productos.copy()
    if df.iloc[0]['SKU'] == 'SKU':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Precio USD'] = pd.to_numeric(df['Precio USD'], errors='coerce')
    
    top_marcas = df.groupby('Marca')['Precio USD'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colores = sns.color_palette("husl", len(top_marcas))
    barras = ax.bar(range(len(top_marcas)), top_marcas.values, color=colores)
    ax.set_xticks(range(len(top_marcas)))
    ax.set_xticklabels(top_marcas.index, rotation=45, ha='right')
    ax.set_title('Top 10 Marcas por Valor Total (Precio USD)', fontsize=14, fontweight='bold')
    ax.set_ylabel('USD')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    guardar_figura(fig, 'top_marcas.png', FIGURES_PRODUCTOS)

def grafico_condicion_estado(df_productos):
    """Gráfico de condición vs estado de productos."""
    logger.info("Generando condición vs estado...")
    
    df = df_productos.copy()
    if df.iloc[0]['SKU'] == 'SKU':
        df = df.iloc[1:].reset_index(drop=True)
    
    cruce = pd.crosstab(df['Condición'], df['Estado'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cruce.plot(kind='bar', ax=ax, color=sns.color_palette("husl", len(cruce.columns)))
    ax.set_title('Condición vs Estado de Productos', fontsize=14, fontweight='bold')
    ax.set_xlabel('Condición')
    ax.set_ylabel('Cantidad')
    ax.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    guardar_figura(fig, 'condicion_vs_estado.png', FIGURES_PRODUCTOS)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de productos listo")