# utils/helpers.py
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def guardar_figura(fig, nombre_archivo, carpeta, dpi=300, bbox_inches='tight'):
    """Guarda una figura en la carpeta especificada."""
    ruta = carpeta / nombre_archivo
    fig.savefig(ruta, dpi=dpi, bbox_inches=bbox_inches)
    plt.close(fig)
    print(f"✓ Figura guardada: {ruta}")

def formatear_moneda(valor):
    """Formatea un valor como moneda USD."""
    return f"${valor:,.2f}"

def calcular_kpis_basicos(df, columna_valor):
    """Calcula KPIs básicos de una columna numérica."""
    return {
        'total': df[columna_valor].sum(),
        'promedio': df[columna_valor].mean(),
        'mediana': df[columna_valor].median(),
        'min': df[columna_valor].min(),
        'max': df[columna_valor].max()
    }

def resumen_categorias(df, columna_categoria, columna_valor):
    """Resumen agrupado por categoría."""
    return df.groupby(columna_categoria)[columna_valor].agg([
        'count', 'sum', 'mean', 'median'
    ]).sort_values('sum', ascending=False)

def detectar_outliers(df, columna, metodo='iqr'):
    """Detecta outliers usando IQR o Z-score."""
    if metodo == 'iqr':
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[columna] < lower) | (df[columna] > upper)]
    elif metodo == 'zscore':
        z_scores = np.abs((df[columna] - df[columna].mean()) / df[columna].std())
        return df[z_scores > 3]
    return pd.DataFrame()