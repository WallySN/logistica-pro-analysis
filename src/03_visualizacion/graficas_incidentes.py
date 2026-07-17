# src/03_visualizacion/graficas_incidentes.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_INCIDENTES
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_incidentes_tipo(df_incidentes):
    """Gráfico de incidentes por tipo."""
    logger.info("Generando incidentes por tipo...")
    
    df = df_incidentes.copy()
    if df.iloc[0]['ID_Incidente'] == 'ID_Incidente':
        df = df.iloc[1:].reset_index(drop=True)
    
    tipo = df['Tipo_Incidente'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(tipo))
    
    wedges, texts, autotexts = ax.pie(tipo, labels=tipo.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(tipo))
    ax.set_title('Distribución de Incidentes por Tipo', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'incidentes_por_tipo.png', FIGURES_INCIDENTES)

def grafico_costo_tipo_incidente(df_incidentes):
    """Costo total por tipo de incidente."""
    logger.info("Generando costo por tipo de incidente...")
    
    df = df_incidentes.copy()
    if df.iloc[0]['ID_Incidente'] == 'ID_Incidente':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Costo_Incidente_USD'] = pd.to_numeric(df['Costo_Incidente_USD'], errors='coerce')
    
    costo_tipo = df.groupby('Tipo_Incidente')['Costo_Incidente_USD'].sum().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.barh(costo_tipo.index, costo_tipo.values, color=sns.color_palette("husl", len(costo_tipo)))
    ax.set_title('Costo Total por Tipo de Incidente', fontsize=14, fontweight='bold')
    ax.set_xlabel('USD')
    
    for bar in barras:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'${width:,.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'costo_por_tipo_incidente.png', FIGURES_INCIDENTES)

def grafico_costo_vs_retraso(df_incidentes):
    """Scatter plot: costo vs horas de retraso."""
    logger.info("Generando costo vs retraso...")
    
    df = df_incidentes.copy()
    if df.iloc[0]['ID_Incidente'] == 'ID_Incidente':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Costo_Incidente_USD'] = pd.to_numeric(df['Costo_Incidente_USD'], errors='coerce')
    df['Horas_Retraso'] = pd.to_numeric(df['Horas_Retraso'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.scatterplot(data=df, x='Horas_Retraso', y='Costo_Incidente_USD',
                    hue='Tipo_Incidente', size='Horas_Retraso', sizes=(50, 300),
                    ax=ax, palette='husl', alpha=0.7)
    ax.set_title('Costo vs Horas de Retraso', fontsize=14, fontweight='bold')
    ax.set_xlabel('Horas de Retraso')
    ax.set_ylabel('Costo Incidente (USD)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    guardar_figura(fig, 'costo_vs_retraso.png', FIGURES_INCIDENTES)

def grafico_top_costosos(df_incidentes):
    """Top 10 incidentes más costosos."""
    logger.info("Generando top incidentes costosos...")
    
    df = df_incidentes.copy()
    if df.iloc[0]['ID_Incidente'] == 'ID_Incidente':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Costo_Incidente_USD'] = pd.to_numeric(df['Costo_Incidente_USD'], errors='coerce')
    
    top = df.nlargest(10, 'Costo_Incidente_USD')[['ID_Incidente', 'Tipo_Incidente', 'Costo_Incidente_USD', 'Horas_Retraso']]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colores = sns.color_palette("husl", len(top))
    barras = ax.bar(range(len(top)), top['Costo_Incidente_USD'].values, color=colores)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels([f"{row['ID_Incidente']}\n{row['Tipo_Incidente']}" for _, row in top.iterrows()], 
                       rotation=45, ha='right', fontsize=8)
    ax.set_title('Top 10 Incidentes Más Costosos', fontsize=14, fontweight='bold')
    ax.set_ylabel('USD')
    
    for bar in barras:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=9, rotation=45)
    
    plt.tight_layout()
    guardar_figura(fig, 'top_incidentes_costosos.png', FIGURES_INCIDENTES)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de incidentes listo")