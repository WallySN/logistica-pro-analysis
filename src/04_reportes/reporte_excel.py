# src/04_reportes/reporte_excel.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from datetime import datetime
from utils.loggers import logger
from utils.config import REPORTS_EXCEL

def generar_reporte_excel_detallado(hojas, resultados_productos, resultados_ventas, resultados_compras,
                                      resultados_proveedores, resultados_inventario, resultados_clientes,
                                      resultados_transporte, resultados_incidentes, resultados_devoluciones):
    """
    Genera un reporte Excel detallado con múltiples hojas incluyendo datos crudos y análisis.
    """
    logger.info("Generando reporte Excel detallado...")
    
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = REPORTS_EXCEL / f"reporte_detallado_{fecha}.xlsx"
    
    with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
        
        # Hoja 1: Datos crudos - Productos
        if 'Productos' in hojas:
            hojas['Productos'].to_excel(writer, sheet_name='RAW_Productos', index=False)
        
        # Hoja 2: Datos crudos - Ventas
        if 'Ventas' in hojas:
            hojas['Ventas'].to_excel(writer, sheet_name='RAW_Ventas', index=False)
        
        # Hoja 3: Datos crudos - Compras
        if 'Compras' in hojas:
            hojas['Compras'].to_excel(writer, sheet_name='RAW_Compras', index=False)
        
        # Hoja 4: Datos crudos - Inventario
        if 'Inventario' in hojas:
            hojas['Inventario'].to_excel(writer, sheet_name='RAW_Inventario', index=False)
        
        # Hoja 5: Datos crudos - Proveedores
        if 'Proveedores' in hojas:
            hojas['Proveedores'].to_excel(writer, sheet_name='RAW_Proveedores', index=False)
        
        # Hoja 6: Datos crudos - Clientes
        if 'Clientes' in hojas:
            hojas['Clientes'].to_excel(writer, sheet_name='RAW_Clientes', index=False)
        
        # Hoja 7: Datos crudos - Transporte
        if 'Transporte' in hojas:
            hojas['Transporte'].to_excel(writer, sheet_name='RAW_Transporte', index=False)
        
        # Hoja 8: Datos crudos - Incidentes
        if 'Incidentes_Transporte' in hojas:
            hojas['Incidentes_Transporte'].to_excel(writer, sheet_name='RAW_Incidentes', index=False)
        
        # Hoja 9: Datos crudos - Devoluciones
        if 'Devoluciones' in hojas:
            hojas['Devoluciones'].to_excel(writer, sheet_name='RAW_Devoluciones', index=False)
        
        # Hoja 10: Resumen Ejecutivo
        resumen = pd.DataFrame({
            'Indicador': [
                'Total Productos',
                'Total Ventas',
                'Total Compras',
                'Valor Inventario',
                'Total Proveedores',
                'Total Clientes',
                'Total Rutas',
                'Total Incidentes',
                'Total Devoluciones',
                'Margen Promedio (%)',
                'Ticket Promedio (USD)',
                'Calif. Proveedores',
                'Costo Incidentes (USD)'
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
        resumen.to_excel(writer, sheet_name='RESUMEN_Ejecutivo', index=False)
        
        # Hoja 11: Análisis Productos
        if 'resumen_categoria' in resultados_productos:
            resultados_productos['resumen_categoria'].to_excel(writer, sheet_name='ANL_Productos_Categoria')
        
        # Hoja 12: Análisis Ventas
        if 'por_canal' in resultados_ventas:
            resultados_ventas['por_canal'].to_excel(writer, sheet_name='ANL_Ventas_Canal')
        
        # Hoja 13: Top Clientes
        if 'top_clientes' in resultados_ventas:
            resultados_ventas['top_clientes'].to_excel(writer, sheet_name='ANL_Top_Clientes')
        
        # Hoja 14: Análisis Compras
        if 'por_proveedor' in resultados_compras:
            resultados_compras['por_proveedor'].to_excel(writer, sheet_name='ANL_Compras_Proveedor')
        
        # Hoja 15: Stock Bajo
        if 'stock_bajo' in resultados_inventario:
            resultados_inventario['stock_bajo'].to_excel(writer, sheet_name='ALERT_Stock_Bajo', index=False)
        
        # Hoja 16: Clientes Morosos
        if 'morosos' in resultados_clientes:
            resultados_clientes['morosos'].to_excel(writer, sheet_name='ALERT_Morosos', index=False)
        
        # Hoja 17: Incidentes
        if 'costo_por_tipo' in resultados_incidentes:
            resultados_incidentes['costo_por_tipo'].to_excel(writer, sheet_name='ANL_Incidentes')
    
    logger.info(f"✓ Reporte Excel detallado generado: {archivo}")
    return archivo

if __name__ == "__main__":
    logger.info("Módulo reporte_excel listo")