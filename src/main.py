# src/main.py
import sys
from pathlib import Path
import importlib.util

# Agregar raíz del proyecto al path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.loggers import logger
from utils.config import EXCEL_FILE, DATA_PROCESSED


def cargar_modulo(ruta_relativa, nombre_modulo):
    """Carga un módulo dinámicamente evitando problemas con nombres que empiezan con número."""
    ruta = PROJECT_ROOT / "src" / ruta_relativa
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre_modulo] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def ejecutar_pipeline():
    """
    Pipeline completo de análisis de datos logísticos.
    """
    logger.info("=" * 60)
    logger.info("  PIPELINE LOGISTICA PRO - ANALISIS COMPLETO")
    logger.info("=" * 60)
    
    # ============================================================
    # PASO 1: CARGA DE DATOS
    # ============================================================
    logger.info("\n" + "=" * 60)
    logger.info("PASO 1: CARGA DE DATOS")
    logger.info("=" * 60)
    
    # Cargar módulo de carga dinámicamente
    mod_carga = cargar_modulo("01_carga_datos/cargar_excel.py", "cargar_excel")
    hojas = mod_carga.cargar_hojas_excel()
    mod_carga.guardar_datos_procesados(hojas)
    
    # Extraer DataFrames
    df_productos = hojas.get('Productos')
    df_ventas = hojas.get('Ventas')
    df_compras = hojas.get('Compras')
    df_proveedores = hojas.get('Proveedores')
    df_inventario = hojas.get('Inventario')
    df_clientes = hojas.get('Clientes')
    df_transporte = hojas.get('Transporte')
    df_incidentes = hojas.get('Incidentes_Transporte')
    df_devoluciones = hojas.get('Devoluciones')
    
    logger.info(f"\n✓ Hojas cargadas: {list(hojas.keys())}")
    
    # ============================================================
    # PASO 2: ANÁLISIS DE DATOS
    # ============================================================
    logger.info("\n" + "=" * 60)
    logger.info("PASO 2: ANÁLISIS DE DATOS")
    logger.info("=" * 60)
    
    # Cargar módulos de análisis dinámicamente
    mod_prod = cargar_modulo("02_analisis/analisis_productos.py", "analisis_productos")
    mod_vent = cargar_modulo("02_analisis/analisis_ventas.py", "analisis_ventas")
    mod_comp = cargar_modulo("02_analisis/analisis_compras.py", "analisis_compras")
    mod_prov = cargar_modulo("02_analisis/analisis_proveedores.py", "analisis_proveedores")
    mod_inv = cargar_modulo("02_analisis/analisis_inventario.py", "analisis_inventario")
    mod_cli = cargar_modulo("02_analisis/analisis_clientes.py", "analisis_clientes")
    mod_trans = cargar_modulo("02_analisis/analisis_transporte.py", "analisis_transporte")
    mod_inc = cargar_modulo("02_analisis/analisis_incidentes.py", "analisis_incidentes")
    mod_dev = cargar_modulo("02_analisis/analisis_devoluciones.py", "analisis_devoluciones")
    mod_fin = cargar_modulo("02_analisis/analisis_financiero_inventario.py", "analisis_financiero_inventario")
    
    resultados_productos = mod_prod.analizar_productos(df_productos)
    resultados_ventas = mod_vent.analizar_ventas(df_ventas)
    resultados_compras = mod_comp.analizar_compras(df_compras)
    resultados_proveedores = mod_prov.analizar_proveedores(df_proveedores)
    resultados_inventario = mod_inv.analizar_inventario(df_inventario)
    resultados_clientes = mod_cli.analizar_clientes(df_clientes)
    resultados_transporte = mod_trans.analizar_transporte(df_transporte)
    resultados_incidentes = mod_inc.analizar_incidentes(df_incidentes)
    resultados_devoluciones = mod_dev.analizar_devoluciones(df_devoluciones)
    resultados_financiero_inv = mod_fin.analizar_financiero_inventario(df_inventario, df_productos)
    
    logger.info("\n✓ Todos los análisis completados")
    
    # ============================================================
    # PASO 3: VISUALIZACIÓN
    # ============================================================
    logger.info("\n" + "=" * 60)
    logger.info("PASO 3: GENERACIÓN DE GRÁFICAS")
    logger.info("=" * 60)
    
    # Cargar módulos de visualización dinámicamente
    mod_gen = cargar_modulo("03_visualizacion/graficas_generales.py", "graficas_generales")
    mod_prod_vis = cargar_modulo("03_visualizacion/graficas_productos.py", "graficas_productos")
    mod_vent_vis = cargar_modulo("03_visualizacion/graficas_ventas.py", "graficas_ventas")
    mod_comp_vis = cargar_modulo("03_visualizacion/graficas_compras.py", "graficas_compras")
    mod_prov_vis = cargar_modulo("03_visualizacion/graficas_proveedores.py", "graficas_proveedores")
    mod_inv_vis = cargar_modulo("03_visualizacion/graficas_inventario.py", "graficas_inventario")
    mod_inc_vis = cargar_modulo("03_visualizacion/graficas_incidentes.py", "graficas_incidentes")
    mod_dev_vis = cargar_modulo("03_visualizacion/graficas_devoluciones.py", "graficas_devoluciones")
    mod_kpi_vis = cargar_modulo("03_visualizacion/graficas_cumplimiento_kpis.py", "graficas_cumplimiento_kpis")
    
    # Gráficas generales
    mod_gen.grafico_resumen_empresa(df_ventas, df_compras, df_inventario, df_productos)
    mod_gen.grafico_tendencias_mensuales(df_ventas, df_compras)
    
    # Gráficas de productos
    mod_prod_vis.grafico_productos_categoria(df_productos)
    mod_prod_vis.grafico_margen_gama(df_productos)
    mod_prod_vis.grafico_top_marcas(df_productos)
    mod_prod_vis.grafico_condicion_estado(df_productos)
    
    # Gráficas de ventas
    mod_vent_vis.grafico_ventas_estado(df_ventas)
    mod_vent_vis.grafico_ventas_canal(df_ventas)
    mod_vent_vis.grafico_top_clientes(df_ventas)
    mod_vent_vis.grafico_ventas_metodo_pago(df_ventas)
    
    # Gráficas de compras
    mod_comp_vis.grafico_compras_estado(df_compras)
    mod_comp_vis.grafico_compras_proveedor(df_compras)
    mod_comp_vis.grafico_cumplimiento_entrega(df_compras)
    mod_comp_vis.grafico_tiempos_entrega(df_compras)
    
    # Gráficas de proveedores
    mod_prov_vis.grafico_proveedores_estado(df_proveedores)
    mod_prov_vis.grafico_proveedores_pais(df_proveedores)
    mod_prov_vis.grafico_calificacion_tipo(df_proveedores)
    mod_prov_vis.grafico_lead_time_calificacion(df_proveedores)
    
    # Gráficas de inventario
    mod_inv_vis.grafico_inventario_estado(df_inventario)
    mod_inv_vis.grafico_inventario_almacen(df_inventario)
    mod_inv_vis.grafico_stock_bajo_sobre(df_inventario)
    mod_inv_vis.grafico_rotacion_inventario(df_inventario)
    
    # Gráficas de incidentes
    mod_inc_vis.grafico_incidentes_tipo(df_incidentes)
    mod_inc_vis.grafico_costo_tipo_incidente(df_incidentes)
    mod_inc_vis.grafico_costo_vs_retraso(df_incidentes)
    mod_inc_vis.grafico_top_costosos(df_incidentes)
    
    # Gráficas de devoluciones
    mod_dev_vis.grafico_devoluciones_motivo(df_devoluciones)
    mod_dev_vis.grafico_devoluciones_estado(df_devoluciones)
    mod_dev_vis.grafico_cruce_motivo_estado(df_devoluciones)
    mod_dev_vis.grafico_devoluciones_mes(df_devoluciones)
    
    # Dashboard de KPIs
    mod_kpi_vis.grafico_kpis_generales(
        resultados_productos, resultados_ventas, resultados_compras,
        resultados_inventario, resultados_proveedores, resultados_incidentes
    )
    mod_kpi_vis.grafico_cumplimiento_vs_meta(df_ventas, meta_ventas=500000, df_compras=df_compras, meta_compras=300000)
    
    logger.info("\n✓ Todas las gráficas generadas")
    
    # ============================================================
    # PASO 4: REPORTES
    # ============================================================
    logger.info("\n" + "=" * 60)
    logger.info("PASO 4: GENERACIÓN DE REPORTES")
    logger.info("=" * 60)
    
    # Carga dinámica de módulos de reporte
    mod_rep_gen = cargar_modulo("04_reportes/generar_reporte.py", "generar_reporte")
    mod_dash = cargar_modulo("04_reportes/dashboard.py", "dashboard")
    mod_rep_excel = cargar_modulo("04_reportes/reporte_excel.py", "reporte_excel")
    mod_rep_pdf = cargar_modulo("04_reportes/reporte_pdf.py", "reporte_pdf")
    mod_rep_pdf_graf = cargar_modulo("04_reportes/reporte_pdf_graficas.py", "reporte_pdf_graficas")
    
    # Reportes base
    archivo_excel = mod_rep_gen.generar_reporte_excel(
        resultados_productos, resultados_ventas, resultados_compras,
        resultados_proveedores, resultados_inventario, resultados_clientes,
        resultados_transporte, resultados_incidentes, resultados_devoluciones,
        resultados_financiero_inv
    )
    
    archivo_texto = mod_rep_gen.generar_reporte_texto(
        resultados_productos, resultados_ventas, resultados_compras,
        resultados_proveedores, resultados_inventario, resultados_clientes,
        resultados_transporte, resultados_incidentes, resultados_devoluciones
    )
    
    # Reportes adicionales
    logger.info("\n--- Generando reportes adicionales ---")
    
    mod_dash.generar_dashboard_ejecutivo(
        df_ventas, df_compras, df_inventario, df_productos, df_proveedores
    )
    
    archivo_excel_detallado = mod_rep_excel.generar_reporte_excel_detallado(
        hojas, resultados_productos, resultados_ventas, resultados_compras,
        resultados_proveedores, resultados_inventario, resultados_clientes,
        resultados_transporte, resultados_incidentes, resultados_devoluciones
    )
    
    archivo_pdf_texto = mod_rep_pdf.generar_reporte_pdf_texto(
        resultados_productos, resultados_ventas, resultados_compras,
        resultados_proveedores, resultados_inventario, resultados_clientes,
        resultados_transporte, resultados_incidentes, resultados_devoluciones
    )
    
    # PDF con gráficas
    logger.info("\n--- Generando PDF con gráficas ---")
    archivo_pdf_graficas = mod_rep_pdf_graf.generar_pdf_con_graficas(
        resultados_productos, resultados_ventas, resultados_compras,
        resultados_proveedores, resultados_inventario, resultados_clientes,
        resultados_transporte, resultados_incidentes, resultados_devoluciones
    )
    
    logger.info("\n✓ Todos los reportes generados con éxito")
    
    # ============================================================
    # RESUMEN FINAL
    # ============================================================
    logger.info("\n" + "=" * 60)
    logger.info("  PIPELINE COMPLETADO CON ÉXITO")
    logger.info("=" * 60)
    logger.info(f"📊 Reporte Excel Base: {archivo_excel}")
    logger.info(f"📄 Reporte Texto Base: {archivo_texto}")
    logger.info(f"📈 Reporte Excel Detallado: {archivo_excel_detallado}")
    logger.info(f"📑 Reporte PDF/Texto: {archivo_pdf_texto}")
    logger.info(f"🖼️ Reporte PDF con Gráficas: {archivo_pdf_graficas}")
    logger.info("=" * 60)
    
    return {
        'resultados': {
            'productos': resultados_productos,
            'ventas': resultados_ventas,
            'compras': resultados_compras,
            'proveedores': resultados_proveedores,
            'inventario': resultados_inventario,
            'clientes': resultados_clientes,
            'transporte': resultados_transporte,
            'incidentes': resultados_incidentes,
            'devoluciones': resultados_devoluciones,
            'financiero_inventario': resultados_financiero_inv
        },
        'reportes': {
            'excel_base': archivo_excel,
            'texto_base': archivo_texto,
            'excel_detallado': archivo_excel_detallado,
            'pdf_texto': archivo_pdf_texto,
            'pdf_graficas': archivo_pdf_graficas
        }
    }


if __name__ == "__main__":
    ejecutar_pipeline()