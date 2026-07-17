# src/03_visualizacion/graficas_proveedores.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import FIGURES_PROVEEDORES
from utils.helpers import guardar_figura
from utils.loggers import logger

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def grafico_proveedores_estado(df_proveedores):
    """Gráfico de proveedores por estado."""
    logger.info("Generando proveedores por estado...")
    
    df = df_proveedores.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    estado = df['Estado'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colores = sns.color_palette("husl", len(estado))
    
    wedges, texts, autotexts = ax.pie(estado, labels=estado.index, autopct='%1.1f%%',
                                       colors=colores, startangle=90, explode=[0.05]*len(estado))
    ax.set_title('Distribución de Proveedores por Estado', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    guardar_figura(fig, 'proveedores_por_estado.png', FIGURES_PROVEEDORES)

def grafico_proveedores_pais(df_proveedores):
    """Proveedores por país."""
    logger.info("Generando proveedores por país...")
    
    df = df_proveedores.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    pais = df['País'].value_counts().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.barh(pais.index, pais.values, color=sns.color_palette("husl", len(pais)))
    ax.set_title('Proveedores por País', fontsize=14, fontweight='bold')
    ax.set_xlabel('Cantidad de Proveedores')
    
    for bar in barras:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    guardar_figura(fig, 'proveedores_por_pais.png', FIGURES_PROVEEDORES)

def grafico_calificacion_tipo(df_proveedores):
    """Calificación por tipo de proveedor."""
    logger.info("Generando calificación por tipo...")
    
    df = df_proveedores.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Calificación'] = pd.to_numeric(df['Calificación'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.boxplot(data=df, x='Tipo', y='Calificación', ax=ax, palette='husl')
    ax.set_title('Calificación por Tipo de Proveedor', fontsize=14, fontweight='bold')
    ax.set_ylabel('Calificación')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    guardar_figura(fig, 'calificacion_por_tipo.png', FIGURES_PROVEEDORES)

def grafico_lead_time_calificacion(df_proveedores):
    """Relación entre lead time y calificación."""
    logger.info("Generando lead time vs calificación...")
    
    df = df_proveedores.copy()
    if df.iloc[0]['ID'] == 'ID':
        df = df.iloc[1:].reset_index(drop=True)
    
    df['Lead Time Días'] = pd.to_numeric(df['Lead Time Días'], errors='coerce')
    df['Calificación'] = pd.to_numeric(df['Calificación'], errors='coerce')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.scatterplot(data=df, x='Lead Time Días', y='Calificación', 
                    hue='Tipo', size='Años de Relación', sizes=(50, 300),
                    ax=ax, palette='husl', alpha=0.7)
    ax.set_title('Lead Time vs Calificación (tamaño = Años de Relación)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Lead Time (días)')
    ax.set_ylabel('Calificación')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    guardar_figura(fig, 'lead_time_vs_calificacion.png', FIGURES_PROVEEDORES)

if __name__ == "__main__":
    logger.info("Módulo de gráficas de proveedores listo")
    