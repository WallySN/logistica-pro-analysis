# src/03_visualizacion/__init__.py
from .graficas_generales import grafico_resumen_empresa, grafico_tendencias_mensuales
from .graficas_productos import (
    grafico_productos_categoria, 
    grafico_margen_gama, 
    grafico_top_marcas, 
    grafico_condicion_estado
)
from .graficas_ventas import (
    grafico_ventas_estado, 
    grafico_ventas_canal, 
    grafico_top_clientes, 
    grafico_ventas_metodo_pago
)
from .graficas_compras import (
    grafico_compras_estado, 
    grafico_compras_proveedor, 
    grafico_cumplimiento_entrega, 
    grafico_tiempos_entrega
)
from .graficas_proveedores import (
    grafico_proveedores_estado, 
    grafico_proveedores_pais, 
    grafico_calificacion_tipo, 
    grafico_lead_time_calificacion
)
from .graficas_inventario import (
    grafico_inventario_estado, 
    grafico_inventario_almacen, 
    grafico_stock_bajo_sobre, 
    grafico_rotacion_inventario
)
from .graficas_incidentes import (
    grafico_incidentes_tipo, 
    grafico_costo_tipo_incidente, 
    grafico_costo_vs_retraso, 
    grafico_top_costosos
)
from .graficas_devoluciones import (
    grafico_devoluciones_motivo, 
    grafico_devoluciones_estado, 
    grafico_cruce_motivo_estado, 
    grafico_devoluciones_mes
)
from .graficas_cumplimiento_kpis import (
    grafico_kpis_generales,
    grafico_cumplimiento_vs_meta
)

__all__ = [
    'grafico_resumen_empresa',
    'grafico_tendencias_mensuales',
    'grafico_productos_categoria',
    'grafico_margen_gama',
    'grafico_top_marcas',
    'grafico_condicion_estado',
    'grafico_ventas_estado',
    'grafico_ventas_canal',
    'grafico_top_clientes',
    'grafico_ventas_metodo_pago',
    'grafico_compras_estado',
    'grafico_compras_proveedor',
    'grafico_cumplimiento_entrega',
    'grafico_tiempos_entrega',
    'grafico_proveedores_estado',
    'grafico_proveedores_pais',
    'grafico_calificacion_tipo',
    'grafico_lead_time_calificacion',
    'grafico_inventario_estado',
    'grafico_inventario_almacen',
    'grafico_stock_bajo_sobre',
    'grafico_rotacion_inventario',
    'grafico_incidentes_tipo',
    'grafico_costo_tipo_incidente',
    'grafico_costo_vs_retraso',
    'grafico_top_costosos',
    'grafico_devoluciones_motivo',
    'grafico_devoluciones_estado',
    'grafico_cruce_motivo_estado',
    'grafico_devoluciones_mes',
    'grafico_kpis_generales',
    'grafico_cumplimiento_vs_meta'
]