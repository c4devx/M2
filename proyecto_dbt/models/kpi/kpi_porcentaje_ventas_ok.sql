{{ config(
    materialized='view',
    description='KPI. Ventas completadas últimos 12 meses.'
) }}

SELECT 
    'ventas_completadas' AS kpi_nombre,
     ROUND(
        100.0 * SUM(CASE WHEN estado='Completado' THEN 1 ELSE 0 END) / COUNT(*), 
        2
    ) AS valor,
    '%' AS unidad,
    'Porcentaje de ventas con estado << Completado >> en los últimos 12 meses' AS descripcion
FROM {{ ref('int_detalle_ordenes_tiempo') }}



