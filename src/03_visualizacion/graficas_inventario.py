# src/03_visualizacion/graficas_inventario.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_INVENTARIO
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_inventario_estado(df_inventario):
    """Gráfico de inventario por estado."""
    logger.info("Generando inventario por estado...")
    
    df = df_inventario.copy()
    if df.iloc[0]['ID Línea'] == 'ID Línea':
        df = df.iloc[1:].reset_index(drop=True)
    
    estado = df['Estado'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(estado))
    
    wedges, texts, autotexts = ax.pie(estado, labels=estado.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(estado))
    ax.set_title('Distribución de Inventario por Estado', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'inventario_por_estado.png', FIGURES_INVENTARIO)

def grafico_inventario_almacen(df_inventario):
    """Valor de inventario por almacén."""
    logger.info("Generando valor por almacén...")
    
    df = df_inventario.copy()
    if df.iloc[0]['ID Línea'] == 'ID Línea':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Valor Inventario USD'] = pd.to_numeric(df['Valor Inventario USD'], errors='coerce')
    
    almacen = df.groupby('Almacén')['Valor Inventario USD'].sum().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.barh(almacen.index, almacen.values, color=sns.color_palette("husl", len(almacen)))
    ax.set_title('Valor de Inventario por Almacén', fontsize=14, fontweight='bold')
    ax.set_xlabel('USD')
    
    for bar in barras:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width:,.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'inventario_por_almacen.png', FIGURES_INVENTARIO)

def grafico_stock_bajo_sobre(df_inventario):
    """Productos con stock bajo vs sobre-stock."""
    logger.info("Generando stock bajo vs sobre-stock...")
    
    df = df_inventario.copy()
    if df.iloc[0]['ID Línea'] == 'ID Línea':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Disponible'] = pd.to_numeric(df['Disponible'], errors='coerce')
    df['Stock Mínimo'] = pd.to_numeric(df['Stock Mínimo'], errors='coerce')
    df['Stock Máximo'] = pd.to_numeric(df['Stock Máximo'], errors='coerce')
    
    stock_bajo = len(df[df['Disponible'] < df['Stock Mínimo']])
    sobre_stock = len(df[df['Disponible'] > df['Stock Máximo']])
    normal = len(df[(df['Disponible'] >= df['Stock Mínimo']) & (df['Disponible'] <= df['Stock Máximo'])])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    categorias = ['Stock Bajo', 'Normal', 'Sobre-Stock']
    valores = [stock_bajo, normal, sobre_stock]
    colores = ['#e74c3c', '#2ecc71', '#f39c12']
    
    barras = ax.bar(categorias, valores, color=colores)
    ax.set_title('Niveles de Stock', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cantidad de Líneas')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    guardar_figura(fig, 'stock_bajo_sobre.png', FIGURES_INVENTARIO)

def grafico_rotacion_inventario(df_inventario):
    """Distribución de rotación anual."""
    logger.info("Generando rotación anual...")
    
    df = df_inventario.copy()
    if df.iloc[0]['ID Línea'] == 'ID Línea':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Rotación Anual'] = pd.to_numeric(df['Rotación Anual'], errors='coerce')
    rotacion = df['Rotación Anual'].dropna()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(rotacion, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
    ax.axvline(rotacion.mean(), color='red', linestyle='--', linewidth=2, 
               label=f'Promedio: {rotacion.mean():.1f}')
    ax.axvline(rotacion.median(), color='green', linestyle='--', linewidth=2,
               label=f'Mediana: {rotacion.median():.1f}')
    ax.set_title('Distribución de Rotación Anual', fontsize=14, fontweight='bold')
    ax.set_xlabel('Rotación Anual')
    ax.set_ylabel('Frecuencia')
    ax.legend()
    
    plt.tight_layout()
    guardar_figura(fig, 'rotacion_anual.png', FIGURES_INVENTARIO)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de inventario listo")