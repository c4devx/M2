{{ config(
    materialized='view',
    description='KPI. Ventas últimos 12 meses.'
) }}

SELECT 
    'total_ventas' AS kpi_nombre,
    SUM(total_facturado_calculado) AS valor,
    'ARS' AS unidad,
    'Monto total facturado últimos 12 meses' AS descripcion
FROM {{ ref('int_detalle_ordenes_tiempo') }}
WHERE estado='Completado'



