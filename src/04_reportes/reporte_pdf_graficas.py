# src/04_reportes/reporte_pdf_graficas.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from datetime import datetime
from utils.loggers import logger
from utils.config import REPORTS_PDF, FIGURES_DIR

# Definición de las subcarpetas de figuras a partir de FIGURES_DIR
FIGURES_GENERALES = FIGURES_DIR / "generales"
FIGURES_PRODUCTOS = FIGURES_DIR / "productos"
FIGURES_VENTAS = FIGURES_DIR / "ventas"
FIGURES_COMPRAS = FIGURES_DIR / "compras"
FIGURES_PROVEEDORES = FIGURES_DIR / "proveedores"
FIGURES_INVENTARIO = FIGURES_DIR / "inventario"
FIGURES_INCIDENTES = FIGURES_DIR / "incidentes"
FIGURES_DEVOLUCIONES = FIGURES_DIR / "devoluciones"


def generar_pdf_con_graficas(resultados_productos, resultados_ventas, resultados_compras,
                              resultados_proveedores, resultados_inventario, resultados_clientes,
                              resultados_transporte, resultados_incidentes, resultados_devoluciones):
    """
    Genera un PDF profesional que incluye todas las gráficas generadas.
    """
    logger.info("Generando PDF con gráficas...")
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo = REPORTS_PDF / f"reporte_completo_con_graficas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Crear documento
    doc = SimpleDocTemplate(
        str(archivo),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    seccion_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#e74c3c'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles["Normal"]
    normal_style.fontSize = 10
    normal_style.leading = 14
    
    # Contenido del PDF
    story = []
    
    # PORTADA
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("REPORTE EJECUTIVO", titulo_style))
    story.append(Paragraph("Análisis Logístico Pro", titulo_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"<b>Fecha de generación:</b> {fecha}", normal_style))
    story.append(Paragraph(f"<b>Período analizado:</b> 2024-2026", normal_style))
    story.append(Spacer(1, 1*inch))
    
    # KPIs en tabla
    kpi_data = [
        ['INDICADOR', 'VALOR'],
        ['Ventas Totales', f"${resultados_ventas.get('kpis_total', {}).get('total', 0):,.2f}"],
        ['Compras Totales', f"${resultados_compras.get('kpis_total', {}).get('total', 0):,.2f}"],
        ['Valor Inventario', f"${resultados_inventario.get('valor_total', 0):,.2f}"],
        ['Margen Promedio', f"{resultados_productos.get('kpis_margen', {}).get('promedio', 0):.1f}%"],
        ['Total Productos', f"{resultados_productos.get('kpis_precio', {}).get('total', 0):,.0f}"],
        ['Total Proveedores', f"{resultados_proveedores.get('total', 0)}"],
        ['Total Clientes', f"{resultados_clientes.get('total', 0)}"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[3*inch, 2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ecf0f1'), colors.HexColor('#bdc3c7')]),
    ]))
    story.append(kpi_table)
    story.append(PageBreak())
    
    # SECCIÓN 1: GRÁFICAS GENERALES
    story.append(Paragraph("1. DASHBOARD GENERAL", subtitulo_style))
    story.append(Spacer(1, 0.2*inch))
    
    graficas_generales = [
        ('dashboard_general.png', 'Dashboard General de la Empresa'),
        ('tendencias_mensuales.png', 'Tendencias Mensuales: Ventas vs Compras'),
        ('kpis_generales_dashboard.png', 'KPIs Generales del Proyecto'),
        ('cumplimiento_vs_metas.png', 'Cumplimiento vs Metas Establecidas'),
    ]
    
    for img_name, desc in graficas_generales:
        img_path = FIGURES_GENERALES / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 2: PRODUCTOS
    story.append(Paragraph("2. ANÁLISIS DE PRODUCTOS", subtitulo_style))
    
    graficas_productos = [
        ('productos_por_categoria.png', 'Productos por Categoría'),
        ('margen_por_gama.png', 'Distribución de Margen por Gama'),
        ('top_marcas.png', 'Top 10 Marcas por Valor'),
        ('condicion_vs_estado.png', 'Condición vs Estado de Productos'),
    ]
    
    for img_name, desc in graficas_productos:
        img_path = FIGURES_PRODUCTOS / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 3: VENTAS
    story.append(Paragraph("3. ANÁLISIS DE VENTAS", subtitulo_style))
    
    graficas_ventas = [
        ('ventas_por_estado.png', 'Ventas por Estado'),
        ('ventas_por_canal.png', 'Ventas por Canal'),
        ('top_clientes_ventas.png', 'Top 10 Clientes por Ventas'),
        ('ventas_por_metodo_pago.png', 'Ventas por Método de Pago'),
    ]
    
    for img_name, desc in graficas_ventas:
        img_path = FIGURES_VENTAS / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 4: COMPRAS
    story.append(Paragraph("4. ANÁLISIS DE COMPRAS", subtitulo_style))
    
    graficas_compras = [
        ('compras_por_estado.png', 'Compras por Estado'),
        ('top_proveedores_compras.png', 'Top 10 Proveedores por Compras'),
        ('cumplimiento_entrega.png', 'Cumplimiento de Entrega'),
        ('tiempos_entrega.png', 'Tiempos de Entrega'),
    ]
    
    for img_name, desc in graficas_compras:
        img_path = FIGURES_COMPRAS / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 5: PROVEEDORES
    story.append(Paragraph("5. ANÁLISIS DE PROVEEDORES", subtitulo_style))
    
    graficas_proveedores = [
        ('proveedores_por_estado.png', 'Proveedores por Estado'),
        ('proveedores_por_pais.png', 'Proveedores por País'),
        ('calificacion_por_tipo.png', 'Calificación por Tipo'),
        ('lead_time_vs_calificacion.png', 'Lead Time vs Calificación'),
    ]
    
    for img_name, desc in graficas_proveedores:
        img_path = FIGURES_PROVEEDORES / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 6: INVENTARIO
    story.append(Paragraph("6. ANÁLISIS DE INVENTARIO", subtitulo_style))
    
    graficas_inventario = [
        ('inventario_por_estado.png', 'Inventario por Estado'),
        ('inventario_por_almacen.png', 'Valor de Inventario por Almacén'),
        ('stock_bajo_sobre.png', 'Niveles de Stock'),
        ('rotacion_anual.png', 'Rotación Anual'),
    ]
    
    for img_name, desc in graficas_inventario:
        img_path = FIGURES_INVENTARIO / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 7: INCIDENTES
    story.append(Paragraph("7. ANÁLISIS DE INCIDENTES", subtitulo_style))
    
    graficas_incidentes = [
        ('incidentes_por_tipo.png', 'Incidentes por Tipo'),
        ('costo_por_tipo_incidente.png', 'Costo por Tipo de Incidente'),
        ('costo_vs_retraso.png', 'Costo vs Horas de Retraso'),
        ('top_incidentes_costosos.png', 'Top 10 Incidentes Más Costosos'),
    ]
    
    for img_name, desc in graficas_incidentes:
        img_path = FIGURES_INCIDENTES / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # SECCIÓN 8: DEVOLUCIONES
    story.append(Paragraph("8. ANÁLISIS DE DEVOLUCIONES", subtitulo_style))
    
    graficas_devoluciones = [
        ('devoluciones_por_motivo.png', 'Devoluciones por Motivo'),
        ('devoluciones_por_estado_producto.png', 'Devoluciones por Estado del Producto'),
        ('cruce_motivo_estado.png', 'Cruce Motivo vs Estado'),
        ('devoluciones_por_mes.png', 'Devoluciones por Mes'),
    ]
    
    for img_name, desc in graficas_devoluciones:
        img_path = FIGURES_DEVOLUCIONES / img_name
        if img_path.exists():
            story.append(Paragraph(f"<b>{desc}</b>", seccion_style))
            img = Image(str(img_path), width=6*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
    
    # PIE DE PÁGINA FINAL
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("=" * 50, normal_style))
    story.append(Paragraph("<b>Fin del Reporte</b>", normal_style))
    story.append(Paragraph("Generado automáticamente por Logística Pro Analysis", normal_style))
    story.append(Paragraph(f"Fecha: {fecha}", normal_style))
    
    # Generar PDF
    doc.build(story)
    
    logger.info(f"✓ PDF con gráficas generado: {archivo}")
    return archivo


if __name__ == "__main__":
    logger.info("Módulo reporte_pdf_graficas listo")