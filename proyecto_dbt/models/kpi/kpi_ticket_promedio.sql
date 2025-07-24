{{ config(
    materialized='view',
    description='KPI. Ticket promedio últimos 12 meses.'
) }}

SELECT 
    'ticket_promedio' AS kpi_nombre,
    ROUND(SUM(total_facturado_calculado) * 1.0 / SUM(total_cantidad_ordenes), 2) AS valor,
    'ARS' AS unidad,
    'Valor promedio por orden completada' AS descripcion
FROM {{ ref('int_detalle_ordenes_tiempo') }}
WHERE estado = 'Completado'