# src/03_visualizacion/graficas_devoluciones.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_DEVOLUCIONES
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_devoluciones_motivo(df_devoluciones):
    """Gráfico de devoluciones por motivo."""
    logger.info("Generando devoluciones por motivo...")
    
    df = df_devoluciones.copy()
    if df.iloc[0]['ID_Devolución'] == 'ID_Devolución':
        df = df.iloc[1:].reset_index(drop=True)
    
    motivo = df['Motivo'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(motivo))
    
    wedges, texts, autotexts = ax.pie(motivo, labels=motivo.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(motivo))
    ax.set_title('Distribución de Devoluciones por Motivo', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'devoluciones_por_motivo.png', FIGURES_DEVOLUCIONES)

def grafico_devoluciones_estado(df_devoluciones):
    """Gráfico de devoluciones por estado del producto."""
    logger.info("Generando devoluciones por estado del producto...")
    
    df = df_devoluciones.copy()
    if df.iloc[0]['ID_Devolución'] == 'ID_Devolución':
        df = df.iloc[1:].reset_index(drop=True)
    
    estado = df['Estado_Producto'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(estado))
    
    wedges, texts, autotexts = ax.pie(estado, labels=estado.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(estado))
    ax.set_title('Distribución por Estado del Producto', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'devoluciones_por_estado_producto.png', FIGURES_DEVOLUCIONES)

def grafico_cruce_motivo_estado(df_devoluciones):
    """Heatmap cruce motivo vs estado del producto."""
    logger.info("Generando heatmap motivo vs estado...")
    
    df = df_devoluciones.copy()
    if df.iloc[0]['ID_Devolución'] == 'ID_Devolución':
        df = df.iloc[1:].reset_index(drop=True)
    
    cruce = pd.crosstab(df['Motivo'], df['Estado_Producto'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(cruce, annot=True, fmt='d', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Cantidad'})
    ax.set_title('Cruce: Motivo vs Estado del Producto', fontsize=14, fontweight='bold')
    ax.set_xlabel('Estado del Producto')
    ax.set_ylabel('Motivo')
    
    plt.tight_layout()
    guardar_figura(fig, 'cruce_motivo_estado.png', FIGURES_DEVOLUCIONES)

def grafico_devoluciones_mes(df_devoluciones):
    """Devoluciones por mes."""
    logger.info("Generando devoluciones por mes...")
    
    df = df_devoluciones.copy()
    if df.iloc[0]['ID_Devolución'] == 'ID_Devolución':
        df = df.iloc[1:].reset_index(drop=True)
    
    # Convertir fecha de forma flexible
    try:
        # Si ya es datetime o string ISO
        df['Fecha_Devolución'] = pd.to_datetime(df['Fecha_Devolución'], errors='coerce')
    except:
        # Si es número serial de Excel
        df['Fecha_Devolución'] = pd.to_datetime(df['Fecha_Devolución'], errors='coerce', unit='D', origin='1899-12-30')
    
    df['Año-Mes'] = df['Fecha_Devolución'].dt.to_period('M')
    
    mes = df['Año-Mes'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(mes.index.astype(str), mes.values, marker='o', linewidth=2, color='#e74c3c')
    ax.set_title('Devoluciones por Mes', fontsize=14, fontweight='bold')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de Devoluciones')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    guardar_figura(fig, 'devoluciones_por_mes.png', FIGURES_DEVOLUCIONES)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de devoluciones listo")