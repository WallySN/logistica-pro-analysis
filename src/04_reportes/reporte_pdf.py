# src/04_reportes/reporte_pdf.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime
from utils.loggers import logger
from utils.config import REPORTS_PDF

def generar_reporte_pdf_texto(resultados_productos, resultados_ventas, resultados_compras,
                                resultados_proveedores, resultados_inventario, resultados_clientes,
                                resultados_transporte, resultados_incidentes, resultados_devoluciones):
    """
    Genera un reporte ejecutivo en formato texto plano (simulando PDF estructurado).
    """
    logger.info("Generando reporte PDF (texto estructurado)...")
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo = REPORTS_PDF / f"reporte_ejecutivo_PDF_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(archivo, 'w', encoding='utf-8') as f:
        # Encabezado
        f.write("=" * 80 + "\n")
        f.write(" " * 20 + "REPORTE EJECUTIVO - LOGÍSTICA PRO\n")
        f.write(" " * 25 + f"Generado: {fecha}\n")
        f.write("=" * 80 + "\n\n")
        
        # Sección 1: Resumen Financiero
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 20 + "1. RESUMEN FINANCIERO" + " " * 35 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        f.write(f"  💰 Ventas Totales:        ${resultados_ventas.get('kpis_total', {}).get('total', 0):>15,.2f} USD\n")
        f.write(f"  📦 Compras Totales:       ${resultados_compras.get('kpis_total', {}).get('total', 0):>15,.2f} USD\n")
        f.write(f"  📊 Valor Inventario:       ${resultados_inventario.get('valor_total', 0):>15,.2f} USD\n")
        f.write(f"  📈 Margen Promedio:        {resultados_productos.get('kpis_margen', {}).get('promedio', 0):>15.1f} %\n")
        f.write(f"  🎫 Ticket Promedio:        ${resultados_ventas.get('kpis_total', {}).get('promedio', 0):>15,.2f} USD\n\n")
        
        # Sección 2: Operaciones
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 22 + "2. OPERACIONES" + " " * 42 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        f.write(f"  📦 Total Productos:        {resultados_productos.get('kpis_precio', {}).get('total', 0):>15,.0f}\n")
        f.write(f"  🚚 Total Ventas:           {resultados_ventas.get('kpis_total', {}).get('count', 801):>15,}\n")
        f.write(f"  📋 Total Compras:          {resultados_compras.get('kpis_total', {}).get('count', 400):>15,}\n")
        f.write(f"  🏭 Total Proveedores:      {resultados_proveedores.get('total', 0):>15}\n")
        f.write(f"  👥 Total Clientes:         {resultados_clientes.get('total', 0):>15}\n")
        f.write(f"  🛣️  Total Rutas:            {resultados_transporte.get('total_rutas', 0):>15}\n")
        f.write(f"  ⚠️  Total Incidentes:       {resultados_incidentes.get('total_incidentes', 0):>15}\n")
        f.write(f"  🔄 Total Devoluciones:     {resultados_devoluciones.get('total', 0):>15}\n\n")
        
        # Sección 3: Alertas
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 25 + "3. ALERTAS" + " " * 43 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        stock_bajo = resultados_inventario.get('stock_bajo', [])
        if len(stock_bajo) > 0:
            f.write(f"  🚨 Productos con stock bajo: {len(stock_bajo)} líneas\n")
        
        morosos = resultados_clientes.get('morosos', [])
        if len(morosos) > 0:
            f.write(f"  🚨 Clientes morosos: {len(morosos)} empresas\n")
        
        costo_inc = resultados_incidentes.get('costo_total', 0)
        if costo_inc > 10000:
            f.write(f"  🚨 Costo de incidentes elevado: ${costo_inc:,.2f} USD\n")
        
        sobre_stock = resultados_inventario.get('sobre_stock', [])
        if len(sobre_stock) > 0:
            f.write(f"  ⚠️  Productos con sobre-stock: {len(sobre_stock)} líneas\n")
        
        f.write("\n")
        
        # Sección 4: Proveedores Top
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 20 + "4. TOP PROVEEDORES" + " " * 38 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        top_calif = resultados_proveedores.get('top_calificaciones', [])
        if len(top_calif) > 0:
            f.write("  🏆 Top 5 por Calificación:\n")
            for i, (_, row) in enumerate(top_calif.head(5).iterrows(), 1):
                f.write(f"     {i}. {row['Nombre']} ({row['País']}) - ⭐ {row['Calificación']}\n")
        
        f.write("\n")
        
        # Sección 5: Clientes Top
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 22 + "5. TOP CLIENTES" + " " * 39 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        top_clientes = resultados_ventas.get('top_clientes', [])
        if len(top_clientes) > 0:
            f.write("  🏆 Top 5 por Ventas:\n")
            for i, (cliente, monto) in enumerate(top_clientes.head(5).items(), 1):
                f.write(f"     {i}. {cliente} - ${monto:>12,.2f} USD\n")
        
        f.write("\n")
        
        # Pie de página
        f.write("=" * 80 + "\n")
        f.write(" " * 25 + "Fin del Reporte Ejecutivo\n")
        f.write(" " * 20 + "Logística Pro - Sistema de Análisis\n")
        f.write("=" * 80 + "\n")
    
    logger.info(f"✓ Reporte PDF (texto) generado: {archivo}")
    return archivo

if __name__ == "__main__":
    logger.info("Módulo reporte_pdf listo")