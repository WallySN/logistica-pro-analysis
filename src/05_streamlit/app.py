# src/05_streamlit/app.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Logística Pro - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #2c3e50; }
    .sub-header { font-size: 1.5rem; color: #3498db; }
    </style>
""", unsafe_allow_html=True)

# ============================================
# CARGA DE DATOS (GLOBAL)
# ============================================
@st.cache_data
def cargar_datos():
    """Carga todas las hojas del Excel."""
    excel_path = list((PROJECT_ROOT / 'data' / 'raw').glob('*.xlsx'))[0]
    excel = pd.ExcelFile(excel_path)
    hojas = {}
    for nombre in excel.sheet_names:
        df = pd.read_excel(excel, sheet_name=nombre)
        if df.iloc[0].astype(str).equals(df.columns.astype(str)):
            df = df.iloc[1:].reset_index(drop=True)
        hojas[nombre] = df
    return hojas

# Cargar datos UNA VEZ
hojas = cargar_datos()

# ============================================
# PREPARAR DATAFRAMES GLOBALES
# ============================================

# Productos
df_prod = hojas['Productos']
df_prod['Precio USD'] = pd.to_numeric(df_prod['Precio USD'], errors='coerce')
df_prod['Margen %'] = pd.to_numeric(df_prod['Margen %'], errors='coerce')
df_prod['Costo USD'] = pd.to_numeric(df_prod['Costo USD'], errors='coerce')

# Ventas
df_ventas = hojas['Ventas']
df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'], errors='coerce')
df_ventas['Total USD'] = pd.to_numeric(df_ventas['Total USD'], errors='coerce')
df_ventas['Año'] = df_ventas['Fecha'].dt.year
df_ventas['Mes'] = df_ventas['Fecha'].dt.month

# Compras
df_compras = hojas['Compras']
df_compras['Total USD'] = pd.to_numeric(df_compras['Total USD'], errors='coerce')

# Inventario - CORREGIDO con nombres reales
df_inv = hojas['Inventario']
df_inv['Valor Inventario USD'] = pd.to_numeric(df_inv['Valor Inventario USD'], errors='coerce')
df_inv['Stock Físico'] = pd.to_numeric(df_inv['Stock Físico'], errors='coerce')
df_inv['Stock Mínimo'] = pd.to_numeric(df_inv['Stock Mínimo'], errors='coerce')
df_inv['Disponible'] = pd.to_numeric(df_inv['Disponible'], errors='coerce')

# Proveedores - CORREGIDO con nombres reales
df_prov = hojas['Proveedores']
df_prov['Calificación'] = pd.to_numeric(df_prov['Calificación'], errors='coerce')
df_prov['Lead Time Días'] = pd.to_numeric(df_prov['Lead Time Días'], errors='coerce')

# Incidentes - CORREGIDO con nombres reales
df_inc = hojas['Incidentes_Transporte']
df_inc['Costo_Incidente_USD'] = pd.to_numeric(df_inc['Costo_Incidente_USD'], errors='coerce')
df_inc['Horas_Retraso'] = pd.to_numeric(df_inc['Horas_Retraso'], errors='coerce')

# Devoluciones
df_dev = hojas['Devoluciones']

# ============================================
# SIDEBAR - NAVEGACIÓN
# ============================================
st.sidebar.title("🧭 Navegación")
pagina = st.sidebar.radio(
    "Selecciona una sección:",
    ["🏠 Inicio", "📦 Productos", "💰 Ventas", "📋 Compras", 
     "🏭 Proveedores", "📊 Inventario", "⚠️ Incidentes", "🔄 Devoluciones"]
)

st.sidebar.markdown("---")
st.sidebar.info("📊 Logística Pro Dashboard v1.0")

# ============================================
# PÁGINA: INICIO
# ============================================
if pagina == "🏠 Inicio":
    st.markdown('<p class="main-header">📊 Logística Pro - Dashboard Ejecutivo</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Productos", f"{len(df_prod):,}")
    
    total_ventas = df_ventas['Total USD'].sum()
    with col2:
        st.metric("💰 Ventas Totales", f"${total_ventas:,.0f}")
    
    total_compras = df_compras['Total USD'].sum()
    with col3:
        st.metric("📋 Compras Totales", f"${total_compras:,.0f}")
    
    total_inv = df_inv['Valor Inventario USD'].sum()
    with col4:
        st.metric("📊 Valor Inventario", f"${total_inv:,.0f}")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Ventas por Estado")
        estado_ventas = df_ventas['Estado'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(estado_ventas, labels=estado_ventas.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución de Ventas')
        st.pyplot(fig)
    
    with col_right:
        st.subheader("Productos por Categoría")
        cat_counts = df_prod['Categoría'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        cat_counts.plot(kind='bar', ax=ax, color='#3498db')
        ax.set_title('Productos por Categoría')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

# ============================================
# PÁGINA: PRODUCTOS
# ============================================
elif pagina == "📦 Productos":
    st.markdown('<p class="main-header">📦 Análisis de Productos</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        categoria_sel = st.selectbox("Filtrar por Categoría", ['Todas'] + sorted(df_prod['Categoría'].dropna().unique().tolist()))
    with col2:
        marca_sel = st.selectbox("Filtrar por Marca", ['Todas'] + sorted(df_prod['Marca'].dropna().unique().tolist()))
    
    df_filtrado = df_prod.copy()
    if categoria_sel != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_sel]
    if marca_sel != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Marca'] == marca_sel]
    
    st.write(f"Mostrando {len(df_filtrado)} productos")
    st.dataframe(df_filtrado[['SKU', 'Nombre', 'Categoría', 'Marca', 'Precio USD', 'Margen %']].head(50))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución de Precios")
        fig, ax = plt.subplots(figsize=(8, 5))
        df_filtrado['Precio USD'].hist(bins=20, ax=ax, color='#2ecc71', edgecolor='black')
        ax.set_xlabel('Precio USD')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Margen vs Precio")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(df_filtrado['Precio USD'], df_filtrado['Margen %'], alpha=0.6, color='#e74c3c')
        ax.set_xlabel('Precio USD')
        ax.set_ylabel('Margen %')
        st.pyplot(fig)

# ============================================
# PÁGINA: VENTAS
# ============================================
elif pagina == "💰 Ventas":
    st.markdown('<p class="main-header">💰 Análisis de Ventas</p>', unsafe_allow_html=True)
    
    años = sorted(df_ventas['Año'].dropna().unique().astype(int).tolist())
    año_sel = st.selectbox("Año", ['Todos'] + años)
    
    if año_sel != 'Todos':
        df_v = df_ventas[df_ventas['Año'] == int(año_sel)]
    else:
        df_v = df_ventas
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Ventas", f"${df_v['Total USD'].sum():,.0f}")
    with col2:
        st.metric("Transacciones", f"{len(df_v):,}")
    with col3:
        st.metric("Ticket Promedio", f"${df_v['Total USD'].mean():.2f}")
    
    st.subheader("Ventas por Mes")
    mensual = df_v.groupby(df_v['Fecha'].dt.to_period('M'))['Total USD'].sum()
    fig, ax = plt.subplots(figsize=(12, 5))
    mensual.plot(ax=ax, marker='o', linewidth=2, color='#3498db')
    ax.set_ylabel('USD')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    st.subheader("Top 10 Clientes")
    top_clientes = df_v.groupby('Cliente')['Total USD'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_clientes.plot(kind='barh', ax=ax, color='#9b59b6')
    st.pyplot(fig)

# ============================================
# PÁGINA: COMPRAS
# ============================================
elif pagina == "📋 Compras":
    st.markdown('<p class="main-header">📋 Análisis de Compras</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Compras", f"${df_compras['Total USD'].sum():,.0f}")
    with col2:
        st.metric("Órdenes", f"{len(df_compras):,}")
    with col3:
        st.metric("Promedio por Orden", f"${df_compras['Total USD'].mean():.2f}")
    
    st.subheader("Top Proveedores por Compras")
    top_prov = df_compras.groupby('Proveedor')['Total USD'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_prov.plot(kind='barh', ax=ax, color='#f39c12')
    st.pyplot(fig)
    
    st.subheader("Compras por Estado")
    estado_comp = df_compras['Estado'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(estado_comp, labels=estado_comp.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)

# ============================================
# PÁGINA: PROVEEDORES
# ============================================
elif pagina == "🏭 Proveedores":
    st.markdown('<p class="main-header">🏭 Análisis de Proveedores</p>', unsafe_allow_html=True)
    
    paises = ['Todos'] + sorted(df_prov['País'].dropna().unique().tolist())
    pais_sel = st.selectbox("País", paises)
    
    if pais_sel != 'Todos':
        df_p = df_prov[df_prov['País'] == pais_sel]
    else:
        df_p = df_prov
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Proveedores", len(df_p))
    with col2:
        st.metric("Calificación Promedio", f"{df_p['Calificación'].mean():.1f}")
    with col3:
        st.metric("Lead Time Promedio", f"{df_p['Lead Time Días'].mean():.0f} días")
    
    st.dataframe(df_p[['ID', 'Nombre', 'País', 'Tipo', 'Calificación', 'Lead Time Días', 'Estado']])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Calificaciones")
        fig, ax = plt.subplots(figsize=(8, 5))
        df_p['Calificación'].hist(bins=10, ax=ax, color='#1abc9c', edgecolor='black')
        st.pyplot(fig)
    with col2:
        st.subheader("Lead Time vs Calificación")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(df_p['Lead Time Días'], df_p['Calificación'], alpha=0.6, color='#e67e22')
        ax.set_xlabel('Lead Time (días)')
        ax.set_ylabel('Calificación')
        st.pyplot(fig)

# ============================================
# PÁGINA: INVENTARIO - CORREGIDO
# ============================================
elif pagina == "📊 Inventario":
    st.markdown('<p class="main-header">📊 Análisis de Inventario</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valor Total", f"${df_inv['Valor Inventario USD'].sum():,.0f}")
    with col2:
        st.metric("Líneas", f"{len(df_inv):,}")
    with col3:
        # CORREGIDO: usar 'Stock Físico' y 'Stock Mínimo'
        stock_bajo = len(df_inv[df_inv['Stock Físico'] < df_inv['Stock Mínimo']])
        st.metric("Stock Bajo", stock_bajo, delta=f"{stock_bajo} alertas")
    
    st.subheader("Valor por Almacén")
    por_almacen = df_inv.groupby('Almacén')['Valor Inventario USD'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    por_almacen.plot(kind='bar', ax=ax, color='#3498db')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    
    if stock_bajo > 0:
        st.subheader("⚠️ Productos con Stock Bajo")
        alertas = df_inv[df_inv['Stock Físico'] < df_inv['Stock Mínimo']][['SKU', 'Almacén', 'Stock Físico', 'Stock Mínimo', 'Valor Inventario USD']]
        st.dataframe(alertas)

# ============================================
# PÁGINA: INCIDENTES - CORREGIDO
# ============================================
elif pagina == "⚠️ Incidentes":
    st.markdown('<p class="main-header">⚠️ Análisis de Incidentes</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Incidentes", len(df_inc))
    with col2:
        # CORREGIDO: usar 'Costo_Incidente_USD'
        st.metric("Costo Total", f"${df_inc['Costo_Incidente_USD'].sum():,.0f}")
    with col3:
        st.metric("Retraso Promedio", f"{df_inc['Horas_Retraso'].mean():.1f} hrs")
    
    st.subheader("Incidentes por Tipo")
    tipo_inc = df_inc['Tipo_Incidente'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(tipo_inc, labels=tipo_inc.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
    
    st.subheader("Costo vs Horas de Retraso")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_inc['Horas_Retraso'], df_inc['Costo_Incidente_USD'], alpha=0.6, color='#e74c3c')
    ax.set_xlabel('Horas de Retraso')
    ax.set_ylabel('Costo USD')
    st.pyplot(fig)

# ============================================
# PÁGINA: DEVOLUCIONES
# ============================================
elif pagina == "🔄 Devoluciones":
    st.markdown('<p class="main-header">🔄 Análisis de Devoluciones</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Devoluciones", len(df_dev))
    with col2:
        st.metric("Motivos", df_dev['Motivo'].nunique())
    
    st.subheader("Devoluciones por Motivo")
    motivo_dev = df_dev['Motivo'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(motivo_dev, labels=motivo_dev.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
    
    st.subheader("Estado del Producto")
    estado_dev = df_dev['Estado_Producto'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    estado_dev.plot(kind='bar', ax=ax, color='#9b59b6')
    st.pyplot(fig)