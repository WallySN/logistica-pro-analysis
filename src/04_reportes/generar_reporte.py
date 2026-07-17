# src/04_reportes/generar_reporte.py
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.config import REPORTS_EXCEL, REPORTS_PDF
from utils.loggers import logger
from utils.helpers import formatear_moneda

def generar_reporte_excel(resultados_productos, resultados_ventas, resultados_compras,
                          resultados_proveedores, resultados_inventario, resultados_clientes,
                          resultados_transporte, resultados_incidentes, resultados_devoluciones,
                          resultados_financiero_inv=None):
    """
    Genera un reporte consolidado en Excel con múltiples hojas.
    """
    logger.info("=" * 50)
    logger.info("GENERANDO REPORTE EXCEL")
    logger.info("=" * 50)
    
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = REPORTS_EXCEL / f"reporte_logistica_pro_{fecha}.xlsx"
    
    with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
        
        # Hoja 1: Resumen Ejecutivo
        resumen = pd.DataFrame({
            'KPI': [
                'Total Productos',
                'Total Ventas (USD)',
                'Total Compras (USD)',
                'Valor Inventario (USD)',
                'Total Proveedores',
                'Total Clientes',
                'Total Rutas Transporte',
                'Total Incidentes',
                'Total Devoluciones',
                'Margen Promedio (%)',
                'Ticket Promedio (USD)',
                'Calif. Proveedores Promedio',
                'Costo Total Incidentes (USD)'
            ],
            'Valor': [
                resultados_productos.get('kpis_precio', {}).get('total', 0),
                resultados_ventas.get('kpis_total', {}).get('total', 0),
                resultados_compras.get('kpis_total', {}).get('total', 0),
                resultados_inventario.get('valor_total', 0),
                resultados_proveedores.get('total', 0),
                resultados_clientes.get('total', 0),
                resultados_transporte.get('total_rutas', 0),
                resultados_incidentes.get('total_incidentes', 0),
                resultados_devoluciones.get('total', 0),
                resultados_productos.get('kpis_margen', {}).get('promedio', 0),
                resultados_ventas.get('kpis_total', {}).get('promedio', 0),
                resultados_proveedores.get('calificacion_promedio', 0),
                resultados_incidentes.get('costo_total', 0)
            ]
        })
        resumen.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
        
        # Hoja 2: Productos por Categoría
        if 'resumen_categoria' in resultados_productos:
            resultados_productos['resumen_categoria'].to_excel(writer, sheet_name='Productos x Categoria')
        
        # Hoja 3: Ventas por Canal
        if 'por_canal' in resultados_ventas:
            resultados_ventas['por_canal'].to_excel(writer, sheet_name='Ventas x Canal')
        
        # Hoja 4: Top Clientes
        if 'top_clientes' in resultados_ventas:
            resultados_ventas['top_clientes'].to_excel(writer, sheet_name='Top Clientes')
        
        # Hoja 5: Compras por Proveedor
        if 'por_proveedor' in resultados_compras:
            resultados_compras['por_proveedor'].to_excel(writer, sheet_name='Compras x Proveedor')
        
        # Hoja 6: Stock Bajo
        if 'stock_bajo' in resultados_inventario:
            resultados_inventario['stock_bajo'].to_excel(writer, sheet_name='Stock Bajo', index=False)
        
        # Hoja 7: Proveedores Top Calificación
        if 'top_calificaciones' in resultados_proveedores:
            resultados_proveedores['top_calificaciones'].to_excel(writer, sheet_name='Top Proveedores', index=False)
        
        # Hoja 8: Incidentes por Tipo
        if 'costo_por_tipo' in resultados_incidentes:
            resultados_incidentes['costo_por_tipo'].to_excel(writer, sheet_name='Incidentes x Tipo')
        
        # Hoja 9: Devoluciones por Motivo
        if 'por_motivo' in resultados_devoluciones:
            motivo_df = resultados_devoluciones['por_motivo'].to_frame(name='Cantidad')
            motivo_df.to_excel(writer, sheet_name='Devoluciones x Motivo')
        
        # Hoja 10: Clientes Morosos
        if 'morosos' in resultados_clientes:
            resultados_clientes['morosos'].to_excel(writer, sheet_name='Clientes Morosos', index=False)
        
        # Hoja 11: Análisis Financiero Inventario (si existe)
        if resultados_financiero_inv:
            if 'valor_por_categoria' in resultados_financiero_inv:
                resultados_financiero_inv['valor_por_categoria'].to_excel(writer, sheet_name='Financiero x Categoria')
            if 'top_congelado' in resultados_financiero_inv:
                resultados_financiero_inv['top_congelado'].to_excel(writer, sheet_name='Valor Congelado', index=False)
    
    logger.info(f"✓ Reporte Excel generado: {archivo}")
    return archivo

def generar_reporte_texto(resultados_productos, resultados_ventas, resultados_compras,
                          resultados_proveedores, resultados_inventario, resultados_clientes,
                          resultados_transporte, resultados_incidentes, resultados_devoluciones):
    """
    Genera un reporte ejecutivo en texto plano.
    """
    logger.info("=" * 50)
    logger.info("GENERANDO REPORTE TEXTO")
    logger.info("=" * 50)
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo = REPORTS_PDF / f"reporte_ejecutivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("  REPORTE EJECUTIVO - LOGÍSTICA PRO\n")
        f.write(f"  Generado: {fecha}\n")
        f.write("=" * 60 + "\n\n")
        
        # Resumen
        f.write("📊 RESUMEN EJECUTIVO\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Productos:      {resultados_productos.get('kpis_precio', {}).get('total', 0):,.0f}\n")
        f.write(f"Ventas Totales:       ${resultados_ventas.get('kpis_total', {}).get('total', 0):,.2f}\n")
        f.write(f"Compras Totales:      ${resultados_compras.get('kpis_total', {}).get('total', 0):,.2f}\n")
        f.write(f"Valor Inventario:     ${resultados_inventario.get('valor_total', 0):,.2f}\n")
        f.write(f"Total Proveedores:    {resultados_proveedores.get('total', 0)}\n")
        f.write(f"Total Clientes:       {resultados_clientes.get('total', 0)}\n")
        f.write(f"Total Rutas:          {resultados_transporte.get('total_rutas', 0)}\n")
        f.write(f"Total Incidentes:     {resultados_incidentes.get('total_incidentes', 0)}\n")
        f.write(f"Total Devoluciones:   {resultados_devoluciones.get('total', 0)}\n")
        f.write(f"Margen Promedio:      {resultados_productos.get('kpis_margen', {}).get('promedio', 0):.1f}%\n")
        f.write(f"Ticket Promedio:      ${resultados_ventas.get('kpis_total', {}).get('promedio', 0):,.2f}\n")
        f.write(f"Calif. Proveedores:   {resultados_proveedores.get('calificacion_promedio', 0):.2f}\n")
        f.write(f"Costo Incidentes:     ${resultados_incidentes.get('costo_total', 0):,.2f}\n\n")
        
        # Alertas
        f.write("🚨 ALERTAS\n")
        f.write("-" * 40 + "\n")
        
        stock_bajo = resultados_inventario.get('stock_bajo', pd.DataFrame())
        if len(stock_bajo) > 0:
            f.write(f"⚠️  Productos con stock bajo: {len(stock_bajo)}\n")
        
        morosos = resultados_clientes.get('morosos', pd.DataFrame())
        if len(morosos) > 0:
            f.write(f"⚠️  Clientes morosos: {len(morosos)}\n")
        
        costo_inc = resultados_incidentes.get('costo_total', 0)
        if costo_inc > 10000:
            f.write(f"⚠️  Costo de incidentes elevado: ${costo_inc:,.2f}\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("Fin del reporte\n")
    
    logger.info(f"✓ Reporte texto generado: {archivo}")
    return archivo

if __name__ == "__main__":
    logger.info("Módulo de reportes listo")