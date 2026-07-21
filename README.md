# 📊 Logística Pro - Análisis de Datos Logísticos: 100% WEB

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

Sistema completo de análisis de datos logísticos con pipeline automatizado, visualizaciones interactivas y dashboard web.

---

## 🚀 Demo en Vivo

🔗 **[Ver Dashboard en Streamlit Cloud](https://share.streamlit.io)** *(desplegar desde tu repo)
*
🔗 **[Ver Dashboard en Streamlit Cloud](https://logistica-pro-analysis-b6rqjbpdizyvndtvydsdv2.streamlit.app/)** *(DESPLEGABLE EN WEB)
*
---

## 📁 Estructura del Proyecto

logistica-pro-analysis/
├── 📂 data/
│   ├── raw/              # Excel original
│   └── processed/        # CSVs generados
├── 📂 notebooks/
│   └── 01_exploracion_inicial.ipynb
├── 📂 outputs/
│   ├── figures/           # 32+ gráficas PNG
│   └── reports/         # Excel, PDF, TXT
├── 📂 src/
│   ├── 01_carga_datos/
│   ├── 02_analisis/
│   ├── 03_visualizacion/
│   ├── 04_reportes/
│   ├── 05_streamlit/    # Dashboard web
│   └── main.py
├── 📂 utils/
├── 📂 tests/
├── requirements.txt
├── pyproject.toml
└── README.md
plain

---

## ⚡ Ejecución Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/WallySN/Analisis-logistico-pro.git
cd Analisis-logistico-pro
2. Instalar dependencias
bash
pip install -r requirements.txt
3. Ejecutar el pipeline completo
bash
python src/main.py
4. Abrir el dashboard interactivo
bash
streamlit run src/05_streamlit/app.py
📊 Funcionalidades
Table
Módulo	Descripción
Carga	Lee Excel con 11 hojas automáticamente
Análisis	9 módulos: productos, ventas, compras, proveedores, inventario, clientes, transporte, incidentes, devoluciones
Visualización	32+ gráficas (pasteles, barras, líneas, heatmaps, boxplots, scatter)
Reportes	Excel multi-hoja, PDF con gráficas, texto ejecutivo
Dashboard	Streamlit interactivo con filtros dinámicos
Notebook	Jupyter para exploración interactiva
🛠️ Tecnologías
Python 3.12
Pandas - Manipulación de datos
Matplotlib + Seaborn - Visualización estática
Streamlit - Dashboard web interactivo
OpenPyXL - Reportes Excel
ReportLab - Reportes PDF
Jupyter - Exploración interactiva
📈 KPIs Calculados
Ventas totales y por canal
Margen promedio de productos
Valor de inventario por almacén
Calificación de proveedores
Costo de incidentes de transporte
Tasa de devoluciones por motivo
🎯 Casos de Uso
Inventario: Detectar stock bajo/sobre-stock
Compras: Evaluar cumplimiento de proveedores
Ventas: Identificar top clientes y canales
Transporte: Analizar costos y retrasos
Devoluciones: Encontrar patrones por motivo
👤 Autor
WallySN - Proyecto académico de análisis de datos logísticos
```