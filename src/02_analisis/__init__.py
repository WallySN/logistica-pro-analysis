# src/02_analisis/__init__.py
from .analisis_productos import analizar_productos
from .analisis_ventas import analizar_ventas
from .analisis_compras import analizar_compras
from .analisis_proveedores import analizar_proveedores
from .analisis_inventario import analizar_inventario
from .analisis_clientes import analizar_clientes
from .analisis_transporte import analizar_transporte
from .analisis_incidentes import analizar_incidentes
from .analisis_devoluciones import analizar_devoluciones
from .analisis_financiero_inventario import analizar_financiero_inventario

__all__ = [
    'analizar_productos',
    'analizar_ventas',
    'analizar_compras',
    'analizar_proveedores',
    'analizar_inventario',
    'analizar_clientes',
    'analizar_transporte',
    'analizar_incidentes',
    'analizar_devoluciones',
    'analizar_financiero_inventario'
]