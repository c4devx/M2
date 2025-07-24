{{ config(
    materialized='view',
    description='KPI. Facturación promedio mensual (últimos 12 meses).'
) }}

SELECT 
    'facturación_promedio' AS kpi_nombre,
    ROUND(SUM(total_facturado_calculado) * 1.0 / 12, 2) AS valor,
    'ARS' AS unidad,
    'Facturación promedio mensual (últimos 12 meses)' AS descripcion
FROM {{ ref('int_detalle_ordenes_tiempo') }}
WHERE estado = 'Completado'